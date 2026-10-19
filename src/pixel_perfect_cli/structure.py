"""Stages 3-5: segment both images into an element tree (XY-cut), pair elements, explain deltas as causes.

Pure translations are never reported per element: every move is decomposed into the gap/padding/align
change of its parent, so one changed margin yields one delta instead of a cascade of shifted regions.
"""

from dataclasses import dataclass, field

import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment

MIN_GAP_X = 8  # vertical cuts need a blank column band this wide, so letters/words stay one element
MAX_DEPTH = 8


@dataclass
class Node:
    x: int
    y: int
    w: int
    h: int
    axis: str = ""  # "y" or "x": how children were cut apart
    children: list["Node"] = field(default_factory=list)
    id: str = ""

    @property
    def box(self):
        return [self.x, self.y, self.w, self.h]


def _border_color(lab, x, y, w, h):
    edge = np.concatenate([lab[y, x:x + w], lab[y + h - 1, x:x + w], lab[y:y + h, x], lab[y:y + h, x + w - 1]])
    return np.median(edge, axis=0)


def _uniform_border(lab, x, y, w, h, color, tol) -> bool:
    """A real container (card, button) has a border of one color; a group of siblings does not."""
    edge = np.concatenate([lab[y, x:x + w], lab[y + h - 1, x:x + w], lab[y:y + h, x], lab[y:y + h, x + w - 1]])
    # ponytail: 0.8 leaves room for rounded corners; very large radii on small boxes will fail this
    return (np.linalg.norm(edge - color, axis=1) <= tol).mean() >= 0.8


def _bands(profile: np.ndarray, min_gap: int) -> list[tuple[int, int]]:
    """Runs of True in profile, merging runs separated by fewer than min_gap blanks."""
    idx = np.flatnonzero(profile)
    if idx.size == 0:
        return []
    breaks = np.flatnonzero(np.diff(idx) > min_gap)
    starts = np.r_[idx[0], idx[breaks + 1]]
    ends = np.r_[idx[breaks], idx[-1]] + 1
    return list(zip(starts.tolist(), ends.tolist()))


def segment(lab: np.ndarray, tol: float) -> Node:
    h, w = lab.shape[:2]
    root = Node(0, 0, w, h)
    root.children = _cut(lab, 0, 0, w, h, _border_color(lab, 0, 0, w, h), tol, 0, root)
    _number(root, "e")
    return root


def _cut(lab, x, y, w, h, bg, tol, depth, parent) -> list[Node]:
    fg = np.linalg.norm(lab[y:y + h, x:x + w] - bg, axis=2) > tol
    rows, cols = _bands(fg.any(axis=1), 1), _bands(fg.any(axis=0), MIN_GAP_X)
    if not rows:
        return []
    if len(rows) > 1:
        parent.axis = "y"
        return [n for a, b in rows for n in _sub(lab, x, y + a, w, b - a, bg, tol, depth)]
    if len(cols) > 1:
        parent.axis = "x"
        return [n for a, b in cols for n in _sub(lab, x + a, y, b - a, h, bg, tol, depth)]
    return _sub(lab, x, y, w, h, bg, tol, depth)


def _sub(lab, x, y, w, h, bg, tol, depth) -> list[Node]:
    """Trim a band to its ink bbox; if it has its own background (card, button) recurse inside it."""
    fg = np.linalg.norm(lab[y:y + h, x:x + w] - bg, axis=2) > tol
    ys, xs = np.flatnonzero(fg.any(axis=1)), np.flatnonzero(fg.any(axis=0))
    if ys.size == 0:
        return []
    node = Node(x + int(xs[0]), y + int(ys[0]), int(xs[-1] - xs[0] + 1), int(ys[-1] - ys[0] + 1))
    own_bg = _border_color(lab, node.x, node.y, node.w, node.h)
    if (depth < MAX_DEPTH and node.w > 2 and node.h > 2 and np.linalg.norm(own_bg - bg) > tol
            and _uniform_border(lab, node.x, node.y, node.w, node.h, own_bg, tol)):
        node.children = _cut(lab, node.x + 1, node.y + 1, node.w - 2, node.h - 2, own_bg, tol, depth + 1, node)
    elif depth < MAX_DEPTH:  # same background: may still hold several bands (e.g. words split by a wide gap)
        kids = _cut(lab, node.x, node.y, node.w, node.h, bg, tol, depth + 1, node)
        if len(kids) > 1:
            node.children = kids
    return [node]


def _number(node: Node, prefix: str) -> None:
    for i, c in enumerate(node.children):
        c.id = f"{prefix}{i}"
        _number(c, f"{c.id}.")


def _walk(node: Node):
    for c in node.children:
        yield c
        yield from _walk(c)


def _crop(img, n: Node, size=None):
    c = img[n.y:n.y + n.h, n.x:n.x + n.w]
    return cv2.resize(c, size, interpolation=cv2.INTER_AREA) if size else c


def _similarity(ref, test, a: Node, b: Node) -> float:
    ca, cb = _crop(ref, a), _crop(test, b, (a.w, a.h))
    return 1.0 - float(np.abs(ca.astype(np.int16) - cb).mean()) / 255.0


def pair(ref, test, rt: Node, tt: Node) -> dict[int, Node]:
    """Hungarian match of all ref nodes to test nodes on content, size and position. Returns {id(ref): test}."""
    rn, tn = list(_walk(rt)), list(_walk(tt))
    if not rn or not tn:
        return {}
    diag = float(np.hypot(*ref.shape[:2]))
    cost = np.full((len(rn), len(tn)), 1e6)
    for i, a in enumerate(rn):
        for j, b in enumerate(tn):
            size = abs(a.w - b.w) / max(a.w, b.w) + abs(a.h - b.h) / max(a.h, b.h)
            if size > 0.5:
                continue
            dist = np.hypot(a.x + a.w / 2 - b.x - b.w / 2, a.y + a.h / 2 - b.y - b.h / 2) / diag
            cost[i, j] = 4 * (1 - _similarity(ref, test, a, b)) + size + dist
    ri, ti = linear_sum_assignment(cost)
    # ponytail: fixed 1.0 cost cutoff decides "same element"; tune on real Figma pairs
    return {id(rn[i]): tn[j] for i, j in zip(ri, ti) if cost[i, j] < 1.0}


def _hex(img, n: Node) -> str:
    """Dominant color of a node: mode of 4-bit-quantized pixels, reported at full precision."""
    px = _crop(img, n).reshape(-1, 3)
    keys = (px >> 4).astype(np.int32) @ np.array([256, 16, 1])
    mode = np.bincount(keys).argmax()
    r, g, b = np.median(px[keys == mode], axis=0).astype(int)
    return f"#{r:02X}{g:02X}{b:02X}"


def explain(ref, test, ref_lab, test_lab, tol: float) -> list[dict]:
    rt, tt = segment(ref_lab, tol), segment(test_lab, tol)
    match = pair(ref, test, rt, tt)
    deltas: list[dict] = []
    matched_test = {id(n) for n in match.values()}

    def walk(parent: Node, tparent: Node | None):
        kids = parent.children
        for i, c in enumerate(kids):
            t = match.get(id(c))
            if t is None:
                if any(id(d) in match for d in _walk(c)):  # regrouped, not gone: look inside
                    walk(c, None)
                else:
                    deltas.append({"type": "missing", "element": c.id, "bbox": c.box})
                continue
            if (c.w, c.h) != (t.w, t.h):
                deltas.append({"type": "size", "element": c.id, "bbox": c.box,
                               "expected": [c.w, c.h], "actual": [t.w, t.h]})
            elif not c.children and _similarity(ref, test, c, t) < 0.995:
                e, a = _hex(ref, c), _hex(test, t)
                kind = "color" if e != a else "appearance"
                deltas.append({"type": kind, "element": c.id, "bbox": c.box, "expected": e, "actual": a}
                              if kind == "color" else {"type": kind, "element": c.id, "bbox": c.box})
            # position relative to previous sibling (gap) or to parent (padding); cross-axis = align
            prev, tprev = (kids[i - 1], match.get(id(kids[i - 1]))) if i else (parent, tparent)
            if tprev is not None:
                ax = parent.axis or "y"
                lead = (lambda n, p: n.y - (p.y + p.h if i else p.y)) if ax == "y" else \
                       (lambda n, p: n.x - (p.x + p.w if i else p.x))
                cross = (lambda n, p: n.x - p.x) if ax == "y" else (lambda n, p: n.y - p.y)
                e, a = lead(c, prev), lead(t, tprev)
                if e != a:
                    deltas.append({"type": "gap" if i else "padding", "element": c.id, "after": prev.id or "root",
                                   "axis": ax, "expected": e, "actual": a})
                e, a = cross(c, parent), cross(t, tparent) if tparent is not None else None
                if a is not None and e != a:
                    deltas.append({"type": "align", "element": c.id, "axis": "x" if ax == "y" else "y",
                                   "expected": e, "actual": a})
            walk(c, t)

    walk(rt, tt)
    # a container's size change is a consequence when something inside it already explains it
    inner = [d["element"] for d in deltas if d["type"] != "size"]
    deltas = [d for d in deltas if not (d["type"] == "size" and any(e.startswith(d["element"] + ".") for e in inner))]
    deltas += [{"type": "extra", "element": n.id, "bbox": n.box}
               for n in _walk(tt) if id(n) not in matched_test and not n.children]
    return deltas

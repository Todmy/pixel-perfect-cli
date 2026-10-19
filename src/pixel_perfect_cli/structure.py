"""Stages 3-5: segment both images into an element tree (XY-cut), pair elements, explain deltas as causes.

Pure translations are never reported per element: every move is decomposed into the gap/padding/align
change of its parent, so one changed margin yields one delta instead of a cascade of shifted regions.
"""

import time
from dataclasses import dataclass, field

import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment

MIN_GAP_X = 8  # vertical cuts need a blank column band this wide, so letters/words stay one element
MAX_DEPTH = 8
TOP_K = 32  # pairing candidates per element that get a content comparison
# Noise floor, calibrated on the same page rendered by Chromium/WebKit/Firefox/Chromium@2x (tests/fixtures/web/noise_*):
# ponytail: one global floor; per-element tolerances (text vs boxes) if real Figma pairs need tighter checks
PX_TOL = 2          # gap/padding/align/size changes below this are rasterizer noise (font metrics shift 1px)
SIZE_REL_TOL = 0.05  # text width differs up to ~4% between engines
MIN_AREA = 50       # smaller leaves are antialiased corner fragments
APPEARANCE_MIN = 0.005  # 1 - similarity below this is identical
APPEARANCE_SURE = 0.05  # above this an appearance change is confident; between -> "review" (escalate to VLM)


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


def _cut(lab, x, y, w, h, bg, tol, depth, parent, fg=None) -> list[Node]:
    # fg (ink mask of this region vs bg) is passed down as a slice when the background is unchanged
    if fg is None:
        fg = np.linalg.norm(lab[y:y + h, x:x + w] - bg, axis=2) > tol
    rows, cols = _bands(fg.any(axis=1), 1), _bands(fg.any(axis=0), MIN_GAP_X)
    if not rows:
        return []
    if len(rows) > 1:
        parent.axis = "y"
        return [n for a, b in rows for n in _sub(lab, x, y + a, w, b - a, bg, tol, depth, fg[a:b])]
    if len(cols) > 1:
        parent.axis = "x"
        return [n for a, b in cols for n in _sub(lab, x + a, y, b - a, h, bg, tol, depth, fg[:, a:b])]
    return _sub(lab, x, y, w, h, bg, tol, depth, fg)


def _sub(lab, x, y, w, h, bg, tol, depth, fg) -> list[Node]:
    """Trim a band to its ink bbox; if it has its own background (card, button) recurse inside it."""
    ys, xs = np.flatnonzero(fg.any(axis=1)), np.flatnonzero(fg.any(axis=0))
    if ys.size == 0:
        return []
    node = Node(x + int(xs[0]), y + int(ys[0]), int(xs[-1] - xs[0] + 1), int(ys[-1] - ys[0] + 1))
    own_bg = _border_color(lab, node.x, node.y, node.w, node.h)
    if (depth < MAX_DEPTH and node.w > 2 and node.h > 2 and np.linalg.norm(own_bg - bg) > tol
            and _uniform_border(lab, node.x, node.y, node.w, node.h, own_bg, tol)):
        node.children = _cut(lab, node.x + 1, node.y + 1, node.w - 2, node.h - 2, own_bg, tol, depth + 1, node)
    elif depth < MAX_DEPTH:  # same background: may still hold several bands (e.g. words split by a wide gap)
        kids = _cut(lab, node.x, node.y, node.w, node.h, bg, tol, depth + 1, node,
                    fg[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1])
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
    ca, cb = _crop(ref, a), _crop(test, b, (a.w, a.h) if (a.w, a.h) != (b.w, b.h) else None)
    return 1.0 - float(np.abs(ca.astype(np.int16) - cb).mean()) / 255.0


def pair(ref, test, rt: Node, tt: Node) -> dict[int, Node]:
    """Hungarian match of all ref nodes to test nodes on content, size and position. Returns {id(ref): test}."""
    rn, tn = list(_walk(rt)), list(_walk(tt))
    if not rn or not tn:
        return {}
    diag = float(np.hypot(*ref.shape[:2]))
    ra, ta = (np.array([[n.x, n.y, n.w, n.h] for n in ns], np.float64) for ns in (rn, tn))
    size = (np.abs(ra[:, None, 2] - ta[None, :, 2]) / np.maximum(ra[:, None, 2], ta[None, :, 2])
            + np.abs(ra[:, None, 3] - ta[None, :, 3]) / np.maximum(ra[:, None, 3], ta[None, :, 3]))
    dist = np.hypot(ra[:, None, 0] + ra[:, None, 2] / 2 - ta[None, :, 0] - ta[None, :, 2] / 2,
                    ra[:, None, 1] + ra[:, None, 3] / 2 - ta[None, :, 1] - ta[None, :, 3] / 2) / diag
    cheap = np.where(size > 0.5, np.inf, size + dist)  # lower bound of the full cost
    # ponytail: only the TOP_K cheapest candidates per row and per column get the (resize-heavy) content term;
    # a true match ranked below TOP_K by size+distance (very repetitive pages) is dropped; raise TOP_K then
    keep = np.zeros(cheap.shape, bool)
    for m, axis in ((cheap, 1), (cheap.T, 0)):
        k = min(TOP_K, m.shape[1])
        near = np.argpartition(m, k - 1, axis=1)[:, :k]
        rows = np.arange(m.shape[0])[:, None]
        if axis:
            keep[rows, near] = True
        else:
            keep[near, rows] = True
    keep &= np.isfinite(cheap) & (cheap < 1.0)  # cost >= cheap, and cost >= 1.0 is never accepted
    cost = np.full(cheap.shape, 1e6)
    for i, j in zip(*np.nonzero(keep)):
        cost[i, j] = 4 * (1 - _similarity(ref, test, rn[i], tn[j])) + cheap[i, j]
    ri, ti = linear_sum_assignment(cost)
    # ponytail: fixed 1.0 cost cutoff decides "same element"; tune on real Figma pairs
    return {id(rn[i]): tn[j] for i, j in zip(ri, ti) if cost[i, j] < 1.0}


def _hex(img, n: Node) -> tuple[str, float]:
    """Dominant color of a node (mode of 4-bit-quantized pixels, full precision) and its share of the area."""
    px = _crop(img, n).reshape(-1, 3)
    keys = (px >> 4).astype(np.int32) @ np.array([256, 16, 1])
    mode = np.bincount(keys).argmax()
    r, g, b = np.median(px[keys == mode], axis=0).astype(int)
    return f"#{r:02X}{g:02X}{b:02X}", float((keys == mode).mean())


def _hex_lab(h: str) -> np.ndarray:
    rgb = np.array([[[int(h[i:i + 2], 16) for i in (1, 3, 5)]]], np.float32) / 255.0
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2Lab)[0, 0]


def explain(ref, test, ref_lab, test_lab, tol: float, timing: dict | None = None) -> list[dict]:
    t0 = time.perf_counter()
    rt, tt = segment(ref_lab, tol), segment(test_lab, tol)
    t1 = time.perf_counter()
    match = pair(ref, test, rt, tt)
    if timing is not None:
        timing["segment"] = round((t1 - t0) * 1000, 1)
        timing["pair"] = round((time.perf_counter() - t1) * 1000, 1)
    deltas: list[dict] = []
    matched_test = {id(n) for n in match.values()}

    def walk(parent: Node, tparent: Node | None):
        kids = parent.children
        for i, c in enumerate(kids):
            t = match.get(id(c))
            if t is None:
                if any(id(d) in match for d in _walk(c)):  # regrouped, not gone: look inside
                    walk(c, None)
                elif c.w * c.h >= MIN_AREA:
                    deltas.append({"type": "missing", "element": c.id, "bbox": c.box})
                continue
            if c.w * c.h < MIN_AREA:
                continue
            dw, dh = t.w - c.w, t.h - c.h
            if (abs(dw) >= PX_TOL and abs(dw) / c.w >= SIZE_REL_TOL) or (abs(dh) >= PX_TOL and abs(dh) / c.h >= SIZE_REL_TOL):
                deltas.append({"type": "size", "element": c.id, "bbox": c.box,
                               "expected": [c.w, c.h], "actual": [t.w, t.h]})
            elif not c.children and (score := 1 - _similarity(ref, test, c, t)) >= APPEARANCE_MIN:
                (e, es), (a, as_) = _hex(ref, c), _hex(test, t)
                if (dw, dh) != (0, 0):  # glyph metrics differ: pixels aren't comparable, text needs OCR
                    deltas.append({"type": "appearance", "element": c.id, "bbox": c.box, "score": round(score, 4),
                                   "confidence": "low"})
                elif min(es, as_) >= 0.5 and np.linalg.norm(_hex_lab(e) - _hex_lab(a)) >= 2:  # solid fill
                    deltas.append({"type": "color", "element": c.id, "bbox": c.box, "expected": e, "actual": a})
                else:
                    deltas.append({"type": "appearance", "element": c.id, "bbox": c.box, "score": round(score, 4),
                                   "confidence": "high" if score >= APPEARANCE_SURE else "low"})
            # position relative to previous sibling (gap) or to parent (padding); cross-axis = align
            prev, tprev = (kids[i - 1], match.get(id(kids[i - 1]))) if i else (parent, tparent)
            if tprev is not None:
                ax = parent.axis or "y"
                lead = (lambda n, p: n.y - (p.y + p.h if i else p.y)) if ax == "y" else \
                       (lambda n, p: n.x - (p.x + p.w if i else p.x))
                cross = (lambda n, p: n.x - p.x) if ax == "y" else (lambda n, p: n.y - p.y)
                e, a = lead(c, prev), lead(t, tprev)
                # a sibling that only grew (wider text) shifts the gap but not the anchor: require both edges moved
                start = (lambda n, p: n.y - p.y) if ax == "y" else (lambda n, p: n.x - p.x)
                anchored = i and abs(start(c, prev) - start(t, tprev)) < PX_TOL
                if abs(e - a) >= PX_TOL and not anchored:
                    deltas.append({"type": "gap" if i else "padding", "element": c.id, "after": prev.id or "root",
                                   "axis": ax, "expected": e, "actual": a})
                e, a = cross(c, parent), cross(t, tparent) if tparent is not None else None
                if a is not None and abs(e - a) >= PX_TOL:
                    deltas.append({"type": "align", "element": c.id, "axis": "x" if ax == "y" else "y",
                                   "expected": e, "actual": a})
            walk(c, t)

    walk(rt, tt)
    # a container's size change is a consequence when something inside it already explains it
    inner = [d["element"] for d in deltas if d["type"] != "size"]
    deltas = [d for d in deltas if not (d["type"] == "size" and any(e.startswith(d["element"] + ".") for e in inner))]
    deltas += [{"type": "extra", "element": n.id, "bbox": n.box}
               for n in _walk(tt) if id(n) not in matched_test and not n.children and n.w * n.h >= MIN_AREA]
    return deltas

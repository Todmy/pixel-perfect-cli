"""Stages 3-5: build an element tree per side (structure map, or XY-cut of the pixels), pair elements,
explain deltas as causes.

Pure translations are never reported per element: every move is decomposed into the gap/padding/align
change of its parent, so one changed margin yields one delta instead of a cascade of shifted regions.
"""

import hashlib
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
HOT_MIN = 4  # a node's pixels "differ" when at least this many differ by more than tol (aligned on its own bbox)
COLOR_PROPS = ("color", "background-color")
LAYOUT_STYLES = {"padding", "gap", "border-width"}  # parent styles that move their children


@dataclass
class Node:
    x: int
    y: int
    w: int
    h: int
    axis: str = ""  # "y" or "x": how children were cut apart
    children: list["Node"] = field(default_factory=list)
    id: str = ""
    selector: str | None = None  # map nodes only
    text: str | None = None
    style: dict = field(default_factory=dict)

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


def _crop(img, n: Node):
    x, y, w, h = (round(v) for v in n.box)
    return img[max(y, 0):y + h, max(x, 0):x + w]


def _aligned(ref, test, a: Node, b: Node):
    """Crops of a and b, b resized to a's shape, or None when a is off-image."""
    ca, cb = _crop(ref, a), _crop(test, b)
    if not ca.size or not cb.size:
        return None
    if ca.shape != cb.shape:
        cb = cv2.resize(cb, ca.shape[1::-1], interpolation=cv2.INTER_AREA)
    return ca, cb


def _similarity(ref, test, a: Node, b: Node) -> float:
    c = _aligned(ref, test, a, b)
    return 1.0 if c is None else 1.0 - float(np.abs(c[0].astype(np.int16) - c[1]).mean()) / 255.0


def _hot(ref_lab, test_lab, a: Node, b: Node, tol: float) -> int:
    c = _aligned(ref_lab, test_lab, a, b)
    return 0 if c is None else int((np.linalg.norm(c[0] - c[1], axis=2) > tol).sum())


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


def _num(v):
    v = round(float(v), 1)
    return int(v) if v == int(v) else v


def _box(n: Node) -> list:
    return [_num(v) for v in n.box]


def causes(ref, test, rt: Node, tt: Node, match: dict[int, Node], look, ident, source: str):
    """Walk the design tree against its matched shot nodes and report causes, not cascades.

    look(c, t, resized) -> [(type, fields)] reports content changes of a matched node; ident(n) gives its stable id.
    Returns (deltas, cover): cover holds (outer, inner) boxes of matched leaves and of matched nodes that moved or
    resized; hot pixels there are judged or are consequences (inside outer, not wholly inside inner when set).
    """
    found: list[tuple[Node, dict]] = []
    cover: list[tuple[list, list | None]] = []

    def add(kind, c, t, **kw):
        d = {"type": kind, "id": ident(c)}
        if c.selector is not None:
            d |= {"selector": c.selector, "text": c.text}
        d |= {"bbox": _box(c), "shot_bbox": _box(t) if t is not None else None}
        found.append((c, d | kw | {"source": source}))

    def walk(parent: Node, tparent: Node | None):
        kids = parent.children
        for i, c in enumerate(kids):
            t = match.get(id(c))
            if t is None:
                if any(id(d) in match for d in _walk(c)):  # regrouped, not gone: look inside
                    walk(c, None)
                elif c.w * c.h >= MIN_AREA:
                    add("missing", c, None)
                continue
            if c.w * c.h < MIN_AREA:
                continue
            dw, dh = t.w - c.w, t.h - c.h
            x0, y0 = min(c.x, t.x), min(c.y, t.y)
            outer = [x0, y0, max(c.x + c.w, t.x + t.w) - x0, max(c.y + c.h, t.y + t.h) - y0]
            if max(abs(t.x - c.x), abs(t.y - c.y)) >= 1 or not c.children:  # moved, or a leaf look() judged
                cover.append((outer, None))
            elif max(abs(dw), abs(dh)) >= 1:  # same origin, grew or shrank: only the band between the edges
                cover.append((outer, [c.x, c.y, min(c.w, t.w), min(c.h, t.h)]))
            resized = bool((abs(dw) >= PX_TOL and abs(dw) / c.w >= SIZE_REL_TOL)
                           or (abs(dh) >= PX_TOL and abs(dh) / c.h >= SIZE_REL_TOL))
            if resized:
                add("size", c, t, expected=[_num(c.w), _num(c.h)], actual=[_num(t.w), _num(t.h)])
            for kind, kw in look(c, t, resized):
                add(kind, c, t, **kw)
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
                    add("gap" if i else "padding", c, t, after=ident(prev) if prev is not rt else "root",
                        axis=ax, expected=_num(e), actual=_num(a))
                e, a = cross(c, parent), cross(t, tparent) if tparent is not None else None
                if a is not None and abs(e - a) >= PX_TOL:
                    add("align", c, t, axis="x" if ax == "y" else "y", expected=_num(e), actual=_num(a))
            walk(c, t)

    walk(rt, tt)
    # a container's size change is a consequence when a content change of its own or anything inside explains it
    own = {id(n) for n, d in found if d["type"] in ("text", "color", "appearance")}
    inner = {id(n) for n, d in found if d["type"] != "size"}
    return [d for n, d in found if not (d["type"] == "size" and (
        id(n) in own or any(id(x) in inner for x in _walk(n))))], cover


def _stable_id(img, n: Node) -> str:
    """Content-derived id: bbox quantized to 4 px + dominant color, so it survives tree renumbering."""
    key = ",".join(str(round(v / 4)) for v in n.box) + _hex(img, n)[0]
    return "p" + hashlib.sha1(key.encode()).hexdigest()[:8]


def explain(ref, test, ref_lab, test_lab, tol: float, timing: dict | None = None) -> list[dict]:
    t0 = time.perf_counter()
    rt, tt = segment(ref_lab, tol), segment(test_lab, tol)
    t1 = time.perf_counter()
    match = pair(ref, test, rt, tt)
    if timing is not None:
        timing["segment"] = round((t1 - t0) * 1000, 1)
        timing["pair"] = round((time.perf_counter() - t1) * 1000, 1)
    ids: dict[int, str] = {}

    def ident(n: Node) -> str:  # design side is constant across fix iterations, so ids come from it
        if id(n) not in ids:
            ids[id(n)] = _stable_id(ref, n)
        return ids[id(n)]

    def look(c: Node, t: Node, resized: bool):
        if resized or c.children or (score := 1 - _similarity(ref, test, c, t)) < APPEARANCE_MIN:
            return []
        (e, es), (a, as_) = _hex(ref, c), _hex(test, t)
        if (t.w, t.h) != (c.w, c.h):  # glyph metrics differ: pixels aren't comparable, text needs OCR
            return [("appearance", {"score": round(score, 4), "confidence": "low"})]
        if min(es, as_) >= 0.5 and np.linalg.norm(_hex_lab(e) - _hex_lab(a)) >= 2:  # solid fill
            return [("color", {"expected": e, "actual": a})]
        return [("appearance", {"score": round(score, 4), "confidence": "high" if score >= APPEARANCE_SURE else "low"})]

    deltas, cover = causes(ref, test, rt, tt, match, look, ident, "pixels")
    matched_test = {id(n) for n in match.values()}
    deltas += [{"type": "extra", "id": _stable_id(test, n), "bbox": n.box, "shot_bbox": n.box, "source": "pixels"}
               for n in _walk(tt) if id(n) not in matched_test and not n.children and n.w * n.h >= MIN_AREA]
    return deltas, cover


def map_tree(smap: dict, k: float, dx: float = 0, dy: float = 0, skip: frozenset = frozenset()) -> Node:
    """Element tree of a structure map in image px (CSS px * k, minus the compensated page shift).

    Nodes in skip (masked) and their subtrees are left out.
    """
    root = Node(0, 0, 0, 0)
    by_id = {}
    for n in smap["nodes"]:  # parents precede children (DOM pre-order)
        parent = root if n.get("parent") is None else by_id.get(n["parent"], root)
        if n["id"] in skip or parent is None:
            by_id[n["id"]] = None  # masked subtree
            continue
        # ponytail: a node whose parent is absent from the map (zero-size wrapper) hangs off the root
        x, y, w, h = n["bbox"]
        node = Node(x * k - dx, y * k - dy, w * k, h * k, id=n["id"], selector=n.get("selector", n["id"]),
                    text=n.get("text"), style=n.get("style") or {})
        parent.children.append(node)
        by_id[n["id"]] = node
    for n in [root, *_walk(root)]:  # a row: every child starts right of where the previous one ended
        cs = n.children
        n.axis = "x" if len(cs) > 1 and all(b.x >= a.x + a.w - 1 for a, b in zip(cs, cs[1:])) else "y"
    return root


def _iou(a: Node, b: Node) -> float:
    iw = min(a.x + a.w, b.x + b.w) - max(a.x, b.x)
    ih = min(a.y + a.h, b.y + b.h) - max(a.y, b.y)
    inter = max(iw, 0) * max(ih, 0)
    return inter / (a.w * a.h + b.w * b.h - inter) if inter else 0.0


def pair_maps(rt: Node, tt: Node) -> dict[int, Node]:
    """Exact id match first (DOM vs DOM), then Hungarian on the rest (e.g. Figma names vs selectors)."""
    rn, tn = list(_walk(rt)), list(_walk(tt))
    tid = {n.id: n for n in tn}
    match = {id(n): tid[n.id] for n in rn if n.id in tid}
    used = {id(t) for t in match.values()}
    ra, ta = [n for n in rn if id(n) not in match], [n for n in tn if id(n) not in used]
    if ra and ta:
        cost = np.array([[(1 - _iou(a, b)) + 0.5 * (a.text != b.text)
                          + abs(a.w - b.w) / max(a.w, b.w) + abs(a.h - b.h) / max(a.h, b.h)
                          + 0.5 * np.mean([a.style.get(p) != b.style.get(p) for p in a.style.keys() | b.style.keys()] or [0])
                          for b in ta] for a in ra])
        # ponytail: same fixed 1.0 "same element" cutoff as the pixel pairing; tune on real Figma maps
        match |= {id(ra[i]): ta[j] for i, j in zip(*linear_sum_assignment(cost)) if cost[i, j] < 1.0}
    return match


def explain_maps(ref, test, ref_lab, test_lab, tol: float, rt: Node, tt: Node) -> list[dict]:
    match = pair_maps(rt, tt)

    def look(c: Node, t: Node, resized: bool):
        out = []
        if c.text != t.text:
            out.append(("text", {"expected": c.text, "actual": t.text, "confidence": "high"}))
        style = {p: [c.style.get(p), t.style.get(p)] for p in sorted(c.style.keys() | t.style.keys())
                 if c.style.get(p) != t.style.get(p)}
        colors = {p: v for p, v in style.items() if p in COLOR_PROPS}
        rest = {p: v for p, v in style.items() if p not in COLOR_PROPS}
        if style and _hot(ref_lab, test_lab, c, t, tol) >= HOT_MIN:
            if colors:
                (e, a), = list(colors.values())[:1]
                out.append(("color", {"expected": e, "actual": a, "style": colors, "confidence": "high"}))
            if rest:
                out.append(("appearance", {"style": rest, "confidence": "high"}))
        elif not out and not style and not c.children and not resized \
                and (score := 1 - _similarity(ref, test, c, t)) >= APPEARANCE_MIN:
            # same text, same style, other pixels: glyph rasterization (engine, hinting), not a code change
            sure = score >= APPEARANCE_SURE and not c.text
            out.append(("appearance", {"score": round(score, 4), "confidence": "high" if sure else "low"}))
        return out

    deltas, cover = causes(ref, test, rt, tt, match, look, lambda n: n.id, "map")
    # a parent's own padding/gap/border-width change already explains its children moving: report it once
    layout = {d["id"] for d in deltas if d["type"] == "appearance" and LAYOUT_STYLES & d.get("style", {}).keys()}
    moved = {k.id for n in _walk(rt) if n.id in layout for k in n.children}
    deltas = [d for d in deltas if not (d["type"] in ("align", "padding", "gap") and d["id"] in moved)]
    matched = {id(n) for n in match.values()}
    # reported once, at the highest unmatched shot node
    for p in [tt, *_walk(tt)]:
        if p is tt or id(p) in matched:
            deltas += [{"type": "extra", "id": n.id, "selector": n.selector, "text": n.text, "bbox": _box(n),
                        "shot_bbox": _box(n), "source": "map"}
                       for n in p.children if id(n) not in matched and n.w * n.h >= MIN_AREA]
    return deltas, cover

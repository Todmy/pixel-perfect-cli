"""Deterministic visual diff of two UI images: design vs screenshot -> JSON deltas."""

import argparse
import io
import json
import sys
import time

import cv2
import flip_evaluator
import numpy as np
from PIL import Image, ImageCms

from pixel_perfect_cli.structure import PX_TOL, SIZE_REL_TOL, Node, _iou, _walk, explain, explain_maps, map_tree

EXIT_PASS, EXIT_DELTAS, EXIT_REVIEW, EXIT_FATAL = 0, 1, 2, 12
SHIFT_CONF = 0.9  # phase-correlation confidence above which a whole-page shift is trusted and undone
MASK_GRAY = 128  # #808080
DPRS = (1, 1.5, 2, 3, 4, 1 / 1.5, 1 / 2, 1 / 3, 1 / 4)  # design/shot px ratios accepted as DPR when no map says so
SRGB = ImageCms.createProfile("sRGB")


class Timing(dict):
    """Per-stage ms. Wall-clock noise is not part of the deterministic result, so it never breaks equality."""

    def __eq__(self, other):
        return isinstance(other, Timing)

    __hash__ = None


def load(path: str) -> np.ndarray:
    """Decode to 8-bit sRGB RGB: convert embedded ICC (e.g. Display P3), flatten alpha onto white."""
    im = Image.open(path)
    if icc := im.info.get("icc_profile"):
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        mode = "RGBA" if "A" in im.getbands() else "RGB"
        im = ImageCms.profileToProfile(im.convert(mode), src, SRGB, outputMode=mode)
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return np.array(Image.alpha_composite(bg, im).convert("RGB"))


def match_size(ref: np.ndarray, test: np.ndarray, scale: float | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Bring test onto ref's pixel grid (DPR 2x/3x). scale = ref px per test px, from the maps' dpr when known.

    Same width after scaling, other height (the layout grew or shrank): both are cut to the shared height and the
    caller reports the difference. Other width = fatal.
    """
    (rh, rw), (th, tw) = ref.shape[:2], test.shape[:2]
    if (rh, rw) == (th, tw):
        return ref, test
    k = scale or rw / tw
    same_aspect = abs(rw / rh - tw / th) <= 0.01
    if abs(tw * k - rw) > 1 or not (scale or same_aspect or any(abs(k - d) <= 0.01 * d for d in DPRS)):
        raise ValueError(f"aspect mismatch: design {rw}x{rh}, shot {tw}x{th}")
    if same_aspect:
        return ref, cv2.resize(test, (rw, rh), interpolation=cv2.INTER_AREA)
    if k != 1:
        test = cv2.resize(test, (rw, max(1, round(th * k))), interpolation=cv2.INTER_AREA)
    h = min(rh, test.shape[0])
    return ref[:h], test[:h]


def crop_to_design(ref: np.ndarray, test: np.ndarray) -> np.ndarray:
    """Scale test to the design width, then crop or pad (white) its height to the design height."""
    (rh, rw), (th, tw) = ref.shape[:2], test.shape[:2]
    test = cv2.resize(test, (rw, max(1, round(th * rw / tw))), interpolation=cv2.INTER_AREA)
    if test.shape[0] >= rh:
        return test[:rh]
    return np.vstack([test, np.full((rh - test.shape[0], rw, 3), 255, np.uint8)])


def load_map(path: str) -> dict:
    """Read and validate a Contract v1 structure map."""
    m = json.load(open(path))
    if not isinstance(m, dict) or m.get("version") != 1 or not isinstance(m.get("nodes"), list):
        raise ValueError(f"{path}: not a structure map v1")
    for n in m["nodes"]:
        if not isinstance(n.get("id"), str) or not isinstance(n.get("bbox"), list) or len(n["bbox"]) != 4:
            raise ValueError(f"{path}: bad node {n.get('id')!r}")
    return m


def mask_rects(smap: dict | None, scale: float) -> list[tuple[int, int, int, int]]:
    """Pixel rects (x0, y0, x1, y1) of masked nodes: CSS px * dpr * scale to the design's pixel grid."""
    k = smap.get("dpr", 1) * scale if smap else 0
    return [(round(x * k), round(y * k), round((x + w) * k), round((y + h) * k))
            for n in (smap["nodes"] if smap else []) if n.get("masked") for x, y, w, h in [n["bbox"]]]


def paint(img: np.ndarray, rects: list[tuple[int, int, int, int]]) -> None:
    for x0, y0, x1, y1 in rects:
        img[max(y0, 0):y1, max(x0, 0):x1] = MASK_GRAY


def global_shift(ref: np.ndarray, test: np.ndarray) -> tuple[float, float, float]:
    """Whole-image translation of test relative to ref via phase correlation: (dx, dy, confidence)."""
    a, b = (cv2.cvtColor(x, cv2.COLOR_RGB2GRAY).astype(np.float32) for x in (ref, test))
    win = cv2.createHanningWindow(a.shape[::-1], cv2.CV_32F)
    (dx, dy), conf = cv2.phaseCorrelate(a, b, win)
    return round(dx, 2), round(dy, 2), round(conf, 3)


def lab(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img.astype(np.float32) / 255.0, cv2.COLOR_RGB2Lab)


def regions(ref: np.ndarray, test: np.ndarray, tol: float, min_area: int, ref_lab=None, test_lab=None) -> list[dict]:
    """Bboxes of pixels whose color differs by more than tol (Lab ΔE76), ranked by FLIP severity."""
    # ponytail: ΔE76 threshold stands in for odiff's antialiasing detector; swap in odiff if AA noise dominates
    mask = (np.linalg.norm((lab(ref) if ref_lab is None else ref_lab) - (lab(test) if test_lab is None else test_lab), axis=2) > tol).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    flip_map, _, _ = flip_evaluator.evaluate(ref / 255.0, test / 255.0, "LDR", applyMagma=False)
    flip_map = flip_map.squeeze()
    _, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    out = []
    for x, y, w, h, area in stats[1:]:
        if area < min_area:
            continue
        out.append({
            "bbox": [int(x), int(y), int(w), int(h)],
            "pixels": int(area),
            "severity": round(float(flip_map[y:y + h, x:x + w].max()), 3),
            "flip_mean": round(float(flip_map[y:y + h, x:x + w].mean()), 3),
        })
    return sorted(out, key=lambda r: (-r["severity"], r["bbox"]))


def annotate(deltas: list[dict], tree: Node, key: str) -> None:
    """Give each pixel delta the selector, text and id of the map node that overlaps its box best."""
    nodes = list(_walk(tree))
    for d in deltas:
        b = d.get(key) or d["bbox"]
        box = Node(*b)
        best = max(nodes, key=lambda n: (_iou(box, n), -n.w * n.h), default=None)  # tie: the innermost
        if best is not None and _iou(box, best) > 0:
            d |= {"id": best.id, "selector": best.selector, "text": best.text}


def unexplained(regs: list[dict], found: list[dict], cover: list) -> list[dict]:
    """Hot regions that no delta's design or shot box touches, and no moved or resized element accounts for."""
    cover = [(d[k], None) for d in found for k in ("bbox", "shot_bbox") if d.get(k)] + cover

    def inside(a, b):
        return b[0] <= a[0] and b[1] <= a[1] and a[0] + a[2] <= b[0] + b[2] and a[1] + a[3] <= b[1] + b[3]

    return [{"type": "unexplained", "bbox": r["bbox"], "severity": r["severity"]} for r in regs
            if not any(_iou(Node(*r["bbox"]), Node(*o)) > 0 and not (i and inside(r["bbox"], i)) for o, i in cover)]


def diff(design: str, shot: str, tol: float = 2.0, min_area: int = 4, *, design_map: str | None = None,
         shot_map: str | None = None, crop: bool = False) -> dict:
    timing = Timing()
    t0 = time.perf_counter()

    def lap(name: str) -> None:
        nonlocal t0
        t1 = time.perf_counter()
        timing[name] = round((t1 - t0) * 1000, 1)
        t0 = t1

    ref, test = load(design), load(shot)
    dmap, smap = (load_map(m) if m else None for m in (design_map, shot_map))
    native_w, native_h = test.shape[1], test.shape[0]
    design_h = ref.shape[0]
    extra = {}
    if crop and abs(ref.shape[1] / ref.shape[0] - native_w / native_h) > 0.01:
        test = crop_to_design(ref, test)
        extra["cropped"] = {"from": [native_w, native_h], "to": list(ref.shape[1::-1])}
    else:
        scale = dmap.get("dpr", 1) / smap.get("dpr", 1) if dmap and smap else None
        ref, test = match_size(ref, test, scale)
        shot_h = round(native_h * ref.shape[1] / native_w)
        if shot_h != design_h:  # only the shared height is compared; the rest is one page-size cause
            extra["height"] = {"design": design_h, "shot": shot_h, "compared": ref.shape[0]}
    # masked nodes from either map are painted on both images, in the design's pixel grid
    rects = mask_rects(dmap, 1) + mask_rects(smap, ref.shape[1] / native_w)
    paint(ref, rects)
    paint(test, rects)
    lap("load")
    dx, dy, conf = global_shift(ref, test)
    # with both maps, element positions are known on each side: moves are explained by the tree, not undone
    shifted = conf >= SHIFT_CONF and max(abs(dx), abs(dy)) >= 0.5 and not (dmap and smap)
    if shifted:  # undo whole-page translation so regions show only what moved relative to the layout
        m = np.float32([[1, 0, -round(dx)], [0, 1, -round(dy)]])
        test = cv2.warpAffine(test, m, test.shape[1::-1], borderMode=cv2.BORDER_REPLICATE)
        paint(test, rects)
    lap("shift")
    ref_lab, test_lab = lab(ref), lab(test)
    lap("lab")
    regs = regions(ref, test, tol, min_area, ref_lab, test_lab)
    lap("regions")
    sx, sy = (round(dx), round(dy)) if shifted else (0, 0)
    masked = frozenset(n["id"] for m in (dmap, smap) if m for n in m["nodes"] if n.get("masked"))
    k = ref.shape[1] / native_w
    rt = map_tree(dmap, dmap.get("dpr", 1), skip=masked) if dmap else None
    tt = map_tree(smap, smap.get("dpr", 1) * k, sx, sy, masked) if smap else None
    if rt and tt:
        found, cover = explain_maps(ref, test, ref_lab, test_lab, tol, rt, tt)
    else:
        found, cover = explain(ref, test, ref_lab, test_lab, tol, timing) if regs else ([], [])
        if rt or tt:
            annotate(found, rt or tt, "bbox" if rt else "shot_bbox")
    found += unexplained(regs, found, cover)
    lap("explain")
    deltas = [d for d in found if d.get("confidence") != "low" and d["type"] != "unexplained"]
    dh = abs(hh["shot"] - hh["design"]) if (hh := extra.get("height")) else 0
    # like any container: a size change nothing inside explains, at least PX_TOL and SIZE_REL_TOL of it
    if dh >= PX_TOL and dh / hh["design"] >= SIZE_REL_TOL and not deltas:
        top = next((n for n in (dmap or {}).get("nodes", []) if n.get("parent") is None), None)
        w = ref.shape[1]
        deltas.append({"type": "size", "id": top["id"] if top else "root"}
                      | ({"selector": top.get("selector", top["id"]), "text": top.get("text")} if top else {})
                      | {"bbox": [0, 0, w, hh["design"]], "shot_bbox": [0, 0, w, hh["shot"]],
                         "expected": [w, hh["design"]], "actual": [w, hh["shot"]], "source": "pixels"})
    review = [d for d in found if d.get("confidence") == "low" or d["type"] == "unexplained"]
    return {
        "status": "deltas" if deltas or shifted else "review" if review else "pass",
        "size": list(ref.shape[1::-1]),
        "global": {"dx": dx, "dy": dy, "confidence": conf, "compensated": shifted, **extra},
        "deltas": deltas,
        "review": review,  # low-confidence appearance changes: escalate crops to a VLM, don't auto-fix
        "regions": regs,
        "timing_ms": timing,
    }


def main() -> None:
    p = argparse.ArgumentParser(prog="pixel-perfect", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diff", help="compare a design image with a screenshot")
    d.add_argument("design")
    d.add_argument("shot")
    d.add_argument("--design-map", help="structure map JSON of the design")
    d.add_argument("--shot-map", help="structure map JSON of the screenshot")
    d.add_argument("--crop-to-design", action="store_true", help="scale shot to design width, crop/pad height, instead of exit 12")
    d.add_argument("--tol", type=float, default=2.0, help="color tolerance, Lab ΔE76; ~2.3 is just noticeable (default 2.0)")
    d.add_argument("--min-area", type=int, default=4, help="drop regions smaller than N px (default 4)")
    c = sub.add_parser("capture", help="screenshot a URL or HTML file, optionally with a structure map")
    c.add_argument("target", metavar="URL_OR_HTML_FILE")
    c.add_argument("--out", required=True, metavar="SHOT.png")
    c.add_argument("--map", metavar="S.json")
    c.add_argument("--width", type=int, default=1440)
    g = c.add_mutually_exclusive_group()
    g.add_argument("--height", type=int, default=900)
    g.add_argument("--full-page", action="store_true")
    c.add_argument("--dpr", type=float, default=1)
    c.add_argument("--mask", action="append", default=[], metavar="SELECTOR", help="paint matching elements #808080 (repeatable)")
    c.add_argument("--browser", choices=["chromium", "webkit", "firefox"], default="chromium")
    a = p.parse_args()
    try:
        if a.cmd == "capture":
            from pixel_perfect_cli.capture import capture
            m = capture(a.target, a.out, map_path=a.map, width=a.width, height=a.height, full_page=a.full_page,
                        dpr=a.dpr, masks=a.mask, browser=a.browser)
            print(json.dumps({"status": "ok", "out": a.out, "map": a.map, "nodes": len(m["nodes"])}))
            sys.exit(EXIT_PASS)
        result = diff(a.design, a.shot, a.tol, a.min_area, design_map=a.design_map, shot_map=a.shot_map,
                      crop=a.crop_to_design)
    except Exception as e:  # capture can fail in Playwright (navigation, timeout); always report as fatal JSON
        print(json.dumps({"status": "fatal", "error": str(e).splitlines()[0] if str(e) else type(e).__name__}))
        sys.exit(EXIT_FATAL)
    print(json.dumps(result, indent=2))
    sys.exit({"pass": EXIT_PASS, "review": EXIT_REVIEW}.get(result["status"], EXIT_DELTAS))

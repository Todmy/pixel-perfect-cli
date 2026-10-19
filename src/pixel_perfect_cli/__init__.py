"""Deterministic visual diff of two UI images: design vs screenshot -> JSON deltas."""

import argparse
import io
import json
import sys

import cv2
import flip_evaluator
import numpy as np
from PIL import Image, ImageCms

EXIT_PASS, EXIT_DELTAS, EXIT_FATAL = 0, 1, 12
SRGB = ImageCms.createProfile("sRGB")


def load(path: str) -> np.ndarray:
    """Decode to 8-bit sRGB RGB: convert embedded ICC (e.g. Display P3), flatten alpha onto white."""
    im = Image.open(path)
    if icc := im.info.get("icc_profile"):
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        mode = "RGBA" if "A" in im.getbands() else "RGB"
        im = ImageCms.profileToProfile(im.convert(mode), src, SRGB, outputMode=mode)
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return np.asarray(Image.alpha_composite(bg, im).convert("RGB"))


def match_size(ref: np.ndarray, test: np.ndarray) -> np.ndarray:
    """Resize test to ref when they differ only by scale (DPR 2x/3x). Different aspect = fatal."""
    (rh, rw), (th, tw) = ref.shape[:2], test.shape[:2]
    if (rh, rw) == (th, tw):
        return test
    if abs(rw / rh - tw / th) > 0.01:
        raise ValueError(f"aspect mismatch: design {rw}x{rh}, shot {tw}x{th}")
    return cv2.resize(test, (rw, rh), interpolation=cv2.INTER_AREA)


def global_shift(ref: np.ndarray, test: np.ndarray) -> tuple[float, float, float]:
    """Whole-image translation of test relative to ref via phase correlation: (dx, dy, confidence)."""
    a, b = (cv2.cvtColor(x, cv2.COLOR_RGB2GRAY).astype(np.float32) for x in (ref, test))
    win = cv2.createHanningWindow(a.shape[::-1], cv2.CV_32F)
    (dx, dy), conf = cv2.phaseCorrelate(a, b, win)
    return round(dx, 2), round(dy, 2), round(conf, 3)


def lab(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img.astype(np.float32) / 255.0, cv2.COLOR_RGB2Lab)


def regions(ref: np.ndarray, test: np.ndarray, tol: float, min_area: int) -> list[dict]:
    """Bboxes of pixels whose color differs by more than tol (Lab ΔE76), ranked by FLIP severity."""
    # ponytail: ΔE76 threshold stands in for odiff's antialiasing detector; swap in odiff if AA noise dominates
    mask = (np.linalg.norm(lab(ref) - lab(test), axis=2) > tol).astype(np.uint8)
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


def diff(design: str, shot: str, tol: float = 2.0, min_area: int = 4) -> dict:
    ref, test = load(design), load(shot)
    test = match_size(ref, test)
    dx, dy, conf = global_shift(ref, test)
    regs = regions(ref, test, tol, min_area)
    return {
        "status": "deltas" if regs else "pass",
        "size": list(ref.shape[1::-1]),
        "global": {"dx": dx, "dy": dy, "confidence": conf},
        "regions": regs,
    }


def main() -> None:
    p = argparse.ArgumentParser(prog="pixel-perfect", description=__doc__)
    p.add_argument("design")
    p.add_argument("shot")
    p.add_argument("--tol", type=float, default=2.0, help="color tolerance, Lab ΔE76; ~2.3 is just noticeable (default 2.0)")
    p.add_argument("--min-area", type=int, default=4, help="drop regions smaller than N px (default 4)")
    a = p.parse_args()
    try:
        result = diff(a.design, a.shot, a.tol, a.min_area)
    except (OSError, ValueError) as e:
        print(json.dumps({"status": "fatal", "error": str(e)}))
        sys.exit(EXIT_FATAL)
    print(json.dumps(result, indent=2))
    sys.exit(EXIT_PASS if result["status"] == "pass" else EXIT_DELTAS)

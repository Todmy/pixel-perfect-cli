from pathlib import Path

import numpy as np
from PIL import Image

from pixel_perfect_cli import diff

FX = Path(__file__).parent / "fixtures"
DESIGN, SHOT = str(FX / "design.png"), str(FX / "shot.png")


def save(arr, tmp_path, name):
    p = tmp_path / name
    Image.fromarray(arr).save(p)
    return str(p)


def test_identical_passes():
    assert diff(DESIGN, DESIGN)["status"] == "pass"


def test_fixture_finds_button_color_and_card_shift():
    boxes = [r["bbox"] for r in diff(DESIGN, SHOT)["regions"]]
    assert [20, 160, 141, 41] in boxes  # button #3366FF -> #3360F0
    assert [40, 40, 6, 21] in boxes     # card shifted 6px: left edge of title


def test_global_shift_detected(tmp_path):
    img = np.asarray(Image.open(DESIGN).convert("RGB"))
    shifted = save(np.roll(img, 6, axis=1), tmp_path, "shifted.png")
    g = diff(DESIGN, shifted)["global"]
    assert abs(g["dx"] - 6) < 0.5 and abs(g["dy"]) < 0.5


def test_retina_2x_screenshot_normalized(tmp_path):
    big = Image.open(DESIGN).convert("RGB").resize((800, 600), Image.NEAREST)
    assert diff(DESIGN, save(np.asarray(big), tmp_path, "2x.png"))["status"] == "pass"


def test_deterministic():
    assert diff(DESIGN, SHOT) == diff(DESIGN, SHOT)

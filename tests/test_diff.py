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


WEB = Path(__file__).parent / "fixtures" / "web"


def web(variant):
    return diff(str(WEB / "base.png"), str(WEB / f"{variant}.png"))


def test_web_rerender_is_noise_free():
    assert web("rerender")["status"] == "pass"


def test_web_single_element_changes_give_one_region():
    assert len(web("color")["regions"]) == 1
    assert len(web("text")["regions"]) == 1


def test_web_whole_page_shift_is_compensated():
    d = web("shift")
    assert d["global"]["compensated"] and d["global"]["dx"] == 6.0
    assert d["status"] == "deltas" and d["regions"] == []


def kinds(variant):
    return [(d["type"], d.get("expected"), d.get("actual")) for d in web(variant)["deltas"]]


def test_web_gap_cascade_collapses_to_one_cause():
    assert kinds("gap") == [("gap", 14, 20)]


def test_web_color_reports_hex():
    assert kinds("color") == [("color", "#3366FF", "#3360F0")]


def test_web_font_size_reports_heading_size():
    assert ("size", [175, 19], [192, 21]) in kinds("font_size")


def test_web_missing_button():
    d = web("missing")["deltas"]
    assert [x["bbox"] for x in d if x["type"] == "missing"] == [[166, 137, 75, 43]]


def test_web_text_change_goes_to_review():
    d = web("text")
    assert d["status"] == "review" and [(x["type"], x["source"]) for x in d["review"]] == [("appearance", "pixels")]


def test_noise_retina_has_no_confident_deltas():
    assert web("noise_chromium2x")["deltas"] == []


def test_noise_other_engines_stay_under_floor():
    # known residue: "Storage" descender height (WebKit/Firefox), Firefox bold "12"
    assert len(web("noise_webkit")["deltas"]) <= 1
    assert len(web("noise_firefox")["deltas"]) <= 2

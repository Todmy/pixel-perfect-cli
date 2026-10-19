import numpy as np
import pytest
from PIL import Image

from pixel_perfect_cli import diff

from test_diff import WEB, web

CARD = "body>div.card:nth-of-type(1)"
BTN = CARD + ">div.row>span.btn:nth-of-type(1)"


def mapped(variant, design="base"):
    return diff(str(WEB / f"{design}.png"), str(WEB / f"{variant}.png"),
                design_map=str(WEB / f"{design}.json"), shot_map=str(WEB / f"{variant}.json"))


def causes(variant):
    d = mapped(variant)["deltas"]
    for x in d:
        assert x["source"] == "map" and {"id", "selector", "text", "bbox", "shot_bbox"} <= x.keys()
    return d


def test_gap_is_the_paragraph_margin():
    [d] = causes("gap")
    assert (d["type"], d["selector"], d["expected"], d["actual"]) == ("gap", CARD + ">p", 8, 14)


def test_color_is_the_button_background():
    [d] = causes("color")
    assert (d["type"], d["selector"], d["expected"], d["actual"]) == ("color", BTN, "#3366FF", "#3360F0")


def test_text_change_carries_both_strings():
    [d] = causes("text")
    assert (d["type"], d["expected"], d["actual"], d["confidence"]) == ("text", "2.1 GB", "2.4 GB", "high")


def test_radius_is_a_confident_style_appearance():
    d = causes("radius")  # .btn rule hits both buttons
    assert [x["selector"] for x in d] == [BTN, CARD + ">div.row>span.btn.ghost:nth-of-type(2)"]
    assert all(x["type"] == "appearance" and x["confidence"] == "high"
               and x["style"] == {"border-radius": ["8px", "12px"]} for x in d)


def test_missing_ghost_button_once():
    [d] = causes("missing")
    assert (d["type"], d["selector"]) == ("missing", CARD + ">div.row>span.btn.ghost:nth-of-type(2)")


def test_font_size_is_one_heading_cause():
    [d] = causes("font_size")
    assert d["selector"] == CARD + ">h2" and d["type"] in ("size", "appearance")
    assert d["style"] == {"font-size": ["20px", "22px"], "line-height": ["28px", "30.8px"]}  # 1.4 follows the size


def test_font_family_is_a_confident_style_appearance():
    [d] = causes("font_family")
    assert (d["type"], d["selector"], d["confidence"]) == ("appearance", CARD + ">h2", "high")
    assert list(d["style"]) == ["font-family"] and d["style"]["font-family"][1] == "Georgia, serif"


def test_shadow_is_a_confident_style_appearance():
    [d] = causes("shadow")
    assert (d["type"], d["selector"], d["confidence"]) == ("appearance", CARD, "high")
    assert d["style"] == {"box-shadow": ["none", "rgba(16, 24, 40, 0.25) 0px 8px 24px 0px"]}


def test_parent_padding_explains_shifted_children():
    [d] = causes("shift")  # not also an align per child
    assert (d["type"], d["selector"], d["confidence"]) == ("appearance", "body", "high")
    assert d["style"] == {"padding": ["32px", "32px 32px 32px 38px"]}


@pytest.mark.parametrize("variant", ["rerender", "noise_webkit", "noise_firefox", "noise_chromium2x"])
def test_noise_with_maps_has_no_confident_deltas(variant):
    assert causes(variant) == []


def test_map_ids_stable_across_iterations():
    first = [x["id"] for x in mapped("color")["deltas"]]
    mapped("gap")
    assert [x["id"] for x in mapped("color")["deltas"]] == first == [BTN]
    assert BTN in [x["id"] for x in mapped("radius")["deltas"]]


def test_pixel_ids_come_from_the_design_side():
    # the same design element keeps its id whatever the shot looks like
    [color] = web("color")["deltas"]
    assert color["id"] in [x["id"] for x in web("radius")["review"]]
    assert not color["id"].startswith("e")  # not a tree position


def test_one_map_annotates_pixel_deltas():
    [d] = diff(str(WEB / "base.png"), str(WEB / "color.png"), design_map=str(WEB / "base.json"))["deltas"]
    assert (d["type"], d["source"], d["selector"], d["text"]) == ("color", "pixels", BTN, "Upgrade")
    [d] = diff(str(WEB / "base.png"), str(WEB / "color.png"), shot_map=str(WEB / "color.json"))["deltas"]
    assert d["selector"] == BTN


def test_uncovered_hot_region_is_unexplained(tmp_path):
    img = np.asarray(Image.open(WEB / "base.png").convert("RGB")).copy()
    img[420:440, 400:420] = (255, 0, 0)  # below body: no element there on either side
    Image.fromarray(img).save(tmp_path / "s.png")
    r = diff(str(WEB / "base.png"), str(tmp_path / "s.png"),
             design_map=str(WEB / "base.json"), shot_map=str(WEB / "base.json"))
    assert r["status"] == "review" and r["deltas"] == []
    assert [(x["type"], x["bbox"]) for x in r["review"]] == [("unexplained", [400, 420, 20, 20])]

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


# review fixes (T12)

VARIANTS = sorted(p.stem for p in WEB.glob("*.png") if p.stem != "base")


@pytest.mark.parametrize("variant", VARIANTS)
@pytest.mark.parametrize("maps", [False, True])
def test_every_delta_and_review_item_carries_the_contract_fields(variant, maps):
    kw = {"design_map": str(WEB / "base.json"), "shot_map": str(WEB / f"{variant}.json")} if maps else {}
    r = diff(str(WEB / "base.png"), str(WEB / f"{variant}.png"), **kw)
    for d in r["deltas"] + r["review"]:
        assert {"type", "id", "bbox", "confidence", "source"} <= d.keys(), d
        assert d["confidence"] in ("high", "low") and d["source"] in ("map", "pixels")


def _run(dm, sm=None):
    from unittest.mock import patch
    import pixel_perfect_cli as p
    a = np.full((100, 100, 3), 255, np.uint8)
    b = a.copy()
    b[10:20, 10:20] = (255, 0, 0)
    with patch.object(p, "load", side_effect=[a, b]), patch.object(p, "load_map", side_effect=[dm] + ([sm] if sm else [])):
        return p.diff("d.png", "s.png", design_map="d.json", shot_map="s.json" if sm else None)


def _m(ident, box, masked=False):
    return {"version": 1, "dpr": 1, "nodes": [{"id": ident, "selector": ident, "bbox": box, "masked": masked}]}


def test_mask_partly_off_image_does_not_wrap_around():
    r = _run(_m("off", [-30, -30, 10, 10], True))
    assert r["status"] == "deltas" and r["regions"][0]["bbox"] == [10, 10, 10, 10]


def test_mask_hides_nodes_of_the_other_side_with_another_id():
    r = _run(_m("figma-clock", [10, 10, 10, 10], True), _m("body>.clock", [10, 10, 10, 10]))
    assert r["deltas"] == [] and r["status"] == "pass"


def test_pair_maps_pairs_differently_named_ids_fast():
    import time
    import pixel_perfect_cli.structure as s
    n = 600
    tree = lambda pre: s.Node(0, 0, 1440, 4000, children=[s.Node(i % 20 * 60, i // 20 * 30, 40, 20, id=pre + str(i)) for i in range(n)])
    rt, tt = tree("figma"), tree("dom")
    t = time.time()
    match = s.pair_maps(rt, tt)
    assert time.time() - t < 0.5
    assert all(match[id(a)].id == "dom" + a.id[5:] for a in rt.children)


# CSS fix hints (T16, contract v1.2)

GHOST = CARD + ">div.row>span.btn.ghost:nth-of-type(2)"


@pytest.mark.parametrize("variant, fixes", [
    ("gap", [{"selector": CARD + ">p", "property": "margin-top", "value": "8px"}]),
    ("color", [{"selector": BTN, "property": "background-color", "value": "#3366FF"}]),
    ("font_size", [{"selector": CARD + ">h2", "property": "font-size", "value": "20px"}]),
    ("radius", [{"selector": s, "property": "border-radius", "value": "8px"} for s in (BTN, GHOST)]),
    ("shift", [{"selector": "body", "property": "padding-left", "value": "32px"}]),
    ("missing", [None]),  # the map carries no display: not knowable
    ("text", [None]),  # content, not CSS
])
def test_map_deltas_carry_the_css_fix(variant, fixes):
    assert [d["fix"] for d in causes(variant)] == fixes


@pytest.mark.parametrize("variant", ["rerender", "noise_webkit", "noise_firefox", "noise_chromium2x"])
def test_noise_has_no_fix(variant):
    r = mapped(variant)
    assert [d for d in r["deltas"] + r["review"] if d.get("fix")] == []


def test_pixel_deltas_have_a_null_fix():
    assert [d["fix"] for d in web("color")["deltas"]] == [None]


def test_border_color_shorthand_splits_per_side():
    import pixel_perfect_cli.structure as s
    st = lambda c: {"border-color": f"rgb(16, 24, 40) rgb(16, 24, 40) rgb(16, 24, 40) {c}"}  # noqa: E731
    a, b = s.Node(0, 0, 10, 10, id="q", selector="q", style=st("#3366FF")), s.Node(0, 0, 10, 10, id="q", style=st("#101828"))
    fix = s._fix({"type": "appearance", "id": "q"}, {"q": a}, {}, {id(a): b})
    assert fix == {"selector": "q", "property": "border-left-color", "value": "#3366FF"}

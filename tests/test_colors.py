import json
import re

from pixel_perfect_cli import diff

from test_diff import WEB

BTN = "body>div.card:nth-of-type(1)>div.row>span.btn:nth-of-type(1)"


def as_rgb(path, out):
    """The same map with every hex color written as rgb(), as another dumper would print it."""
    rgb = lambda m: "rgb({}, {}, {})".format(*(int(m[1][i:i + 2], 16) for i in (0, 2, 4)))
    m = json.load(open(path))
    for n in m["nodes"]:
        n["style"] = {p: re.sub(r"#([0-9A-Fa-f]{6})\b", rgb, v) for p, v in n["style"].items()}
    json.dump(m, open(out, "w"))
    return str(out)


def test_hex_design_vs_rgb_shot_is_no_delta(tmp_path):
    shot = as_rgb(WEB / "noise_firefox.json", tmp_path / "noise.json")  # other engine: pixels differ, styles do not
    assert "#" not in open(shot).read()
    r = diff(str(WEB / "base.png"), str(WEB / "noise_firefox.png"), design_map=str(WEB / "base.json"), shot_map=shot)
    assert r["deltas"] == []


def test_one_color_change_is_one_hex_delta(tmp_path):
    shot = as_rgb(WEB / "color.json", tmp_path / "color.json")
    [d] = diff(str(WEB / "base.png"), str(WEB / "color.png"), design_map=str(WEB / "base.json"), shot_map=shot)["deltas"]
    assert (d["type"], d["selector"], d["expected"], d["actual"]) == ("color", BTN, "#3366FF", "#3360F0")
    assert d["fix"] == {"selector": BTN, "property": "background-color", "value": "#3366FF"}

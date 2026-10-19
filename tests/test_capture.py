import json
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

from pixel_perfect_cli import diff
from pixel_perfect_cli.capture import capture

HTML = """<!doctype html><style>body{margin:0;font:16px Arial}.card{width:300px;height:100px;background:#F2F4F7;margin:20px}
.clock{width:120px;height:40px;background:#ff0000;margin:20px}</style>
<body><div class="card"><h2>Title</h2></div><div class="card"><p>Two</p></div><div class="clock">12:00</div></body>"""
GREEN = HTML.replace("#ff0000", "#00aa00")


def shoot(tmp_path, name, html=HTML, **kw):
    src = tmp_path / f"{name}.html"
    src.write_text(html)
    return capture(str(src), str(tmp_path / f"{name}.png"), map_path=str(tmp_path / f"{name}.json"),
                   width=400, height=300, **kw)


def test_map_is_stable_and_follows_contract(tmp_path):
    a, b = shoot(tmp_path, "a"), shoot(tmp_path, "b")
    assert a["nodes"] == b["nodes"]
    ids = [n["id"] for n in a["nodes"]]
    assert "body>div.card:nth-of-type(2)>p" in ids and len(ids) == len(set(ids))
    card = next(n for n in a["nodes"] if n["id"] == "body>div.card:nth-of-type(1)")
    assert card["bbox"] == [20, 20, 300, 100] and card["parent"] == "body"
    assert card["style"]["background-color"] == "#F2F4F7" and card["selector"] == card["id"]
    assert next(n for n in a["nodes"] if n["tag"] == "h2")["text"] == "Title"


def test_mask_painted_and_marked(tmp_path):
    m = shoot(tmp_path, "m", masks=[".clock"])
    assert Image.open(tmp_path / "m.png").convert("RGB").getpixel((40, 280)) == (128, 128, 128)
    assert [n["id"] for n in m["nodes"] if n.get("masked")] == ["body>div.clock:nth-of-type(3)"]
    assert json.loads((tmp_path / "m.json").read_text())["nodes"] == m["nodes"]


def test_dpr_scales_image_not_map(tmp_path):
    m = shoot(tmp_path, "d", dpr=2)
    assert Image.open(tmp_path / "d.png").size == (800, 600) and m["dpr"] == 2


def test_diff_masks_hide_dynamic_region(tmp_path):
    shoot(tmp_path, "a"), shoot(tmp_path, "b", GREEN)
    assert diff(str(tmp_path / "a.png"), str(tmp_path / "b.png"))["regions"]
    shoot(tmp_path, "ma", masks=[".clock"]), shoot(tmp_path, "mb", GREEN, masks=[".clock"])
    assert diff(str(tmp_path / "ma.png"), str(tmp_path / "mb.png"))["status"] == "pass"
    # maps alone (unmasked images) paint the region on both sides
    r = diff(str(tmp_path / "a.png"), str(tmp_path / "b.png"), design_map=str(tmp_path / "ma.json"))
    assert r["regions"] == []
    r = diff(str(tmp_path / "a.png"), str(tmp_path / "b.png"), shot_map=str(tmp_path / "mb.json"))
    assert r["regions"] == []


@pytest.mark.parametrize("name,rows,expect", [("tall", 300, [100, 300]), ("short", 120, [100, 120])])
def test_crop_to_design(tmp_path, name, rows, expect):
    img = np.full((300, 100, 3), 255, np.uint8)
    img[10:30, 10:50] = (200, 0, 0)
    design = np.full((200, 100, 3), 255, np.uint8)
    design[10:30, 10:50] = (200, 0, 0)
    Image.fromarray(design).save(tmp_path / "d.png")
    Image.fromarray(img[:rows]).save(tmp_path / "s.png")
    r = diff(str(tmp_path / "d.png"), str(tmp_path / "s.png"), crop=True)
    assert r["global"]["cropped"] == {"from": expect, "to": [100, 200]} and r["status"] == "pass"
    with pytest.raises(ValueError, match="aspect mismatch"):
        diff(str(tmp_path / "d.png"), str(tmp_path / "s.png"))


def cli(*args):
    return subprocess.run([sys.executable, "-c", "from pixel_perfect_cli import main; main()", *args],
                          capture_output=True, text=True)


def test_cli_subcommands(tmp_path):
    (tmp_path / "p.html").write_text(HTML)
    out = str(tmp_path / "s.png")
    r = cli("capture", str(tmp_path / "p.html"), "--out", out, "--width", "400")
    assert r.returncode == 0 and json.loads(r.stdout)["status"] == "ok", r.stderr
    r = cli("diff", out, out)
    assert r.returncode == 0 and json.loads(r.stdout)["status"] == "pass"
    assert cli(out, out).returncode == 2  # bare form dropped (argparse usage error)

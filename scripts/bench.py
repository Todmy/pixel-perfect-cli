"""Time diff() per stage on a deterministic 1440x4000 page (300+ elements) vs a mutated copy.

Run: uv run python scripts/bench.py [--keep DIR]
"""

import argparse
import hashlib
import json
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from pixel_perfect_cli import diff

CSS = """
* { box-sizing: border-box; margin: 0; }
body { font: 15px/1.4 Helvetica, Arial, sans-serif; background: #fff; color: #101828; padding: 32px; width: 1440px; }
.grid { display: flex; flex-wrap: wrap; gap: 24px; }
.card { width: 320px; padding: 20px; border-radius: 12px; background: #F2F4F7; }
.card h3 { font-size: 18px; } .card p { margin-top: 6px; color: #667085; }
.row { display: flex; gap: 10px; margin-top: 14px; }
.btn { padding: 8px 14px; border-radius: 8px; background: #3366FF; color: #fff; font-weight: 600; }
.btn.ghost { background: transparent; color: #3366FF; border: 1px solid #3366FF; }
h1 { margin: 32px 0 16px; font-size: 28px; }
table { border-collapse: collapse; width: 1376px; }
td { padding: 10px 12px; border-bottom: 1px solid #EAECF0; }
.hero { width: 600px; height: 160px; background: linear-gradient(135deg, #7A5AF8, #3366FF); border-radius: 16px; }
"""


ROWS = 60


def page(mutated: bool) -> str:
    cards = "".join(
        f'<div class="card"><h3>Plan {i}</h3><p>Includes {i * 3} seats and support.</p>'
        f'<div class="row"><span class="btn">Buy</span><span class="btn ghost">Later</span></div></div>'
        for i in range(24)
    )
    rows = "".join(
        f"<tr><td>User {i}</td><td>user{i}@example.com</td><td>{'Admin' if i % 5 == 0 else 'Member'}</td><td>{i * 7 % 100} GB</td></tr>"
        for i in range(ROWS)
    )
    html = f'<body><div class="hero"></div><h1>Plans</h1><div class="grid">{cards}</div><h1>Team</h1><table>{rows}</table></body>'
    if mutated:  # a few changes: one gap, one color, one text, one missing button
        html = html.replace("Includes 6 seats", "Includes 9 seats", 1)
        html = html.replace('<span class="btn ghost">Later</span>', "", 1)
    extra = ".card:nth-child(7) p { margin-top: 14px; } .card:nth-child(12) .btn { background: #3360F0; }" if mutated else ""
    return f"<!doctype html><html><head><style>{CSS}{extra}</style></head>{html}</html>"


def render(out: Path) -> None:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 4000}, device_scale_factor=1)
        for name, m in (("ref", False), ("test", True)):
            pg.set_content(page(m))
            pg.screenshot(path=out / f"{name}.png", clip={"x": 0, "y": 0, "width": 1440, "height": 4000}, animations="disabled", caret="hide")
        n = pg.evaluate("document.querySelectorAll('body *').length")
        b.close()
    print(f"rendered 1440x4000, {n} elements")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", help="directory to keep the PNGs in")
    ap.add_argument("--rows", type=int, default=60, help="table rows (more rows = more elements)")
    a = ap.parse_args()
    global ROWS
    ROWS = a.rows
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(a.keep or tmp)
        out.mkdir(parents=True, exist_ok=True)
        render(out)
        t = time.perf_counter()
        r = diff(str(out / "ref.png"), str(out / "test.png"))
        wall = (time.perf_counter() - t) * 1000
    stages = r.get("timing_ms", {})
    for k, v in stages.items():
        print(f"{k:>10}: {v:9.1f} ms")
    print(f"{'total':>10}: {wall:9.1f} ms   ({'OK' if wall < 5000 else 'OVER'} vs 5000 ms budget)")
    body = {k: v for k, v in r.items() if k != "timing_ms"}
    print(f"status={r['status']} deltas={len(r['deltas'])} review={len(r['review'])} regions={len(r['regions'])}")
    print("result sha256:", hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16])


if __name__ == "__main__":
    main()

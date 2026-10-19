"""Render a test page and mutated variants to tests/fixtures/web/*.png + *.json (structure map, via capture).
Each variant = one known delta.

Run: uv run python tests/make_fixtures.py
"""

import tempfile
from pathlib import Path

from pixel_perfect_cli.capture import capture

OUT = Path(__file__).parent / "fixtures" / "web"

PAGE = """<!doctype html><html><head><style>
* { box-sizing: border-box; margin: 0; }
body { font: 15px/1.4 -apple-system, "Helvetica Neue", Arial, sans-serif; background: #fff; color: #101828; padding: 32px; }
.card { width: 360px; padding: 24px; border-radius: 12px; background: #F2F4F7; }
.card h2 { font-size: 20px; font-weight: 600; }
.card p { margin-top: 8px; color: #667085; }
.row { display: flex; gap: 12px; margin-top: 24px; }
.btn { padding: 10px 18px; border-radius: 8px; background: #3366FF; color: #fff; font-weight: 600; }
.btn.ghost { background: transparent; color: #3366FF; border: 1px solid #3366FF; }
.list { margin-top: 32px; width: 360px; }
.item { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #EAECF0; }
%s
</style></head><body>
<div class="card">
  <h2>Upgrade your plan</h2>
  <p>Get unlimited projects and priority support.</p>
  <div class="row"><span class="btn">Upgrade</span><span class="btn ghost">Later</span></div>
</div>
<div class="list">
  <div class="item"><span>Projects</span><b>12</b></div>
  <div class="item"><span>Members</span><b>4</b></div>
  <div class="item"><span>Storage</span><b>2.1 GB</b></div>
</div>
</body></html>"""

# name -> (extra CSS, text replacements). Each variant carries exactly one known delta vs base.
VARIANTS = {
    "base": ("", {}),
    "rerender": ("", {}),                                           # identical: measures render noise
    "gap": (".card p { margin-top: 14px; }", {}),                   # gap 8 -> 14px
    "color": (".btn { background: #3360F0; }", {}),                 # #3366FF -> #3360F0
    "radius": (".btn { border-radius: 12px; }", {}),                # radius 8 -> 12px
    "font_size": (".card h2 { font-size: 22px; }", {}),             # 20 -> 22px
    "text": ("", {"2.1 GB": "2.4 GB"}),                             # text change
    "missing": (".btn.ghost { display: none; }", {}),               # element missing
    "shift": ("body { padding-left: 38px; }", {}),                  # whole layout +6px x
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(name, css, repl, "chromium", 1) for name, (css, repl) in VARIANTS.items()]
    # noise floor: same page, other rasterizers. Must yield no deltas.
    jobs += [("noise_webkit", "", {}, "webkit", 1), ("noise_firefox", "", {}, "firefox", 1),
             ("noise_chromium2x", "", {}, "chromium", 2)]
    with tempfile.TemporaryDirectory() as tmp:
        for name, css, repl, browser, dpr in jobs:
            html = PAGE % css
            for a, b in repl.items():
                html = html.replace(a, b)
            src = Path(tmp) / f"{name}.html"
            src.write_text(html)
            capture(str(src), str(OUT / f"{name}.png"), map_path=str(OUT / f"{name}.json"),
                    width=440, height=480, dpr=dpr, browser=browser)
    print(f"wrote {len(jobs)} PNG + map pairs to {OUT}")

if __name__ == "__main__":
    main()

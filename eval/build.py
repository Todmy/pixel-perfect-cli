"""Render the eval corpus into eval/corpus/ deterministically. SYNTHETIC PROXY, not real Figma pairs.

Design side: Chromium at DPR 2, box-downscaled to 1x (stands in for a Figma 2x export).
Shot side: Chromium DPR 1 by default, WebKit or Firefox for a seeded subset; one mutation applied per pair.

Run: uv run python -m eval.build
"""

import io
import json
import random
import shutil
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

from eval.dom import dump, style_of
from eval.pages import DYNAMIC_SELECTORS, MOBILE_MUTATIONS, MUTATIONS, PAGES, SEED, dynamic

OUT = Path(__file__).parent / "corpus"
NOTE = "SYNTHETIC PROXY: design is a Chromium DPR2 render downscaled 1x, not a Figma export"
TEXT_JS = """(e, t) => { const n = [...e.childNodes].find(c => c.nodeType === 3 && c.textContent.trim());
  if (n) n.textContent = t; else e.textContent = t; }"""


def render(browser, html: str, w: int, h: int, dpr: int, mutate=None):
    """Return (png bytes at 1x, structure map, resolver) for html; mutate(page) runs before capture."""
    pg = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=dpr)
    pg.set_content(html)
    pg.evaluate("document.fonts.ready")
    if mutate:
        mutate(pg)
    png = pg.screenshot(full_page=True, animations="disabled", caret="hide")
    if dpr != 1:
        buf = io.BytesIO()
        Image.open(io.BytesIO(png)).convert("RGB").reduce(dpr).save(buf, "PNG")
        png = buf.getvalue()
    smap, _ = dump(pg, {"width": w, "height": h}, 1)
    resolve = lambda sels: dump(pg, {}, 1, sels)[1]  # noqa: E731
    return pg, png, smap, resolve


def node(smap: dict, nid: str | None) -> dict | None:
    return next((n for n in smap["nodes"] if n["id"] == nid), None)


def mutator(mtype: str, sel: str, prop: str | None, to: str | None):
    def apply(pg):
        if mtype == "text":
            pg.eval_on_selector(sel, TEXT_JS, to)
        elif mtype == "added":
            pg.eval_on_selector(sel, "(e, h) => e.insertAdjacentHTML('beforeend', h)", to)
        else:
            pg.add_style_tag(content=f"{sel}{{{'display:none' if mtype == 'removed' else f'{prop}:{to}'} !important}}")
    return apply


def write(d: Path, png: bytes, smap: dict, name: str):
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.png").write_bytes(png)
    (d / f"{name}-map.json").write_text(json.dumps(smap, indent=1))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    rng = random.Random(SEED)
    pairs = 0
    with sync_playwright() as pw:
        eng = {"chromium": pw.chromium.launch(), "webkit": pw.webkit.launch(), "firefox": pw.firefox.launch()}
        for name, (tpl, w, h, split) in PAGES.items():
            html = tpl()
            kind = tpl.__name__ + ("-mobile" if w < 600 else "")
            pdir = OUT / name
            clean = {}
            dpg, dpng, dmap, dres = render(eng["chromium"], html, w, h, 2)
            write(pdir, dpng, dmap, "design")
            dyn = [i for i in dres(DYNAMIC_SELECTORS).values() if i] if tpl is dynamic else []
            base = {"page": name, "split": split, "page_kind": kind, "viewport": [w, h], "synthetic": True, "note": NOTE,
                    "design": "../design.png", "design_map": "../design-map.json", "dynamic": dyn}

            def pair(pid: str, kind_: str, engine: str, shot_html: str, muts=(), mutate=None, noise=None, design=None):
                nonlocal pairs
                spg, spng, smap, sres = render(eng[engine], shot_html, w, h, 1, mutate)
                if muts:  # a mutation that renders identically would make a pair the CLI cannot possibly pass
                    if engine not in clean:
                        cpg, clean[engine], _, _ = render(eng[engine], html, w, h, 1)
                        cpg.close()
                    assert spng != clean[engine], f"{name}/{pid}: mutation has no visible effect"
                d = pdir / pid
                write(d, spng, smap, "shot")
                truth = {**base, "pair": f"{name}/{pid}", "kind": kind_, "shot_engine": engine, "noise": noise,
                         "mutations": [m(sres, smap) for m in muts]}
                if design:
                    write(d, design[0], design[1], "design")
                    truth.update(design="design.png", design_map="design-map.json")
                (d / "truth.json").write_text(json.dumps(truth, indent=1))
                spg.close()
                pairs += 1

            cat = MUTATIONS[tpl.__name__]
            for mtype, sel, prop, to in cat[:MOBILE_MUTATIONS] if w < 600 else cat:
                r = rng.random()
                engine = "webkit" if r < 0.15 else "firefox" if r < 0.30 else "chromium"
                did = dres([sel])[sel]
                assert mtype == "added" or node(dmap, did), f"{name}: {sel} must hit one visible element"
                parent = node(dmap, node(dmap, did)["parent"]) if did and node(dmap, did) else None
                frm = (None if mtype == "added" else "visible" if mtype == "removed" else
                       node(dmap, did)["text"] if mtype == "text" else style_of(dpg, sel, prop))

                def truth_mut(sres, smap, mtype=mtype, sel=sel, prop=prop, to=to, did=did, parent=parent, frm=frm):
                    target = f"{sel} > .new" if mtype == "added" else sel
                    sid = sres([target])[target]
                    mid = sid if mtype == "added" else did
                    smap_node = None if mtype == "removed" else node(smap, sid)
                    assert mtype == "removed" or smap_node, f"{name}: {target} not visible in shot"
                    par = node(smap, smap_node["parent"]) if mtype == "added" else parent
                    return {"type": mtype, "selector": mid, "css": target, "property": "display" if mtype == "removed" else prop,
                            "from": frm, "to": "none" if mtype == "removed" else to,
                            "bbox": None if mtype == "added" else node(dmap, did)["bbox"], "shot_bbox": smap_node and smap_node["bbox"],
                            "parent": (par or {}).get("id"),
                            "parent_bbox": (par or {}).get("bbox")}
                pair(mtype, "mutation", engine, html, [truth_mut], mutator(mtype, sel, prop, to))
            for engine in ("chromium", "webkit", "firefox"):
                pair(f"noise-{engine}", "noise", engine, html, noise="rasterizer")
            rpg, rpng, rmap, _ = render(eng["chromium"], html, w, h, 1)
            rpg.close()
            pair("rerender", "noise", "chromium", html, noise="rerender", design=(rpng, rmap))
            if tpl is dynamic:
                pair("dynamic", "dynamic", "chromium", dynamic("shot"), noise="dynamic-content")
            dpg.close()
        for b in eng.values():
            b.close()
    print(f"wrote {pairs} pairs over {len(PAGES)} pages to {OUT}")


if __name__ == "__main__":
    main()

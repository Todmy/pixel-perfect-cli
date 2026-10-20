"""Render the eval corpus into eval/corpus/ deterministically. SYNTHETIC PROXY, not real Figma pairs.

Design side: Chromium at DPR 2, box-downscaled to 1x (stands in for a Figma 2x export).
Shot side: Chromium DPR 1 by default, WebKit or Firefox for a seeded subset; one mutation applied per pair.
Replay pairs (v1.3): replay-0/1/2 of one page, Chromium shots with mutations A+B, then B, then none.
Held-out files from an earlier build must come out byte-identical (asserted); only new replay-* dirs may appear there.

Run: uv run python -m eval.build
"""

import hashlib
import io
import json
import random
import shutil
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

from eval.dom import dump, style_of
from eval.pages import DYNAMIC_SELECTORS, MOBILE_MUTATIONS, MUTATIONS, PAGES, REPLAY, SEED, dynamic

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


def heldout_files() -> dict:
    """{path: sha256} of every held-out file except replay pairs."""
    return {f: hashlib.sha256(f.read_bytes()).hexdigest() for name, (*_, split) in PAGES.items() if split == "heldout"
            for f in sorted((OUT / name).rglob("*")) if f.is_file() and not f.parent.name.startswith("replay-")}


def main() -> None:
    held = heldout_files() if OUT.exists() else {}
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

            def pair(pid: str, kind_: str, engine: str, shot_html: str, muts=(), mutate=None, noise=None, design=None,
                     step=None, fixed=()):
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
                if step is not None:  # fixed: mutations of earlier replay steps, absent from this shot
                    truth.update(replay_step=step, fixed=[m(sres, smap) for m in fixed])
                if design:
                    write(d, design[0], design[1], "design")
                    truth.update(design="design.png", design_map="design-map.json")
                (d / "truth.json").write_text(json.dumps(truth, indent=1))
                spg.close()
                pairs += 1

            def spec(mtype: str, sel: str, prop: str | None, to: str | None, role: str | None = None):
                """Truth builder of one mutation: called with the shot's resolver and map."""
                did = dres([sel])[sel]
                assert mtype == "added" or node(dmap, did), f"{name}: {sel} must hit one visible element"
                parent = node(dmap, node(dmap, did)["parent"]) if did and node(dmap, did) else None
                frm = (None if mtype == "added" else "visible" if mtype == "removed" else
                       node(dmap, did)["text"] if mtype == "text" else style_of(dpg, sel, prop))

                def truth_mut(sres, smap):
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
                            "parent_bbox": (par or {}).get("bbox"), **({"replay_role": role} if role else {})}
                return truth_mut

            cat = MUTATIONS[tpl.__name__]
            for mtype, sel, prop, to in cat[:MOBILE_MUTATIONS] if w < 600 else cat:
                r = rng.random()
                engine = "webkit" if r < 0.15 else "firefox" if r < 0.30 else "chromium"
                pair(mtype, "mutation", engine, html, [spec(mtype, sel, prop, to)], mutator(mtype, sel, prop, to))
            for engine in ("chromium", "webkit", "firefox"):
                pair(f"noise-{engine}", "noise", engine, html, noise="rasterizer")
            rpg, rpng, rmap, _ = render(eng["chromium"], html, w, h, 1)
            rpg.close()
            pair("rerender", "noise", "chromium", html, noise="rerender", design=(rpng, rmap))
            if name in REPLAY:  # no RNG draws here: later pages keep their engines
                ma, mb = (next(m for m in cat if m[0] == t) for t in REPLAY[name])
                a, b = spec(*ma, role="A"), spec(*mb, role="B")
                both = lambda pg, ma=ma, mb=mb: (mutator(*ma)(pg), mutator(*mb)(pg))  # noqa: E731
                for i, (muts, mutate, fixed) in enumerate([([a, b], both, []), ([b], mutator(*mb), [a]), ([], None, [a, b])]):
                    pair(f"replay-{i}", "replay", "chromium", html, muts, mutate, step=i, fixed=fixed)
            if tpl is dynamic:
                pair("dynamic", "dynamic", "chromium", dynamic("shot"), noise="dynamic-content")
            dpg.close()
        for b in eng.values():
            b.close()
    changed = [str(f.relative_to(OUT)) for f, h in held.items() if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest() != h]
    added = [str(f.relative_to(OUT)) for f in heldout_files().keys() - held.keys()] if held else []
    assert not changed and not added, f"held-out corpus changed: {changed[:5]} added: {added[:5]}"
    print(f"wrote {pairs} pairs over {len(PAGES)} pages to {OUT}; {len(held)} held-out files byte-identical")


if __name__ == "__main__":
    main()

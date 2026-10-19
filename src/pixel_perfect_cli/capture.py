"""Deterministic page capture: screenshot + Contract v1 structure map via Playwright."""

from pathlib import Path

STYLES = ["color", "background-color", "font-size", "font-weight", "border-radius", "padding", "margin", "gap",
          "font-family", "box-shadow", "border-color", "border-width", "line-height", "letter-spacing"]
COLOR_PROPS = {"color", "background-color"}
FREEZE_CSS = (
    "*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}"
    "html{scrollbar-width:none!important}::-webkit-scrollbar{display:none!important}"
)

# Runs in the page. Ids: tag + classes + :nth-of-type when a same-tag sibling exists, joined by ">".
MAP_JS = """([styles, colorProps, masks]) => {
  const hex = (c) => {
    const m = c.match(/rgba?\\(([^)]+)\\)/); if (!m) return c;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    if (p.length > 3 && p[3] === 0) return 'transparent';
    const h = (n) => Math.round(n).toString(16).padStart(2, '0');
    return ('#' + h(p[0]) + h(p[1]) + h(p[2]) + (p.length > 3 && p[3] < 1 ? h(p[3] * 255) : '')).toUpperCase();
  };
  const seg = (el) => {
    let s = el.tagName.toLowerCase();
    for (const c of el.classList) s += '.' + CSS.escape(c);
    const sibs = [...el.parentElement.children].filter((e) => e.tagName === el.tagName);
    return sibs.length > 1 ? s + ':nth-of-type(' + (sibs.indexOf(el) + 1) + ')' : s;
  };
  const ids = new Map(), nodes = [];
  const walk = (el, parent) => {
    const id = parent === null ? el.tagName.toLowerCase() : parent + '>' + seg(el);
    ids.set(el, id);
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    if (cs.display === 'none') return;
    if (r.width > 0 && r.height > 0 && cs.visibility !== 'hidden') {
      const text = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join(' ').replace(/\\s+/g, ' ').trim();
      const style = {}; for (const p of styles) style[p] = colorProps.includes(p) ? hex(cs.getPropertyValue(p)) : cs.getPropertyValue(p).replace(/["']/g, '');
      const n = {id, selector: id, tag: el.tagName.toLowerCase(), parent: parent,
        bbox: [r.x + scrollX, r.y + scrollY, r.width, r.height].map((v) => Math.round(v * 100) / 100),
        text: text || null, style};
      if (masks.some((m) => el.matches(m))) n.masked = true;
      nodes.push(n);
    }
    for (const c of el.children) walk(c, id);
  };
  walk(document.body, null);
  return nodes;
}"""

# Paint each masked bbox as a solid #808080 overlay. Must run after the map so overlays stay out of it.
MASK_JS = """(masks) => {
  for (const el of document.querySelectorAll(masks.join(','))) {
    const r = el.getBoundingClientRect(), d = document.createElement('div');
    d.style.cssText = `position:absolute;left:${r.x + scrollX}px;top:${r.y + scrollY}px;width:${r.width}px;height:${r.height}px;background:#808080;z-index:2147483647;pointer-events:none`;
    document.body.appendChild(d);
  }
}"""


def to_url(target: str) -> str:
    p = Path(target)
    if p.exists():
        return p.resolve().as_uri()
    if "://" not in target:
        raise ValueError(f"no such file or URL: {target}")
    return target


def capture(target: str, out: str, *, map_path: str | None = None, width: int = 1440, height: int = 900,
            full_page: bool = False, dpr: float = 1, masks: list[str] | None = None,
            browser: str = "chromium") -> dict:
    from playwright.sync_api import sync_playwright

    masks = masks or []
    with sync_playwright() as pw:
        b = getattr(pw, browser).launch()
        try:
            page = b.new_context(viewport={"width": width, "height": height}, device_scale_factor=dpr,
                                 reduced_motion="reduce").new_page()
            page.goto(to_url(target), wait_until="networkidle")
            page.add_style_tag(content=FREEZE_CSS)
            page.evaluate("document.fonts.ready")
            nodes = page.evaluate(MAP_JS, [STYLES, sorted(COLOR_PROPS), masks])
            if masks:
                page.evaluate(MASK_JS, masks)
            page.screenshot(path=out, full_page=full_page, animations="disabled", caret="hide")
        finally:
            b.close()
    smap = {"version": 1, "source": "dom", "viewport": {"width": width, "height": height}, "dpr": dpr, "nodes": nodes}
    if map_path:
        import json
        Path(map_path).write_text(json.dumps(smap, indent=1))
    return smap

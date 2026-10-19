"""Independent DOM dumper: Contract v1 structure map from a live Playwright page (any engine).

Deliberately separate from the CLI's capture code so the oracle cannot inherit its bugs.
"""

# Ids are CSS paths: tag + classes + :nth-of-type(n) when a same-tag sibling exists. Valid selectors, so id == selector.
# Shorthands are rebuilt from longhands: engines disagree on computed shorthand serialization.
JS = r"""
(resolve) => {
  const SKIP = new Set(['SCRIPT', 'STYLE', 'HEAD', 'META', 'LINK', 'TITLE', 'NOSCRIPT', 'TEMPLATE']);
  const hex = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return c;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    if (p.length > 3 && p[3] === 0) return 'transparent';
    const h = p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
    return '#' + h + (p.length > 3 && p[3] < 1 ? Math.round(p[3] * 255).toString(16).padStart(2, '0').toUpperCase() : '');
  };
  const box4 = (s, names) => {
    const [t, r, b, l] = names.map(n => s.getPropertyValue(n));
    if (t === r && r === b && b === l) return t;
    if (t === b && r === l) return `${t} ${r}`;
    if (r === l) return `${t} ${r} ${b}`;
    return `${t} ${r} ${b} ${l}`;
  };
  const seg = (el) => {
    const tag = el.tagName.toLowerCase();
    let s = tag + [...el.classList].map(c => '.' + CSS.escape(c)).join('');
    const same = el.parentElement ? [...el.parentElement.children].filter(c => c.tagName === el.tagName) : [];
    if (same.length > 1) s += `:nth-of-type(${same.indexOf(el) + 1})`;
    return s;
  };
  const path = (el) => {
    const parts = [];
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) parts.unshift(seg(e));
    return parts.join('>');
  };
  const ownText = (el) => {
    const t = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim();
    return t || null;
  };
  const r2 = (v) => Math.round(v * 100) / 100;
  const visible = (el, s, r) => r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'
    && (!el.checkVisibility || el.checkVisibility({opacityProperty: true, visibilityProperty: true}));
  const nodes = [];
  const kept = new Map();
  const walk = (el, parentId) => {
    if (SKIP.has(el.tagName)) return;
    const s = getComputedStyle(el);
    if (s.display === 'none') return;
    const r = el.getBoundingClientRect();
    let id = parentId;
    if (visible(el, s, r)) {
      id = path(el);
      kept.set(el, id);
      nodes.push({id, selector: id, tag: el.tagName.toLowerCase(), parent: parentId,
        bbox: [r2(r.left + scrollX), r2(r.top + scrollY), r2(r.width), r2(r.height)], text: ownText(el),
        style: {color: hex(s.color), 'background-color': hex(s.backgroundColor), 'font-size': s.fontSize,
          'font-weight': s.fontWeight,
          'border-radius': box4(s, ['border-top-left-radius', 'border-top-right-radius', 'border-bottom-right-radius', 'border-bottom-left-radius']),
          padding: box4(s, ['padding-top', 'padding-right', 'padding-bottom', 'padding-left']),
          margin: box4(s, ['margin-top', 'margin-right', 'margin-bottom', 'margin-left']),
          gap: s.rowGap === s.columnGap ? s.rowGap : `${s.rowGap} ${s.columnGap}`}});
    }
    if (el.tagName.toLowerCase() === 'svg') return;  // shapes inside an icon are not elements an agent edits
    for (const c of el.children) walk(c, id);
  };
  walk(document.body, null);
  const ids = {};
  for (const sel of resolve) {
    const els = document.querySelectorAll(sel);
    ids[sel] = els.length === 1 ? path(els[0]) : null;
  }
  return {nodes, ids, scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight]};
}
"""


def dump(page, viewport: dict, dpr: int = 1, resolve: list[str] = ()) -> tuple[dict, dict]:
    """Return (structure map, {selector: id or None}). bbox in CSS px, page coords."""
    out = page.evaluate(JS, list(resolve))
    smap = {"version": 1, "source": "dom", "viewport": viewport, "dpr": dpr, "nodes": out["nodes"]}
    return smap, out["ids"]


def style_of(page, selector: str, prop: str):
    """Computed value as the map would report it (hex colors, rebuilt shorthands)."""
    smap, ids = dump(page, {}, 1, [selector])
    node = next(n for n in smap["nodes"] if n["id"] == ids[selector])
    return node["style"].get(prop, page.eval_on_selector(selector, f"e => getComputedStyle(e).getPropertyValue('{prop}')"))

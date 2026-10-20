"""Page corpus and mutation catalog. SYNTHETIC PROXY: no real Figma pairs; the design side is a browser render.

Every page is self-contained HTML (no network). Content is fixed or drawn from a seeded RNG.
A mutation is (type, selector, property, to): exactly one change, applied to the SHOT side only.
"""

import base64
import random

import cv2
import numpy as np

SEED = 20261019
FONT = '-apple-system, "Helvetica Neue", Arial, sans-serif'
BASE = f"""*{{box-sizing:border-box;margin:0;padding:0}}
body{{font:15px/1.5 {FONT};color:#101828;background:#fff;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.btn{{display:inline-block;padding:10px 18px;border-radius:8px;font-weight:600;font-size:15px;background:#F2F4F7;color:#101828}}
.btn.primary{{background:#3366FF;color:#fff}}
.btn.ghost{{background:transparent;color:#3366FF;border:1px solid #3366FF}}
.nav{{display:flex;align-items:center;justify-content:space-between;height:72px;padding:0 64px;border-bottom:1px solid #EAECF0;background:#fff}}
.nav .logo{{font-weight:700;font-size:20px;display:flex;align-items:center;gap:8px}}
.nav .links{{display:flex;gap:32px;color:#475467}}
@media (max-width:600px){{.nav{{padding:0 20px;height:60px}}.nav .links{{display:none}}}}
"""
ICON = ('<svg width="24" height="24" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="6" fill="{c}"/>'
        '<path d="M7 12l3 3 7-7" stroke="#fff" stroke-width="2.5" fill="none"/></svg>')


def photo(w: int = 560, h: int = 400, seed: int = SEED, grain: int = 4) -> str:
    """Photo-like texture (smooth blobs + sensor grain) as a PNG data URI."""
    rng = np.random.default_rng(seed)
    small = rng.integers(0, 255, (h // 40, w // 40, 3), dtype=np.uint8)
    img = cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
    img = cv2.GaussianBlur(img, (0, 0), 12)
    img = np.clip(img.astype(np.int16) + rng.integers(-grain, grain + 1, img.shape), 0, 255).astype(np.uint8)
    ok, png = cv2.imencode(".png", img)
    return "data:image/png;base64," + base64.b64encode(png.tobytes()).decode()


def nav(brand: str = "Northwind") -> str:
    return (f'<header class="nav"><div class="logo">{ICON.format(c="#3366FF")}<span>{brand}</span></div>'
            '<nav class="links"><a>Product</a><a>Pricing</a><a>Docs</a><a>Blog</a></nav>'
            '<a class="btn primary signin">Sign in</a></header>')


def page(css: str, body: str) -> str:
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{body}</body></html>"


def landing() -> str:
    css = """.hero{display:flex;gap:48px;align-items:center;padding:80px 64px;background:linear-gradient(135deg,#EEF4FF 0%,#F9F5FF 60%,#FFF 100%)}
.hero .copy{flex:1}.hero h1{font-size:56px;line-height:1.1;letter-spacing:-1px;margin-bottom:16px}
.hero .lead{font-size:19px;color:#475467;max-width:520px}.hero .actions{display:flex;gap:12px;margin-top:32px}
.visual{position:relative;flex:0 0 560px}.visual .photo{display:block;width:560px;height:400px;border-radius:16px}
.visual .stat{position:absolute;left:-32px;bottom:-24px;background:#fff;padding:20px 24px;border-radius:16px;box-shadow:0 12px 32px rgba(16,24,40,.18)}
.stat .label{font-size:13px;color:#667085}.stat .value{font-size:28px;font-weight:700;color:#067647}
.visual .badge{position:absolute;left:60px;bottom:64px;background:#F04438;color:#fff;font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px}
.logos{display:flex;justify-content:center;gap:56px;padding:32px 64px;color:#98A2B3;font-weight:700;font-size:20px}
.features{display:flex;gap:32px;padding:32px 64px 80px}.feature{flex:1}.feature h3{font-size:18px;margin:12px 0 6px}.feature p{color:#475467}
@media (max-width:600px){.hero{flex-direction:column;padding:40px 20px}.hero h1{font-size:36px}.visual{flex:none;width:100%}
.visual .photo{width:100%;height:240px}.visual .stat{left:12px}.logos{gap:20px;padding:24px 20px;font-size:15px;flex-wrap:wrap}
.features{flex-direction:column;padding:24px 20px 48px}}"""
    feats = "".join(f'<div class="feature">{ICON.format(c=c)}<h3>{t}</h3><p>{p}</p></div>' for c, t, p in [
        ("#3366FF", "Structure-aware", "Deltas name the element, not a pixel blob."),
        ("#12B76A", "Deterministic", "Same inputs give byte-identical output, every run."),
        ("#F79009", "Fast", "Full 1440 pages in well under five seconds.")])
    return page(css, nav() + f"""<section class="hero"><div class="copy"><h1>Ship pixel-perfect interfaces</h1>
<p class="lead">Compare every screen to its design and get a short list of fixes your agent can act on.</p>
<div class="actions"><a class="btn primary start">Start free trial</a><a class="btn ghost demo">Book a demo</a></div></div>
<div class="visual"><img class="photo" src="{photo()}"><div class="stat"><div class="label">Conversion</div><div class="value">+38%</div></div>
<span class="badge">New</span></div></section>
<section class="logos"><span>Acme</span><span>Globex</span><span>Initech</span><span>Umbrella</span><span>Hooli</span></section>
<section class="features">{feats}</section>""")


def pricing() -> str:
    css = """.head{text-align:center;padding:64px 64px 40px}.head h1{font-size:44px}.head p{color:#475467;margin-top:12px;font-size:18px}
.plans{display:flex;gap:24px;justify-content:center;padding:0 64px 80px}
.plan{width:360px;border:1px solid #EAECF0;border-radius:16px;padding:32px;background:#fff}
.plan.pro{border:2px solid #3366FF;box-shadow:0 8px 24px rgba(51,102,255,.15)}
.plan h3{font-size:18px;color:#475467}.plan .price{font-size:48px;font-weight:700;margin:12px 0 4px}.plan .price small{font-size:16px;color:#667085;font-weight:500}
.plan ul{list-style:none;margin:24px 0;display:flex;flex-direction:column;gap:12px}.plan li{display:flex;gap:10px;align-items:center;color:#344054}
.plan .btn{display:block;text-align:center}
@media (max-width:600px){.head{padding:40px 20px 24px}.head h1{font-size:32px}.plans{flex-direction:column;padding:0 20px 48px;gap:16px}.plan{width:100%;padding:24px}}"""
    plans = [("Starter", "$0", ["3 projects", "Pixel diff", "Community support"], ""),
             ("Pro", "$24", ["Unlimited projects", "Structure maps", "Priority support", "CI integration"], " pro"),
             ("Team", "$79", ["Everything in Pro", "SSO", "Audit log"], "")]
    body = "".join(f'<div class="plan{c}"><h3>{n}</h3><div class="price">{p}<small> / month</small></div><ul>'
                   + "".join(f"<li>{ICON.format(c='#12B76A')}<span>{f}</span></li>" for f in fs)
                   + f'</ul><a class="btn{" primary" if c else ""}">Choose {n}</a></div>' for n, p, fs, c in plans)
    return page(css, nav() + f'<section class="head"><h1>Simple pricing</h1><p>Start free, upgrade when your team grows.</p></section>'
                f'<section class="plans">{body}</section>')


def plans() -> str:
    """Train sibling of pricing: four tinted cards, badge, billing switch, check-icon feature lists."""
    css = """.intro{display:flex;justify-content:space-between;align-items:flex-end;padding:56px 64px 32px}
.intro h1{font-size:40px;letter-spacing:-.5px}.intro p{color:#667085;margin-top:8px;font-size:17px}
.billing{display:flex;gap:4px;padding:4px;background:#F2F4F7;border-radius:10px}.billing a{padding:8px 16px;border-radius:8px;font-weight:600;color:#475467}
.billing a.on{background:#fff;color:#101828;box-shadow:0 1px 3px rgba(16,24,40,.12)}
.tiers{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;padding:0 64px 72px}
.tier{position:relative;display:flex;flex-direction:column;background:#F9FAFB;border-radius:12px;padding:28px 24px}
.tier.hot{background:#F4EBFF;outline:1px solid #D6BBFB}
.tier .badge{position:absolute;top:16px;right:16px;background:#7F56D9;color:#fff;font-size:12px;font-weight:600;padding:2px 10px;border-radius:999px}
.tier h2{font-size:16px;font-weight:600;color:#53389E}.tier .cost{font-size:40px;font-weight:700;margin-top:16px}
.tier .cost em{font-style:normal;font-size:14px;color:#667085;font-weight:500}.tier .blurb{font-size:14px;color:#475467;margin-top:4px}
.tier ul{list-style:none;flex:1;display:flex;flex-direction:column;gap:10px;margin:20px 0 28px}.tier li{display:flex;gap:8px;align-items:center;font-size:14px;color:#344054}
.tier .btn{text-align:center;background:#fff;border:1px solid #D0D5DD}.tier.hot .btn{background:#7F56D9;color:#fff;border-color:#7F56D9}
@media (max-width:600px){.intro{flex-direction:column;align-items:flex-start;gap:16px;padding:32px 20px 20px}.intro h1{font-size:30px}
.tiers{grid-template-columns:1fr;gap:14px;padding:0 20px 40px}}"""
    tiers = [("Hobby", "€0", "For side projects", ["1 site", "Weekly snapshots", "Forum help"], ""),
             ("Studio", "€12", "For small teams", ["10 sites", "Daily snapshots", "Review links", "Slack app"], " hot"),
             ("Agency", "€39", "For client work", ["50 sites", "Hourly snapshots", "White label"], ""),
             ("Enterprise", "Custom", "For regulated orgs", ["Unlimited sites", "SAML", "Data residency"], "")]
    body = "".join(f'<div class="tier{c}">' + ('<span class="badge">Most popular</span>' if c else "")
                   + f'<h2>{n}</h2><div class="cost">{p}' + ("<em> / user / mo</em>" if p[0] == "€" else "") + "</div>"
                   + f'<p class="blurb">{b}</p><ul>' + "".join(f"<li>{ICON.format(c='#9E77ED')}<span>{f}</span></li>" for f in fs)
                   + f'</ul><a class="btn">{"Contact us" if p == "Custom" else "Get " + n}</a></div>' for n, p, b, fs, c in tiers)
    return page(css, nav("Lumenframe") + '<section class="intro"><div><h1>Plans for every studio</h1><p>Pay per seat. Switch or cancel any time.</p></div>'
                '<div class="billing"><a class="on">Monthly</a><a>Yearly</a></div></section>' + f'<section class="tiers">{body}</section>')


def membership() -> str:
    """Train sibling of pricing: tinted header with eyebrow badge, banded cards, one dark featured card, tag, pill buttons."""
    css = """.top{text-align:center;padding:72px 64px 48px;background:#F0FDF9}
.top .eyebrow{display:inline-block;background:#CCFBEF;color:#107569;font-size:13px;font-weight:600;padding:4px 12px;border-radius:999px}
.top h1{font-size:48px;letter-spacing:-1px;margin-top:16px}.top p{color:#475467;margin-top:10px;font-size:18px}
.cards{display:flex;justify-content:center;gap:32px;padding:48px 64px}
.card{width:380px;border:1px solid #D0D5DD;border-radius:20px;overflow:hidden;background:#fff}
.card .band{height:8px;background:#15B79E}.card .inner{padding:28px 32px 32px}
.card.dark{background:#101828;color:#fff;border-color:#101828}.card.dark .band{background:#FDB022}
.card h3{font-size:22px}.card .tag{display:inline-block;margin-left:8px;font-size:12px;background:#FEF0C7;color:#B54708;padding:2px 8px;border-radius:6px;vertical-align:middle}
.card .amount{font-size:52px;font-weight:800;letter-spacing:-1px;margin-top:20px}.card .per{color:#667085;font-size:14px}.card.dark .per{color:#98A2B3}
.card ul{list-style:none;margin:24px 0;padding-top:20px;border-top:1px solid #EAECF0}.card.dark ul{border-color:#344054}
.card li{display:flex;gap:12px;align-items:center;padding:6px 0}
.card .btn{display:block;text-align:center;border-radius:999px;padding:12px}.card.dark .btn{background:#FDB022;color:#101828}
.note{text-align:center;color:#667085;font-size:14px;padding:0 64px 64px}
@media (max-width:600px){.top{padding:40px 20px 28px}.top h1{font-size:34px}.cards{flex-direction:column;gap:20px;padding:24px 20px}
.card{width:100%}.card .inner{padding:24px}.note{padding:0 20px 40px}}"""
    cards = [("Basic", "$9", ["Members area", "Monthly workshop", "Recordings"], "", "#15B79E"),
             ("Plus", "$19", ["Everything in Basic", "Weekly office hours", "Private channel", "Templates"], " dark", "#FDB022"),
             ("Studio", "$49", ["Up to 5 seats", "Team onboarding", "Invoice billing"], "", "#15B79E")]
    body = "".join(f'<div class="card{c}"><div class="band"></div><div class="inner"><h3>{n}'
                   + ('<span class="tag">Save 20%</span>' if c else "") + f'</h3><div class="amount">{p}</div>'
                   + '<p class="per">per member / month, billed yearly</p><ul>'
                   + "".join(f"<li>{ICON.format(c=ic)}<span>{f}</span></li>" for f in fs)
                   + f'</ul><a class="btn{"" if c else " ghost"}">Join {n}</a></div></div>' for n, p, fs, c, ic in cards)
    return page(css, nav("Guildhall") + '<section class="top"><span class="eyebrow">Membership</span><h1>Learn with the guild</h1>'
                '<p>One membership, every workshop and recording.</p></section>'
                f'<section class="cards">{body}</section><p class="note">30-day money-back guarantee. Cancel anytime.</p>')


def table() -> str:
    rng = random.Random(SEED)
    css = """.wrap{padding:32px 64px}.wrap h1{font-size:28px}.bar{display:flex;gap:12px;align-items:center;margin:16px 0 20px}
.bar .search{width:320px;height:40px;border:1px solid #D0D5DD;border-radius:8px;padding:0 12px;font:inherit}
table{width:100%;border-collapse:collapse;font-size:14px}th{text-align:left;color:#475467;font-weight:600;background:#F9FAFB;padding:10px 16px;border-bottom:1px solid #EAECF0}
td{padding:9px 16px;border-bottom:1px solid #EAECF0}td.num{text-align:right;font-variant-numeric:tabular-nums}
.st{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:600}.st.ok{background:#ECFDF3;color:#067647}.st.warn{background:#FFFAEB;color:#B54708}"""
    names = ["Atlas", "Borealis", "Cobalt", "Delta", "Ember", "Fjord", "Granite", "Helix", "Indigo", "Juniper", "Kestrel",
             "Lumen", "Meridian", "Nimbus", "Onyx", "Pulsar", "Quartz", "Raven", "Sierra", "Tundra", "Umber", "Vertex"]
    rows = "".join(f'<tr><td>{n}</td><td>{rng.choice(["eu-west-1", "us-east-1", "ap-south-1"])}</td>'
                   f'<td><span class="st {"ok" if rng.random() > .25 else "warn"}">{"Healthy" if rng.random() > .25 else "Degraded"}</span></td>'
                   f'<td class="num">{rng.randint(10, 999)}</td><td class="num">{rng.uniform(0, 100):.1f}%</td><td class="num">${rng.randint(100, 9999):,}</td></tr>'
                   for n in names)
    return page(css, nav() + f"""<div class="wrap"><h1>Services</h1><div class="bar"><input class="search" placeholder="Search services">
<a class="btn primary">New service</a></div><table><thead><tr><th>Name</th><th>Region</th><th>Status</th><th class="num">Requests/s</th>
<th class="num">CPU</th><th class="num">Cost</th></tr></thead><tbody>{rows}</tbody></table></div>""")


def form() -> str:
    css = """.wrap{display:flex;justify-content:center;padding:56px 24px}.panel{width:100%;max-width:480px}.panel h1{font-size:30px}.panel .sub{color:#475467;margin:8px 0 28px}
.field{display:flex;flex-direction:column;gap:6px;margin-bottom:20px}.field label{font-size:14px;font-weight:600;color:#344054}
.field input{min-width:0}.field input,.field select,.field textarea{height:44px;border:1px solid #D0D5DD;border-radius:8px;padding:0 14px;font:inherit;color:#101828;background:#fff}
.field textarea{height:96px;padding:10px 14px;resize:none}.row{display:flex;gap:16px}.row .field{flex:1;min-width:0}
.check{display:flex;gap:10px;align-items:center;font-size:14px;color:#475467;margin-bottom:24px}.check .box{width:18px;height:18px;border:1px solid #D0D5DD;border-radius:4px}
.submit{width:100%;text-align:center;padding:12px}"""
    return page(css, nav() + """<div class="wrap"><form class="panel"><h1>Contact sales</h1><p class="sub">We reply within one business day.</p>
<div class="row"><div class="field"><label>First name</label><input value="Ada"></div><div class="field"><label>Last name</label><input value="Lovelace"></div></div>
<div class="field email"><label>Work email</label><input value="ada@example.com"></div>
<div class="field"><label>Team size</label><select><option>11-50</option></select></div>
<div class="field msg"><label>Message</label><textarea>We need visual regression for 40 screens.</textarea></div>
<div class="check"><span class="box"></span><span>I agree to the privacy policy</span></div>
<a class="btn primary submit">Send message</a></form></div>""")


def grid() -> str:
    rng = random.Random(SEED + 1)
    css = """.wrap{padding:40px 64px}.wrap h1{font-size:32px;margin-bottom:24px}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.card{border:1px solid #EAECF0;border-radius:12px;overflow:hidden;background:#fff}.card .thumb{height:140px}
.card .body{padding:16px}.card h3{font-size:16px}.card p{font-size:14px;color:#667085;margin-top:4px}.card .meta{display:flex;justify-content:space-between;margin-top:12px;font-size:13px;color:#475467}
@media (max-width:600px){.wrap{padding:24px 20px}.cards{grid-template-columns:1fr;gap:16px}}"""
    hues = ["#FEE4E2", "#D1E9FF", "#D1FADF", "#FEF0C7", "#EBE9FE", "#FCE7F6", "#CCFBEF", "#FFE6D5"]
    cards = "".join(f'<div class="card"><div class="thumb" style="background:linear-gradient(160deg,{h},#fff)"></div><div class="body">'
                    f'<h3>Template {i + 1:02d}</h3><p>{rng.choice(["Dashboard", "Landing", "Checkout", "Onboarding"])} layout</p>'
                    f'<div class="meta"><span>{rng.randint(2, 40)} screens</span><b>${rng.randint(9, 99)}</b></div></div></div>'
                    for i, h in enumerate(hues))
    return page(css, nav() + f'<div class="wrap"><h1>Templates</h1><div class="cards">{cards}</div></div>')


def borderless() -> str:
    css = """section{padding:56px 160px}section h2{font-size:32px;margin-bottom:12px}section p{font-size:17px;color:#475467;max-width:760px}
.alt{background:#F9FAFB}.split{display:flex;gap:64px}.split div{flex:1}.quote{font-size:24px;line-height:1.4;font-style:italic;color:#344054}
.who{margin-top:16px;color:#667085;font-size:15px}"""
    return page(css, nav() + """<section class="intro"><h2>Why structure beats pixels</h2><p>Pixel diffs tell you that something changed.
Structure tells you what to change: the element, the property and the value.</p></section>
<section class="alt how"><div class="split"><div><h2>Capture</h2><p>Render the page at the design width and record every element box.</p></div>
<div><h2>Compare</h2><p>Pair elements by identity, then report gaps, padding and colors that differ.</p></div></div></section>
<section class="testimonial"><p class="quote">"We cut design review from two days to an hour."</p><p class="who">Grace Hopper, Head of Design</p></section>
<section class="alt cta"><h2>Try it on your next screen</h2><p>One command, one JSON document, no account needed.</p></section>""")


def settings() -> str:
    css = """.layout{display:flex;min-height:760px}.side{width:248px;border-right:1px solid #EAECF0;padding:24px 16px;display:flex;flex-direction:column;gap:4px}
.side a{padding:8px 12px;border-radius:6px;color:#344054;font-weight:500}.side a.on{background:#F2F4F7;color:#101828}
.main{flex:1;padding:32px 48px}.main h1{font-size:26px}.main .sub{color:#475467;margin:4px 0 24px}
.opt{display:flex;justify-content:space-between;align-items:center;padding:18px 0;border-bottom:1px solid #EAECF0;max-width:720px}
.opt b{display:block;font-weight:600}.opt span{color:#667085;font-size:14px}
.tog{width:44px;height:24px;border-radius:12px;background:#D0D5DD;position:relative}.tog.on{background:#3366FF}
.tog i{position:absolute;top:2px;left:2px;width:20px;height:20px;border-radius:50%;background:#fff}.tog.on i{left:22px}"""
    opts = "".join(f'<div class="opt"><div><b>{t}</b><span>{d}</span></div><div class="tog{" on" if on else ""}"><i></i></div></div>'
                   for t, d, on in [("Email digests", "A weekly summary of visual changes", True),
                                    ("Slack alerts", "Post failing screens to #design", False),
                                    ("Auto-approve noise", "Skip pairs below the noise floor", True),
                                    ("Strict mode", "Treat review items as failures", False)])
    side = "".join(f'<a{" class=on" if i == 1 else ""}>{t}</a>' for i, t in enumerate(["Profile", "Notifications", "Billing", "Members", "API keys"]))
    return page(css, nav() + f'<div class="layout"><aside class="side">{side}</aside><main class="main"><h1>Notifications</h1>'
                f'<p class="sub">Choose how we keep you informed.</p>{opts}</main></div>')


def dark() -> str:
    css = """body{background:#0C111D;color:#F5F5F6}.nav{background:#0C111D;border-color:#1F242F}.nav .links{color:#94969C}
.wrap{padding:48px 64px}.wrap h1{font-size:34px}.wrap .sub{color:#94969C;margin-top:8px}
.kpis{display:flex;gap:24px;margin-top:32px}.kpi{flex:1;background:#161B26;border:1px solid #1F242F;border-radius:12px;padding:24px}
.kpi .l{color:#94969C;font-size:14px}.kpi .v{font-size:32px;font-weight:700;margin-top:8px}.kpi .d{font-size:13px;color:#47CD89;margin-top:4px}
.chart{margin-top:24px;background:#161B26;border:1px solid #1F242F;border-radius:12px;padding:24px;height:300px;display:flex;align-items:flex-end;gap:14px}
.chart i{flex:1;background:linear-gradient(#528BFF,#2E5BFF);border-radius:6px 6px 0 0}"""
    rng = random.Random(SEED + 2)
    bars = "".join(f'<i style="height:{rng.randint(30, 250)}px"></i>' for _ in range(18))
    kpis = "".join(f'<div class="kpi"><div class="l">{l}</div><div class="v">{v}</div><div class="d">{d}</div></div>'
                   for l, v, d in [("Screens checked", "12,480", "+12% vs last week"), ("Median deltas", "0.6", "-0.3"),
                                   ("Converged", "94%", "+4 pts"), ("Runtime p95", "2.1 s", "-0.4 s")])
    return page(css, nav() + f'<div class="wrap"><h1>Overview</h1><p class="sub">Last 7 days across all projects</p>'
                f'<div class="kpis">{kpis}</div><div class="chart">{bars}</div></div>')


def article() -> str:
    rng = random.Random(SEED + 3)
    words = ("layout element padding margin render browser pixel design token baseline screen component review agent "
             "contract delta capture structure noise engine glyph").split()
    css = """.art{width:720px;margin:0 auto;padding:64px 0 120px}.art h1{font-size:44px;line-height:1.15}.art .by{color:#667085;margin:16px 0 40px}
.art h2{font-size:26px;margin:48px 0 16px}.art p{font-size:18px;line-height:1.7;color:#344054;margin-bottom:20px}
.art figure{margin:32px 0}.art figure img{display:block;width:720px;height:360px;border-radius:12px}.art figcaption{font-size:14px;color:#667085;margin-top:8px}
.art blockquote{border-left:4px solid #3366FF;padding:4px 0 4px 20px;font-size:20px;color:#101828;margin:32px 0}"""
    secs = []
    for s in range(4):
        paras = "".join("<p>" + " ".join(rng.choice(words) for _ in range(rng.randint(55, 80))).capitalize() + ".</p>" for _ in range(3))
        extra = (f'<figure><img src="{photo(720, 360, SEED + s, grain=0)}"><figcaption>Figure {s + 1}. Render of section {s + 1}.</figcaption></figure>'
                 if s % 2 == 0 else '<blockquote>Structure tells you what to change, pixels only that something did.</blockquote>')
        secs.append(f'<section class="s{s + 1}"><h2>Part {s + 1}: {rng.choice(words).capitalize()} and {rng.choice(words)}</h2>{paras}{extra}</section>')
    return page(css, nav() + f'<article class="art"><h1>What a pixel diff cannot tell you</h1><p class="by">By the platform team · 14 min read</p>'
                + "".join(secs) + "</article>")


DYNAMIC_VALUES = {"design": ("Monday, 19 October 2026", "1,284", "#7F56D9", "AL"),
                  "shot": ("Tuesday, 20 October 2026", "1,311", "#F79009", "GH")}


def dynamic(values: str = "design") -> str:
    date, count, avatar, initials = DYNAMIC_VALUES[values]
    css = """.wrap{padding:40px 64px}.top{display:flex;justify-content:space-between;align-items:center}.top h1{font-size:30px}
.top .date{color:#667085;margin-top:4px}.who{display:flex;align-items:center;gap:12px}.avatar{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}
.panels{display:grid;grid-template-columns:2fr 1fr;gap:24px;margin-top:32px}.box{border:1px solid #EAECF0;border-radius:12px;padding:24px}
.box h2{font-size:16px;color:#475467}.box .big{font-size:40px;font-weight:700;margin-top:8px}.feed{list-style:none;margin-top:12px}
.feed li{padding:12px 0;border-bottom:1px solid #EAECF0;display:flex;justify-content:space-between}.feed li span{color:#667085}"""
    feed = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in [("Checkout v2 converged", "3 iterations"),
                    ("Pricing page", "1 delta left"), ("Settings", "passed"), ("Onboarding step 3", "review")])
    return page(css, nav() + f"""<div class="wrap"><div class="top"><div><h1>Good morning</h1><p class="date">{date}</p></div>
<div class="who"><span>Signed in</span><div class="avatar" style="background:{avatar}">{initials}</div></div></div>
<div class="panels"><div class="box activity"><h2>Recent activity</h2><ul class="feed">{feed}</ul></div>
<div class="box live"><h2>Active sessions</h2><div class="big counter">{count}</div></div></div></div>""")


DYNAMIC_SELECTORS = [".top .date", ".avatar", ".counter"]

# name -> (template, width, height, split). Mobile variants share their template's split: no layout leaks across splits.
PAGES = {
    "landing": (landing, 1440, 900, "train"), "landing-m": (landing, 390, 844, "train"),
    "table": (table, 1440, 900, "train"),
    "form": (form, 1440, 900, "train"), "form-m": (form, 390, 844, "train"),
    "grid": (grid, 1440, 900, "train"), "grid-m": (grid, 390, 844, "train"),
    "borderless": (borderless, 1440, 900, "train"), "settings": (settings, 1440, 900, "train"),
    "pricing": (pricing, 1440, 900, "heldout"), "pricing-m": (pricing, 390, 844, "heldout"),
    "dark": (dark, 1440, 900, "heldout"), "article": (article, 1440, 900, "heldout"),
    "dynamic": (dynamic, 1440, 900, "heldout"),
    # v1.3, appended last: build draws shot engines from one seeded RNG in this order, so earlier pages keep theirs.
    "plans": (plans, 1440, 900, "train"), "plans-m": (plans, 390, 844, "train"),
    "membership": (membership, 1440, 900, "train"), "membership-m": (membership, 390, 844, "train"),
}

# template name -> [(type, selector, property, to)]. Selector must hit exactly one element (build asserts it).
# removed: display none. added: `to` is HTML appended as last child of `selector` (no sibling renumbering).
MUTATIONS = {
    "landing": [("gap", ".hero .actions", "gap", "20px"), ("padding", ".btn.start", "padding", "10px 28px"),
                ("margin", ".hero h1", "margin-bottom", "26px"), ("color", ".btn.start", "background-color", "#2952CC"),
                ("font-size", ".hero h1", "font-size", "50px"), ("radius", ".visual .stat", "border-radius", "4px"),
                ("text", ".hero .lead", "text", "Compare every screen to its Figma frame and get fixes your agent can apply."),
                ("removed", ".logos span:nth-child(3)", None, None), ("added", ".nav .links", None, "<a class='new'>Changelog</a>"),
                ("align", ".features .feature:nth-child(2)", "text-align", "center")],
    "pricing": [("gap", ".plan.pro ul", "gap", "20px"), ("padding", ".plan.pro", "padding", "40px"),
                ("margin", ".head p", "margin-top", "24px"), ("color", ".plan.pro .btn", "background-color", "#7F56D9"),
                ("font-size", ".plan.pro .price", "font-size", "42px"), ("radius", ".plan:nth-child(3)", "border-radius", "4px"),
                ("text", ".plan.pro .price", "text", "$29"), ("removed", ".plan.pro li:nth-child(4)", None, None),
                ("added", ".plan:nth-child(3) ul", None, "<li class='new'><span>Dedicated manager</span></li>"),
                ("align", ".head", "text-align", "left")],
    "table": [("gap", ".bar", "gap", "40px"), ("padding", "tbody tr:nth-child(5) td:nth-child(1)", "padding", "9px 32px"),
              ("margin", ".wrap h1", "margin-bottom", "32px"), ("color", "tbody tr:nth-child(8) td:nth-child(1)", "color", "#D92D20"),
              ("font-size", "thead th:nth-child(2)", "font-size", "16px"), ("radius", ".bar .search", "border-radius", "20px"),
              ("text", "tbody tr:nth-child(12) td:nth-child(6)", "text", "$12,345"), ("removed", ".bar .btn", None, None),
              ("added", ".bar", None, "<span class='new'>22 services</span>"), ("align", "tbody tr:nth-child(3) td:nth-child(2)", "text-align", "right")],
    "form": [("gap", ".field.email", "gap", "14px"), ("padding", ".field.email input", "padding", "0 28px"),
             ("margin", ".panel .sub", "margin-bottom", "40px"), ("color", ".submit", "background-color", "#12B76A"),
             ("font-size", ".panel h1", "font-size", "26px"), ("radius", ".field.msg textarea", "border-radius", "0px"),
             ("text", ".panel .sub", "text", "We reply within two business days."), ("removed", ".check", None, None),
             ("added", ".panel", None, "<p class='new'>Or email sales@example.com</p>"), ("align", ".panel h1", "text-align", "center")],
    "grid": [("gap", ".cards", "gap", "36px"), ("padding", ".card:nth-child(3) .body", "padding", "28px"),
             ("margin", ".wrap h1", "margin-bottom", "40px"), ("color", ".card:nth-child(5) h3", "color", "#3366FF"),
             ("font-size", ".card:nth-child(6) h3", "font-size", "20px"), ("radius", ".card:nth-child(7)", "border-radius", "0px"),
             ("text", ".card:nth-child(1) h3", "text", "Starter kit"), ("removed", ".card:nth-child(4) .meta b", None, None),
             ("added", ".card:nth-child(8) .body", None, "<span class='new'>Bestseller</span>"),
             ("align", ".card:nth-child(2) .body", "text-align", "center")],
    "borderless": [("gap", ".split", "gap", "120px"), ("padding", ".testimonial", "padding", "80px 160px"),
                   ("margin", ".intro h2", "margin-bottom", "28px"), ("color", ".cta", "background-color", "#EEF4FF"),
                   ("font-size", ".quote", "font-size", "28px"), ("radius", ".cta", "border-radius", "24px"),
                   ("text", ".intro h2", "text", "Why structure beats raw pixels"), ("removed", ".who", None, None),
                   ("added", ".cta", None, "<a class='btn primary new'>Get started</a>"), ("align", ".cta", "text-align", "center")],
    "settings": [("gap", ".side", "gap", "14px"), ("padding", ".main", "padding", "48px 48px"),
                 ("margin", ".main .sub", "margin-bottom", "48px"), ("color", ".opt:nth-of-type(3) .tog", "background-color", "#12B76A"),
                 ("font-size", ".main h1", "font-size", "32px"), ("radius", ".side a.on", "border-radius", "16px"),
                 ("text", ".opt:nth-of-type(2) b", "text", "Microsoft Teams alerts"), ("removed", ".side a:nth-child(5)", None, None),
                 ("added", ".side", None, "<a class='new'>Integrations</a>"), ("align", ".opt:nth-of-type(4)", "align-items", "flex-start")],
    "dark": [("gap", ".kpis", "gap", "40px"), ("padding", ".kpi:nth-child(2)", "padding", "36px"),
             ("margin", ".wrap .sub", "margin-top", "20px"), ("color", ".kpi:nth-child(1) .d", "color", "#F97066"),
             ("font-size", ".kpi:nth-child(3) .v", "font-size", "26px"), ("radius", ".chart", "border-radius", "0px"),
             ("text", ".kpi:nth-child(4) .v", "text", "2.6 s"), ("removed", ".kpi:nth-child(2) .d", None, None),
             ("added", ".kpi:nth-child(3)", None, "<div class='d new'>target 90%</div>"), ("align", ".wrap h1", "text-align", "right")],
    "article": [("gap", ".s2 blockquote", "margin-top", "64px"), ("padding", ".s4 blockquote", "padding", "4px 0 4px 48px"),
                ("margin", ".s3 h2", "margin-top", "80px"), ("color", ".s4 blockquote", "border-left-color", "#F04438"),
                ("font-size", ".art h1", "font-size", "38px"), ("radius", ".s3 figure img", "border-radius", "0px"),
                ("text", ".s1 h2", "text", "Part 1: A different heading"), ("removed", ".s3 figcaption", None, None),
                ("added", ".s3", None, "<p class='new'>Editor's note: this section was updated.</p>"), ("align", ".art .by", "text-align", "center")],
    "dynamic": [("gap", ".panels", "gap", "48px"), ("padding", ".box.live", "padding", "40px"),
                ("color", ".box.live .big", "color", "#3366FF"), ("text", ".feed li:nth-child(2) b", "text", "Pricing page v2"),
                ("removed", ".feed li:nth-child(4)", None, None), ("align", ".box.live", "text-align", "center")],
    "plans": [("gap", ".tier.hot ul", "gap", "18px"), ("padding", ".tier.hot", "padding", "36px 24px"),
              ("margin", ".intro p", "margin-top", "20px"), ("color", ".tier.hot .btn", "background-color", "#12B76A"),
              ("font-size", ".tier.hot .cost", "font-size", "34px"), ("radius", ".tier:nth-child(1)", "border-radius", "0px"),
              ("text", ".tier:nth-child(3) .cost", "text", "€45"), ("removed", ".tier.hot .badge", None, None),
              ("added", ".tier:nth-child(4) ul", None, "<li class='new'><span>On-prem option</span></li>"),
              ("align", ".intro", "align-items", "center")],
    "membership": [("gap", ".cards", "gap", "48px"), ("padding", ".card.dark .inner", "padding", "40px"),
                   ("margin", ".top p", "margin-top", "24px"), ("color", ".card.dark .btn", "background-color", "#F04438"),
                   ("font-size", ".card.dark .amount", "font-size", "44px"), ("radius", ".card:nth-child(1)", "border-radius", "4px"),
                   ("text", ".card:nth-child(3) .amount", "text", "$59"), ("removed", ".card.dark .tag", None, None),
                   ("added", ".card:nth-child(1) ul", None, "<li class='new'><span>Email support</span></li>"),
                   ("align", ".note", "text-align", "left")],
}
MOBILE_MUTATIONS = 6  # mobile variants use the first N of their template's catalog

# replay pairs: page -> (A, B), two catalog entries by type. shot_0 has A+B, shot_1 only B (A fixed), shot_2 neither.
# A moves B's box (layout change above it) so a position-derived id would renumber; never `added` (A must exist when fixed).
REPLAY = {"landing": ("margin", "color"), "grid": ("gap", "color"), "settings": ("margin", "text"),
          "pricing": ("margin", "color"), "dark": ("margin", "text"), "article": ("font-size", "color")}

#!/usr/bin/env python3
"""Builds the HR Connect static website.

Usage:  python3 _build/build.py

Page content lives in content.py. This file holds the shared layout
(header, footer, navigation) and the building blocks pages are made from.
Every page is written to <path>/index.html next to the _build folder,
e.g. /product/payroll/ -> product/payroll/index.html.
"""
import html, os, re, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import content as C  # noqa: E402

e = html.escape

# --------------------------------------------------------------------------- icons
ICONS = {
  "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  "wallet": '<path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/>',
  "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
  "receipt": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
  "banknote": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
  "logout": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
  "user": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
  "sparkles": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9Z"/><path d="M19 3v4M17 5h4M5 17v4M3 19h4"/>',
  "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
  "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
  "chart": '<path d="M3 3v18h18"/><path d="M18 17V9M13 17V5M8 17v-3"/>',
  "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
  "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10Z"/>',
  "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
  "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
  "calc": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/>',
  "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15Z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
  "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2M2 13h20"/>',
  "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
  "layers": '<path d="m12 2 10 5-10 5L2 7Z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
  "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
  "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
  "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/>',
  "org": '<rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/><path d="M12 7v5M5 17v-3h14v3"/>',
  "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
  "chev": '<path d="m6 9 6 6 6-6"/>',
  "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
  "refresh": '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
  "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
  "list": '<path d="M9 6h12M9 12h12M9 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
  "chev-left": '<path d="m15 18-6-6 6-6"/>',
  "chev-right": '<path d="m9 18 6-6-6-6"/>',
  "phone": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>',
}

def icon(name, cls=""):
    return (f'<svg{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#6C3845"/>'
        '<circle cx="12.5" cy="16" r="6" fill="none" stroke="#fff" stroke-width="2.6"/>'
        '<circle cx="19.5" cy="16" r="6" fill="none" stroke="#D9C8CC" stroke-width="2.6"/></svg>')

# --------------------------------------------------------------------------- blocks
def md(s):
    """Tiny inline formatting: **bold** and [text](/link)."""
    s = e(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s

def btns(ctas, light=False):
    out = []
    for i, (label, href) in enumerate(ctas):
        if light:
            cls = "btn-light" if i == 0 else "btn-outline-light"
        else:
            cls = "btn-primary" if i == 0 else "btn-ghost"
        arrow = icon("arrow") if i == 0 else ""
        out.append(f'<a class="btn {cls}" href="{href}">{e(label)}{arrow}</a>')
    return "".join(out)

def mock(m):
    if not m:
        return ""
    kpis = "".join(f'<div class="mock-kpi"><small>{e(a)}</small><strong>{e(b)}</strong></div>' for a, b in m.get("kpis", []))
    rows = []
    for r in m.get("rows", []):
        title, sub, value = r[0], r[1], r[2]
        pill = r[3] if len(r) > 3 else None
        initials = r[4] if len(r) > 4 and r[4] else "".join(w[0] for w in title.split()[:2]).upper()
        pv = ""
        forced = None
        if isinstance(pill, tuple):  # (label, colour) to override the default colour
            pill, forced = pill
        if pill:
            kind = {"Approved": "ok", "Paid": "ok", "Active": "ok", "Verified": "ok", "Sent": "ok", "Read": "ok", "Done": "ok", "Cleared": "ok",
                    "Pending": "warn", "Renew": "warn", "Pending approval": "warn", "Scheduled": "warn", "Unread": "warn", "In progress": "warn"}.get(pill, "")
            if forced is not None:
                kind = forced
            pv = f'<span class="pill {kind}">{e(pill)}</span>'
        val = f'<span class="v">{e(value)}</span>' if value else ""
        rows.append(f'<div class="mock-row"><span class="av">{e(initials)}</span><span class="t"><b>{e(title)}</b><span>{e(sub)}</span></span>{val}{pv}</div>')
    foot = f'<div class="mock-foot">{md(m["foot"])}</div>' if m.get("foot") else ""
    return (f'<div class="mock" aria-hidden="true"><div class="mock-bar"><i></i><i></i><i></i><b>{e(m["title"])}</b></div>'
            f'<div class="mock-body">{f"<div class=mock-kpis>{kpis}</div>" if kpis else ""}{"".join(rows)}{foot}</div></div>')

def ai_hub(nodes):
    """Decorative 'connected hub': AI core in the middle, modules around it,
    with pulses travelling along the links. nodes = [(label, icon, angle_deg)]."""
    import math
    lines, pulses, pills = [], [], []
    for i, (label, ic, ang) in enumerate(nodes):
        a = math.radians(ang)
        x, y = 200 + 150 * math.cos(a), 200 + 150 * math.sin(a)
        lines.append(f'<line x1="200" y1="200" x2="{x:.1f}" y2="{y:.1f}"/>')
        # Pulses rest at the centre (hidden behind the core) until their animation begins
        pulses.append(f'<circle class="hub-pulse" cx="200" cy="200" r="3.5"><animateMotion dur="3s" begin="{i * 0.5:.1f}s" repeatCount="indefinite" '
                      f'path="M0 0 L{x - 200:.1f} {y - 200:.1f}"/></circle>')
        left, top = 50 + 37.5 * math.cos(a), 50 + 37.5 * math.sin(a)
        pills.append(f'<span class="hub-node" style="left:{left:.2f}%;top:{top:.2f}%"><span class="hub-ic">{icon(ic)}</span>{e(label)}</span>')
    svg = f'<svg class="hub-links" viewBox="0 0 400 400">{"".join(lines)}{"".join(pulses)}</svg>'
    core = f'<span class="hub-core">{LOGO.replace("<svg ", '<svg class="hub-logo" ', 1)}<b>HRConnect.AI</b></span>'
    return f'<div class="hub" aria-hidden="true">{svg}{core}{"".join(pills)}</div>'

def b_hero(b, page):
    crumbs = ""
    if b.get("crumbs"):
        parts = [f'<a href="{h}">{e(t)}</a>' for t, h in b["crumbs"]]
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb">{" / ".join(parts)}</nav>'
    eyebrow = f'<div class="eyebrow">{e(b["eyebrow"])}</div>' if b.get("eyebrow") else ""
    trust = ""
    if b.get("trust"):
        trust = '<div class="trust">' + "".join(f'<span>{icon("check")}{e(t)}</span>' for t in b["trust"]) + "</div>"
    dark = b.get("dark", False)  # brand-coloured background, like the CTA band
    ctas = f'<div class="ctas">{btns(b["ctas"], light=dark)}</div>' if b.get("ctas") else ""
    side = mock(b.get("mock"))
    solo = "" if side else " solo"
    return (f'<section class="hero{solo}{" dark" if dark else ""}"><div class="wrap hero-grid"><div>{crumbs}{eyebrow}<h1>{md(b["title"])}</h1>'
            f'<p class="lead">{md(b["lead"])}</p>{ctas}{trust}</div>{f"<div>{side}</div>" if side else ""}</div></section>')

def b_hero_slider(b, page):
    """Rotating dark hero: one slide per message, arrows and dots below.
    Only the first slide uses <h1>; the rest use a same-looking <h2>."""
    slides = b["slides"]
    n = len(slides)
    out = []
    for i, sl in enumerate(slides):
        eyebrow = f'<div class="eyebrow">{e(sl["eyebrow"])}</div>' if sl.get("eyebrow") else ""
        heading = f'<h1>{md(sl["title"])}</h1>' if i == 0 else f'<h2 class="hs-title">{md(sl["title"])}</h2>'
        ctas = f'<div class="ctas">{btns(sl["ctas"], light=True)}</div>' if sl.get("ctas") else ""
        trust = ""
        if sl.get("trust"):
            trust = '<div class="trust">' + "".join(f'<span>{icon("check")}{e(t)}</span>' for t in sl["trust"]) + "</div>"
        hidden = "" if i == 0 else ' aria-hidden="true" inert'
        out.append(f'<div class="hs-slide" role="group" aria-roledescription="slide" aria-label="{i + 1} of {n}"{hidden}>'
                   f'<div class="wrap"><div class="hero-grid"><div>{eyebrow}{heading}<p class="lead">{md(sl["lead"])}</p>{ctas}{trust}</div>'
                   f'<div>{ai_hub(sl["visual"]) if sl.get("visual") else mock(sl.get("mock"))}</div></div></div></div>')
    dots = "".join(f'<button class="hs-dot" type="button" aria-label="Show slide {i + 1}"{" aria-current=" + chr(34) + "true" + chr(34) if i == 0 else ""}></button>'
                   for i in range(n))
    # Slides span the full page width; arrows sit at the left/right middle of
    # the slides (beside the dots on phones); dots stay centred below.
    arrows = (f'<button class="hs-arrow hs-prev" type="button" data-hs="prev" aria-label="Previous slide">{icon("chev-left")}</button>'
              f'<button class="hs-arrow hs-next" type="button" data-hs="next" aria-label="Next slide">{icon("chev-right")}</button>')
    return (f'<section class="hero dark hero-slider" aria-roledescription="carousel" aria-label="{e(b.get("label", "Product highlights"))}" '
            f'data-interval="{int(b.get("interval", 6000))}"><span class="hs-orb" aria-hidden="true"></span><div class="hs-stage"><div class="hs-viewport"><div class="hs-track">{"".join(out)}</div></div>{arrows}</div>'
            f'<div class="wrap"><div class="hs-controls"><div class="hs-dots">{dots}</div></div></div></section>')

def head(b, center=False):
    if not b.get("title"):
        return ""
    eyebrow = f'<div class="eyebrow">{e(b["eyebrow"])}</div>' if b.get("eyebrow") else ""
    lead = f'<p>{md(b["lead"])}</p>' if b.get("lead") else ""
    return f'<div class="section-head{" center" if center else ""}">{eyebrow}<h2>{md(b["title"])}</h2>{lead}</div>'

def sec(inner, b):
    cls = " ".join(x for x in [("alt" if b.get("alt") else ""), ("tight" if b.get("tight") else "")] if x)
    sid = f' id="{b["id"]}"' if b.get("id") else ""
    return f'<section{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}{sid}><div class="wrap">{inner}</div></section>'

def b_features(b, page):
    cols = b.get("cols", 3)
    cards = []
    for it in b["items"]:
        ic, title, text = it[0], it[1], it[2]
        cards.append(f'<div class="card"><div class="ic">{icon(ic)}</div><h3>{e(title)}</h3><p>{md(text)}</p></div>')
    return sec(head(b, b.get("center", True)) + f'<div class="grid g{cols}">{"".join(cards)}</div>', b)

def b_cards(b, page):
    cols = b.get("cols", 3)
    cards = []
    for it in b["items"]:
        ic, title, text, href = it[0], it[1], it[2], it[3]
        tag = it[4] if len(it) > 4 else None
        tg = f'<span class="tag{" soon" if tag == "Coming soon" else ""}">{e(tag)}</span>' if tag else ""
        icn = f'<div class="ic">{icon(ic)}</div>' if ic else ""
        if href:
            cards.append(f'<a class="card" href="{href}">{icn}{tg}<h3>{e(title)}</h3><p>{md(text)}</p><span class="more">Learn more{icon("arrow")}</span></a>')
        else:
            cards.append(f'<div class="card">{icn}{tg}<h3>{e(title)}</h3><p>{md(text)}</p></div>')
    return sec(head(b, b.get("center", True)) + f'<div class="grid g{cols}">{"".join(cards)}</div>', b)

def b_steps(b, page):
    steps = "".join(f'<div class="step"><h3>{e(t)}</h3><p>{md(x)}</p></div>' for t, x in b["items"])
    return sec(head(b, True) + f'<div class="steps">{steps}</div>', b)

def b_split(b, page):
    checks = ""
    if b.get("bullets"):
        checks = '<ul class="checks">' + "".join(f'<li>{icon("check")}<span>{md(x)}</span></li>' for x in b["bullets"]) + "</ul>"
    eyebrow = f'<div class="eyebrow">{e(b["eyebrow"])}</div>' if b.get("eyebrow") else ""
    ctas = f'<div class="ctas" style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap">{btns(b["ctas"])}</div>' if b.get("ctas") else ""
    text = f'<div>{eyebrow}<h2>{md(b["title"])}</h2><p class="lead">{md(b["text"])}</p>{checks}{ctas}</div>'
    side = mock(b.get("mock")) if b.get("mock") else b.get("side_html", "")
    return sec(f'<div class="split{" rev" if b.get("rev") else ""}">{text}<div>{side}</div></div>', b)

def b_faq(b, page):
    items = []
    for q, a in b["items"]:
        paras = "".join(f"<p>{md(p)}</p>" for p in (a if isinstance(a, list) else [a]))
        items.append(f'<details><summary>{e(q)}</summary><div>{paras}</div></details>')
    b = dict(b); b.setdefault("title", "Frequently asked questions")
    return sec(head(b, True) + f'<div class="faq">{"".join(items)}</div>', b)

def b_table(b, page):
    th = "".join(f"<th>{e(h)}</th>" for h in b["head"])
    rows = []
    for r in b["rows"]:
        tds = []
        for c in r:
            cls = ' class="yes"' if c.startswith("✓") else (' class="no"' if c in ("—", "✕") or c.startswith("✕") else "")
            tds.append(f"<td{cls}>{md(c)}</td>")
        rows.append("<tr>" + "".join(tds) + "</tr>")
    return sec(head(b, b.get("center", True)) + f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>', b)

def b_stats(b, page):
    items = "".join(f'<div class="stat"><strong>{e(v)}</strong><span>{e(l)}</span></div>' for v, l in b["items"])
    return sec(head(b, True) + f'<div class="stats">{items}</div>', b)

def b_cta(b, page):
    title = b.get("title", "See HR Connect with your own team’s data")
    text = b.get("text", "Book a 30-minute demo. We’ll show you payroll, leave and expenses set up the way your company works.")
    ctas = b.get("ctas", [("Book a demo", "/book-a-demo/"), ("See pricing", "/pricing/")])
    return (f'<section class="cta-band"><div class="wrap"><div class="cta-box"><div><h2>{md(title)}</h2><p>{md(text)}</p></div>'
            f'<div class="ctas">{btns(ctas, light=True)}</div></div></div></section>')

def b_prose(b, page):
    notice = ""
    if b.get("notice"):
        notice = f'<div class="notice">{icon("info")}<span>{md(b["notice"])}</span></div>'
    return sec(f'<div class="prose">{notice}{b["html"]}</div>', b)

def b_plans(b, page):
    plans = []
    for p in b["plans"]:
        checks = '<ul class="checks">' + "".join(f'<li>{icon("check")}<span>{md(x)}</span></li>' for x in p["items"]) + "</ul>"
        plans.append(f'<div class="plan{" featured" if p.get("featured") else ""}">'
                     f'{"<span class=tag>Most complete</span>" if p.get("featured") else ""}<h3>{e(p["name"])}</h3>'
                     f'<div class="price"><strong>{e(p["price"])}</strong>{e(p["unit"])}</div><p class="desc">{md(p["desc"])}</p>'
                     f'{checks}<a class="btn {"btn-primary" if p.get("featured") else "btn-ghost"}" href="{p["href"]}">{e(p["cta"])}</a></div>')
    return sec(head(b, True) + f'<div class="plans">{"".join(plans)}</div>', b)

def field(f):
    name, label, kind = f[0], f[1], f[2]
    opts = f[3] if len(f) > 3 else None
    full = " full" if kind in ("textarea",) or (len(f) > 4 and f[4] == "full") else ""
    req = "" if label.endswith("(optional)") else " required"
    fid = f"f-{name}"
    if kind == "textarea":
        ctrl = f'<textarea id="{fid}" name="{e(label.replace(" (optional)", ""))}"{req}></textarea>'
    elif kind == "select":
        o = "".join(f"<option>{e(x)}</option>" for x in opts)
        ctrl = f'<select id="{fid}" name="{e(label.replace(" (optional)", ""))}"{req}><option value="">Select…</option>{o}</select>'
    else:
        ctrl = f'<input id="{fid}" type="{kind}" name="{e(label.replace(" (optional)", ""))}" autocomplete="on"{req}>'
    return f'<div class="field{full}"><label for="{fid}">{e(label)}</label>{ctrl}</div>'

def b_form(b, page):
    fields = "".join(field(f) for f in b["fields"])
    form = (f'<form class="form-card" data-mailto="{C.CONTACT_EMAIL}" data-subject="{e(b["subject"])}" novalidate>'
            f'<div class="form-grid">{fields}</div><div style="margin-top:22px"><button class="btn btn-primary" type="submit">{e(b["button"])}{icon("arrow")}</button></div>'
            f'<p class="form-note">Sending opens your email app with your details filled in, addressed to {C.CONTACT_EMAIL}.</p>'
            f'<div class="form-ok" role="status">Thanks. Your email app should have opened; press send there and we’ll reply within one working day.</div></form>')
    aside = b.get("aside", "")
    return sec(f'<div class="split" style="align-items:start"><div>{aside}</div><div>{form}</div></div>', b)

def b_calc(b, page):
    fields = []
    for f in b["fields"]:
        name, label, kind = f[0], f[1], f[2]
        extra = f[3] if len(f) > 3 else {}
        if kind == "select":
            o = "".join(f'<option value="{v}">{e(t)}</option>' for v, t in extra["options"])
            ctrl = f'<select id="c-{name}" name="{name}">{o}</select>'
        else:
            attrs = " ".join(f'{k}="{v}"' for k, v in extra.items() if k != "today")
            today = " data-today" if extra.get("today") else ""
            ctrl = f'<input id="c-{name}" name="{name}" type="{kind}" {attrs}{today}>'
        fields.append(f'<div class="field full"><label for="c-{name}">{e(label)}</label>{ctrl}</div>')
    form = f'<form class="form-card"><div class="form-grid">{"".join(fields)}</div><p class="disclaimer">{md(b["disclaimer"])}</p></form>'
    result = (f'<div class="calc-result" aria-live="polite"><small>{e(b["result_label"])}</small><div class="amount" data-out="amount">—</div>'
              f'<ul data-out="rows"></ul><p class="notes" data-out="notes"></p></div>')
    return sec(f'<div class="calc" data-calc="{b["kind"]}">{form}{result}</div>', b)

def b_glossary(b, page):
    terms = sorted(b["terms"], key=lambda t: t[0].lower())
    letters = sorted({t[0][0].upper() for t in terms})
    az = '<nav class="az" aria-label="Jump to letter">' + "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters) + "</nav>"
    out, seen = [], set()
    for t, d in terms:
        l = t[0].upper()
        anchor = f' id="letter-{l}"' if l not in seen else ""
        seen.add(l)
        slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
        out.append(f'<article class="term"{anchor}><h3 id="{slug}">{e(t)}</h3><p>{md(d)}</p></article>')
    search = '<input class="search" type="search" placeholder="Search terms…" aria-label="Search terms" data-filter=".term">'
    return sec(search + az + f'<div class="terms">{"".join(out)}</div>', b)

def b_help(b, page):
    out = []
    for cat, ic, items in b["groups"]:
        qs = "".join(f'<details class="help-q"><summary>{e(q)}</summary><div>{"".join(f"<p>{md(p)}</p>" for p in (a if isinstance(a, list) else [a]))}</div></details>' for q, a in items)
        out.append(f'<div class="help-group" style="margin-bottom:40px"><h3 style="display:flex;gap:10px;align-items:center;margin-bottom:16px">'
                   f'<span class="ic" style="width:36px;height:36px;border-radius:10px;background:var(--brand-soft);color:var(--brand);display:grid;place-items:center">{icon(ic)}</span>{e(cat)}</h3>'
                   f'<div class="faq" style="margin:0;max-width:none">{qs}</div></div>')
    search = '<input class="search" type="search" placeholder="Search help articles…" aria-label="Search help articles" data-filter=".help-q">'
    return sec(search + "".join(out), b)

def b_spotlight(b, page):
    """Tabbed slider: one tab and one slide per audience."""
    slides = b["slides"]
    n = len(slides)
    tabs = "".join(
        f'<button class="sp-tab" type="button" role="tab" id="sp-tab-{i}" aria-controls="sp-slide-{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(sl["tab"])}</button>'
        for i, sl in enumerate(slides))
    out = []
    for i, sl in enumerate(slides):
        checks = '<ul class="checks">' + "".join(f'<li>{icon("check")}<span>{md(x)}</span></li>' for x in sl["bullets"]) + "</ul>"
        label, href = sl["cta"]
        out.append(f'<div class="sp-slide" role="tabpanel" id="sp-slide-{i}" aria-labelledby="sp-tab-{i}" aria-roledescription="slide" aria-label="{i + 1} of {n}"{"" if i == 0 else ' aria-hidden="true" inert'}>'
                   f'<div class="split"><div><div class="eyebrow">{e(sl["eyebrow"])}</div><h3 class="sp-title">{md(sl["title"])}</h3>'
                   f'<p class="lead">{md(sl["text"])}</p>{checks}'
                   f'<div class="sp-cta"><a class="btn btn-primary" href="{href}">{e(label)}{icon("arrow")}</a></div></div>'
                   f'<div>{mock(sl["mock"])}</div></div></div>')
    controls = (f'<div class="sp-controls"><button class="sp-arrow" type="button" data-sp="prev" aria-label="Previous solution">{icon("chev-left")}</button>'
                f'<div class="sp-progress" aria-hidden="true"><span></span></div>'
                f'<button class="sp-arrow" type="button" data-sp="next" aria-label="Next solution">{icon("chev-right")}</button></div>')
    return (f'<section class="alt spotlight" aria-roledescription="carousel" aria-label="{e(b.get("label", "Solutions spotlight"))}"><div class="wrap">'
            f'{head(b, True)}<div class="sp-tabs" role="tablist" aria-label="Choose a solution">{tabs}</div>'
            f'<div class="sp-viewport"><div class="sp-track">{"".join(out)}</div></div>{controls}</div></section>')

def b_video(b, page):
    """Animated promo video with chapter buttons. Needs promo-video.css/js (added in render)."""
    player = ('<div class="pv-frame"><div class="pv" data-auto data-demo-href="/book-a-demo/"></div>'
              '<div class="pv-chapters" role="group" aria-label="Video chapters"></div></div>')
    cta = f'<div class="pv-cta">{btns(b["ctas"])}</div>' if b.get("ctas") else ""
    return sec(head(b, True) + player + cta, {**b, "id": b.get("id")})

def b_html(b, page):
    return sec(b["html"], b) if b.get("wrap", True) else b["html"]

BLOCKS = {k[2:]: v for k, v in globals().items() if k.startswith("b_")}

# --------------------------------------------------------------------------- layout
def nav_html():
    items = []
    for label, menu in C.NAV:
        if isinstance(menu, str):
            items.append(f'<li class="nav-item"><a class="nav-link" href="{menu}">{e(label)}</a></li>')
            continue
        wide = " menu-wide" if len(menu) > 6 else ""
        links = "".join(f'<a href="{h}"><span class="mi">{icon(ic)}</span><span><b>{e(t)}</b><span>{e(d)}</span></span></a>' for t, h, ic, d in menu)
        items.append(f'<li class="nav-item"><button class="nav-link" type="button" aria-haspopup="true">{e(label)}{icon("chev", "chev")}</button>'
                     f'<div class="menu{wide}"><div class="menu-inner">{links}</div></div></li>')
    mobile = []
    for label, menu in C.NAV:
        if isinstance(menu, str):
            mobile.append(f'<a href="{menu}">{e(label)}</a>')
        else:
            mobile.append(f'<details><summary>{e(label)}</summary>' + "".join(f'<a href="{h}">{e(t)}</a>' for t, h, ic, d in menu) + "</details>")
    return f"""<header class="site-header">
  <div class="wrap nav">
    <a class="logo" href="/">{LOGO}<span>HRConnect.AI</span></a>
    <ul class="nav-links">{"".join(items)}</ul>
    <div class="nav-cta"><a class="login" href="{C.APP_URL}">Log in</a><a class="btn btn-primary" href="/book-a-demo/">Book a demo</a></div>
    <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false">{icon("menu")}</button>
  </div>
  <nav class="mobile-nav" aria-label="Mobile">{"".join(mobile)}<div class="mobile-cta"><a class="btn btn-ghost" href="{C.APP_URL}">Log in</a><a class="btn btn-primary" href="/book-a-demo/">Book a demo</a></div></nav>
</header>"""

def footer_html():
    cols = "".join(f'<div><h4>{e(t)}</h4><ul>' + "".join(f'<li><a href="{h}">{e(n)}</a></li>' for n, h in links) + "</ul></div>" for t, links in C.FOOTER)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about"><a class="logo" href="/">{LOGO}<span>HRConnect.AI</span></a><p>{e(C.TAGLINE)}</p></div>
      {cols}
    </div>
    <div class="foot-bottom"><span>© <span id="year">{date.today().year}</span> HR Connect. All rights reserved.</span><span><a href="mailto:{C.CONTACT_EMAIL}">{C.CONTACT_EMAIL}</a></span></div>
  </div>
</footer>"""

def relativize(doc, path):
    depth = len([p for p in path.split("/") if p])
    prefix = "../" * depth or "./"
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith("//"):
            return m.group(0)
        target = url[1:]
        # Point folder links at their index.html so pages also work opened
        # as files or on hosts that don't serve folder indexes.
        path_part, sep, frag = target.partition("#")
        if path_part == "" or path_part.endswith("/"):
            path_part += "index.html"
        target = path_part + sep + frag
        if prefix == "./" :
            return f'{attr}="./{target}"'
        return f'{attr}="{prefix}{target}"'
    return re.sub(r'(href|src)="(/[^"]*)"', fix, doc)

def render(path, page, nav, foot):
    body = "".join(BLOCKS[b["type"]](b, page) for b in page["blocks"])
    scripts = '<script src="/assets/js/site.js" defer></script>'
    if any(b["type"] == "calc" for b in page["blocks"]):
        scripts += '<script src="/assets/js/calculators.js" defer></script>'
    if any(b["type"] == "video" for b in page["blocks"]):
        scripts += '\n<link rel="stylesheet" href="/assets/css/promo-video.css">\n<script src="/assets/js/promo-video.js" defer></script>'
    canonical = C.SITE_URL + ("/" + path + "/" if path else "/")
    title = page["title"] if path == "" else f'{page["title"]} | HR Connect'
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(page["desc"])}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(page["desc"])}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#6C3845">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
{scripts}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav}
<main id="main">
{body}
</main>
{foot}
</body>
</html>
"""
    return relativize(doc, path)

def main():
    nav, foot = nav_html(), footer_html()
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    with open(os.path.join(ROOT, "assets", "img", "favicon.svg"), "w") as f:
        f.write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    urls = []
    for path, page in C.PAGES.items():
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render(path, page, nav, foot))
        urls.append(C.SITE_URL + ("/" + path + "/" if path else "/"))
    # 404 page sits at the root
    nf = render("", C.NOT_FOUND, nav, foot)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(nf)
    today = date.today().isoformat()
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write("".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls))
        f.write("</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nDisallow: /_build/\nDisallow: /research/\n\nSitemap: {C.SITE_URL}/sitemap.xml\n")
    print(f"Built {len(urls)} pages into {ROOT}")

if __name__ == "__main__":
    main()

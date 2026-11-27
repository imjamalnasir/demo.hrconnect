"""Build the HRConnect.AI sales documents.

Expands the %%MACRO%% placeholders in src/*.tpl.html, writes the finished HTML
next to this folder, prints each to PDF with headless Chrome and saves preview
images for research/sales-documents.html.

Run from anywhere:  python3 research/sales-docs/src/build_docs.py
"""
import os, re, subprocess, shutil, tempfile

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SRC)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

ICONS = {
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "pay": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/>',
    "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "receipt": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    "coins": '<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18M7 6h1v4M16.71 13.88l.7.71-2.82 2.82"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "exit": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
    "self": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="10" r="3"/><path d="M7 20.66V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.66"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M18 17V9M13 17V5M8 17v-3"/>',
    "spark": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 3v4M17 5h4"/>',
    "case": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3M12 17h.01"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "sheet": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
}

def ico(name, size, bg="#F6EEF0", fg="#6C3845", r=None):
    r = round(size * .28) if r is None else r
    return f'<span class="ico" style="width:{size}px;height:{size}px;border-radius:{r}px;background:{bg};color:{fg}"><svg viewBox="0 0 24 24">{ICONS[name]}</svg></span>'

def logo(size, dark):
    tile, r1, r2 = ("#fff", "#6C3845", "#B97A8A") if dark else ("#6C3845", "#fff", "#D9C8CC")
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 48 48"><rect width="48" height="48" rx="13" fill="{tile}"/>'
            f'<path d="M14 13V35M34 13V35M14 24H34" fill="none" stroke="{r1}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<circle cx="14" cy="13" r="3.4" fill="{r1}"/><circle cx="14" cy="35" r="3.4" fill="{r1}"/>'
            f'<circle cx="34" cy="13" r="3.4" fill="{r1}"/><circle cx="34" cy="35" r="3.4" fill="{r1}"/>'
            f'<circle cx="24" cy="24" r="4.4" fill="{r2}"/></svg>')

CHECK = '<span style="flex:none;width:22px;height:22px;border-radius:50%;background:#E5F6EF;display:inline-grid;place-items:center"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#0F8A5F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></span>'
CROSS = '<span style="flex:none;width:22px;height:22px;border-radius:50%;background:#F4EFF1;display:inline-grid;place-items:center"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#9A8F97" stroke-width="3" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg></span>'

def hub():
    mods = [("users", "Core HR"), ("cal", "Leave"), ("receipt", "Expenses"), ("coins", "Loans"), ("exit", "Offboarding"), ("self", "Self-service"), ("spark", "AI assistant"), ("chart", "Reports")]
    import math
    cx, cy, R = 280, 270, 205
    lines, nodes = [], []
    for i, (k, t) in enumerate(mods):
        a = -math.pi / 2 + i * 2 * math.pi / len(mods)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="rgba(255,255,255,.28)" stroke-width="2" stroke-dasharray="6 6"/>')
        nodes.append(f'<div style="position:absolute;left:{x - 66:.0f}px;top:{y - 21:.0f}px;width:132px;display:flex;align-items:center;gap:8px;background:#5B2F3B;border:1px solid rgba(255,255,255,.22);border-radius:14px;padding:7px 10px;font-size:13.5px;font-weight:700;color:#fff;white-space:nowrap;box-shadow:0 8px 20px rgba(0,0,0,.25)">{ico(k, 28, "#fff", "#6C3845", 8)}{t}</div>')
    core = (f'<div style="position:absolute;left:{cx - 78}px;top:{cy - 70}px;width:156px;height:140px;border-radius:26px;background:#fff;color:#4A2530;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;'
            f'box-shadow:0 0 0 12px rgba(255,255,255,.08),0 24px 60px rgba(0,0,0,.4)">{ico("pay", 52, "#F6EEF0", "#6C3845", 15)}<div style="font-size:19px;font-weight:800">Payroll</div></div>')
    return f'<svg width="560" height="540" style="position:absolute;inset:0">{"".join(lines)}</svg>{"".join(nodes)}{core}'

def li(items, size="15.5px"):
    return "".join(f'<div style="display:flex;gap:9px;align-items:center;font-size:{size};color:#3A3340">{CHECK}{x}</div>' for x in items)

def expand(s):
    def m(match):
        name, _, arg = match.group(1).partition(":")
        a = arg.split("|") if arg else []
        if name == "ICON":
            return ico(a[0], 36, "#fff", "#6C3845", 10)
        if name == "ICON_S":
            return ico(a[0], 22, "#fff", "#6C3845", 6)
        if name == "ICON_BIG":
            return ico(a[0], 46, "#6C3845", "#fff", 13)
        if name == "LOGO":
            return logo(22, False)
        if name == "LOGO_DARK":
            return logo(22, True)
        if name == "HUB":
            return hub()
        if name == "PAIN":
            return (f'<div class="card" style="padding:20px 22px">{ico(a[0], 42)}<h3 style="margin-top:12px">{a[1]}</h3>'
                    f'<p style="margin-top:6px;font-size:15.5px;line-height:1.45;color:#6B6470">{a[2]}</p></div>')
        if name == "CMP":
            return (f'<tr style="border-top:1px solid #ECE4E7"><td style="padding:14px 0;font-weight:700;color:#1B1620">{a[0]}</td>'
                    f'<td style="padding:14px 0;color:#6B6470"><span style="display:inline-flex;gap:10px;align-items:center">{CROSS}{a[1]}</span></td>'
                    f'<td style="padding:14px 0;color:#1B1620;font-weight:600"><span style="display:inline-flex;gap:10px;align-items:center">{CHECK}{a[2]}</span></td></tr>')
        if name == "ROW":
            av, n, sub, v, cls, pill = a
            return (f'<div class="row"><span class="av">{av}</span><div class="n">{n}<span>{sub}</span></div>'
                    f'{f"<div class=v>{v}</div>" if v else ""}<span class="pill {cls}">{pill}</span></div>')
        if name == "AI":
            return (f'<div style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:24px">'
                    f'{ico(a[0], 48, "#fff", "#6C3845", 14)}<div style="margin-top:16px;font-size:21px;font-weight:700;color:#fff">{a[1]}</div>'
                    f'<p style="margin-top:8px;font-size:16px;line-height:1.45;color:rgba(255,255,255,.75)">{a[2]}</p></div>')
        if name == "TEAM":
            items = a[3].split("~")
            return (f'<div class="card" style="padding:22px 24px"><div style="display:flex;align-items:center;gap:14px">{ico(a[0], 48)}'
                    f'<div><h3 style="font-size:22px">{a[1]}</h3><div style="font-size:16px;font-weight:600;color:#6C3845;margin-top:2px">{a[2]}</div></div></div>'
                    f'<div style="margin-top:14px;display:grid;gap:8px">{li(items, "16px")}</div></div>')
        if name == "PROOF":
            return (f'<div class="card" style="padding:20px 22px"><div style="display:flex;align-items:center;gap:12px">{ico(a[0], 40)}<h3>{a[1]}</h3></div>'
                    f'<p style="margin-top:10px;font-size:15.5px;line-height:1.45;color:#6B6470">{a[2]}</p></div>')
        if name == "STEP":
            return (f'<div class="card" style="padding:28px"><div style="width:52px;height:52px;border-radius:50%;background:#6C3845;color:#fff;display:grid;place-items:center;font-size:24px;font-weight:800">{a[0]}</div>'
                    f'<h3 style="margin-top:18px;font-size:23px">{a[1]}</h3><p style="margin-top:8px;font-size:17px;line-height:1.45;color:#6B6470">{a[2]}</p></div>')
        if name == "MINI":
            return (f'<div style="display:flex;gap:14px;align-items:flex-start">{ico(a[0], 44)}<div><div style="font-size:18px;font-weight:700;color:#1B1620">{a[1]}</div>'
                    f'<div style="font-size:15.5px;color:#6B6470;margin-top:3px">{a[2]}</div></div></div>')
        if name == "LIST":
            return li(a[0].split("~"))
        if name == "FEAT":
            return f'<div class="f">{ico(a[0], 24, r=7)}<div><b>{a[1]}</b><span>{a[2]}</span></div></div>'
        if name == "BEN":
            return f'<div class="b"><h3>{ico(a[0], 20, r=6)}{a[1]}</h3><p>{a[2]}</p></div>'
        raise ValueError(f"Unknown macro {name}")
    out = re.sub(r"%%([A-Z_]+(?::[^%]*)?)%%", m, s)
    assert "%%" not in out, "unexpanded macro"
    return out

def chrome(*args):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-pdf-header-footer",
                    "--virtual-time-budget=10000", *args], check=True, capture_output=True)

DOCS = [  # template, output name, page width, page height, preview pages
    ("pitch-deck.tpl.html", "HRConnect-AI-Sales-Pitch-Deck", 1280, 720, 13),
    ("one-pager.tpl.html", "HRConnect-AI-Product-One-Pager", 794, 1123, 1),
]
NO_SCREEN = "<style>.slide,.page{margin:0!important;box-shadow:none!important}body{background:#fff!important}</style>"

def main():
    os.makedirs(os.path.join(OUT, "previews"), exist_ok=True)
    tmp = tempfile.mkdtemp()
    try:
        for tpl, name, w, h, pages in DOCS:
            html = expand(open(os.path.join(SRC, tpl), encoding="utf-8").read())
            html_path = os.path.join(OUT, tpl.replace(".tpl", ""))
            open(html_path, "w", encoding="utf-8").write(html)
            chrome(f"--print-to-pdf={os.path.join(OUT, name + '.pdf')}", "file://" + html_path)
            # one preview image per page
            sel = ".slide" if pages > 1 else ".page"
            for i in range(1, pages + 1):
                only = f"<style>{sel}{{display:none!important}}{sel}:nth-of-type({i}){{display:block!important}}</style>" if pages > 1 else ""
                p = os.path.join(tmp, f"{name}-{i}.html")
                open(p, "w", encoding="utf-8").write(html.replace("</head>", NO_SCREEN + only + "</head>"))
                png = os.path.join(tmp, f"{name}-{i}.png")
                chrome(f"--window-size={w},{h}", f"--screenshot={png}", "file://" + p)
                # JPEG previews keep the downloads page light (sips ships with macOS)
                subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", "-Z", str(max(w, h)), png,
                                "--out", os.path.join(OUT, "previews", f"{name}-{i}.jpg")], check=True, capture_output=True)
            print(f"{name}: pdf + {pages} preview(s)")
    finally:
        shutil.rmtree(tmp)

if __name__ == "__main__":
    main()

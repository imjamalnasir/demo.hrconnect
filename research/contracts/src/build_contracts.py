"""Build the HRConnect.AI sample contracts and their download page.

Reads the contract text from contracts.py and, for each contract, writes:
  research/contracts/<file>.html   print layout (A4)
  research/contracts/<file>.pdf    printed with headless Chrome
  research/contracts/<file>.docx   editable Word file (python-docx)
  research/contracts/previews/<file>-1.jpg   first page, rendered from the PDF with sips
Then writes research/contracts.html, the internal page that lists them.

Run from anywhere:  python3 research/contracts/src/build_contracts.py
Needs Google Chrome on a Mac and python-docx (pip3 install python-docx).
"""
import html, os, re, subprocess, sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SRC)
RESEARCH = os.path.dirname(OUT)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
sys.path.insert(0, SRC)
from contracts import CONTRACTS, GROUPS  # noqa: E402

def segments(text):
    """Split text into (is_placeholder, part). Handles nested brackets: the outermost [...] is one placeholder."""
    out, buf, depth = [], "", 0
    for ch in text:
        if ch == "[" and depth == 0:
            if buf:
                out.append((False, buf))
            buf = ""
        depth += ch == "["
        buf += ch
        if ch == "]" and depth:
            depth -= 1
            if depth == 0:
                out.append((True, buf))
                buf = ""
    if buf:
        out.append((depth > 0, buf))
    return out
KIND = {"client": "Client contract", "people": "Employee and contractor contract"}
SAMPLE_NOTE = ("Sample template. Replace everything in [brackets], delete what doesn't apply, and have it "
               "reviewed by a qualified lawyer in your jurisdiction before use. It is not legal advice.")


def logo(size):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 32 32"><rect width="32" height="32" rx="9" fill="#6C3845"/>'
            f'<circle cx="12.5" cy="16" r="6" fill="none" stroke="#fff" stroke-width="2.6"/>'
            f'<circle cx="19.5" cy="16" r="6" fill="none" stroke="#D9C8CC" stroke-width="2.6"/></svg>')


def chrome(*args):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-pdf-header-footer",
                    "--virtual-time-budget=10000", *args], check=True, capture_output=True)


def split_items(items, numbered, n):
    """Yield (kind, number, payload) for each item in a clause."""
    count = sum(1 for it in items if isinstance(it, str) and not it.startswith(("- ", "> ")))
    k = 0
    for it in items:
        if isinstance(it, dict):
            yield ("kv", None, it["kv"]) if "kv" in it else ("table", None, it["table"])
        elif it.startswith("- "):
            yield "bullet", None, it[2:]
        elif it.startswith("> ") or not numbered:
            yield "p", None, it[2:] if it.startswith("> ") else it
        else:
            k += 1
            yield "p", (f"{n}.{k}" if count > 1 else None), it


# ------------------------------------------------------------------ HTML / PDF

def h(text):
    out = []
    for is_ph, part in segments(text):
        out.append(f'<span class="ph">{html.escape(part)}</span>' if is_ph else html.escape(part))
    return "".join(out).replace("\n", "<br>")


def h_table(rows, kv):
    if kv:
        body = "".join(f"<tr><th>{h(a)}</th><td>{h(b)}</td></tr>" for a, b in rows)
        return f'<table class="kv">{body}</table>'
    head = "".join(f"<th>{h(c)}</th>" for c in rows[0])
    body = "".join("<tr>" + "".join(f"<td>{h(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f'<table class="grid"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def h_items(items, numbered, n):
    out = []
    for kind, num, payload in split_items(items, numbered, n):
        if kind in ("kv", "table"):
            out.append(h_table(payload, kind == "kv"))
        elif kind == "bullet":
            out.append(f'<p class="bul">{h(payload)}</p>')
        elif num:
            out.append(f'<p class="num"><span class="n">{num}</span>{h(payload)}</p>')
        else:
            out.append(f'<p class="{"plain" if numbered else "body"}">{h(payload)}</p>')
    return "".join(out)


def sig_lines(label):
    """Heading and lines for one signature box. Individuals don't sign with a job title."""
    if label == "Candidate acceptance":
        return "Candidate acceptance", ["Signature", "Name", "Date"]
    if label == "Employee":
        return "Signed by the employee", ["Signature", "Name", "Date"]
    return f"Signed for and on behalf of the {label}" if label in ("Company", "Customer", "Contractor") else f"Signed for and on behalf of {label}", ["Signature", "Name", "Title", "Date"]


def h_signatures(c):
    letter = c.get("letter")
    cells = []
    for label in c["signatures"]:
        lead, rows = sig_lines(label)
        note = f'<p class="signote">{h(c["signature_note"])}</p>' if label == "Candidate acceptance" and c.get("signature_note") else ""
        cells.append(f'<div class="sig"><div class="sig-h">{lead}</div>{note}' +
                     "".join(f'<div class="line"><span>{r}</span></div>' for r in rows) + "</div>")
    title = "" if letter else "<h2 class=\"sigt\">Signatures</h2>"
    return f'<section class="sigs">{title}<div class="sig-grid">{"".join(cells)}</div></section>'


CSS = """
@page{size:A4;margin:18mm 18mm 20mm;
  @bottom-left{content:"HRConnect.AI \\00b7  %TITLE% \\00b7  Sample template";font:8pt Inter,system-ui,sans-serif;color:#8A8290}
  @bottom-right{content:"Page " counter(page) " of " counter(pages);font:8pt Inter,system-ui,sans-serif;color:#8A8290}}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#2E2833;font-size:9.6pt;line-height:1.55;-webkit-font-smoothing:antialiased;-webkit-print-color-adjust:exact;print-color-adjust:exact}
@media screen{body{background:#EDE7EA}.doc{width:210mm;margin:24px auto;background:#fff;padding:18mm;box-shadow:0 10px 30px rgba(0,0,0,.12)}}
.top{display:flex;align-items:center;justify-content:space-between;padding-bottom:4mm;border-bottom:1.5px solid #6C3845}
.brand{display:flex;align-items:center;gap:7px;font-weight:700;font-size:11pt;color:#1B1620;letter-spacing:-.01em}
.brand .ai{color:#6C3845}
.kind{font-size:7.5pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#6C3845}
h1{margin:7mm 0 2mm;font-size:22pt;line-height:1.1;letter-spacing:-.025em;color:#1B1620}
.purpose{margin:0 0 4mm;color:#6B6470;font-size:10pt}
.note{background:#F6EEF0;border-left:3px solid #6C3845;border-radius:4px;padding:2.6mm 3.6mm;font-size:8.4pt;color:#4A2530;margin-bottom:6mm}
.parties p{margin:0 0 2.2mm}
h2{font-size:11pt;color:#1B1620;margin:6mm 0 2mm;letter-spacing:-.01em;break-after:avoid}
h2 .hn{color:#6C3845;display:inline-block;min-width:9mm}
p{margin:0 0 2mm}
p.num{padding-left:9mm;text-indent:-9mm}
p.num .n{display:inline-block;width:9mm;text-indent:0;color:#6C3845;font-weight:600}
p.plain,p.bul,table{margin-left:9mm}
p.bul{padding-left:4mm;text-indent:-4mm;margin-left:13mm}
p.bul::before{content:"\\2022";display:inline-block;width:4mm;text-indent:0;color:#6C3845}
.flat p.plain,.flat table{margin-left:0;width:100%}
.letter h2{margin-top:5mm}
.letter p.body,.letter p.bul{margin-left:0}
.letter p.bul{margin-left:4mm}
.letter table{margin-left:0;width:100%}
.letter .parties p{margin-bottom:4mm}
table{border-collapse:collapse;width:calc(100% - 9mm);margin-bottom:3mm;font-size:8.8pt;break-inside:auto}
tr{break-inside:avoid}
th,td{text-align:left;vertical-align:top;padding:1.6mm 2.4mm;border:1px solid #E2D7DB}
table.kv th{width:34%;background:#FBF8F9;font-weight:600;color:#1B1620}
table.grid thead th{background:#6C3845;color:#fff;font-weight:600;border-color:#6C3845}
.ph{background:#F6E3E8;color:#6C3845;border-radius:2px;padding:0 1px;font-weight:500}
thead .ph{background:rgba(255,255,255,.2);color:#fff}
.sigs{break-inside:avoid;margin-top:8mm}
.sigt{margin-bottom:4mm}
.sig-grid{display:grid;grid-template-columns:1fr 1fr;gap:10mm}
.sig-h{font-weight:700;color:#1B1620;margin-bottom:1mm}
.signote{font-size:8.8pt;color:#6B6470}
.line{border-bottom:1px solid #B9AEB3;height:10mm;display:flex;align-items:flex-end;padding-bottom:1mm}
.line span{font-size:7.8pt;color:#8A8290;text-transform:uppercase;letter-spacing:.08em}
.schedule{break-before:page}
.schedule h2{font-size:13pt;margin-top:0}
.schedule + .schedule{break-before:auto;margin-top:10mm}
.schedule table{margin-left:0;width:100%}
.schedule p.bul{margin-left:4mm}
"""


def build_html(c):
    numbered = c.get("numbered", True)
    parts = []
    for i, (head, items) in enumerate(c["clauses"], 1):
        hn = f'<span class="hn">{i}.</span>' if numbered else ""
        parts.append(f"<h2>{hn}{h(head)}</h2>{h_items(items, numbered, i)}")
    sched = "".join(f'<section class="schedule"><h2>{h(head)}</h2>{h_items(items, False, 0)}</section>'
                    for head, items in c.get("schedules", []))
    parties = "".join(f"<p>{h(p)}</p>" for p in c["parties"])
    css = CSS.replace("%TITLE%", c["title"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">
<title>{html.escape(c['title'])} · HRConnect.AI sample</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body><div class="doc{' letter' if c.get('letter') else ''}{'' if numbered else ' flat'}">
<div class="top"><div class="brand">{logo(20)}<span>HRConnect<span class="ai">.AI</span></span></div><div class="kind">{KIND[c['group']]} · sample</div></div>
<h1>{html.escape(c['title'])}</h1>
<p class="purpose">{html.escape(c['purpose'])}</p>
<div class="note">{h(SAMPLE_NOTE)}</div>
<section class="parties">{parties}</section>
{''.join(parts)}
{h_signatures(c)}
{sched}
</div></body></html>"""


def pdf_pages(path):
    return len(re.findall(rb"/Type\s*/Page(?![s\w])", open(path, "rb").read()))


# ------------------------------------------------------------------ DOCX

BRAND = RGBColor(0x6C, 0x38, 0x45)
INK = RGBColor(0x1B, 0x16, 0x20)
MUTED = RGBColor(0x6B, 0x64, 0x70)


def shade(el, fill):
    pr = el.get_or_add_rPr() if hasattr(el, "get_or_add_rPr") else el.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pr.append(shd)


def runs(par, text, bold=False, color=None, size=None):
    for i, line in enumerate(text.split("\n")):
        if i:
            par.add_run().add_break(WD_BREAK.LINE)
        for is_ph, part in segments(line):
            r = par.add_run(part)
            r.bold = bold
            if size:
                r.font.size = Pt(size)
            if is_ph:
                shade(r._r, "F6E3E8")
                r.font.color.rgb = BRAND
            elif color:
                r.font.color.rgb = color


def spacing(par, after=4, before=0):
    par.paragraph_format.space_after = Pt(after)
    par.paragraph_format.space_before = Pt(before)


def d_table(doc, rows, kv, indent):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = t.cell(ri, ci)
            p = cell.paragraphs[0]
            spacing(p, 0)
            head = (kv and ci == 0) or (not kv and ri == 0)
            runs(p, val, bold=head, size=9, color=RGBColor(0xFF, 0xFF, 0xFF) if (head and not kv) else INK)
            if head:
                shade(cell._tc, "FBF8F9" if kv else "6C3845")
    if kv:
        for r in t.rows:
            r.cells[0].width, r.cells[1].width = Cm(5), Cm(11.5 - indent)
    if indent:
        tblPr = t._tbl.tblPr
        ind = OxmlElement("w:tblInd")
        ind.set(qn("w:w"), str(int(indent * 567)))
        ind.set(qn("w:type"), "dxa")
        tblPr.append(ind)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def d_items(doc, items, numbered, n, letter):
    ind = 0 if letter else 1.0
    for kind, num, payload in split_items(items, numbered, n):
        if kind in ("kv", "table"):
            d_table(doc, payload, kind == "kv", ind)
            continue
        p = doc.add_paragraph()
        spacing(p, 4)
        f = p.paragraph_format
        if kind == "bullet":
            f.left_indent, f.first_line_indent = Cm(ind + 0.6), Cm(-0.5)
            runs(p, "•\t", color=BRAND)
            f.tab_stops.add_tab_stop(Cm(ind + 0.6))
            runs(p, payload)
        elif num:
            f.left_indent, f.first_line_indent = Cm(1.0), Cm(-1.0)
            f.tab_stops.add_tab_stop(Cm(1.0))
            runs(p, num + "\t", bold=True, color=BRAND)
            runs(p, payload)
        else:
            f.left_indent = Cm(ind)
            runs(p, payload)


def add_page_field(par):
    for code in ("PAGE",):
        r = par.add_run()
        for tag, extra in (("w:fldChar", "begin"), ("w:instrText", code), ("w:fldChar", "end")):
            el = OxmlElement(tag)
            if tag == "w:fldChar":
                el.set(qn("w:fldCharType"), extra)
            else:
                el.set(qn("xml:space"), "preserve")
                el.text = extra
            r._r.append(el)


def build_docx(c, path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2)
    sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    st.font.size = Pt(10)
    st.font.color.rgb = INK
    for name in ("Heading 1", "Heading 2"):
        hs = doc.styles[name]
        hs.font.name, hs.font.color.rgb = "Arial", INK
        fonts = hs.element.rPr.rFonts  # drop theme fonts so Arial wins
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            fonts.attrib.pop(qn(a), None)
    doc.styles["Heading 1"].font.size = Pt(20)
    doc.styles["Heading 2"].font.size = Pt(11.5)

    fp = sec.footer.paragraphs[0]
    runs(fp, f"HRConnect.AI · {c['title']} · Sample template · Page ", color=MUTED, size=8)
    add_page_field(fp)

    p = doc.add_paragraph()
    runs(p, f"HRConnect.AI  ·  {KIND[c['group']].upper()} · SAMPLE", bold=True, color=BRAND, size=8)
    doc.add_heading(c["title"], level=1)
    p = doc.add_paragraph()
    runs(p, c["purpose"], color=MUTED)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "F6EEF0")
    pPr.append(shd)
    runs(p, SAMPLE_NOTE, size=8.5)
    spacing(p, 10)

    for text in c["parties"]:
        p = doc.add_paragraph()
        spacing(p, 8 if c.get("letter") else 5)
        runs(p, text)

    numbered = c.get("numbered", True)
    for i, (head, items) in enumerate(c["clauses"], 1):
        hd = doc.add_heading(f"{i}.  {head}" if numbered else head, level=2)
        spacing(hd, 3, 10)
        d_items(doc, items, numbered, i, c.get("letter"))

    # signatures
    if not c.get("letter"):
        spacing(doc.add_heading("Signatures", level=2), 6, 14)
    labels = c["signatures"]
    t = doc.add_table(rows=1, cols=len(labels))
    for ci, label in enumerate(labels):
        cell = t.cell(0, ci)
        lead, lines = sig_lines(label)
        p = cell.paragraphs[0]
        runs(p, lead, bold=True)
        if label == "Candidate acceptance" and c.get("signature_note"):
            runs(cell.add_paragraph(), c["signature_note"], color=MUTED, size=9)
        for r in lines:
            q = cell.add_paragraph()
            spacing(q, 2, 14)
            runs(q, f"{r}: ________________________________", color=MUTED, size=9)

    for head, items in c.get("schedules", []):
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        doc.add_heading(head, level=2)
        d_items(doc, items, False, 0, False)

    doc.core_properties.title = c["title"]
    doc.core_properties.author = "HRConnect.AI"
    doc.save(path)


# ------------------------------------------------------------------ page

ICON_DL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>'


def kb(path):
    n = os.path.getsize(path)
    return f"{n / 1024:.0f} KB" if n < 1048576 else f"{n / 1048576:.1f} MB"


def build_page(info):
    sections = []
    for key, name, blurb in GROUPS:
        cards = []
        for c, pages in info:
            if c["group"] != key:
                continue
            f = c["file"]
            cards.append(f"""
    <article class="card">
      <button class="thumb" type="button" data-file="{f}" data-title="{html.escape(c['title'])}" data-pages="{pages}" aria-label="Enlarge the first page of the {html.escape(c['title'])}"><img src="contracts/previews/{f}-1.jpg" width="595" height="842" alt="" loading="lazy"></button>
      <div class="body">
        <span class="tag">{html.escape(c['short'])}</span>
        <h3>{html.escape(c['title'])}</h3>
        <p>{html.escape(c['purpose'])}</p>
        <div class="meta"><span>{pages} page{'s' if pages != 1 else ''}</span><span>PDF · {kb(os.path.join(OUT, f + '.pdf'))}</span><span>DOCX · {kb(os.path.join(OUT, f + '.docx'))}</span></div>
        <div class="actions">
          <a class="btn primary" href="contracts/{f}.pdf" download>{ICON_DL}PDF</a>
          <a class="btn" href="contracts/{f}.docx" download>{ICON_DL}Word</a>
          <a class="btn ghost" href="contracts/{f}.pdf" target="_blank" rel="noopener">Open</a>
        </div>
      </div>
    </article>""")
        sections.append(f"""
  <section class="group" aria-labelledby="g-{key}">
    <div class="ghead"><h2 id="g-{key}">{name}</h2><p>{blurb}</p></div>
    <div class="cards">{''.join(cards)}
    </div>
  </section>""")
    tpl = open(os.path.join(SRC, "page.tpl.html"), encoding="utf-8").read()
    out = tpl.replace("%%SECTIONS%%", "".join(sections)).replace("%%COUNT%%", str(len(info)))
    open(os.path.join(RESEARCH, "contracts.html"), "w", encoding="utf-8").write(out)


def main():
    os.makedirs(os.path.join(OUT, "previews"), exist_ok=True)
    info = []
    for c in CONTRACTS:
        f = c["file"]
        html_path = os.path.join(OUT, f + ".html")
        open(html_path, "w", encoding="utf-8").write(build_html(c))
        pdf = os.path.join(OUT, f + ".pdf")
        chrome(f"--print-to-pdf={pdf}", "file://" + html_path)
        build_docx(c, os.path.join(OUT, f + ".docx"))
        # sips renders the PDF's first page as vectors, so the preview matches the print exactly
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", "-Z", "1190", pdf,
                        "--out", os.path.join(OUT, "previews", f + "-1.jpg")], check=True, capture_output=True)
        pages = pdf_pages(pdf)
        info.append((c, pages))
        print(f"{f}: {pages} page(s), pdf + docx + preview")
    build_page(info)
    print("research/contracts.html written")


if __name__ == "__main__":
    main()

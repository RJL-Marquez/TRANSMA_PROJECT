import sys

import docx
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding="utf-8")
d = docx.Document(sys.argv[1])
body = d.element.body
ti = 0
for el in body.iterchildren():
    tag = el.tag.split("}")[1]
    if tag == "p":
        p = docx.text.paragraph.Paragraph(el, d._body)
        text = p.text.strip()
        imgs = len(el.findall(".//" + qn("w:drawing")))
        red = any(r.font.color is not None and r.font.color.rgb is not None and str(r.font.color.rgb) in ("FF0000", "E06666", "CC0000") for r in p.runs if r.text.strip())
        if text or imgs:
            print(f"{'[RED] ' if red else ''}{'[IMG x%d] ' % imgs if imgs else ''}{p.style.name}: {text[:400]}")
    elif tag == "tbl":
        t = docx.table.Table(el, d._body)
        print(f"--- TABLE {ti} ({len(t.rows)} rows)")
        for r in t.rows:
            seen, vals = [], []
            for c in r.cells:
                if c._tc not in seen:
                    seen.append(c._tc)
                    vals.append(c.text.strip().replace("\n", " / ")[:80])
            print("   | " + " | ".join(vals))
        ti += 1

import sys, docx
sys.stdout.reconfigure(encoding="utf-8")
from docx.oxml.ns import qn
d = docx.Document(sys.argv[1])
M = '{http://schemas.openxmlformats.org/officeDocument/2006/math}t'
def ct(c):
    return ''.join((e.text or '') for e in c._tc.iter() if e.tag in (qn('w:t'), M))
print('tables', len(d.tables), 'paras', len(d.paragraphs), 'inline', len(d.inline_shapes))
for i, t in enumerate(d.tables):
    print('T', i, 'rows', len(t.rows), 'cols', len(t.columns))
    if i >= 3:
        for r in list(t.rows)[:7]:
            seen=[]; out=[]
            for c in r.cells:
                if c._tc in seen: continue
                seen.append(c._tc); out.append(ct(c)[:34])
            print('   ', out)
s = d.sections[0]
print('page', s.page_width.inches, s.page_height.inches, 'margins', s.left_margin.inches, s.right_margin.inches)
for i,p in enumerate(d.paragraphs):
    if p.style.name.startswith('Heading') and p.text.strip(): print(i,p.style.name,p.text)

import os
import re
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(HERE, "opt_pages")
os.makedirs(out, exist_ok=True)
checks = {
    "a": dict(must=["Frassati", "6.6614", "60.0400", "40.0700", "129.4161", "107.0531", "10.6473", "-97.7978", "108.4452", "135.3630", "ERZ-LNA-0800-1220-26-2", "FMAD1245", "OPTION A"],
              never=["Pacific Icon", "Narda", "BGPOP", "Buenaventura", "LNA-30", "69.7863"]),
    "b": dict(must=["BGPOP", "6.6877", "69.7863", "37.6263", "49.8163", "129.4504", "107.3982", "10.9581", "-98.4978", "109.4560", "140.0522", "LNA-30-08001200-15-15P", "FMAD1245", "OPTION B"],
              never=["ERZ-LNA", "11.3781", "109.8760", "139.6322", "107.8182"]),
}
for tag, c in checks.items():
    doc = pymupdf.open(os.path.join(HERE, f"option_{tag}.pdf"))
    pages = [p.get_text() for p in doc]
    text = "\n".join(pages)
    flat = re.sub(r"\s+", " ", text)
    print(tag, "pages", doc.page_count)
    print(" missing:", [m for m in c["must"] if m not in flat])
    print(" stale:", [m for m in c["never"] if m in flat])
    want = {}
    for label, pat in (("map", "Figure 1\\."), ("profile", "Figure 2\\."), ("table5", "Fairview FMWCA1025"), ("rsl", "Received signal level"), ("notes", "DRAFT NOTES")):
        for i, t in enumerate(pages):
            if i > 3 and re.search(pat, t):
                want[label] = i
                break
    print(" pages:", {k: v + 1 for k, v in want.items()})
    if tag == "a":
        for label, i in want.items():
            doc[i].get_pixmap(dpi=62).save(os.path.join(out, f"a_{label}.png"))
    else:
        doc[want["table5"]].get_pixmap(dpi=62).save(os.path.join(out, "b_table5.png"))

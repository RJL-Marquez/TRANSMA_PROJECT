import os
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for tag, src in zip(("a", "b"), sys.argv[2:]):
    doc = pymupdf.open(src)
    print(f"=== {tag} pages {doc.page_count}")
    print(doc[0].get_text()[:1500])
    doc[0].get_pixmap(dpi=110).save(os.path.join(out, f"adapter_{tag}.png"))

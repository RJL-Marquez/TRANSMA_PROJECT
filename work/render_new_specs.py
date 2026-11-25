import os
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
out = sys.argv[1]
for name, src in (("lna_ERZ-LNA-0800-1220-26-2_p1.png", sys.argv[2]), ("adapter_FMAD1245_p1.png", sys.argv[3])):
    doc = pymupdf.open(src)
    doc[0].get_pixmap(dpi=130).save(os.path.join(out, name))
    print("===", name, doc.page_count)
    if "FMAD" in name:
        print(" ".join(doc[0].get_text().split())[:1500])

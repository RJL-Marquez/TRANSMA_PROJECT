import os
import sys

import fitz

sys.stdout.reconfigure(encoding="utf-8")
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
doc = fitz.open(src)
print("pages", doc.page_count)
for i, page in enumerate(doc):
    print(f"--- page {i + 1} ---")
    print(page.get_text()[:3500])
    if i < 3:
        page.get_pixmap(dpi=120).save(os.path.join(out, f"erzia_{i + 1}.png"))

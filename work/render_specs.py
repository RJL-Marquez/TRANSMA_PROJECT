import os
import sys
import pymupdf

src = r"C:\Users\Lenovo\.claude\projects\C--UST-TRANSMA-PROJECT\84d6406d-f149-4c45-afef-396d97e96f97\tool-results"
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
files = {
    "antenna_VHLP6-11W-A": "webfetch-1795456668795-o22iiv.pdf",
    "lna_LNA-40-08001200-30-20P": "webfetch-1795456631863-rdvner.pdf",
    "adapter_FMWCA1107": "webfetch-1795456630151-8y4all.pdf",
    "adapter_FMWCA1025": "webfetch-1795456630243-gmi7uc.pdf",
}
for name, fn in files.items():
    doc = pymupdf.open(os.path.join(src, fn))
    print(name, "pages", doc.page_count)
    for i in range(min(doc.page_count, 2)):
        pix = doc[i].get_pixmap(dpi=120)
        pix.save(os.path.join(out, f"{name}_p{i+1}.png"))
    if name.startswith("antenna"):
        for i in range(min(doc.page_count, 3)):
            pass

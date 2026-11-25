"""Overlay the simulated azimuth pattern on the Option A map at both sites."""
import csv
import math
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "matlab")
SHOT = r"C:\Users\Lenovo\.claude\projects\C--UST-TRANSMA-PROJECT\84d6406d-f149-4c45-afef-396d97e96f97\tool-results\mcp-Claude_Browser-blob-1795468641453-mx4aj1.jpg"
CROP = (170, 110, 640, 665)
SITE_A = (415 - CROP[0], 508 - CROP[1])   # Frassati, measured from the pin cluster spacing
SITE_B = (388 - CROP[0], 217 - CROP[1])   # Fini Homes
RANGE_DB = 60.0
RADIUS = 105.0

log = open(os.path.join(MD, "sim_antenna.log"), encoding="utf-8", errors="replace").read()
m = re.search(r"Dmax = ([\d.]+) dBi at az = ([-\d.]+) deg, el = ([-\d.]+) deg", log)
dmax, az_peak = float(m.group(1)), float(m.group(2))
rows = [tuple(map(float, r)) for r in csv.reader(open(os.path.join(MD, "azimuth_cut.csv")))]

img = Image.open(SHOT).convert("RGB").crop(CROP)
w, h = img.size
fig, ax = plt.subplots(figsize=(w / 100, h / 100), dpi=250)
ax.imshow(img)
ax.set_xlim(0, w)
ax.set_ylim(h, 0)
ax.axis("off")


def draw(site, toward, color, label):
    dx, dy = toward[0] - site[0], toward[1] - site[1]
    theta0 = math.atan2(-dy, dx)
    xs, ys = [], []
    for az, d in rows:
        r = RADIUS * max(0.0, (d - (dmax - RANGE_DB)) / RANGE_DB)
        th = theta0 + math.radians(az - az_peak)
        xs.append(site[0] + r * math.cos(th))
        ys.append(site[1] - r * math.sin(th))
    ax.fill(xs, ys, color=color, alpha=0.35, lw=0)
    ax.plot(xs, ys, color=color, lw=0.9, label=label)
    for k in (0.25, 0.5, 0.75, 1.0):
        ax.add_patch(plt.Circle(site, RADIUS * k, fill=False, color="white", lw=0.3, alpha=0.6, ls=":"))


ax.plot([SITE_A[0], SITE_B[0]], [SITE_A[1], SITE_B[1]], color="white", lw=0.9, ls="--")
draw(SITE_A, SITE_B, "#ff3b30", "Site A (Frassati) azimuth pattern")
draw(SITE_B, SITE_A, "#ffd60a", "Site B (Fini Homes) azimuth pattern")
mx, my = (SITE_A[0] + SITE_B[0]) / 2, (SITE_A[1] + SITE_B[1]) / 2
ax.text(mx + 14, my, "D = 6,661.37 m", color="white", fontsize=6.5, fontweight="bold",
        bbox=dict(facecolor="black", alpha=0.6, pad=1.5, lw=0))
ax.legend(loc="lower left", fontsize=4.8, framealpha=0.75)
ax.text(w - 4, h - 6, f"Pattern radius: {RANGE_DB:.0f} dB below the {dmax:.2f} dBi peak", color="white",
        fontsize=4.5, ha="right", bbox=dict(facecolor="black", alpha=0.6, pad=1, lw=0))
fig.subplots_adjust(0, 0, 1, 1)
out = os.path.join(HERE, "map_overlay_A.png")
fig.savefig(out)
print("saved", out, "peak", dmax, az_peak)

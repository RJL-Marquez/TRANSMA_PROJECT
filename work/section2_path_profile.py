"""Section 2 path profile drawing: UST Frassati (Site A) to Metro Industries, Valenzuela (Site B).

Self-contained: only needs matplotlib (pip install matplotlib). Every value is computed here from the
raw inputs below (distance from Site A, ground elevation, floors), with the same formulas as the report:

    h_elevation   = ground + floors * 2.5
    h_earth bulge = d1 * d2 / (12.75 k), k = 4/3      (d in km, answer in m)
    F1            = 17.3 * sqrt(d1 * d2 / (f * D))    (f in GHz, d in km, answer in m)
    THE           = h_elevation + h_earth bulge + 0.6 F1

Tilted mounting with a safety margin kept above every THE:
    hA = THE(P1) + margin
    hB = max over points of  hA - (hA - (THE + margin)) * D / d1
    tower = antenna height - h_elevation of the site

Run:  python section2_path_profile.py [output.png]
"""
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------- inputs -----------------------------
F_GHZ = 10.59625          # operating frequency
D_KM = 6.927011124        # Site A to Site B straight-line distance
FLOOR = 2.5               # metres per floor
K_FACTOR = 4 / 3          # effective earth radius factor (standard atmosphere)
MARGIN = 2.5              # extra clearance kept above every THE (one floor), added to both antennas

# point, d1 (km), ground elevation (m), floors, what is there
POINTS = [
    (1, 0.0000, 2.47, 23, "Frassati Building (Site A)"),
    (2, 0.3556, 2.55, 6, "mid-rise block"),
    (3, 0.7472, 2.74, 3, "low-rise residential"),
    (4, 1.0837, 3.55, 3, "commercial building"),
    (5, 1.4833, 3.52, 3, "low-rise residential"),
    (6, 1.8029, 4.79, 3, "low-rise block"),
    (7, 2.1995, 6.68, 2, "beside A. Bonifacio Ave"),
    (8, 2.5381, 10.78, 0, "La Loma Cemetery"),
    (9, 2.9376, 14.70, 1, "cemetery mausoleum"),
    (10, 3.2542, 13.48, 3, "row house"),
    (11, 3.6158, 15.69, 2, "houses, cemetery edge"),
    (12, 4.0174, 17.33, 3, "block south of warehouses"),
    (13, 4.3600, 18.17, 3, "warehouse, Caloocan City Hall"),
    (14, 4.7645, 17.59, 4, "near CAI Sports Center"),
    (15, 5.0921, 18.15, 3, "street-front buildings"),
    (16, 5.4777, 19.63, 3, "row houses, MCU Hospital"),
    (17, 5.8253, 20.48, 4, "white mid-rise north of EDSA"),
    (18, 6.1729, 11.63, 3, "gated subdivision house"),
    (19, 6.5424, 3.63, 2, "south of Tullahan River"),
    (20, D_KM, 10.98, 6, "Metro Industries (Site B), 5 storeys + rooftop structure"),
]
# near-line structures checked in addition to the 20 points: tag, d1 (km), ground (m), floors, name
STRUCTURES = [
    ("M", 1.6670, 4.35, 9, "Maranatha/PMCC tower"),
    ("L", 5.3531, 19.31, 5, "LRT-1 viaduct on EDSA"),
]


# --------------------------- computation --------------------------
def profile(d1, ground, floors):
    d2 = max(D_KM - d1, 0.0)
    elev = ground + floors * FLOOR
    bulge = d1 * d2 / (12.75 * K_FACTOR)
    f1 = 17.3 * math.sqrt(d1 * d2 / (F_GHZ * D_KM))
    return dict(d1=d1, d2=d2, ground=ground, floors=floors, elev=elev, bulge=bulge, f60=0.6 * f1, the=elev + bulge + 0.6 * f1)


pts = [dict(profile(d1, g, fl), n=n, desc=desc) for n, d1, g, fl, desc in POINTS]
structs = [dict(profile(d1, g, fl), tag=t, desc=desc) for t, d1, g, fl, desc in STRUCTURES]

hA = pts[0]["the"] + MARGIN
checks = [(q.get("n") and f"P{q['n']}" or q["tag"], q) for q in pts[1:-1] + structs]
need = [(hA - (hA - (q["the"] + MARGIN)) * D_KM / q["d1"], name) for name, q in checks]
hB, governs = max(need)
hB = max(hB, pts[-1]["the"] + MARGIN)
tower_a, tower_b = hA - pts[0]["elev"], hB - pts[-1]["elev"]
tilt = math.degrees(math.atan((hA - hB) / (D_KM * 1000)))
los = lambda d1: hA - (hA - hB) * d1 / D_KM
clear = {name: los(q["d1"]) - q["the"] for name, q in checks}
assert min(clear.values()) > MARGIN - 1e-9

print(f"Site A antenna {hA:.4f} m (tower {tower_a:.4f} m), Site B antenna {hB:.4f} m (tower {tower_b:.4f} m)")
print(f"tilt {tilt:.4f} deg, set by {governs}; clearance above THE: P17 {clear['P17']:.4f} m, LRT viaduct {clear['L']:.4f} m")

# ------------------------------ drawing ---------------------------
GROUND, BLDG, BLDG_EDGE = "#c9bca3", "#dfe3e8", "#7c8591"
C_ELEV, C_BULGE, C_THE, C_LOS = "#7b2d8e", "#1f7a4d", "#1677c8", "#c62828"
C_STRUCT, C_STRUCT_EDGE, C_STRUCT_THE = "#f2c94c", "#9a7b0a", "#e67e22"

x = [p["d1"] for p in pts]
elev = [p["elev"] for p in pts]
bulge = [p["elev"] + p["bulge"] for p in pts]
the = [p["the"] for p in pts]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#555", "axes.linewidth": 0.8})
fig, ax = plt.subplots(figsize=(12, 7.2), dpi=200)


def draw_profile(a, small=False):
    """Everything except labels, so the main plot and the zoomed inset match."""
    ms = 4.5 if small else 3.4
    a.fill_between(x, 0, [p["ground"] for p in pts], color=GROUND, alpha=0.85, lw=0, zorder=1)
    a.plot(x, [p["ground"] for p in pts], color="#9c8d72", lw=0.8, zorder=1)
    for p in pts:
        if p["floors"]:
            a.bar(p["d1"], p["floors"] * FLOOR, bottom=p["ground"], width=0.075, color=BLDG, edgecolor=BLDG_EDGE, lw=0.6, zorder=2)
    for s in structs:
        a.bar(s["d1"], s["floors"] * FLOOR, bottom=s["ground"], width=0.06, color=C_STRUCT, edgecolor=C_STRUCT_EDGE, lw=0.6, zorder=3)
        a.plot(s["d1"], s["the"], marker="^", color=C_STRUCT_THE, ms=ms + 3, mec="white", mew=0.6, zorder=7)
    a.fill_between(x, the, [los(v) for v in x], color=C_LOS, alpha=0.06, lw=0, zorder=2)
    a.plot(x, elev, color=C_ELEV, marker="o", ms=ms - 0.4, lw=1.1, zorder=4)
    a.plot(x, bulge, color=C_BULGE, marker="o", ms=ms - 0.4, lw=1.1, zorder=5)
    a.plot(x, the, color=C_THE, marker="o", ms=ms, mec="white", mew=0.5, lw=1.7, zorder=6)
    a.plot([0, D_KM], [hA, hB], color=C_LOS, ls=(0, (6, 3)), lw=1.8, zorder=8)


draw_profile(ax)

# masts and antennas
for xs, base, top in ((0.0, pts[0]["elev"], hA), (D_KM, pts[-1]["elev"], hB)):
    ax.plot([xs, xs], [base, top], color="#1a1a1a", lw=3.6, solid_capstyle="butt", zorder=9)
    ax.plot(xs, top, marker="D", color=C_LOS, mec="white", mew=0.8, ms=7, zorder=10)
for s in structs:
    ax.text(s["d1"], s["ground"] + 0.8, s["tag"], ha="center", fontsize=7.5, fontweight="bold", color="#6b5300", zorder=4)

box = dict(boxstyle="round,pad=0.35", fc="white", ec="#bbbbbb", lw=0.6)
line = dict(arrowstyle="-", color="#666", lw=0.7)
ax.annotate(f"Site A: UST Frassati Building\nantenna at {hA:.4f} m\n{tower_a:.4f} m mast on the rooftop", (0, hA),
            xytext=(0.12, 96), fontsize=8, bbox=box, arrowprops=line, zorder=11, va="top")
ax.annotate(f"Site B: Metro Industries\nantenna at {hB:.4f} m\n{tower_b:.4f} m mast on the rooftop", (D_KM, hB),
            xytext=(D_KM - 0.05, 56), fontsize=8, bbox=box, arrowprops=line, ha="right", va="bottom", zorder=11)
ax.text(1.5, los(1.5) + 1.0, f"tilted line of sight, {tilt:.4f}°", rotation=math.degrees(math.atan2(hB - hA, D_KM)),
        transform_rotates_text=True, rotation_mode="anchor", color=C_LOS, fontsize=8, ha="center", va="bottom", zorder=11)

# zoomed inset around the points that set the tilt
X0, X1, Y0, Y1 = 4.85, 6.25, 27.5, 42.5
axin = ax.inset_axes([0.33, 0.63, 0.36, 0.30])
draw_profile(axin, small=True)
for name, q, col in (("P17", pts[16], C_THE), ("LRT-1 viaduct", structs[1], C_STRUCT_THE)):
    top = los(q["d1"])
    axin.annotate("", (q["d1"], q["the"]), (q["d1"], top), arrowprops=dict(arrowstyle="<|-|>", color="#222", lw=0.9, mutation_scale=7), zorder=11)
    axin.text(q["d1"] - 0.03, (q["the"] + top) / 2 - 0.3, f"{name}\n{los(q['d1']) - q['the']:.4f} m", fontsize=7, va="center", ha="right",
              bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85), zorder=12)
for p in pts:
    if X0 < p["d1"] < X1:
        axin.text(p["d1"], Y0 + 0.4, f"P{p['n']}", ha="center", va="bottom", fontsize=6.5, color="#333", zorder=12)
axin.set_xlim(X0, X1)
axin.set_ylim(Y0, Y1)
axin.tick_params(labelsize=6.5, length=2)
axin.grid(True, color="#ececec", lw=0.5, zorder=0)
axin.set_title(f"Zoom: clearance of the line of sight above THE (margin {MARGIN:g} m)", fontsize=7.5, pad=3)
axin.set_facecolor("white")
ax.indicate_inset_zoom(axin, edgecolor="#777", lw=0.7, alpha=0.9)

# axes, point numbers, legend
for p in pts:
    ax.text(p["d1"], -4.6, str(p["n"]), ha="center", va="top", fontsize=7, color="#333", clip_on=False)
ax.text(-0.18, -4.6, "Pt.", ha="right", va="top", fontsize=7, color="#333", clip_on=False)
ax.set_xlim(-0.18, D_KM + 0.18)
ax.set_ylim(0, 100)
ax.set_xlabel("Distance from Site A, d₁ (km)", labelpad=16)
ax.set_ylabel("Height above sea level (m)")
fig.suptitle("Path Profile: UST Frassati (Site A) to Metro Industries, Valenzuela (Site B)", fontweight="bold", fontsize=11.5, y=0.975)
ax.set_title(f"D = {D_KM:.4f} km   ·   f = {F_GHZ} GHz   ·   k = 4/3   ·   20 points + 2 near-line structures   ·   "
             f"{MARGIN:g} m kept above every THE", fontsize=8.5, color="#444", pad=6)
ax.grid(True, color="#ececec", lw=0.6, zorder=0)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
handles = [
    Patch(fc=GROUND, ec="#9c8d72", label="Ground elevation"),
    Patch(fc=BLDG, ec=BLDG_EDGE, label="Buildings (floors × 2.5 m)"),
    Patch(fc=C_STRUCT, ec=C_STRUCT_EDGE, label="M: Maranatha tower, L: LRT-1 viaduct"),
    Line2D([], [], color=C_ELEV, marker="o", ms=3, lw=1.1, label=r"$h_{elevation}$"),
    Line2D([], [], color=C_BULGE, marker="o", ms=3, lw=1.1, label=r"$h_{elevation}+h_{earth\ bulge}$"),
    Line2D([], [], color=C_THE, marker="o", ms=3.4, lw=1.7, label=r"THE $=h_{elevation}+h_{earth\ bulge}+0.6F_1$"),
    Line2D([], [], color=C_STRUCT_THE, marker="^", ms=6, ls="none", label="THE of near-line structures"),
    Line2D([], [], color=C_LOS, ls=(0, (6, 3)), lw=1.8, label=f"Line of sight: {hA:.4f} m to {hB:.4f} m"),
    Patch(fc=C_LOS, alpha=0.12, ec="none", label="Clearance above THE"),
    Line2D([], [], color="#1a1a1a", lw=3.6, marker="D", mfc=C_LOS, mec="white", ms=6, label="Mast and antenna"),
]
fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=7.6, frameon=False, bbox_to_anchor=(0.5, 0.005),
           columnspacing=1.6, handlelength=2.2)
fig.tight_layout(rect=(0, 0.075, 1, 0.97))

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "path_profile_M.png")
fig.savefig(out, facecolor="white")
print("saved", out)

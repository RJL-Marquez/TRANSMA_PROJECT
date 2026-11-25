import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(here, "results.json"), encoding="utf-8"))
rows = data["rows"]
hmin = data["main"]["hmin"]

x = [r["d1"] for r in rows]
ground = [r["ground"] for r in rows]
elev = [r["elev"] for r in rows]
bulge = [r["elev"] + r["bulge"] for r in rows]
the = [r["the"] for r in rows]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, ax = plt.subplots(figsize=(9.2, 4.9), dpi=200)
ax.fill_between(x, 0, ground, color="#b9ad97", alpha=0.75, label="Ground elevation", zorder=1)
for r in rows:
    if r["floors"]:
        ax.bar(r["d1"], r["obstruction"], bottom=r["ground"], width=0.075, color="#d7dbe0",
               edgecolor="#6f7782", linewidth=0.6, zorder=2)
ax.bar([0], [0], color="#d7dbe0", edgecolor="#6f7782", label="Building height (floors × 2.5 m)")
ax.plot(x, elev, color="#7b2d8e", marker="o", ms=3.2, lw=1.2, label=r"$h_{elevation}$", zorder=4)
ax.plot(x, bulge, color="#1f7a4d", marker="o", ms=3.2, lw=1.2, label=r"$h_{elevation}+h_{earth\ bulge}$", zorder=5)
ax.plot(x, the, color="#1677c8", marker="o", ms=3.2, lw=1.4, label=r"THE $=h_{elevation}+h_{earth\ bulge}+0.6F_1$", zorder=6)
ax.axhline(hmin, color="#c62828", ls="--", lw=1.3, label=f"Minimum antenna height = {hmin:.4f} m", zorder=7)
ax.plot([x[0], x[0]], [elev[0], hmin], color="#111", lw=2.2, zorder=8)
ax.plot([x[-1], x[-1]], [elev[-1], hmin], color="#111", lw=2.2, zorder=8)
ax.annotate(f"Site A tower\n{hmin-elev[0]:.4f} m", (x[0], (elev[0]+hmin)/2), xytext=(0.52, 44), arrowprops=dict(arrowstyle="-", color="#444", lw=0.7), fontsize=8)
ax.annotate(f"Site B tower\n{hmin-elev[-1]:.4f} m", (x[-1], (elev[-1]+hmin)/2), xytext=(5.72, 47), fontsize=8)
ax.annotate("P2: Pacific Icon 2\n(governing THE)", (x[1], the[1]), xytext=(0.72, 60),
            arrowprops=dict(arrowstyle="-", color="#444", lw=0.7), fontsize=8)
for r in rows:
    ax.text(r["d1"], -5.0, str(r["n"]), ha="center", va="top", fontsize=7, color="#333", clip_on=False)
ax.text(-0.14, -5.0, "Pt.", ha="right", va="top", fontsize=7, color="#333", clip_on=False)
ax.set_xlim(-0.14, data["common"]["d_km"] + 0.14)
ax.set_ylim(0, 78)
ax.set_xlabel("Distance from Site A, d₁ (km)", labelpad=15)
ax.set_ylabel("Height above sea level (m)")
ax.set_title("Path Profile: UST BGPOP (Site A) to Fini Homes, Valenzuela (Site B)", fontweight="bold", fontsize=10)
ax.grid(True, color="#e6e6e6", lw=0.6, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.62, 0.86), ncol=2, frameon=True, fontsize=7.2, framealpha=0.95)
fig.tight_layout()
fig.savefig(os.path.join(here, "path_profile.png"))
print("saved")

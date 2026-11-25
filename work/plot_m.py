import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(here, "results_M.json"), encoding="utf-8"))
rows = data["rows"]
M = data["main"]
ha, hb, tilt, tg = M["h_ant_a"], M["h_ant_b"], M["tilt_deg"], M["tilt_point"]
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
ax.plot([x[0], x[-1]], [ha, hb], color="#c62828", ls="--", lw=1.3,
        label=f"Tilted line of sight, {ha:.4f} m to {hb:.4f} m ({tilt:.4f}°)", zorder=7)
ax.plot([x[-1], x[-1]], [elev[-1], hb], color="#111", lw=3.0, zorder=8)
for e in M["extras"]:
    ax.bar(e["d1"], e["floors"] * 2.5, bottom=e["ground"], width=0.06, color="#f2c94c", edgecolor="#9a7b0a", linewidth=0.6, zorder=3)
    ax.plot([e["d1"]], [e["the"]], marker="^", color="#e67e22", ms=6, zorder=6)
ax.plot([], [], marker="^", color="#e67e22", ls="none", label="THE of near-line structures (M: Maranatha tower, L: LRT-1 viaduct)")
g = tg
ax.annotate("P17 and the LRT-1 viaduct set the tilt\n(line just clears their THE)",(g["d1"], g["the"]), xytext=(g["d1"] - 2.4, 50),
            arrowprops=dict(arrowstyle="-", color="#444", lw=0.7), fontsize=8)
ax.annotate("Site A: antenna on the\nFrassati rooftop, 0 m tower", (x[0], ha), xytext=(0.28, 66),
            arrowprops=dict(arrowstyle="-", color="#444", lw=0.7), fontsize=8)
ax.annotate(f"Site B tower\n{hb - elev[-1]:.4f} m", (x[-1], hb), xytext=(6.05, 44),
            arrowprops=dict(arrowstyle="-", color="#444", lw=0.7), fontsize=8)
for r in rows:
    ax.text(r["d1"], -5.0, str(r["n"]), ha="center", va="top", fontsize=7, color="#333", clip_on=False)
ax.text(-0.14, -5.0, "Pt.", ha="right", va="top", fontsize=7, color="#333", clip_on=False)
ax.set_xlim(-0.14, data["common"]["d_km"] + 0.14)
ax.set_ylim(0, 78)
ax.set_xlabel("Distance from Site A, d₁ (km)", labelpad=15)
ax.set_ylabel("Height above sea level (m)")
ax.set_title("Path Profile: UST Frassati (Site A) to Metro Industries, Valenzuela (Site B)", fontweight="bold", fontsize=10)
ax.grid(True, color="#e6e6e6", lw=0.6, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(loc="upper right", ncol=2, frameon=True, fontsize=7.2, framealpha=0.95)
fig.tight_layout()
fig.savefig(os.path.join(here, "path_profile_M.png"))
print("saved")

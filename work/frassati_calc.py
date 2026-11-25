"""Option 2 for ECE21129: UST Frassati (Site A) to Fini Homes (Site B)."""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_MD = r"C:\UST\TRANSMA PROJECT\Option2_Frassati_Fini.md"

C, K, FC_GHZ = 3e8, 1.38e-23, 10.59625
FC_HZ = FC_GHZ * 1e9
FLOOR = 2.5
ANT, LNA_G, LNA_NF, P1DB, MAX_IN = 44.0, 30.0, 1.5, 15.0, 13.0
WG = 2.995 / 30.48
CONN = 2 * (0.2 + 0.3)
HORIZ, T, BW, SNR, A, B = 3.0, 290.0, 2.5e6, 10.0, 1.0, 0.5
FIBER, ROAD_KM = 0.22, 8.9


def db(x):
    return 10 * math.log10(x)


def row(n, d1m, D, ground, floors, desc, basis):
    d1, d2 = d1m / 1000, (D - d1m) / 1000
    elev = ground + floors * FLOOR
    bulge = d1 * d2 / 12.75
    f60 = 0.6 * 17.3 * math.sqrt(d1 * d2 / (FC_GHZ * (d1 + d2)))
    return dict(n=n, d1=d1, d2=d2, ground=ground, floors=floors, elev=elev, bulge=bulge, f60=f60,
                the=elev + bulge + f60, desc=desc, basis=basis)


def link(rows, D):
    hmin = max(r["the"] for r in rows)
    gov = max(rows, key=lambda r: r["the"])["n"]
    ta, tb = hmin - rows[0]["elev"], hmin - rows[-1]["elev"]
    la, lb = ta + HORIZ, tb + HORIZ
    wa, wb = la * WG, lb * WG
    fsl = 20 * math.log10(4 * math.pi / C) + 20 * math.log10(FC_HZ) + 20 * math.log10(D)
    pin = db(2000)
    gt = 2 * ANT + LNA_G - wa - wb - CONN
    rsl = pin + gt - fsl
    n = db(K * T * BW / 1e-3)
    pth = n + SNR + LNA_NF
    fm = rsl - pth
    base = 30 * math.log10(D / 1000) + db(6 * A * B * FC_GHZ) - 70
    theo = {r: base - db(1 - r / 100) for r in (99, 99.9, 99.99, 99.999)}
    fiber_len = ROAD_KM + ((rows[0]["elev"] - rows[0]["ground"]) + (rows[-1]["elev"] - rows[-1]["ground"])) / 1000
    return dict(D=D, hmin=hmin, gov=gov, ta=ta, tb=tb, la=la, lb=lb, wa=wa, wb=wb, fsl=fsl, gt=gt, rsl=rsl,
                rsl_in=rsl - LNA_G, pth=pth, fm=fm, fm_in=fm - LNA_G, theo=theo,
                unrel=10 ** ((base - fm) / 10), micro=fsl + wa + wb + CONN,
                fiber_len=fiber_len, fiber=fiber_len * FIBER)


# Regression: the same function must reproduce the saved BGPOP answer.
saved = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
bg = link(saved["rows"], saved["common"]["d_m"])
for key, ref in (("hmin", "hmin"), ("ta", "tower_a"), ("tb", "tower_b"), ("rsl", "rsl_out"), ("fm", "fm"), ("fiber", "fiber_loss")):
    assert abs(bg[key] - saved["main"][ref]) < 1e-6, key

pts = json.load(open(os.path.join(HERE, "frassati_points.json"), encoding="utf-8"))
D = pts["D"]
GROUND = {1: 2.54, 2: 2.67, 3: 3.35, 4: 3.08, 5: 3.08, 6: 4.35, 7: 5.77, 8: 8.73, 9: 14.60, 10: 13.78,
          11: 14.09, 12: 16.60, 13: 17.98, 14: 17.55, 15: 17.53, 16: 19.47, 17: 19.89, 18: 16.88, 19: 10.43, 20: 4.97}
INFO = {
    1: (23, "Site A: UST Frassati", "User-stated, unconfirmed"), 2: (4, "Mid-rise block", "Satellite estimate"),
    3: (2, "Row houses", "Satellite estimate"), 4: (2, "Rail corridor structure", "Satellite estimate"),
    5: (2, "Houses", "Satellite estimate"), 6: (3, "Roadside buildings", "Satellite estimate"),
    7: (2, "Roadside buildings", "Satellite estimate"), 8: (0, "Cemetery, cloud in image", "Satellite estimate"),
    9: (0, "Cemetery, cloud in image", "Satellite estimate"), 10: (2, "Houses", "Satellite estimate"),
    11: (2, "Houses", "Satellite estimate"), 12: (2, "Low-rise compound", "Satellite estimate"),
    13: (2, "Warehouse", "Satellite estimate"), 14: (3, "Low-rise buildings", "Satellite estimate"),
    15: (4, "Low-rise buildings", "Satellite estimate"), 16: (2, "Low-rise, trees", "Satellite estimate"),
    17: (2, "Low-rise, trees", "Satellite estimate"), 18: (3, "Townhouses", "Satellite estimate"),
    19: (0, "Open lot", "Satellite estimate"), 20: (6, "Site B: Fini Homes", "User-confirmed"),
}
rows = [row(p["n"], p["d1_m"] if p["n"] < 20 else D, D, GROUND[p["n"]], INFO[p["n"]][0], INFO[p["n"]][1], INFO[p["n"]][2]) for p in pts["rows"]]
main = link(rows, D)

# Near-line obstruction that falls between F5 and F6.
lat = 14 + 37 / 60 + 26.83 / 3600
t = (lat - 14.6091583) / (14.6690889 - 14.6091583)
mar = row("M", t * D, D, 4.35, 9, "Maranatha/PMCC tower", "Street View count")
all_checked = rows + [mar]
assert max(r["the"] for r in all_checked) == rows[0]["the"]

margins = []
for r in rows[1:-1]:
    allowed = math.floor((rows[0]["elev"] - r["ground"] - r["bulge"] - r["f60"]) / FLOOR)
    margins.append((allowed, r["n"]))
limit, limit_n = min(margins)
mar_allowed = math.floor((rows[0]["elev"] - mar["ground"] - mar["bulge"] - mar["f60"]) / FLOOR)

sens = {}
for fl in (20, 21, 22, 23):
    s = [dict(r) for r in rows]
    s[0] = row(1, 0.0, D, 2.54, fl, "Site A", "")
    sens[fl] = link(s, D)

print(f"D {D:.2f} m  hmin {main['hmin']:.4f} at P{main['gov']}  towers {main['ta']:.4f}/{main['tb']:.4f}")
print(f"FSL {main['fsl']:.4f} G {main['gt']:.4f} RSL {main['rsl']:.4f} in {main['rsl_in']:.4f} FM {main['fm']:.4f} input-ref {main['fm_in']:.4f}")
print(f"WG {main['la']:.4f}/{main['lb']:.4f} m, {main['wa']:.4f}/{main['wb']:.4f} dB; micro {main['micro']:.4f}; fiber {main['fiber_len']:.4f} km {main['fiber']:.4f} dB")
print("theo", {k: round(v, 4) for k, v in main["theo"].items()}, f"1-R {main['unrel']:.4e}")
print(f"RSL over P1dB by {main['rsl'] - P1DB:.4f} dB; Maranatha d1 {mar['d1']:.4f} km THE {mar['the']:.4f}, floors allowed {mar_allowed}")
print(f"Lowest floors allowed at sampled point: {limit} at F{limit_n}")
for fl, s in sens.items():
    print(f"{fl} floors: hmin {s['hmin']:.4f} gov {s['gov']} A {s['ta']:.4f} B {s['tb']:.4f} RSL {s['rsl']:.4f}")
for r in rows:
    print(f"{r['n']:>2} {r['d1']:.4f} {r['d2']:.4f} {r['ground']:6.2f} {r['floors']:2d} {r['elev']:8.4f} {r['bulge']:.4f} {r['f60']:.4f} {r['the']:8.4f}")

lines = [
    "# Option 2: UST Frassati to Fini Homes",
    "",
    "Working comparison only. The BGPOP draft was not changed.",
    "",
    "| Item | BGPOP to Fini | Frassati to Fini |",
    "|---|---:|---:|",
    f"| Path length (m) | {bg['D']:.2f} | {main['D']:.2f} |",
    f"| Minimum antenna height (m) | {bg['hmin']:.4f} | {main['hmin']:.4f} |",
    f"| Site A tower (m) | {bg['ta']:.4f} | {main['ta']:.4f} |",
    f"| Site B tower (m) | {bg['tb']:.4f} | {main['tb']:.4f} |",
    f"| Waveguide A / B (m) | {bg['la']:.4f} / {bg['lb']:.4f} | {main['la']:.4f} / {main['lb']:.4f} |",
    f"| Free-space loss (dB) | {bg['fsl']:.4f} | {main['fsl']:.4f} |",
    f"| RSL at amplifier output (dBm) | {bg['rsl']:.4f} | {main['rsl']:.4f} |",
    f"| Fade margin (dB) | {bg['fm']:.4f} | {main['fm']:.4f} |",
    f"| Microwave loss (dB) | {bg['micro']:.4f} | {main['micro']:.4f} |",
    f"| Fiber loss, 8.9 km road assumed (dB) | {bg['fiber']:.4f} | {main['fiber']:.4f} |",
    "",
    f"The current amplifier saturates at +15 dBm, so Option 2 is {main['rsl'] - P1DB:.4f} dB over its limit and needs a different amplifier.",
    "",
    "## Path profile",
    "",
    "| Pt | d1 (km) | d2 (km) | Ground (m) | Floors | h elevation (m) | Bulge (m) | 0.6F1 (m) | THE (m) | Location | Floor basis |",
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
]
for r in rows:
    name = "P1" if r["n"] == 1 else "P20" if r["n"] == 20 else f"F{r['n']}"
    lines.append(f"| {name} | {r['d1']:.4f} | {r['d2']:.4f} | {r['ground']:.2f} | {r['floors']} | {r['elev']:.4f} | {r['bulge']:.4f} | {r['f60']:.4f} | {r['the']:.4f} | {r['desc']} | {r['basis']} |")
lines += [
    "",
    "## Near-line building checks",
    "",
    f"- Maranatha/PMCC tower: the line touches its west corner at d1 = {mar['d1']:.4f} km. About 9 floors from Street View gives THE = {mar['the']:.4f} m, below {main['hmin']:.4f} m. It would need more than {mar_allowed} floors to change the result.",
    "- Tall tower north of Frassati (Anytime Fitness label): its base is about 17 m east of the line, so it does not block the path.",
    f"- At the sampled points, a building would need more than {limit} floors to change the minimum antenna height. The tightest point is F{limit_n}.",
    "",
    "## Frassati floor sensitivity",
    "",
    "| Frassati floors | Min. antenna height (m) | Site A tower (m) | Site B tower (m) | RSL (dBm) |",
    "|---:|---:|---:|---:|---:|",
]
for fl, s in sens.items():
    lines.append(f"| {fl} | {s['hmin']:.4f} | {s['ta']:.4f} | {s['tb']:.4f} | {s['rsl']:.4f} |")
open(OUT_MD, "w", encoding="utf-8").write("\n".join(lines) + "\n")
json.dump(dict(main={k: v for k, v in main.items() if k != "theo"}, theo={str(k): v for k, v in main["theo"].items()}, rows=rows),
          open(os.path.join(HERE, "frassati_results.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("regression passed; wrote comparison")

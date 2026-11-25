"""Compute Option A (Frassati) and Option B (BGPOP) with the corrected connector chain."""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
C0, K, FC_GHZ = 3e8, 1.38e-23, 10.59625
FC_HZ = FC_GHZ * 1e9
ANT, WG, HORIZ, T, BW, SNR, A_F, B_F = 44.0, 2.995 / 30.48, 3.0, 290.0, 2.5e6, 10.0, 1.0, 0.5
CONN = 2 * (0.2 + 0.3 + 0.21)   # antenna adapter, waveguide adapter, SMA male-male adapter at each site
FIBER, ROAD = 0.22, 8.9
AMPS = {
    "A": dict(name="ERZIA ERZ-LNA-0800-1220-26-2", band="8.0 to 12.2 GHz", gain=25.0, nf=2.2, p1db=20.0, max_in=10.0, max_gain=28.0),
    "B": dict(name="Narda-MITEQ LNA-30-08001200-15-15P", band="8.0 to 12.0 GHz", gain=30.0, nf=1.5, p1db=15.0, max_in=13.0, max_gain=None),
}


def db(x):
    return 10 * math.log10(x)


def common(D):
    lam = 0.0283   # rounded to match the group's handwritten Section 1 (AD and beamwidth only)
    ad = (math.pi * 1.8 / lam) ** 2
    return dict(lam=lam, ad_lin=ad, ad_db=db(ad), theta=70 * lam / 1.8, ap_theory=db(ad) + db(0.55),
                fsl=20 * math.log10(4 * math.pi / C0) + 20 * math.log10(FC_HZ) + 20 * math.log10(D), pin=db(2000),
                wg_db_m=WG, d_m=D, d_km=D / 1000, fc=FC_GHZ)


def link(rows, D, amp, tilted=False, extras=()):
    c = common(D)
    hmin = max(r["the"] for r in rows)
    gov = max(rows, key=lambda r: r["the"])["n"]
    dkm = D / 1000
    if tilted:
        # Site A antenna stays at its THE; Site B is lowered until the straight line just clears every THE
        ha = rows[0]["the"]
        pts_ = [dict(name=f"P{r['n']}", d1=r["d1"], the=r["the"]) for r in rows[1:-1]] + [dict(name=e["name"], d1=e["d1"], the=e["the"]) for e in extras]
        need = [(ha - (ha - q["the"]) * dkm / q["d1"], i) for i, q in enumerate(pts_)]
        hb, idx = max(need)
        tpoint = pts_[idx]
        if hb < rows[-1]["the"]:
            hb, tpoint = rows[-1]["the"], dict(name="P20", d1=rows[-1]["d1"], the=rows[-1]["the"])
    else:
        ha = hb = hmin
        tpoint = dict(name=f"P{gov}", d1=rows[gov - 1]["d1"], the=hmin)
    line = [ha + (hb - ha) * r["d1"] / dkm for r in rows]
    clearance = [dict(name=f"P{r['n']}", d1=r["d1"], the=r["the"], line=h, margin=h - r["the"]) for r, h in zip(rows, line)]
    for e in extras:
        h = ha + (hb - ha) * e["d1"] / dkm
        clearance.append(dict(name=e["name"], d1=e["d1"], the=e["the"], line=h, margin=h - e["the"]))
    clearance.sort(key=lambda x: x["d1"])
    assert all(x["margin"] > -1e-9 for x in clearance)
    tilt = math.degrees(math.atan(abs(ha - hb) / D))
    ta, tb = ha - rows[0]["elev"], hb - rows[-1]["elev"]
    la, lb = ta + HORIZ, tb + HORIZ
    wa, wb = la * WG, lb * WG
    gt = 2 * ANT + amp["gain"] - wa - wb - CONN
    rsl = c["pin"] + gt - c["fsl"]
    ref = c["pin"] + 2 * c["ap_theory"] + amp["gain"] - wa - wb - CONN - c["fsl"]
    n = db(K * T * BW / 1e-3)
    pth = n + SNR + amp["nf"]
    fm = rsl - pth
    base = 30 * math.log10(D / 1000) + db(6 * A_F * B_F * FC_GHZ) - 70
    theo = {str(r): base - db(1 - r / 100) for r in (99, 99.9, 99.99, 99.999)}
    fib = ROAD + (rows[0]["obstruction"] + rows[-1]["obstruction"]) / 1000
    return dict(hmin=hmin, governing=gov, tilted=tilted, h_ant_a=ha, h_ant_b=hb, tilt_point=tpoint, extras=list(extras), tilt_deg=tilt,
                clearance=clearance, flat_tower_b=hmin - rows[-1]["elev"], tower_a=ta, tower_b=tb, len_a=la, len_b=lb, wg_a=wa, wg_b=wb, conn=CONN,
                g_total=gt, rsl_out=rsl, rsl_in=rsl - amp["gain"], rsl_ref=ref, n=n, pth=pth, fm=fm,
                fm_in=fm - amp["gain"], fm_base=base, fm_theory=theo, unreliability=10 ** ((base - fm) / 10),
                fiber_len=fib, fiber_loss=fib * FIBER, micro_loss=c["fsl"] + wa + wb + CONN)


old = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
fa = json.load(open(os.path.join(HERE, "frassati_results.json"), encoding="utf-8"))
pts = json.load(open(os.path.join(HERE, "frassati_points.json"), encoding="utf-8"))
D_A = pts["D"]
rows_a = []
for r, p in zip(fa["rows"], pts["rows"]):
    q = dict(r)
    q.update(lat=p["lat_dms"], lon=p["lon_dms"], obstruction=r["floors"] * 2.5, f1=r["f60"] / 0.6, evidence=r["basis"])
    rows_a.append(q)
rows_a[0]["evidence"] = "Group-confirmed"


def extra(name, label, d1, ground, floors):
    d2 = D_A / 1000 - d1
    bulge = d1 * d2 / 12.75
    f60 = 0.6 * 17.3 * math.sqrt(d1 * d2 / (FC_GHZ * (d1 + d2)))
    elev = ground + floors * 2.5
    return dict(name=name, label=label, d1=d1, d2=d2, ground=ground, floors=floors, elev=elev, bulge=bulge, f60=f60, the=elev + bulge + f60)


NEW_LAT = 14 + 39 / 60 + 36.01 / 3600
EXTRAS_A = [
    extra("M", "Maranatha/PMCC tower (Street View, 9 floors)", 1.6630, 4.35, 9),
    extra("N", "Building under construction on Asuncion St (Street View, 8 floors)",
          (NEW_LAT - 14.6091583) / (14.6690889 - 14.6091583) * D_A / 1000, 20.04, 8),
]
rows_b = old["rows"]
D_B = old["common"]["d_m"]
main_a, main_b = link(rows_a, D_A, AMPS["A"], tilted=True, extras=EXTRAS_A), link(rows_b, D_B, AMPS["B"])
alt_b = link(old["alt_rows"], D_B, AMPS["B"])

# Independent checks
assert abs(main_a["hmin"] - 60.04) < 1e-9 and main_a["governing"] == 1 and abs(main_a["tower_a"]) < 1e-9
assert abs(main_b["hmin"] - old["main"]["hmin"]) < 1e-9
assert abs(main_b["rsl_out"] - (old["main"]["rsl_out"] - 0.42)) < 1e-9
assert main_a["rsl_out"] < AMPS["A"]["p1db"] and main_a["rsl_in"] < AMPS["A"]["max_in"]
assert main_a["rsl_in"] + AMPS["A"]["max_gain"] < AMPS["A"]["p1db"]
assert main_b["rsl_out"] < AMPS["B"]["p1db"] and main_b["rsl_in"] < AMPS["B"]["max_in"]
assert all(main_a["fm"] > v for v in main_a["fm_theory"].values())
assert all(main_b["fm"] > v for v in main_b["fm_theory"].values())

json.dump(dict(common=common(D_A), rows=rows_a, main=main_a, alt=main_a, amp=AMPS["A"]),
          open(os.path.join(HERE, "results_A.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(dict(common=common(D_B), rows=rows_b, main=main_b, alt=alt_b, amp=AMPS["B"]),
          open(os.path.join(HERE, "results_B.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for name, m, c in (("A Frassati", main_a, common(D_A)), ("B BGPOP", main_b, common(D_B))):
    print(f"{name}: D {c['d_m']:.2f} hmin {m['hmin']:.4f} towers {m['tower_a']:.4f}/{m['tower_b']:.4f} FSL {c['fsl']:.4f} "
          f"G {m['g_total']:.4f} RSL {m['rsl_out']:.4f} in {m['rsl_in']:.4f} Pth {m['pth']:.4f} FM {m['fm']:.4f} "
          f"loss {m['micro_loss']:.4f} fiber {m['fiber_loss']:.4f} 1-R {m['unreliability']:.4e}")
print(f"A tilted: antennas {main_a['h_ant_a']:.4f}/{main_a['h_ant_b']:.4f} set by {main_a['tilt_point']['name']}, tilt {main_a['tilt_deg']:.4f} deg, flat tower would be {main_a['flat_tower_b']:.4f}")
print("B alternate RSL", round(alt_b["rsl_out"], 4), "checks passed")

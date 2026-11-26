"""Compute every Section 2 step (Frassati to Metro Industries) and write sec2_steps.json for the docx builder."""
import json, math, os, sys
sys.stdout.reconfigure(encoding="utf-8")
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "sec2_steps.json")
R = json.load(open(os.path.join(WORK, "results_M.json"), encoding="utf-8"))
P = json.load(open(os.path.join(WORK, "metro_pts.json"), encoding="utf-8"))
m = R["main"]
D = R["common"]["d_m"]; DK = D / 1000; F = 10.59625
f4 = lambda x: f"{x:.4f}"
f6 = lambda x: f"{x:.6f}"
r4 = lambda x: round(x + 0.0, 4)

# ---------- WGS-84 local (flat-ellipsoid) distance, hand-checkable ----------
A_E = 6378137.0; FL = 1 / 298.257223563; E2 = FL * (2 - FL)


def dms_parts(x):
    d = int(x); mm = (x - d) * 60; mi = int(mm); s = round((mm - mi) * 60, 2)
    return d, mi, s


def flat(lat1, lon1, lat2, lon2):
    pm = math.radians((lat1 + lat2) / 2); s = math.sin(pm)
    Mr = A_E * (1 - E2) / (1 - E2 * s * s) ** 1.5
    Nr = A_E / math.sqrt(1 - E2 * s * s)
    dphi = math.radians(lat2 - lat1); dlam = math.radians(lon2 - lon1)
    dy = Mr * dphi; dx = Nr * math.cos(pm) * dlam
    return dict(phim=math.degrees(pm), M=Mr, N=Nr, dphi=dphi, dlam=dlam, dy=dy, dx=dx, D=math.hypot(dx, dy),
                az=math.degrees(math.atan2(dx, dy)) % 360)


A = (14 + 36 / 60 + 32.71 / 3600, 120 + 59 / 60 + 31.75 / 3600)
B = (14 + 40 / 60 + 17.32 / 3600, 120 + 59 / 60 + 12.63 / 3600)
geo = flat(*A, *B)
assert abs(geo["D"] - D) < 0.005, geo["D"]
sites = []
for (lat, lon), name in ((A, "Site A (Frassati)"), (B, "Site B (Metro Industries)")):
    sites.append(dict(name=name, lat=lat, lon=lon, latp=dms_parts(lat), lonp=dms_parts(lon)))

# d1 of each point from its own coordinates (same method)
d1rows = []
for n in range(2, 20):
    p = P[str(n)]
    g = flat(*A, p["lat"], p["lon"])
    d1rows.append(dict(n=n, lat=p["lat"], lon=p["lon"], dy=g["dy"], dx=g["dx"], d1m=g["D"], used=p["d1_m"],
                       even=(n - 1) * D / 19, shift=p["d1_m"] - (n - 1) * D / 19))
    assert abs(g["D"] - p["d1_m"]) < 1.0, (n, g["D"], p["d1_m"])

# ---------- Table 3 rows, full working ----------


def steps(name, d1, ground, floors, the_ref, f60_ref, bulge_ref, elev_ref):
    d2 = DK - d1
    if d2 < 1e-9: d2 = 0.0
    prod = d1 * d2
    bulge = prod / (12.75 * 4 / 3)
    arg = prod / (F * DK) if prod else 0.0
    f1 = 17.3 * math.sqrt(arg)
    f60 = 0.6 * f1
    elev = ground + floors * 2.5
    the = elev + bulge + f60
    # the 6-decimal working must round to the report's 4-decimal values
    the_hand = round(elev, 6) + round(bulge, 6) + round(f60, 6)
    for a, b in ((the_hand, the_ref), (bulge, bulge_ref), (f60, f60_ref), (elev, elev_ref)):
        assert abs(r4(a) - r4(b)) < 1e-9, (name, a, b)
    return dict(name=name, d1=d1, d2=d2, ground=ground, floors=floors, obst=floors * 2.5, elev=elev, prod=prod,
                bulge=bulge, arg=arg, sq=math.sqrt(arg), f1=f1, f60=f60, the=the, the_hand=the_hand)


rows = []
for r in R["rows"]:
    s = steps(f"P{r['n']}", r["d1"], r["ground"], r["floors"], r["the"], r["f60"], r["bulge"], r["elev"])
    s.update(n=r["n"], desc=r["desc"], lat=r["lat"], lon=r["lon"])
    rows.append(s)
extras = []
for e in m["extras"]:
    s = steps(e["name"], e["d1"], e["ground"], e["floors"], e["the"], e["f60"], e["bulge"], e["elev"])
    s.update(label=e["label"])
    extras.append(s)

# ---------- Table 4: flat and tilted ----------
hmin = max(r["the"] for r in rows)
gov = max(rows, key=lambda r: r["the"])["n"]
hA = m["h_ant_a"]; hB = m["h_ant_b"]; MG = m["design_margin"]
assert abs(hA - (rows[0]["the"] + MG)) < 1e-9
req = []
for q in rows[1:-1] + extras:
    need = hA - (hA - q["the"] - MG) * DK / q["d1"]
    req.append(dict(name=q["name"], d1=q["d1"], the=q["the"], ratio=DK / q["d1"], diff=hA - q["the"] - MG, need=need))
req.sort(key=lambda x: x["d1"])
top = max(req, key=lambda x: x["need"])
assert top["name"] == "P17" and abs(top["need"] - hB) < 1e-9
slope = (hA - hB) / DK
tilt = math.degrees(math.atan((hA - hB) / D))
assert abs(tilt - m["tilt_deg"]) < 1e-12
clear = []
allpts = sorted([dict(name=r["name"], d1=r["d1"], the=r["the"]) for r in rows] +
                [dict(name=e["name"], d1=e["d1"], the=e["the"]) for e in extras], key=lambda x: x["d1"])
for q in allpts:
    los = hA - slope * q["d1"]
    clear.append(dict(q, los=los, margin=los - q["the"]))
ref = {c["name"]: c for c in m["clearance"]}
for c in clear:
    assert abs(c["los"] - ref[c["name"]]["line"]) < 1e-9 and abs(c["margin"] - ref[c["name"]]["margin"]) < 1e-9

data = dict(margin=MG, D=D, DK=DK, F=F, geo=geo, sites=sites, d1rows=d1rows, rows=rows, extras=extras, hmin=hmin, gov=gov,
            hA=hA, hB=hB, elevA=rows[0]["elev"], elevB=rows[-1]["elev"], towerA=m["tower_a"], towerB=m["tower_b"],
            flatB=m["flat_tower_b"], req=req, slope=slope, tilt=tilt, clear=clear, E2=E2, a=A_E, fl=FL,
            lam=0.3e9 / (F * 1e9) * 1000 / 1000)
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", f4(geo["D"]), f4(geo["az"]), "P17 needs", f4(top["need"]), "tilt", f4(tilt))
for d in d1rows:
    print(d["n"], round(d["d1m"], 2), d["used"], round(d["shift"], 2))

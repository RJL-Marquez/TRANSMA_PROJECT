"""Option 2: 20 evenly spaced points, UST Frassati (Site A) to Fini Homes (Site B)."""
import csv
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))

A_WGS = 6378137.0
F_WGS = 1 / 298.257223563
B_WGS = A_WGS * (1 - F_WGS)


def dms(d, m, s):
    return d + m / 60 + s / 3600


def to_dms(x):
    d = int(x)
    rem = (x - d) * 60
    m = int(rem)
    s = round((rem - m) * 60, 2)
    if s >= 60:
        s -= 60
        m += 1
    if m >= 60:
        m -= 60
        d += 1
    return d, m, s


def vincenty(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    L = math.radians(lon2 - lon1)
    U1, U2 = math.atan((1 - F_WGS) * math.tan(phi1)), math.atan((1 - F_WGS) * math.tan(phi2))
    lam = L
    for _ in range(200):
        sl, cl = math.sin(lam), math.cos(lam)
        ss = math.hypot(math.cos(U2) * sl, math.cos(U1) * math.sin(U2) - math.sin(U1) * math.cos(U2) * cl)
        cs = math.sin(U1) * math.sin(U2) + math.cos(U1) * math.cos(U2) * cl
        sigma = math.atan2(ss, cs)
        sa = math.cos(U1) * math.cos(U2) * sl / ss
        c2a = 1 - sa * sa
        c2sm = cs - 2 * math.sin(U1) * math.sin(U2) / c2a
        C = F_WGS / 16 * c2a * (4 + F_WGS * (4 - 3 * c2a))
        new = L + (1 - C) * F_WGS * sa * (sigma + C * ss * (c2sm + C * cs * (-1 + 2 * c2sm * c2sm)))
        if abs(new - lam) < 1e-13:
            lam = new
            break
        lam = new
    u2 = c2a * (A_WGS ** 2 - B_WGS ** 2) / B_WGS ** 2
    AA = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    BB = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    ds = BB * ss * (c2sm + BB / 4 * (cs * (-1 + 2 * c2sm ** 2) - BB / 6 * c2sm * (-3 + 4 * ss ** 2) * (-3 + 4 * c2sm ** 2)))
    return B_WGS * AA * (sigma - ds)


FRASSATI = (dms(14, 36, 32.97), dms(120, 59, 32.27))
FINI = (dms(14, 40, 8.72), dms(120, 59, 11.05))
BGPOP = (dms(14, 36, 31.23), dms(120, 59, 17.80))

D = vincenty(*FRASSATI, *FINI)
check = vincenty(*BGPOP, *FINI)
print(f"Frassati to Fini: {D:.2f} m")
print(f"BGPOP to Fini check: {check:.2f} m (Google Earth 6687.72 m)")

rows = []
for i in range(20):
    t = i / 19
    lat = FRASSATI[0] + t * (FINI[0] - FRASSATI[0])
    lon = FRASSATI[1] + t * (FINI[1] - FRASSATI[1])
    d1 = vincenty(*FRASSATI, lat, lon) if i else 0.0
    la, lo = to_dms(lat), to_dms(lon)
    rows.append(dict(n=i + 1, d1_m=round(d1, 2), d2_m=round(D - d1, 2), lat=round(lat, 7), lon=round(lon, 7),
                     lat_dms=f"{la[0]}°{la[1]:02d}'{la[2]:05.2f}\"N", lon_dms=f"{lo[0]}°{lo[1]:02d}'{lo[2]:05.2f}\"E"))

with open(os.path.join(HERE, "frassati_points.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
json.dump(dict(D=D, rows=rows), open(os.path.join(HERE, "frassati_points.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    print(f"{r['n']:2d} {r['d1_m']:8.2f} {r['d2_m']:8.2f} {r['lat']:.7f} {r['lon']:.7f} {r['lat_dms']} {r['lon_dms']}")

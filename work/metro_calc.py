"""Frassati (group pin) to Metro Industries, 84 Ramon Delfin St: path profile, tilted towers, link budget."""
import json, math, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "option_data.py"), encoding="utf-8").read()
exec(src[:src.index("old = json.load")])          # constants, AMPS, common(), link()
from draft_points import to_dms  # noqa: E402

L = json.load(open(os.path.join(HERE, "metro_line.json")))
P = json.load(open(os.path.join(HERE, "metro_pts.json")))
D = L["D"]; DK = D / 1000


def dms(x, h):
    d, m, s = to_dms(x)
    return f"{d}°{m:02d}'{s:05.2f}\"{h}"


def pt(n, d1, ground, floors):
    d2 = DK - d1
    bulge = d1 * d2 / 12.75
    f1 = 17.3 * math.sqrt(d1 * d2 / (FC_GHZ * DK)) if 0 < d1 < DK else 0.0
    elev = ground + floors * 2.5
    return dict(n=n, d1=d1, d2=d2, ground=ground, floors=floors, obstruction=floors * 2.5, elev=elev,
                bulge=bulge, f1=f1, f60=0.6 * f1, the=elev + bulge + 0.6 * f1)


rows = []
for n in range(1, 21):
    r = P[str(n)]
    q = pt(n, round(r["d1_m"] / 1000, 4) if n < 20 else DK, r["ground"], r["floors"])
    q.update(lat=dms(r["lat"], "N"), lon=dms(r["lon"], "E"), desc=r["note"], evidence=r["note"])
    rows.append(q)


def extra(name, label, d1, ground, floors):
    q = pt(name, d1, ground, floors)
    q.update(name=name, label=label)
    return q


EXTRAS = [
    extra("M", "Maranatha/PMCC tower (9 floors, corner about 5 m east of the line)", 1.6670, 4.35, 9),
    extra("L", "LRT-1 viaduct on EDSA with a train on it (about 12.5 m, taken as 5 floors)", 5.3531, 19.31, 5),
]
main = link(rows, D, AMPS["A"], tilted=True, extras=EXTRAS)
c = common(D)
json.dump(dict(common=c, rows=rows, main=main, alt=main, amp=AMPS["A"]),
          open(os.path.join(HERE, "results_M.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"D {D:.2f} m, FSL {c['fsl']:.4f}")
for r in rows:
    print(f"P{r['n']:<2} d1 {r['d1']:.4f} d2 {r['d2']:.4f} g {r['ground']:6.2f} fl {r['floors']:2d} elev {r['elev']:7.4f} "
          f"bulge {r['bulge']:.4f} 0.6F1 {r['f60']:.4f} THE {r['the']:.4f}")
for e in EXTRAS:
    print(e["name"], f"THE {e['the']:.4f}")
m = main
print(f"hmin {m['hmin']:.4f} (P{m['governing']}); tilted antennas {m['h_ant_a']:.4f}/{m['h_ant_b']:.4f} set by {m['tilt_point']['name']}, "
      f"tilt {m['tilt_deg']:.4f} deg; towers {m['tower_a']:.4f}/{m['tower_b']:.4f}; flat tower B {m['flat_tower_b']:.4f}")
print(f"WG {m['len_a']:.4f}/{m['len_b']:.4f} m, loss {m['wg_a']:.4f}/{m['wg_b']:.4f}; G {m['g_total']:.4f}; RSL {m['rsl_out']:.4f} (in {m['rsl_in']:.4f}); "
      f"Pth {m['pth']:.4f}; FM {m['fm']:.4f}; loss {m['micro_loss']:.4f}; fiber {m['fiber_loss']:.4f}")
print("margins:", ", ".join(f"{x['name']} {x['margin']:.3f}" for x in m["clearance"]))

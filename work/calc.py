"""ECE21129 4ECE-B Group 5: path profile and link budget."""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.dirname(os.path.abspath(__file__))

C = 3e8
K = 1.38e-23
FC_GHZ = 10.59625
FC_HZ = FC_GHZ * 1e9
D_M = 6687.72
D_KM = D_M / 1000
DIA = 1.8
FLOOR = 2.5

# point, d1 (m), lat, lon, ground (m), floors, description, floor evidence
STEP = D_M / 19
POINTS = [
    (1, 0.0, "14°36'31.23\"N", "120°59'17.80\"E", 2.16, 12, "Site A: UST BGPOP", "Group decision"),
    (2, STEP, "14°36'42.67\"N", "120°59'17.44\"E", 2.77, 26, "Pacific Icon Residences 2", "Property listing"),
    (3, 2 * STEP, "14°36'54.12\"N", "120°59'17.08\"E", 3.11, 2, "Row houses, Gov. Forbes", "Street View"),
    (4, 3 * STEP, "14°37'05.57\"N", "120°59'16.73\"E", 4.00, 2, "House, Becerra St.", "Street View"),
    (5, 4 * STEP, "14°37'17.01\"N", "120°59'16.37\"E", 3.46, 2, "Houses, Elias St.", "Street View"),
    (6, 5 * STEP, "14°37'28.46\"N", "120°59'16.02\"E", 3.86, 2, "House, Elias St.", "Street View"),
    (7, 2000.0, "14°37'36.27\"N", "120°59'15.78\"E", 6.92, 8, "Chinese General Hospital", "Estimate, partial view"),
    (8, 7 * STEP, "14°37'51.35\"N", "120°59'15.31\"E", 8.31, 2, "Houses near cemetery", "Satellite estimate"),
    (9, 8 * STEP, "14°38'02.80\"N", "120°59'14.95\"E", 11.92, 2, "Houses", "Satellite estimate"),
    (10, 9 * STEP, "14°38'14.25\"N", "120°59'14.60\"E", 14.86, 0, "La Loma Cemetery", "Street View"),
    (11, 10 * STEP, "14°38'25.69\"N", "120°59'14.24\"E", 15.08, 2, "Houses", "Satellite estimate"),
    (12, 11 * STEP, "14°38'37.14\"N", "120°59'13.89\"E", 15.31, 2, "Low-rise beside warehouse", "Satellite estimate"),
    (13, 12 * STEP, "14°38'48.59\"N", "120°59'13.53\"E", 16.96, 4, "Building, 4th St.", "Street View"),
    (14, 13 * STEP, "14°39'00.03\"N", "120°59'13.18\"E", 16.59, 2, "Warehouse, 9th Ave.", "Street View"),
    (15, 14 * STEP, "14°39'11.48\"N", "120°59'12.82\"E", 16.89, 5, "Building, 11th Ave.", "Street View"),
    (16, 15 * STEP, "14°39'22.93\"N", "120°59'12.47\"E", 19.94, 2, "Low-rise structure", "Satellite estimate"),
    (17, 16 * STEP, "14°39'34.37\"N", "120°59'12.11\"E", 20.08, 4, "MCU Grade School Bldg.", "Satellite estimate"),
    (18, 17 * STEP, "14°39'45.82\"N", "120°59'11.76\"E", 17.27, 3, "Townhouses", "Satellite estimate"),
    (19, 18 * STEP, "14°39'57.27\"N", "120°59'11.40\"E", 10.62, 0, "Open lot", "Satellite estimate"),
    (20, D_M, "14°40'08.72\"N", "120°59'11.05\"E", 4.97, 6, "Site B: Fini Homes", "Street View"),
]


def profile(floor_override=None):
    rows = []
    for n, d1m, lat, lon, ground, floors, desc, ev in POINTS:
        if floor_override and n in floor_override:
            floors = floor_override[n]
        d1, d2 = d1m / 1000, (D_M - d1m) / 1000
        obstruction = floors * FLOOR
        elev = ground + obstruction
        bulge = d1 * d2 / 12.75
        f1 = 17.3 * math.sqrt(d1 * d2 / (FC_GHZ * (d1 + d2)))
        f60 = 0.6 * f1
        rows.append(dict(n=n, d1=d1, d2=d2, lat=lat, lon=lon, ground=ground, floors=floors,
                         obstruction=obstruction, elev=elev, bulge=bulge, f1=f1, f60=f60,
                         the=elev + bulge + f60, desc=desc, evidence=ev))
    return rows


def db(x):
    return 10 * math.log10(x)


LAMBDA = C / FC_HZ
AD_LIN = (math.pi * DIA / LAMBDA) ** 2
AD_DB = db(AD_LIN)
THETA = 70 * LAMBDA / DIA
AP_THEORY = AD_DB + db(0.55)

FSL = 20 * math.log10(4 * math.pi / C) + 20 * math.log10(FC_HZ) + 20 * math.log10(D_M)
PIN = db(2000)
ANT_GAIN = 44.0            # VHLP6-11W/A mid band, closest listed band
INSTALL = 0.0              # not listed, guideline default
WG_DB_M = 2.995 / 30.48    # ATM WR-90 copper, 12.4 GHz value is the closest listed
HORIZ = 3.0
CONN_ANT = 0.2             # FMWCA1107 max
CONN_AMP = 0.3             # FMWCA1025 typ
LNA_GAIN = 30.0            # LNA-30-08001200-15-15P min
LNA_NF = 1.5               # max
LNA_P1DB = 15.0
LNA_MAX_IN = 13.0
T = 290.0
BW = 2.5e6
SNR = 10.0
A_FACTOR = 1.0
B_FACTOR = 0.5
FIBER_DB_KM = 0.22
ROAD_KM = 8.9


def link(rows):
    hmin = max(r["the"] for r in rows)
    gov = max(rows, key=lambda r: r["the"])["n"]
    ta, tb = hmin - rows[0]["elev"], hmin - rows[-1]["elev"]
    la, lb = ta + HORIZ, tb + HORIZ
    wga, wgb = la * WG_DB_M, lb * WG_DB_M
    conn = 2 * (CONN_ANT + CONN_AMP)
    gt = 2 * ANT_GAIN + LNA_GAIN - wga - wgb - conn - 2 * INSTALL
    rsl_out = PIN + gt - FSL
    rsl_in = rsl_out - LNA_GAIN
    # same chain, simulated dish, theoretical AD used only as a stand-in until MATLAB is run
    gt_ref = 2 * AP_THEORY + LNA_GAIN - wga - wgb - conn - 2 * INSTALL
    rsl_ref = PIN + gt_ref - FSL
    n_dbm = db(K * T * BW / 1e-3)
    pth = n_dbm + SNR + LNA_NF
    fm = rsl_out - pth
    fm_in = rsl_in - pth
    base = 30 * math.log10(D_KM) + db(6 * A_FACTOR * B_FACTOR * FC_GHZ) - 70
    theo = {r: base - db(1 - r / 100) for r in (99, 99.9, 99.99, 99.999)}
    unrel = 10 ** ((base - fm) / 10)
    unrel_in = 10 ** ((base - fm_in) / 10)
    fiber_len = ROAD_KM + (rows[0]["obstruction"] + rows[-1]["obstruction"]) / 1000
    fiber = fiber_len * FIBER_DB_KM
    micro_loss = FSL + wga + wgb + conn + 2 * INSTALL
    return dict(hmin=hmin, governing=gov, tower_a=ta, tower_b=tb, len_a=la, len_b=lb, wg_a=wga, wg_b=wgb,
                conn=conn, g_total=gt, rsl_out=rsl_out, rsl_in=rsl_in, rsl_ref=rsl_ref, n=n_dbm, pth=pth,
                fm=fm, fm_in=fm_in, fm_base=base, fm_theory={str(k): v for k, v in theo.items()},
                unreliability=unrel, unreliability_in=unrel_in, fiber_len=fiber_len, fiber_loss=fiber,
                micro_loss=micro_loss, p1db_ok=rsl_out <= LNA_P1DB, input_ok=rsl_in <= LNA_MAX_IN)


main_rows = profile()
alt_rows = profile({2: 0})
main = link(main_rows)
alt = link(alt_rows)
common = dict(lam=LAMBDA, ad_lin=AD_LIN, ad_db=AD_DB, theta=THETA, ap_theory=AP_THEORY, fsl=FSL, pin=PIN,
              wg_db_m=WG_DB_M, d_m=D_M, d_km=D_KM, fc=FC_GHZ)
json.dump(dict(common=common, rows=main_rows, main=main, alt=alt, alt_rows=alt_rows),
          open(os.path.join(OUT, "results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"lambda {LAMBDA:.6f} m  AD {AD_LIN:.4f} = {AD_DB:.4f} dBi  theta {THETA:.4f} deg  Ap(55%) {AP_THEORY:.4f}")
print(f"FSL {FSL:.4f}  Pin {PIN:.4f}  WG {WG_DB_M:.5f} dB/m")
print("pt   d1     d2    elev    bulge   .6F1    THE")
for r in main_rows:
    print(f"{r['n']:2d} {r['d1']:.4f} {r['d2']:.4f} {r['elev']:8.4f} {r['bulge']:.4f} {r['f60']:.4f} {r['the']:8.4f}")
for name, L in (("MAIN", main), ("ALT (Pacific Icon off line)", alt)):
    print("\n" + name)
    for k, v in L.items():
        print(f"  {k}: {v if not isinstance(v, float) else format(v, '.4f')}")
    print(f"  unreliability exact: {L['unreliability']:.3e}, input-referred {L['unreliability_in']:.3e}")

# independent checks
assert abs(main_rows[0]["bulge"]) < 1e-9 and abs(main_rows[-1]["f60"]) < 1e-9
assert abs(FSL - (32.44 + 20 * math.log10(FC_GHZ * 1000) + 20 * math.log10(D_KM))) < 0.02
assert abs(main["tower_a"] - (main["hmin"] - 32.16)) < 1e-9
assert abs(main["fm"] - main["fm_in"] - LNA_GAIN) < 1e-9
print("\nchecks passed")

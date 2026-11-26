"""Section 3 link budget (Frassati to Metro Industries), following the ECE21129 guideline Part 2 items 6 to 13.

Reads the Section 2 results (results_M.json) for D and the tower heights, so rerun metro_calc.py first.
Writes results_S3.json. Every equipment value below comes from a spec sheet in ../specs or the ATM waveguide table.
"""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
S2 = json.load(open(os.path.join(HERE, "results_M.json"), encoding="utf-8"))
M = S2["main"]

# ---------------- given (guideline) ----------------
C0 = 3e8                  # speed of light (m/s)
F_GHZ = 10.59625          # assigned center frequency, 4ECE-B Group 5
P_IN_W = 2.0              # input signal power (guideline item 7)
SNR_DB = 10.0             # minimum SNR at the receiver front end (guideline item 10)
K_B = 1.38e-23            # Boltzmann constant (J/K)
T_K = 290.0               # standard noise temperature (amplifier NF is specified at 290 K)
BW_HZ = 2.5e6             # channel bandwidth: 4ECE-B assigned channels are 2.5 MHz apart (NTC channel plan)
HORIZ_M = 3.0             # horizontal waveguide run to the cabinet (guideline item 2)
A_FACTOR, B_FACTOR = 1.0, 0.5   # average terrain; hot humid area (M03B lecture table)
RELIABILITY = [0.99, 0.999, 0.9999, 0.99999]

# ---------------- equipment (spec sheets) ----------------
ANT_GAIN = 44.0           # ANDREW VHLP6-11W-6WH/A, Gain Mid Band (10.000-11.700 GHz band)
ANT_INSTALL = 0.0         # not given on the sheet -> 0 dB (guideline item 1)
WG_DB_PER_100FT = 2.995   # ATM WR-90 copper (RG-52/U), theoretical attenuation at 12.4 GHz end (closest to fc)
WG_DB_PER_M = WG_DB_PER_100FT / 30.48
AMP_GAIN, AMP_NF = 25.0, 2.2          # ERZIA ERZ-LNA-0800-1220-26-2: min gain, max NF (worst case)
AMP_P1DB_MIN = 20.0                    # dBm, min output P1dB
CONN_ANT = 0.9            # Pasternack PE-W90SF006-12 WR-90 flexible section, CPR-90G both ends, max insertion loss
CONN_WG2COAX = 0.3        # Fairview FMWCA1025 WR-90 (UG-135/U) to SMA female, typ insertion loss
CONN_SMA = 0.21           # Fairview FMAD1245 SMA male-male, max insertion loss
CONN_PER_SITE = CONN_ANT + CONN_WG2COAX + CONN_SMA
FIBER_DB_PER_KM = 0.22    # Prysmian G.652.D, max attenuation at 1550 nm
ROAD_KM = 9.2             # Google Maps shortest road route (via R-9), Frassati pin to Metro Industries

# ---------------- simulated antenna (Section 1) ----------------
SIM_DMAX = 42.2339        # dBi, MATLAB Antenna Designer
EFF = 0.55


def db(x):
    return 10 * math.log10(x)


D_M = S2["common"]["d_m"]
D_KM = D_M / 1000
f_hz = F_GHZ * 1e9

fsl_terms = (20 * math.log10(4 * math.pi / C0), 20 * math.log10(f_hz), 20 * math.log10(D_M))
fsl = sum(fsl_terms)
p_in = db(P_IN_W * 1000)

tower_a, tower_b = M["tower_a"], M["tower_b"]
len_a, len_b = tower_a + HORIZ_M, tower_b + HORIZ_M
wg_a, wg_b = len_a * WG_DB_PER_M, len_b * WG_DB_PER_M
conn = 2 * CONN_PER_SITE
install = 2 * ANT_INSTALL


def total_gain(g_ant):
    return 2 * g_ant + AMP_GAIN - wg_a - wg_b - conn - install


g_total = total_gain(ANT_GAIN)
rsl = p_in + g_total - fsl
sim_gain = SIM_DMAX + db(EFF)
g_total_sim = total_gain(sim_gain)
rsl_sim = p_in + g_total_sim - fsl

ktb = K_B * T_K * BW_HZ
n_dbm = db(ktb / 1e-3)
p_th = n_dbm + SNR_DB + AMP_NF
fm = rsl - p_th
fm_sim = rsl_sim - p_th

base_terms = (30 * math.log10(D_KM), db(6 * A_FACTOR * B_FACTOR * F_GHZ), -70.0)
base = sum(base_terms)
fm_theory = [dict(R=R, term=-db(1 - R), fm=base - db(1 - R), meets=fm >= base - db(1 - R)) for R in RELIABILITY]
unrel = 10 ** ((base - fm) / 10)

micro_loss = fsl + wg_a + wg_b + conn + install
elev_a, elev_b = S2["rows"][0]["obstruction"], S2["rows"][-1]["obstruction"]   # building heights (m)
fiber_len = ROAD_KM + (elev_a + elev_b) / 1000
fiber_loss = fiber_len * FIBER_DB_PER_KM

# amplifier sanity checks
rsl_amp_in = rsl - AMP_GAIN
assert rsl < AMP_P1DB_MIN, "LNA would be driven past P1dB"
assert abs(tower_a - 2.5) < 1e-9 and abs(D_M - 6927.0111) < 1e-3

R = dict(
    given=dict(c=C0, f_ghz=F_GHZ, p_in_w=P_IN_W, snr=SNR_DB, k=K_B, T=T_K, B=BW_HZ, horiz=HORIZ_M, A=A_FACTOR, Bf=B_FACTOR),
    equip=dict(ant_gain=ANT_GAIN, ant_install=ANT_INSTALL, wg_db_100ft=WG_DB_PER_100FT, wg_db_m=WG_DB_PER_M, amp_gain=AMP_GAIN,
               amp_nf=AMP_NF, amp_p1db=AMP_P1DB_MIN, conn_ant=CONN_ANT, conn_wg=CONN_WG2COAX, conn_sma=CONN_SMA,
               conn_site=CONN_PER_SITE, fiber_db_km=FIBER_DB_PER_KM, road_km=ROAD_KM),
    d_m=D_M, d_km=D_KM, tilt=M["tilt_deg"], fsl_terms=fsl_terms, fsl=fsl, p_in=p_in, tower_a=tower_a, tower_b=tower_b, len_a=len_a, len_b=len_b,
    wg_a=wg_a, wg_b=wg_b, conn=conn, install=install, g_total=g_total, rsl=rsl, rsl_amp_in=rsl_amp_in,
    sim_dmax=SIM_DMAX, sim_gain=sim_gain, g_total_sim=g_total_sim, rsl_sim=rsl_sim, ktb=ktb, n_dbm=n_dbm, p_th=p_th,
    fm=fm, fm_sim=fm_sim, base_terms=base_terms, base=base, fm_theory=fm_theory, unrel=unrel,
    micro_loss=micro_loss, elev_a=elev_a, elev_b=elev_b, fiber_len=fiber_len, fiber_loss=fiber_loss,
)
json.dump(R, open(os.path.join(HERE, "results_S3.json"), "w", encoding="utf-8"), indent=1)

f4 = lambda x: f"{x:.4f}"
print(f"D {f4(D_KM)} km  FSL {f4(fsl)} dB  Pin {f4(p_in)} dBm")
print(f"WG A {f4(len_a)} m -> {f4(wg_a)} dB, B {f4(len_b)} m -> {f4(wg_b)} dB; connectors {f4(conn)} dB")
print(f"G_total {f4(g_total)} dB  RSL {f4(rsl)} dBm (amp input {f4(rsl_amp_in)})  RSL_sim {f4(rsl_sim)} dBm (G_sim {f4(sim_gain)})")
print(f"N {f4(n_dbm)} dBm  PRth {f4(p_th)} dBm  FM {f4(fm)} dB  FM_sim {f4(fm_sim)} dB")
print("theory:", ", ".join(f"{x['R']*100:g}% {f4(x['fm'])}" for x in fm_theory), f" 1-R = {unrel:.4e}")
print(f"microwave loss {f4(micro_loss)} dB  fiber {f4(fiber_len)} km -> {f4(fiber_loss)} dB")

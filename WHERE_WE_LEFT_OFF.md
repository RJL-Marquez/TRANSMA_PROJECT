# Where we left off (November 26, 2026)

## 1. Decisions so far

- **Site A:** UST Saint Pier Giorgio Frassati Building rooftop, the group's pin 14°36'32.71"N 120°59'31.75"E, ground 2.47 m, 23 floors (59.97 m rooftop). Antenna sits on the roof, no tower.
- **Site B:** Metro Industries, 84 Ramon Delfin St, Marulas, Valenzuela, 14°40'17.32"N 120°59'12.63"E, ground 10.98 m, **5 floors assumed** (the group's doc still says "TBC"). In Google Earth this pin is named `DRAFT-01`.
- **Tilted mounting** (guideline Part 3, item 9), because equal antenna heights would need a 36.4900 m tower at Site B. Justified by the ANDREW VHLP6-11W/A mount's ±5° fine elevation adjustment and the 1° beamwidth.
- **20 points are not evenly spaced on purpose.** They start from D/19 = 364.58 m and each one slides up to 30 m along the line onto the tallest nearby roof, as the guideline asks ("favor obviously tall infrastructure while keeping spacing relatively even"). Tables use each point's real d1.
- Earlier candidates (Fini Homes and BGPOP) are kept as history in `report/` and `notes/`; they are no longer the main design.

## 2. Current numbers (Frassati to Metro Industries)

| Item | Value |
|---|---|
| D | 6927.01 m |
| Antenna height A / B | 59.9700 m / 29.1511 m |
| Tower A / B | 0.0000 m / 5.6711 m |
| Tilt | 0.2549° |
| What sets the tilt | P17 (white mid-rise north of EDSA, clearance 0.0000 m) and the LRT-1 viaduct (clearance 0.1660 m) |
| Waveguide length A / B (tower + 3 m) | 3.0000 m / 8.6711 m |
| Waveguide loss A / B (WR-90, 0.0983 dB/m) | 0.2948 dB / 0.8520 dB |
| Connectors (both sites) | 1.4200 dB (FMWCA1107 0.2 dB, FMWCA1025 0.3 dB, FMAD1245 0.21 dB per site) |
| FSL | 129.7557 dB |
| Total gain | 110.4332 dB |
| RSL at amplifier output | 13.6878 dBm (amplifier input -11.3122 dBm) |
| Receiver sensitivity | -97.7978 dBm |
| Fade margin | 111.4856 dB |
| Microwave system loss | 132.3225 dB |
| Fiber loss | 1.9734 dB (uses the 8.9 km road length from the old Fini route; recheck) |

Equipment: ANDREW VHLP6-11W/A antenna, WR-90 waveguide, ERZIA ERZ-LNA-0800-1220-26-2 amplifier (25 dB gain, 2.2 dB NF), Fairview FMWCA1107 / FMWCA1025 waveguide adapters, FMAD1245 SMA male-male adapter, 2 W input. MATLAB (R2025b, MoM-PO): Dmax 42.2339 dBi at az 270° (−90°), el 0°; HPBW 1.16° (az), 0.92° (el); simulated power gain at 55% efficiency 39.6375 dBi.

## 3. Still to do

1. **Confirm three heights in Street View** (they are guesses, taken on the high side):
   - Metro Industries floors (5 assumed). Each extra floor shortens the mast by 2.5 m, and each floor fewer lengthens it by 2.5 m.
   - P17 white building at 14°39'41.60"N 120°59'15.69"E (4 floors assumed).
   - LRT-1 viaduct on EDSA at 14°39'26.30"N 120°59'17.00"E (12.5 m with a train assumed).

   Site B mast for each case (Metro Industries at 5 floors):

   | P17 floors | Viaduct 10 m | Viaduct 12.5 m | Viaduct 15 m |
   |---|---|---|---|
   | 3 | 2.6982 m | 5.4563 m | 8.6913 m |
   | 4 | 5.6711 m | 5.6711 m (current) | 8.6913 m |

   After changing a value in `work/metro_pts.json` or the `EXTRAS` list in `work/metro_calc.py`, rerun the scripts (section 5).
2. **Section 3 (link budget) is not filled for Metro Industries yet.** Use the numbers above. Recheck the fiber road distance.
3. **Handwritten computations** for Sections 2 and 3 (the red reminders are still in the doc). Four decimal places, metric units.
4. **Section 1 fixes still in the group's doc:** 46.0124 should be 46.0127 dBi; frequency range 10.09325–11.09325 GHz should be 10.09625–11.09625 GHz; experimental beamwidth 1.2° vs simulated 1.16° (az) / 0.92° (el); use 42.2339 dBi consistently; add MATLAB version and PC specs; add the 3D view; recompute the error percentages.
5. Executive summary, conclusion (at least 250 words), and the specification sheet appendix (`specs/`).
6. **Member Attestation** still says no AI was used. Update it to match what the professor allowed before anyone signs. The AI log is `notes/AI_Use_Log_ECE21129.md`.
7. Final submission: `4ECEB_Group5_Report.pdf` and `4ECEB_Group5_Antenna.mat` (in `report/`).

## 4. Google Earth

- Project **TRANSMA SHIFTED** (in the Google Drive account used in Earth): `FRASSATI`, `M2` to `M19`, `DRAFT-01` (= Metro Industries), and `LRT EDSA`. Hidden: `D2` to `D11` (old even-spaced trace), `FINI HOMES`, and two `Untitled placemark` entries. There is a duplicate `D7` at D6's location that can be deleted.
- Project **TRANSMA**: the older Fini Homes and BGPOP traces.
- Read ground elevation from a saved placemark's "Ground elevation" field, not from the URL altitude.

## 5. How to rerun the scripts

```powershell
cd work
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python metro_calc.py          # path profile, tilt, towers, link budget -> results_M.json
.venv\Scripts\python plot_m.py              # path_profile_M.png
.venv\Scripts\python overlay_pattern_m.py   # map_overlay_M.png
.venv\Scripts\python build_sec2_m.py "<group export>.docx" "<output>.docx"   # fills Section 2
.venv\Scripts\python write_md_m.py          # Section 2 Markdown (edit the output path inside first)
```

Notes: `metro_calc.py` reuses the formulas in `option_data.py` and `draft_points.py`; importing `draft_points.py` rewrites `draft_points.csv/json` (harmless). `write_md_m.py` writes to `C:\UST\TRANSMA PROJECT`, so change that path on a new laptop. The MATLAB simulation is `work/matlab/sim_antenna.m` (about 12 minutes on an i5-9400).

## 6. Point data (current)

| Point | d1 (km) | Ground (m) | Floors | THE (m) | What is there |
|---|---|---|---|---|---|
| 1 | 0.0000 | 2.47 | 23 | 59.9700 | Frassati Building rooftop (group pin) |
| 2 | 0.3556 | 2.55 | 6 | 19.5854 | mid-rise block east of the tall towers, satellite estimate |
| 3 | 0.7472 | 2.74 | 3 | 13.2056 | low-rise residential, satellite estimate |
| 4 | 1.0837 | 3.55 | 3 | 14.5955 | commercial building east of the highway, satellite estimate |
| 5 | 1.4833 | 3.52 | 3 | 15.0961 | low-rise residential, satellite estimate |
| 6 | 1.8029 | 4.79 | 3 | 16.6971 | low-rise block north of the Maranatha/PMCC tower, satellite estimate |
| 7 | 2.1995 | 6.68 | 2 | 16.4024 | low-rise beside A. Bonifacio Ave, satellite estimate |
| 8 | 2.5381 | 10.78 | 0 | 15.6974 | La Loma Cemetery, open ground |
| 9 | 2.9376 | 14.70 | 1 | 22.2668 | cemetery mausoleum, about one storey |
| 10 | 3.2542 | 13.48 | 3 | 26.1060 | three-storey row house, satellite estimate |
| 11 | 3.6158 | 15.69 | 2 | 25.8213 | houses at the east edge of the cemetery, satellite estimate |
| 12 | 4.0174 | 17.33 | 3 | 29.8891 | three-storey block south of the warehouses, satellite estimate |
| 13 | 4.3600 | 18.17 | 3 | 30.6011 | beside a tall warehouse west of Caloocan City Hall; warehouse counted as 3 floors |
| 14 | 4.7645 | 17.59 | 4 | 32.2871 | commercial building near CAI Sports Center, satellite estimate (taken high) |
| 15 | 5.0921 | 18.15 | 3 | 30.0863 | line follows a street here; the street-front buildings (about 3 floors) are counted |
| 16 | 5.4777 | 19.63 | 3 | 31.1664 | row houses east of MCU Hospital, satellite estimate |
| 17 | 5.8253 | 20.48 | 4 | 34.0527 | white mid-rise north of EDSA, satellite estimate (taken high) |
| 18 | 6.1729 | 11.63 | 3 | 22.1091 | large house in a gated subdivision, satellite estimate |
| 19 | 6.5424 | 3.63 | 2 | 10.7492 | two-storey house south of the Tullahan River, satellite estimate |
| 20 | 6.9270 | 10.98 | 5 | 23.4800 | Metro Industries, 84 Ramon Delfin St (Site B) |

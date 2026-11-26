# Where we left off (November 26, 2026, evening)

Due **November 27, 2026**. Submit `4ECEB_Group5_Report.pdf` and `4ECEB_Group5_Antenna.mat`.

## 1. Where we stopped

- **Section 2 write-up (in the group's Google Doc):** Marquez rewrote the Table 2 discussion in his own words, added a new **Figure 2.1** (Google Earth ruler: 6,927 m, heading 355.3°, with the elevation profile) and **Figure 2.2** (the 20 pins). The next thing to write is the **Figure 2.2 discussion** (how the pins were spaced: D/19 = 364.58 m, then moved up to 30 m onto the tallest nearby roof after checking satellite and Street View), then an optional **Table 2.1** (point, coordinates, picture, notes; coordinates and notes were drafted in the chat), then the **radiation overlay (now Figure 2.3)** and the **reflection question** (azimuth pattern).
  - Fix in the Google Doc: the Site B paragraph still says 5 floors / 12.5 m; it is now 6 floors at the pin, (5 + 1) × 2.5 = 15 m. "was able to estimate … 6.927 kilometers" should read "measured … 6.9270 km". Figure 2.2 must show all 20 pins including FRASSATI. Adding the ruler figure shifted the numbers: overlay is Figure 2.3, path profile is Figure 2.4.
- **Handwritten computations:** split among the members in `report/4ECEB_Group5_Section2_Task_Distribution.docx` (checklist, each member's solutions to copy, scan boxes). Not written yet.
- **Section 3:** a full draft exists as a separate file, `report/4ECEB_Group5_Section3_DRAFT.docx`. It has not been put into the main report.

## 2. What changed today (November 26)

1. **Site B moved to Metro Industries** (84 Ramon Delfin St, Marulas), the group's pin. Section 2 tables filled in `report/4ECEB_Group5_Report_Metro_Section2.docx`.
2. **2.5 m safety margin** (one floor) kept above every THE and added to both antennas, because P17 and the LRT-1 viaduct heights are estimates.
3. **Earth bulge fixed to the guideline formula d1·d2 / (12.75k), k = 4/3** (the first version divided by 12.75 only). Every bulge and THE value changed; 0.6F1 did not.
4. **Site B counted as 6 floors at the pin:** a 5-storey building (Street View, May 2026) plus the 1-storey rooftop structure the pin and mast sit on. Only P20, the Site B mast and the waveguide length changed.
5. **Tower section shortened:** h_B is found from P17 only (one line), and the proof is a 2-row clearance check (P17 and the LRT viaduct) plus the path profile figure. The 20-row h_B table and the 22-row Table 4.1 were removed.
6. **Path profile redrawn** by a standalone script (`work/section2_path_profile.py`): zoom box on P17 and the viaduct, legend below, no margin line.
7. **Section 3 drafted** against guideline items 1 to 13 (see section 4 below).
8. **Cleanup:** the old Fini Homes / BGPOP report drafts and the stale preview PDF were deleted (still in git history).

## 3. Section 2 numbers (final)

| Item | Value |
|---|---|
| D | 6.9270 km (6927.0111 m), heading 355.2621° (A to B), 175.2621° (B to A) |
| Point spacing | D / 19 = 364.58 m, each pin then moved up to 30 m onto the tallest nearby roof |
| Highest THE | 59.9700 m at P1 (Frassati roof) |
| Antenna height A / B | 62.4700 m / 31.5014 m (tilted, THE + 2.5 m margin) |
| Mast A / B | 2.5000 m / 5.5214 m (equal heights would need 36.4900 m at Site B) |
| Tilt | 0.2562°, set by P17 (exactly 2.5000 m above THE); LRT-1 viaduct next at 2.7155 m; every other point clears by 6.9701 m or more |
| Justification | ANDREW mount has ±5° fine elevation adjustment; 0.2562° is less than half the 1° beamwidth |

## 4. Section 3 draft (`report/4ECEB_Group5_Section3_DRAFT.docx`)

Computed by `work/section3_calc.py` into `work/results_S3.json`. Guideline: `D:\Downloads\ECE21129_Design_Project_Guidelines.pdf` (old version; the only change in the new one is that AI use is now allowed).

| Part | Choice | Value used |
|---|---|---|
| Antenna | ANDREW VHLP6-11W-6WH/A, 1.8 m, CPR90G flange | 44 dBi (mid band, closest to fc), 0 dB installation loss |
| Waveguide | WR-90 copper RG-52/U (ATM table, cited in lecture M05A) | 2.995 dB/100 ft = 0.0983 dB/m; A 5.5000 m, B 8.5214 m |
| Amplifier | ERZIA ERZ-LNA-0800-1220-26-2 (Site B only) | 25 dB gain (min), 2.2 dB NF (max) |
| Antenna to waveguide | Pasternack PE-W90SF006-12 flexible section, CPR-90G both ends | 0.9 dB max |
| Waveguide to amplifier | Fairview FMWCA1025 + FMAD1245 | 0.3 + 0.21 dB |

| Result | Value |
|---|---|
| FSL | 129.7557 dB |
| Total gain | 108.8022 dB |
| RSL (output of Site B amplifier, 2 W input) | 12.0568 dBm (simulated antenna: 3.3319 dBm) |
| Receiver sensitivity (T = 290 K, B = 2.5 MHz, SNR 10 dB) | −97.7978 dBm |
| Fade margin | 109.8546 dB (simulated antenna: 101.1297 dB) |
| Theoretical FM (A = 1, B = 0.5) | −9.7609 / 0.2391 / 10.2391 / 20.2391 dB at 99 / 99.9 / 99.99 / 99.999%; all met |
| Microwave loss vs fiber | 133.9535 dB vs 2.0399 dB (G.652.D, 0.22 dB/km, 9.2 km road via R-9 + 72.5 m building heights) |

Still needed for Section 3: three spec sheets for the appendix (ATM WR-90 table rows, VHLP6-11W-6WH/A product page, PE-W90SF006-12 data sheet), the handwritten computations, and copying the draft into the main report in the group's words.

## 5. Still to do

1. Finish the Section 2 write-up (section 1 above), then the handwritten pages, scanned and inserted with figure numbers and captions; delete the red reminders.
2. Optional: confirm P17 (4 floors) and the LRT viaduct (12.5 m) in Street View. Site B mast for other cases:

   | P17 floors | Viaduct 10 m | Viaduct 12.5 m | Viaduct 15 m |
   |---|---|---|---|
   | 3 | 2.5486 m | 5.2425 m | 8.4775 m |
   | 4 | 5.5214 m | 5.5214 m (current) | 8.4775 m |

3. Section 3 into the main report (section 4 above).
4. Section 1 fixes still in the group's doc: 46.0124 should be 46.0127 dBi; frequency range should be 10.09625–11.09625 GHz; experimental beamwidth 1.2° vs simulated 1.16° (az) / 0.92° (el); use 42.2339 dBi consistently; add the MATLAB version and PC specs; add the 3D view; recompute the error percentages.
5. Introduction, conclusion (at least 250 words), specification sheet appendix (`specs/`), references.
6. Member Attestation: update the AI sentence to match what the professor now allows. AI log: `notes/AI_Use_Log_ECE21129.md`.
7. Export `4ECEB_Group5_Report.pdf`; submit it with `4ECEB_Group5_Antenna.mat`.

## 6. Files

| File | What it is |
|---|---|
| `report/4ECEB_Group5_Report_Metro_Section2.docx` | Group export with Section 2 tables, figures and text filled (final numbers) |
| `report/4ECEB_Group5_Report_group_latest_export.docx` | The group's export that the Section 2 builder starts from |
| `report/4ECEB_Group5_Section2_Task_Distribution.docx` | Handwritten-solution split, checklist, solutions to copy, scan boxes |
| `report/4ECEB_Group5_Section3_DRAFT.docx` | Section 3 draft with a guideline compliance checklist |
| `report/Section2_Metro_Text.md`, `Section2_Metro_Industries.md` | Section 2 text for Google Docs (without / with figures) |
| `report/Section 3 ideas.docx` | The group's own Section 3 notes |
| `figures/path_profile_M.png` | Path profile (also in `report/` and `work/`) |

Handwritten task split (`4ECEB_Group5_Section2_Task_Distribution.docx`): Marquez MQ-1 to MQ-6 (Table 2); Dimalanta DM-1 to DM-11 (formulas, P1 to P10); Cabatian CB-1 to CB-11 (formulas, P11 to P20); Rocero RC-1 to RC-7 (Maranatha tower, LRT viaduct, Table 3 copy, margin, equal-height comparison, h_B from P17, tilt angle); Manuel MN-1 to MN-3 (tower heights, Table 4, 2-row clearance check).

## 7. How to regenerate everything

```powershell
cd work
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python metro_calc.py                 # Section 2 numbers -> results_M.json
.venv\Scripts\python section2_path_profile.py      # path_profile_M.png (copy to figures/ and report/)
.venv\Scripts\python build_sec2_m.py "..\report\4ECEB_Group5_Report_group_latest_export.docx" "..\report\4ECEB_Group5_Report_Metro_Section2.docx"
.venv\Scripts\python write_md_m.py                 # report/Section2_Metro_Industries.md
.venv\Scripts\python section3_calc.py              # Section 3 numbers -> results_S3.json
cd docgen
npm install
..\.venv\Scripts\python gen_data.py                # sec2_steps.json
node build_tasks.js sec2_steps.json "..\..\report\4ECEB_Group5_Section2_Task_Distribution.docx"
node build_s3.js ..\results_S3.json "..\..\report\4ECEB_Group5_Section3_DRAFT.docx"
node build_solutions.js sec2_steps.json "<out>.docx"   # optional: full Section 2 answer key in one file
```

Inputs to edit: point floors and ground in `work/metro_pts.json`; near-line structures in `EXTRAS` in `work/metro_calc.py`; the margin in `MARGIN` (`metro_calc.py` and `section2_path_profile.py`); Section 3 equipment values at the top of `work/section3_calc.py`. Close the report in Word before rebuilding it. The MATLAB simulation is `work/matlab/sim_antenna.m` (about 12 minutes on an i5-9400).

## 8. Google Earth

- Project **TRANSMA SHIFTED**: `FRASSATI`, `M2` to `M19`, `DRAFT-01` (= Metro Industries), and `LRT EDSA`. Hidden: `D2` to `D11` (old even-spaced trace), `FINI HOMES`, two `Untitled placemark` entries, and a duplicate `D7`.
- Project **TRANSMA**: the older Fini Homes and BGPOP traces.
- Read ground elevation from a saved placemark's "Ground elevation" field, not the URL altitude.

## 9. Point data (current)

| Point | d1 (km) | Ground (m) | Floors | h_elevation (m) | Bulge (m) | 0.6F1 (m) | THE (m) | Clearance (m) | What is there |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0000 | 2.47 | 23 | 59.9700 | 0.0000 | 0.0000 | 59.9700 | 2.5000 | Frassati Building rooftop (group pin) |
| 2 | 0.3556 | 2.55 | 6 | 17.5500 | 0.1375 | 1.8521 | 19.5395 | 41.3407 | mid-rise block east of the tall towers, satellite estimate |
| 3 | 0.7472 | 2.74 | 3 | 10.2400 | 0.2716 | 2.6035 | 13.1151 | 46.0144 | low-rise residential, satellite estimate |
| 4 | 1.0837 | 3.55 | 3 | 11.0500 | 0.3725 | 3.0488 | 14.4713 | 43.1538 | commercial building east of the highway, satellite estimate |
| 5 | 1.4833 | 3.52 | 3 | 11.0200 | 0.4750 | 3.4428 | 14.9378 | 40.9008 | low-rise residential, satellite estimate |
| M | 1.6670 | 4.35 | 9 | 26.8500 | 0.5158 | 3.5876 | 30.9534 | 24.0639 | Maranatha/PMCC tower (9 floors, corner about 5 m east of the line) |
| 6 | 1.8029 | 4.79 | 3 | 12.2900 | 0.5434 | 3.6825 | 16.5159 | 37.8938 | low-rise block north of the Maranatha/PMCC tower, satellite estimate |
| 7 | 2.1995 | 6.68 | 2 | 11.6800 | 0.6117 | 3.9068 | 16.1985 | 36.4382 | low-rise beside A. Bonifacio Ave, satellite estimate |
| 8 | 2.5381 | 10.78 | 0 | 10.7800 | 0.6553 | 4.0437 | 15.4790 | 35.6439 | La Loma Cemetery, open ground |
| 9 | 2.9376 | 14.70 | 1 | 17.2000 | 0.6894 | 4.1476 | 22.0370 | 27.2999 | cemetery mausoleum, about one storey |
| 10 | 3.2542 | 13.48 | 3 | 20.9800 | 0.7031 | 4.1886 | 25.8717 | 22.0498 | three-storey row house, satellite estimate |
| 11 | 3.6158 | 15.69 | 2 | 20.6900 | 0.7043 | 4.1922 | 25.5865 | 20.7183 | houses at the east edge of the cemetery, satellite estimate |
| 12 | 4.0174 | 17.33 | 3 | 24.8300 | 0.6876 | 4.1423 | 29.6599 | 14.8495 | three-storey block south of the warehouses, satellite estimate |
| 13 | 4.3600 | 18.17 | 3 | 25.6700 | 0.6584 | 4.0533 | 30.3816 | 12.5961 | beside a tall warehouse west of Caloocan City Hall; warehouse counted as 3 floors |
| 14 | 4.7645 | 17.59 | 4 | 27.5900 | 0.6061 | 3.8890 | 32.0851 | 9.0843 | commercial building near CAI Sports Center, satellite estimate (taken high) |
| 15 | 5.0921 | 18.15 | 3 | 25.6500 | 0.5496 | 3.7034 | 29.9031 | 9.8017 | line follows a street here; the street-front buildings (about 3 floors) are counted |
| L | 5.3531 | 19.31 | 5 | 31.8100 | 0.4956 | 3.5167 | 35.8224 | 2.7155 | LRT-1 viaduct on EDSA with a train on it (about 12.5 m, taken as 5 floors) |
| 16 | 5.4777 | 19.63 | 3 | 27.1300 | 0.4670 | 3.4137 | 31.0107 | 6.9701 | row houses east of MCU Hospital, satellite estimate |
| 17 | 5.8253 | 20.48 | 4 | 30.4800 | 0.3775 | 3.0693 | 33.9268 | 2.5000 | white mid-rise north of EDSA, satellite estimate (taken high) |
| 18 | 6.1729 | 11.63 | 3 | 19.1300 | 0.2738 | 2.6140 | 22.0179 | 12.8550 | large house in a gated subdivision, satellite estimate |
| 19 | 6.5424 | 3.63 | 2 | 8.6300 | 0.1480 | 1.9219 | 10.6999 | 22.5210 | two-storey house south of the Tullahan River, satellite estimate |
| 20 | 6.9270 | 10.98 | 6 | 25.9800 | 0.0000 | 0.0000 | 25.9800 | 5.5214 | Metro Industries, 84 Ramon Delfin St (Site B): 5-storey block + 1-storey rooftop structure |

Clearance is the tilted line of sight minus THE (must be at least 2.5 m). M = Maranatha/PMCC tower, L = LRT-1 viaduct.

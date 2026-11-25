
Status as of 2026-11-24. Sites are **not final**.

Site A candidates:
- BGPOP: 14°36'31.23"N 120°59'17.80"E, ground 2.16 m, 12 floors (user's decision; mezzanine not counted; do not use the unverified 43 m height), rooftop 32.16 m. The line now leaves the roof left of the north-corner rooftop structure
- Frassati: 14°36'32.97"N 120°59'32.27"E, ground 2.54 m, 23 storeys (not confirmed in a readable UST document), rooftop 60.04 m

Site B candidates:
- Fini Homes (working Site B): 14°40'08.72"N 120°59'11.05"E, ground 4.97 m, 6 storeys (user confirmed), rooftop 19.97 m, 12.19 m tower if nothing exceeds BGPOP's rooftop. Saved line `FINI to BGPOP`: D = 6,687.72 m, heading 178.28°. Its graph distance is d2
- Use Google Earth's lengths: an earlier spherical-Earth calculation overstated distances by about 0.5%
- OLFU Basic Ed 1: 14°40'55.75"N 120°58'51.64"E, ground 19.65 m, 4 storeys, rooftop 29.65 m, 8,183.89 m from BGPOP
- Isabelle de Valenzuela is taken by another group

Draft computed 2026-11-24 for BGPOP to Fini (`4ECEB_Group5_Report_DRAFT.docx`): governing point P2 Pacific Icon Residences 2 (26 floors from one listing), hmin 69.7863 m, towers 37.6263 m (A) and 49.8163 m (B), FSL 129.4504 dB, RSL 11.3781 dBm, FM 109.8760 dB. Those original draft values are superseded by the connector fix below.

User decision 2026-11-24: **Option A = Frassati to Fini (main), Option B = BGPOP to Fini.** Files: `4ECEB_Group5_Report_OPTION_A_Frassati.docx`, `4ECEB_Group5_Report_OPTION_B_BGPOP.docx`, `Option_A_vs_B_Comparison.md`. The original DRAFT docx was left unchanged.

Option A: D = 6,661.37 m from coordinates (Earth line reads 6,660.58 m), hmin 60.04 m set by Frassati, towers 0 m and 40.07 m, ERZIA ERZ-LNA-0800-1220-26-2 (25 dB min, NF 2.2 max, P1dB +20, max input +10), RSL 10.6473 dBm, FM 108.4452 dB. The group confirmed Frassati's 23 storeys on 2026-11-25. Maranatha/PMCC tower (about 9 floors from Street View) touches the line near d1 = 1.663 km but does not govern.

Option B now includes the same connector fix: RSL 10.9581 dBm, FM 109.4560 dB. Both options add a 0.21 dB FMAD1245 SMA male-male adapter at each site because the waveguide adapter and amplifiers are all SMA female.

User chose tilted mounting for Option A on 2026-11-25: antennas 60.04 m (Frassati) and 23.3739 m (Fini), towers 0 m and 3.4039 m, tilt 0.3154 deg set by P18 (zero margin), RSL 14.2502 dBm, FM 112.0480 dB. Justified by the ANDREW mount's ±5° fine elevation adjustment. P15 to P18 floor counts are satellite estimates with ≤1.19 m margin.

Street View check 2026-11-25: a tall building under construction (green netting, May 2026 imagery) on the west side of Asuncion St, Caloocan, at about 14°39'35.1"N, 120°59'14.46"–15.21"E (d1 ≈ 5.623 km), sits about 3 m east of the Frassati–Fini line, inside 0.6F1. Counted 8 floors from the user's Street View screenshots; saved as pin `NEW BLDG 8F` (14°39'36.01"N, 120°59'14.29"E, ground 20.04 m, d1 = 5.6514 km). It now sets the Option A tilt: antennas 60.04/40.4727 m, Fini tower 20.5027 m, tilt 0.1683°, RSL 12.5700 dBm, FM 110.3679 dB (supersedes the 3.4039 m tilt). P18 townhouses are not visible in Street View (gated subdivision behind a wall).

**2026-11-26: Site B is now Metro Industries, 84 Ramon Delfin St, Marulas** (the group's doc; earlier pin name DRAFT-01, 14°40'17.32"N 120°59'12.63"E, ground 10.98 m, 5 floors assumed). Site A uses the group's Frassati pin 14°36'32.71"N 120°59'31.75"E, ground 2.47 m. D = 6,927.01 m. User wanted pins "not too perfect": points M2 to M19 in TRANSMA SHIFTED sit up to 30 m from even spacing, on the tallest nearby roof (data in scratchpad `metro_pts.json`, calc `metro_calc.py`, builder `build_sec2_m.py`). Tilted result: antennas 59.97/29.1511 m, Site B mast 5.6711 m, tilt 0.2549°, set by P17 (white mid-rise north of EDSA, 4 floors assumed) with the LRT-1 viaduct on EDSA (12.5 m assumed, pin `LRT EDSA`, d1 5.3531 km) at 0.166 m margin; flat method would need 36.49 m. RSL 13.6878 dBm, FM 111.4856 dB (ERZIA amp). Section 2 filled in `4ECEB_Group5_Report_Metro_Section2.docx`; Section 3 not filled. D2 to D11, FINI HOMES, and two Untitled placemarks are hidden in TRANSMA SHIFTED. Street View doesn't render in the built-in browser pane.

MATLAB run 2026-11-25 (R2025b Update 7, MoM-PO, about 12 min on i5-9400): Dmax 42.2339 dBi at az -90, el 0; HPBW 1.16 deg (az) and 0.92 deg (el); simulated AP 39.6375 dBi. Both option drafts now have Section 1 filled; only Option A has the radiation overlay. Scripts are in the scratchpad `matlab` folder.

In the TRANSMA project, BGPOP pin, P2 to P19, and `FINI to BGPOP` are hidden; F2 to F19 and `FINI to FRASSATI` are visible.

Earth reading method: use the Ground elevation field on a saved placemark, not the altitude in the URL.

Trace findings:
- BGPOP to Basic Ed 1 is blocked about 1.12 km from BGPOP by the high-rise complex beside SM San Lazaro (apparently Avida Towers San Lazaro, at least 18 floors), THE at least 52.76 m, combined towers at least 43.82 m
- BGPOP to Fini: clears Avida by about 12 m. Now passes visibly west of The Garden Suites tower at Chinese General Hospital, about 2 km from BGPOP (hospital reports 16 storeys), with its closest base corner about 4.5 m from the line (scaled from the user's 8.76 m ruler reading, about ±0.5 m), passing the 3.78 m requirement. Next step: collect ground elevation and floors at 20 evenly spaced points, 351.99 m apart
- Ridge of 15 to 20 m ground lies about 0.7 to 3.7 km from Fini, peak 20.44 m near 0.9 km
- Frassati to Basic Ed 1: 30.39 m tower if clear, not traced

**Why:** Google Earth returned HTTP 429 in the built-in browser after repeated reloads, so the trace stopped partway.

**How to apply:** Re-verify pins with the user before final calculations, since they move them. Do not hammer Google Earth with reloads. Related: [[ece21129-path-planning-rules]], [[ece21129-project-setup]].

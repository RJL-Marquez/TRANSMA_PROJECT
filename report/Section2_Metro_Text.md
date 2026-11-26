# Section 2. Path Planning (UST Frassati to Metro Industries)

## Site Locations

**Table 2. Site Information**

| | Site A | Site B |
|---|---|---|
| Area | Saint Pier Giorgio Frassati Building, España Boulevard, Sampaloc, Manila | Metro Industries, 84 Ramon Delfin St, Marulas, Valenzuela, Metro Manila |
| Map coordinates | 14°36'32.71"N 120°59'31.75"E | 14°40'17.32"N 120°59'12.63"E |
| Location description | A 23-storey building, with a rooftop | Roof of the 1-storey rooftop structure on the 5-storey Metro Industries building, Marulas (counted from Google Street View, May 2026) |
| Height of building | 23 × 2.5 m = 57.5 m | (5 + 1) × 2.5 m = 15 m |
| Ground elevation (Google Earth) | 2.47 m | 10.98 m |
| Distance between sites A and B | 6.9270 km | |
| List of obstructions on the straight-line path | White mid-rise north of EDSA (P17, 4 floors assumed), LRT-1 viaduct on EDSA (about 12.5 m with a train, between P15 and P16), Maranatha/PMCC tower (9 floors, about 5 m east of the line near d1 = 1.667 km), commercial buildings near CAI Sports Center (P14), warehouses near Caloocan City Hall (P12 to P13), and the cemetery and residential blocks from P8 to P11 | |

Discussion: Site A is on the rooftop of the 23-storey Saint Pier Giorgio Frassati Building, and Site B is on the rooftop of the Metro Industries building at 84 Ramon Delfin St, Marulas, Valenzuela. The straight-line distance between the sites is 6.9270 km. Building heights use 2.5 m per floor.

[Insert Figure 2.1 here]

*Figure 2.1: Straight-line path and the 20 points (FRASSATI, M2 to M19, and Site B) in Google Earth. The view is rotated so the path runs left to right; north is toward the left.*

Discussion: The 18 points between the sites start from an even spacing of D/19 = 364.58 m. Each point was then moved by up to 30 m along the line so that it sits on the tallest roof nearby, as the guideline asks, so the actual spacing is uneven. The table uses each point's actual distance from Site A. The LRT EDSA pin marks where the line crosses the LRT-1 viaduct; it is checked separately below.

[Insert Figure 2.2 here]

*Figure 2.2: Simulated azimuth patterns at both sites, each pointed at the other site, with the 6.9270 km distance*

Discussion: Each antenna's main lobe is pointed at the other site, so the maximum directive gain lies along the path.

Reflection question: The azimuth pattern is used for the overlay. Google Maps shows the horizontal plane, and the azimuth pattern is the cut in that same plane, so it shows how the beam is pointed from one site toward the other. The elevation pattern describes the vertical plane, which a flat map cannot show.

## Path Profile

[Insert Figure 2.3 here]

*Figure 2.3: Path profile showing all 20 points, THE, the near-line structures, and the tilted line of sight, with a zoom on the clearance at P17 and the LRT-1 viaduct*

Discussion: The ground rises from about 2.5 m near UST to about 20 m around EDSA (P16 and P17), drops to 3.63 m at the Tullahan River (P19), and rises again to 10.98 m at Site B. The dashed red line is the tilted line of sight from 62.4700 m at Frassati to 31.5014 m at Metro Industries. It stays at least 2.5 m (the safety margin) above THE at every point and at both near-line structures: 2.5000 m above the THE of P17 and 2.7155 m above the THE of the LRT-1 viaduct.

**Table 3. Path Profile: Elevation, Earth Bulge, and Fresnel Clearance**

| Point | d1 (km) | d2 (km) | Ground (m) | Floors | h_elevation (m) | h_earth bulge (m) | 0.6F1 (m) | THE (m) |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.0000 | 6.9270 | 2.47 | 23 | 59.9700 | 0.0000 | 0.0000 | 59.9700 |
| 2 | 0.3556 | 6.5714 | 2.55 | 6 | 17.5500 | 0.1375 | 1.8521 | 19.5395 |
| 3 | 0.7472 | 6.1798 | 2.74 | 3 | 10.2400 | 0.2716 | 2.6035 | 13.1151 |
| 4 | 1.0837 | 5.8433 | 3.55 | 3 | 11.0500 | 0.3725 | 3.0488 | 14.4713 |
| 5 | 1.4833 | 5.4437 | 3.52 | 3 | 11.0200 | 0.4750 | 3.4428 | 14.9378 |
| 6 | 1.8029 | 5.1241 | 4.79 | 3 | 12.2900 | 0.5434 | 3.6825 | 16.5159 |
| 7 | 2.1995 | 4.7275 | 6.68 | 2 | 11.6800 | 0.6117 | 3.9068 | 16.1985 |
| 8 | 2.5381 | 4.3889 | 10.78 | 0 | 10.7800 | 0.6553 | 4.0437 | 15.4790 |
| 9 | 2.9376 | 3.9894 | 14.70 | 1 | 17.2000 | 0.6894 | 4.1476 | 22.0370 |
| 10 | 3.2542 | 3.6728 | 13.48 | 3 | 20.9800 | 0.7031 | 4.1886 | 25.8717 |
| 11 | 3.6158 | 3.3112 | 15.69 | 2 | 20.6900 | 0.7043 | 4.1922 | 25.5865 |
| 12 | 4.0174 | 2.9096 | 17.33 | 3 | 24.8300 | 0.6876 | 4.1423 | 29.6599 |
| 13 | 4.3600 | 2.5670 | 18.17 | 3 | 25.6700 | 0.6584 | 4.0533 | 30.3816 |
| 14 | 4.7645 | 2.1625 | 17.59 | 4 | 27.5900 | 0.6061 | 3.8890 | 32.0851 |
| 15 | 5.0921 | 1.8349 | 18.15 | 3 | 25.6500 | 0.5496 | 3.7034 | 29.9031 |
| 16 | 5.4777 | 1.4493 | 19.63 | 3 | 27.1300 | 0.4670 | 3.4137 | 31.0107 |
| 17 | 5.8253 | 1.1017 | 20.48 | 4 | 30.4800 | 0.3775 | 3.0693 | 33.9268 |
| 18 | 6.1729 | 0.7541 | 11.63 | 3 | 19.1300 | 0.2738 | 2.6140 | 22.0179 |
| 19 | 6.5424 | 0.3846 | 3.63 | 2 | 8.6300 | 0.1480 | 1.9219 | 10.6999 |
| 20 | 6.9270 | 0.0000 | 10.98 | 6 | 25.9800 | 0.0000 | 0.0000 | 25.9800 |

(The Ground and Floors columns are extra, to show where h_elevation comes from; the group's template table has only d1, d2, h_elevation, h_earth bulge, 0.6F1, and THE.)

**Point locations and what is on each point**

| Point | Latitude | Longitude | What is there |
|---|---|---|---|
| 1 | 14°36'32.71"N | 120°59'31.75"E | Frassati Building rooftop (group pin) |
| 2 | 14°36'44.24"N | 120°59'30.77"E | mid-rise block east of the tall towers, satellite estimate |
| 3 | 14°36'56.94"N | 120°59'29.69"E | low-rise residential, satellite estimate |
| 4 | 14°37'07.85"N | 120°59'28.76"E | commercial building east of the highway, satellite estimate |
| 5 | 14°37'20.81"N | 120°59'27.66"E | low-rise residential, satellite estimate |
| 6 | 14°37'31.17"N | 120°59'26.77"E | low-rise block north of the Maranatha/PMCC tower, satellite estimate |
| 7 | 14°37'44.03"N | 120°59'25.68"E | low-rise beside A. Bonifacio Ave, satellite estimate |
| 8 | 14°37'55.01"N | 120°59'24.74"E | La Loma Cemetery, open ground |
| 9 | 14°38'07.96"N | 120°59'23.64"E | cemetery mausoleum, about one storey |
| 10 | 14°38'18.23"N | 120°59'22.77"E | three-storey row house, satellite estimate |
| 11 | 14°38'29.95"N | 120°59'21.77"E | houses at the east edge of the cemetery, satellite estimate |
| 12 | 14°38'42.97"N | 120°59'20.66"E | three-storey block south of the warehouses, satellite estimate |
| 13 | 14°38'54.08"N | 120°59'19.72"E | beside a tall warehouse west of Caloocan City Hall; warehouse counted as 3 floors |
| 14 | 14°39'07.20"N | 120°59'18.60"E | commercial building near CAI Sports Center, satellite estimate (taken high) |
| 15 | 14°39'17.82"N | 120°59'17.69"E | line follows a street here; the street-front buildings (about 3 floors) are counted |
| 16 | 14°39'30.33"N | 120°59'16.63"E | row houses east of MCU Hospital, satellite estimate |
| 17 | 14°39'41.60"N | 120°59'15.67"E | white mid-rise north of EDSA, satellite estimate (taken high) |
| 18 | 14°39'52.87"N | 120°59'14.71"E | large house in a gated subdivision, satellite estimate |
| 19 | 14°40'04.85"N | 120°59'13.69"E | two-storey house south of the Tullahan River, satellite estimate |
| 20 | 14°40'17.32"N | 120°59'12.63"E | Metro Industries, 84 Ramon Delfin St (Site B): 5-storey block + 1-storey rooftop structure |

**Sample computation at the highest intermediate point (P17)**

- h_elevation = 20.48 + 4(2.5) = 30.4800 m
- h_earth bulge = d1·d2 / (12.75k) = (5.8253)(1.1017) / [12.75(4/3)] = 0.3775 m
- F1 = 17.3√[d1·d2 / (f(d1 + d2))] = 17.3√[(5.8253)(1.1017) / (10.59625 × 6.9270)] = 5.1155 m
- 0.6F1 = 0.6(5.1155) = 3.0693 m
- THE = 30.4800 + 0.3775 + 3.0693 = 33.9268 m

**Near-line structure check**

- Maranatha/PMCC tower (9 floors, corner about 5 m east of the line): d1 = 1.6670 km, THE = 4.35 + 9(2.5) + 0.5158 + 3.5876 = 30.9534 m
- LRT-1 viaduct on EDSA with a train on it (about 12.5 m, taken as 5 floors): d1 = 5.3531 km, THE = 19.31 + 5(2.5) + 0.4956 + 3.5167 = 35.8224 m

## Antenna Towers

**Table 4. Antenna Heights**

| Parameter | Site A Tower | Site B Tower |
|---|---|---|
| h_antenna | 62.4700 m | 31.5014 m (tilted) |
| h_elevation | 59.9700 m | 25.9800 m |
| h_tower | 2.5000 m | 5.5214 m |

**Tilted antenna mounting (guideline Part 3, item 9)**

Safety margin: THE already keeps 0.6F1 of the Fresnel zone and the earth bulge clear. Because the heights of P17 (4 floors) and the LRT-1 viaduct (12.5 m) are estimates, the design keeps an extra 2.5 m (one floor) above every THE and adds 2.5 m to both antenna heights.

With equal antenna heights, both antennas would sit at the maximum THE of 59.9700 m (P1) plus the margin, 62.4700 m, which needs a 36.4900 m tower at Site B. The antennas are instead mounted at an angle, keeping line of sight and the margin above every THE.

- Site A antenna height: hA = THE at P1 + 2.5 = 59.9700 + 2.5000 = 62.4700 m, so h_tower,A = 62.4700 − 59.9700 = 2.5000 m
- The tilted line must stay at least 2.5 m above THE at every point: hA − (hA − hB)(d1 / D) ≥ THE + 2.5, so hB ≥ hA − (hA − THE − 2.5)(D / d1). The path profile (Figure 2.3) shows the line comes closest to THE at P17, so P17 sets hB.
- hB = 62.4700 − (62.4700 − 33.9268 − 2.5000)(6.9270 / 5.8253) = 31.5014 m
- h_tower,B = 31.5014 − 25.9800 = 5.5214 m
- Tilt angle = tan⁻¹[(hA − hB) / D] = tan⁻¹[(62.4700 − 31.5014) / 6927.01] = 0.2562°, downward at Site A and upward at Site B
- Check at the next-closest structure, the LRT-1 viaduct (d1 = 5.3531 km): line of sight = 62.4700 − (30.9686)(5.3531 / 6.9270) = 38.5379 m, clearance = 38.5379 − 35.8224 = 2.7155 m, above the 2.5 m margin. Every other point clears THE by 6.9701 m or more (P16 is the next closest), as Figure 2.3 shows.

Justification: the ANDREW VHLP6-11W/A antenna mount has a ±5° fine elevation adjustment, so a 0.2562° tilt is within its range. The tilt is also smaller than half of the antenna's vertical beamwidth (1° on the specification sheet, 0.9200° simulated), and each antenna is aimed directly at the other.

Discussion: Site A needs a 2.5000 m mast on the Frassati rooftop and Site B a mast of 5.5214 m on the Metro Industries rooftop, instead of a 36.4900 m tower. P17 sets the tilt because the line of sight passes exactly 2.5000 m (the safety margin) above its THE; the LRT-1 viaduct is the next closest at 2.7155 m. Both heights are estimates (P17 at 4 floors, the viaduct with a train at 12.5 m), so the margin covers either one being about one floor taller.

---

## Numbers for Section 3 (not yet in the report)

| Item | Value |
|---|---|
| Waveguide length A / B (tower + 3 m) | 5.5000 m / 8.5214 m |
| Waveguide loss A / B | 0.5404 dB / 0.8373 dB |
| Free-space loss | 129.7557 dB |
| Total gain | 110.2022 dB |
| RSL at amplifier output | 13.4568 dBm |
| Receiver sensitivity | -97.7978 dBm |
| Fade margin | 111.2546 dB |
| Microwave system loss | 132.5535 dB |
| Fiber loss (8.9 km road length carried over from the Fini route; recheck for Metro Industries) | 1.9740 dB |

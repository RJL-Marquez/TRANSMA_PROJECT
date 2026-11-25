# Section 2. Path Planning (UST Frassati to Metro Industries)

## Site Locations

**Table 2. Site Information**

| | Site A | Site B |
|---|---|---|
| Area | Saint Pier Giorgio Frassati Building, España Boulevard, Sampaloc, Manila | Metro Industries, 84 Ramon Delfin St, Marulas, Valenzuela, Metro Manila |
| Map coordinates | 14°36'32.71"N 120°59'31.75"E | 14°40'17.32"N 120°59'12.63"E |
| Location description | A 23-storey building, with a rooftop | Rooftop of the Metro Industries building, Marulas (5 storeys assumed from satellite and street imagery; to be confirmed on site) |
| Height of building | 23 × 2.5 m = 57.5 m | 5 × 2.5 m = 12.5 m |
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

*Figure 2.3: Path profile showing all 20 points, THE, the near-line structures, and the tilted line of sight*

Discussion: The ground rises from about 2.5 m near UST to about 20 m around EDSA (P16 and P17), drops to 3.63 m at the Tullahan River (P19), and rises again to 10.98 m at Site B. The dashed red line is the tilted line of sight from 59.9700 m at Frassati to 29.1511 m at Metro Industries. It stays at or above THE at every point and at both near-line structures. It just touches the THE of P17 and passes 0.17 m above the THE of the LRT-1 viaduct.

**Table 3. Path Profile: Elevation, Earth Bulge, and Fresnel Clearance**

| Point | d1 (km) | d2 (km) | Ground (m) | Floors | h_elevation (m) | h_earth bulge (m) | 0.6F1 (m) | THE (m) |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.0000 | 6.9270 | 2.47 | 23 | 59.9700 | 0.0000 | 0.0000 | 59.9700 |
| 2 | 0.3556 | 6.5714 | 2.55 | 6 | 17.5500 | 0.1833 | 1.8521 | 19.5854 |
| 3 | 0.7472 | 6.1798 | 2.74 | 3 | 10.2400 | 0.3622 | 2.6035 | 13.2056 |
| 4 | 1.0837 | 5.8433 | 3.55 | 3 | 11.0500 | 0.4967 | 3.0488 | 14.5955 |
| 5 | 1.4833 | 5.4437 | 3.52 | 3 | 11.0200 | 0.6333 | 3.4428 | 15.0961 |
| 6 | 1.8029 | 5.1241 | 4.79 | 3 | 12.2900 | 0.7246 | 3.6825 | 16.6971 |
| 7 | 2.1995 | 4.7275 | 6.68 | 2 | 11.6800 | 0.8155 | 3.9068 | 16.4024 |
| 8 | 2.5381 | 4.3889 | 10.78 | 0 | 10.7800 | 0.8737 | 4.0437 | 15.6974 |
| 9 | 2.9376 | 3.9894 | 14.70 | 1 | 17.2000 | 0.9192 | 4.1476 | 22.2668 |
| 10 | 3.2542 | 3.6728 | 13.48 | 3 | 20.9800 | 0.9374 | 4.1886 | 26.1060 |
| 11 | 3.6158 | 3.3112 | 15.69 | 2 | 20.6900 | 0.9390 | 4.1922 | 25.8213 |
| 12 | 4.0174 | 2.9096 | 17.33 | 3 | 24.8300 | 0.9168 | 4.1423 | 29.8891 |
| 13 | 4.3600 | 2.5670 | 18.17 | 3 | 25.6700 | 0.8778 | 4.0533 | 30.6011 |
| 14 | 4.7645 | 2.1625 | 17.59 | 4 | 27.5900 | 0.8081 | 3.8890 | 32.2871 |
| 15 | 5.0921 | 1.8349 | 18.15 | 3 | 25.6500 | 0.7328 | 3.7034 | 30.0863 |
| 16 | 5.4777 | 1.4493 | 19.63 | 3 | 27.1300 | 0.6227 | 3.4137 | 31.1664 |
| 17 | 5.8253 | 1.1017 | 20.48 | 4 | 30.4800 | 0.5034 | 3.0693 | 34.0527 |
| 18 | 6.1729 | 0.7541 | 11.63 | 3 | 19.1300 | 0.3651 | 2.6140 | 22.1091 |
| 19 | 6.5424 | 0.3846 | 3.63 | 2 | 8.6300 | 0.1974 | 1.9219 | 10.7492 |
| 20 | 6.9270 | 0.0000 | 10.98 | 5 | 23.4800 | 0.0000 | 0.0000 | 23.4800 |

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
| 20 | 14°40'17.32"N | 120°59'12.63"E | Metro Industries, 84 Ramon Delfin St (Site B) |

**Sample computation at the highest intermediate point (P17)**

- h_elevation = 20.48 + 4(2.5) = 30.4800 m
- h_earth bulge = d1·d2 / 12.75 = (5.8253)(1.1017) / 12.75 = 0.5034 m
- F1 = 17.3√[d1·d2 / (f(d1 + d2))] = 17.3√[(5.8253)(1.1017) / (10.59625 × 6.9270)] = 5.1155 m
- 0.6F1 = 0.6(5.1155) = 3.0693 m
- THE = 30.4800 + 0.5034 + 3.0693 = 34.0527 m

**Near-line structure check**

- Maranatha/PMCC tower (9 floors, corner about 5 m east of the line): d1 = 1.6670 km, THE = 4.35 + 9(2.5) + 0.6877 + 3.5876 = 31.1254 m
- LRT-1 viaduct on EDSA with a train on it (about 12.5 m, taken as 5 floors): d1 = 5.3531 km, THE = 19.31 + 5(2.5) + 0.6608 + 3.5167 = 35.9876 m

## Antenna Towers

**Table 4. Antenna Heights**

| Parameter | Site A Tower | Site B Tower |
|---|---|---|
| h_antenna | 59.9700 m | 29.1511 m (tilted) |
| h_elevation | 59.9700 m | 23.4800 m |
| h_tower | 0.0000 m | 5.6711 m |

**Tilted antenna mounting (guideline Part 3, item 9)**

With equal antenna heights, both antennas would sit at the maximum THE of 59.9700 m (P1), which needs a 36.4900 m tower at Site B. The antennas are instead mounted at an angle, keeping line of sight and clearance from every THE.

- Site A antenna height: hA = THE at P1 = 59.9700 m, so h_tower,A = 59.9700 − 59.9700 = 0.0000 m
- For each point, the straight line from Site A must stay at or above THE: hA − (hA − hB)(d1 / D) ≥ THE, so hB ≥ hA − (hA − THE)(D / d1).
- The largest required hB is at P17: hB = 59.9700 − (59.9700 − 34.0527)(6.9270 / 5.8253) = 29.1511 m
- h_tower,B = 29.1511 − 23.4800 = 5.6711 m
- Tilt angle = tan⁻¹[(hA − hB) / D] = tan⁻¹[(59.9700 − 29.1511) / 6927.01] = 0.2549°, downward at Site A and upward at Site B

Justification: the ANDREW VHLP6-11W/A antenna mount has a ±5° fine elevation adjustment, so a 0.2549° tilt is within its range. The tilt is also smaller than half of the antenna's vertical beamwidth (1° on the specification sheet, 0.9200° simulated), and each antenna is aimed directly at the other.

**Table 4.1. Clearance of the tilted line of sight at all 20 points and the two near-line structures (M: Maranatha/PMCC tower, L: LRT-1 viaduct)**

| Point | d1 (km) | THE (m) | Line of sight (m) | Clearance above THE (m) |
|---|---|---|---|---|
| P1 | 0.0000 | 59.9700 | 59.9700 | 0.0000 |
| P2 | 0.3556 | 19.5854 | 58.3879 | 38.8025 |
| P3 | 0.7472 | 13.2056 | 56.6456 | 43.4400 |
| P4 | 1.0837 | 14.5955 | 55.1485 | 40.5530 |
| P5 | 1.4833 | 15.0961 | 53.3707 | 38.2746 |
| M | 1.6670 | 31.1254 | 52.5534 | 21.4280 |
| P6 | 1.8029 | 16.6971 | 51.9487 | 35.2516 |
| P7 | 2.1995 | 16.4024 | 50.1842 | 33.7818 |
| P8 | 2.5381 | 15.6974 | 48.6777 | 32.9803 |
| P9 | 2.9376 | 22.2668 | 46.9003 | 24.6335 |
| P10 | 3.2542 | 26.1060 | 45.4917 | 19.3857 |
| P11 | 3.6158 | 25.8213 | 43.8830 | 18.0617 |
| P12 | 4.0174 | 29.8891 | 42.0962 | 12.2071 |
| P13 | 4.3600 | 30.6011 | 40.5719 | 9.9708 |
| P14 | 4.7645 | 32.2871 | 38.7723 | 6.4852 |
| P15 | 5.0921 | 30.0863 | 37.3147 | 7.2285 |
| L | 5.3531 | 35.9876 | 36.1535 | 0.1660 |
| P16 | 5.4777 | 31.1664 | 35.5992 | 4.4328 |
| P17 | 5.8253 | 34.0527 | 34.0527 | 0.0000 |
| P18 | 6.1729 | 22.1091 | 32.5062 | 10.3970 |
| P19 | 6.5424 | 10.7492 | 30.8622 | 20.1130 |
| P20 | 6.9270 | 23.4800 | 29.1511 | 5.6711 |

Discussion: Site A needs no added tower, only a rooftop mount on the Frassati Building. Site B needs a 5.6711 m mast on the Metro Industries rooftop instead of a 36.4900 m tower. P17 sets the tilt because the line of sight just touches its THE; the LRT-1 viaduct is the next closest. Both heights are estimates (P17 at 4 floors, the viaduct with a train at 12.5 m), taken on the high side, so the real clearance should be larger.

---

## Numbers for Section 3 (not yet in the report)

| Item | Value |
|---|---|
| Waveguide length A / B (tower + 3 m) | 3.0000 m / 8.6711 m |
| Waveguide loss A / B | 0.2948 dB / 0.8520 dB |
| Free-space loss | 129.7557 dB |
| Total gain | 110.4332 dB |
| RSL at amplifier output | 13.6878 dBm |
| Receiver sensitivity | -97.7978 dBm |
| Fade margin | 111.4856 dB |
| Microwave system loss | 132.3225 dB |
| Fiber loss (8.9 km road length carried over from the Fini route; recheck for Metro Industries) | 1.9734 dB |

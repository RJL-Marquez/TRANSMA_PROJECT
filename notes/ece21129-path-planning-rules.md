
User asked to keep these guideline rules (pages 8-9) in mind for Section 2.

- Site A must be on top of a UST Manila campus building; Site B in the assigned area. Measure straight-line distance. Overlay the radiation pattern on the map, aimed at the other antenna.
- Use **20 points** on the straight line: 2 sites + 18 between. Favor obviously tall infrastructure while keeping spacing relatively even.
- h_elevation = h_earth contour (Google Earth soil height) + h_obstruction (floors × 2.5 m, since Philippine buildings are not 3D)
- h_earth bulge = d1·d2 / (12.75), d in km, k = 4/3
- F1 = 17.3·sqrt(d1·d2 / (f·(d1+d2))), f in GHz; clearance = 0.6·F1
- THE = h_elevation + h_earth bulge + 0.6·F1
- h_antenna(min) = maximum THE of all 20 points; h_tower = h_antenna(min) − h_elevation at each site
- Tower height sets the vertical transmission line length. Both antennas may simply use the same minimum height. Tilted mounting is allowed only with added justification and proof it is practical.
- Path profile graph must show all 20 points with h_elevation, + bulge, + 0.6F1, and the minimum antenna height, with a legend.

**Why:** The rubric grades path profile (20 pts) and towers (5 pts) on these exact steps.

**How to apply:** Use this method and these formulas for every candidate pair. Related: [[ece21129-project-setup]], [[ece21129-site-selection-status]].

"""Switch Option A text to the tilted design (run after patch_options.py and patch_sim.py)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "build_opt.py")
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)


rep("The minimum antenna height is {f4(M['hmin'])} m. The Frassati rooftop already reaches this height, so Site A needs no added tower and Site B needs a {f4(M['tower_b'])} m tower.",
    "The antennas are mounted at {f4(M['h_ant_a'])} m and {f4(M['h_ant_b'])} m above sea level with a {M['tilt_deg']:.4f}° tilt, so Site A needs no added tower and Site B needs a {f4(M['tower_b'])} m tower.")

rep('''c = cells(t.rows[2]); set_cell(c[-1], f"{f4(M['hmin'])} m")''',
    '''c = cells(t.rows[2]); set_cell(c[-1], f"{f4(M['h_ant_a'])} m (Site A), {f4(M['h_ant_b'])} m (Site B), tilted" if M.get("tilted") else f"{f4(M['hmin'])} m")''')

rep('"Maranatha/PMCC tower (between P5 and P6), mid-rise block (P2), low-rise buildings (P14, P15), and the 15 to 20 m ridge (P12 to P17)" if IS_A',
    '"8-storey building under construction on Asuncion St (between P17 and P18), Maranatha/PMCC tower (between P5 and P6), mid-rise block (P2), low-rise buildings (P14, P15), and the 15 to 20 m ridge (P12 to P17)" if IS_A')

old_towers = '''cur.para(f"hantenna(min) = maximum THE = {f4(M['hmin'])} m (P{M['governing']})")
cur.para(f"htower,A = {f4(M['hmin'])} - {f4(ROWS[0]['elev'])} = {f4(M['tower_a'])} m")
cur.para(f"htower,B = {f4(M['hmin'])} - {f4(ROWS[-1]['elev'])} = {f4(M['tower_b'])} m")'''
new_towers = '''if M.get("tilted"):
    g = M["tilt_point"]
    EX = {e["name"]: e for e in M["extras"]}
    D_KM = C["d_km"]
    cur.para("Tilted antenna mounting (guideline Part 3, item 9)", bold=True)
    cur.para(f"With equal antenna heights, both antennas would sit at the maximum THE of {f4(M['hmin'])} m (P1), which needs a {f4(M['flat_tower_b'])} m tower at Site B. The antennas are instead mounted at an angle, keeping line of sight and clearance from every THE.")
    cur.para("Two buildings between the sampled points were also checked because they sit within the 0.6F1 clearance of the line:")
    for e in M["extras"]:
        cur.para(f"• {e['name']} = {e['label']}: d1 = {f4(e['d1'])} km, THE = {e['ground']:.2f} + {e['floors']}(2.5) + {f4(e['bulge'])} + {f4(e['f60'])} = {f4(e['the'])} m")
    cur.para(f"Site A antenna height: hA = THE at P1 = {f4(M['h_ant_a'])} m, so htower,A = {f4(M['h_ant_a'])} - {f4(ROWS[0]['elev'])} = {f4(M['tower_a'])} m")
    cur.para("For each point, the straight line from Site A must stay at or above THE: hA - (hA - hB)(d1 / D) ≥ THE, so hB ≥ hA - (hA - THE)(D / d1).")
    cur.para(f"The largest required hB is at {g['name']}: hB = {f4(M['h_ant_a'])} - ({f4(M['h_ant_a'])} - {f4(g['the'])})({f4(D_KM)} / {f4(g['d1'])}) = {f4(M['h_ant_b'])} m")
    cur.para(f"htower,B = {f4(M['h_ant_b'])} - {f4(ROWS[-1]['elev'])} = {f4(M['tower_b'])} m")
    cur.para(f"Tilt angle = tan⁻¹[(hA - hB) / D] = tan⁻¹[({f4(M['h_ant_a'])} - {f4(M['h_ant_b'])}) / {C['d_m']:.2f}] = {M['tilt_deg']:.4f}°, downward at Site A and upward at Site B")
    cur.para(f"Justification: the ANDREW VHLP6-11W/A mount has a ±5° fine elevation adjustment [1], so a {M['tilt_deg']:.4f}° tilt is within its range. The tilt is also smaller than half of the antenna's vertical beamwidth (1° on the specification sheet, {SIM['bw_el']:.4f}° simulated), and each antenna is aimed directly at the other.")
    data = [["Point", "d1 (km)", "THE (m)", "Line of sight (m)", "Clearance above THE (m)"]]
    for c_ in M["clearance"]:
        data.append([c_["name"], f4(c_["d1"]), f4(c_["the"]), f4(c_["line"]), f4(c_["margin"])])
    cur.table(data, [0.6, 1.1, 1.3, 1.6, 1.9], size=8.5)
    cur.caption("Table 4.1. Clearance of the tilted line of sight at all 20 points and the two near-line buildings")
else:
''' + "\n".join("    " + line for line in old_towers.splitlines())
rep(old_towers, new_towers)

rep('which is below the 60.0400 m minimum antenna height.")',
    'which is below the " + f"{f4(M[\'h_ant_a\'] + (M[\'h_ant_b\'] - M[\'h_ant_a\']) * 1.6630 / C[\'d_km\'])}" + " m height of the tilted line of sight at that point.")')

rep('"The Site A tower is 0 m because the Frassati rooftop sets the minimum height. The antenna still needs a rooftop mount, and only the 3 m horizontal waveguide run is counted there.",',
    'f"Tilted mounting is used, as guideline Part 3, item 9 allows. If the professor requires equal antenna heights, the Site B tower becomes {f4(M[\'flat_tower_b\'])} m and the link budget must be redone.",\n        f"The tilt is set by the building under construction on Asuncion St (8 floors counted in May 2026 Street View). It is not in the February 2026 satellite image. If it ends up taller, each extra floor raises the Site B antenna by about {2.5 * C[\'d_km\'] / M[\'tilt_point\'][\'d1\']:.2f} m.",')
rep('"Floor counts at P2 to P19 are satellite estimates. A sampled point would need more than 14 floors to change the minimum antenna height.",',
    'f"Floor counts at P2 to P19 are satellite estimates. The tightest sampled point now has {f4(min(c_[\'margin\'] for c_ in M[\'clearance\'] if c_[\'name\'].startswith(\'P\') and c_[\'name\'] not in (\'P1\', \'P20\')))} m of spare clearance, so a single wrong floor count there would not change the design.",')
rep('"The Maranatha/PMCC floor count is from Street View. It would need more than 20 floors to change the result.",',
    'f"The Maranatha/PMCC floor count is from Street View. It has {f4(next(c_[\'margin\'] for c_ in M[\'clearance\'] if c_[\'name\'] == \'M\'))} m of spare clearance below the tilted line.",')
open(p, "w", encoding="utf-8").write(s)
print("tilt patched")

import copy
import json
import os
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.table import Table
from docx.text.paragraph import Paragraph
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\Lenovo\Downloads\Copy of ECE21129 Project Template AY26-27 [PLEASE DUPLICATE].docx"
OPT = os.environ["OPT"]
DST = {"A": r"C:\UST\TRANSMA PROJECT\4ECEB_Group5_Report_OPTION_A_Frassati.docx", "B": r"C:\UST\TRANSMA PROJECT\4ECEB_Group5_Report_OPTION_B_BGPOP.docx"}[OPT]
TR = r"C:\Users\Lenovo\.claude\projects\C--UST-TRANSMA-PROJECT\84d6406d-f149-4c45-afef-396d97e96f97\tool-results"
MAP_SHOT = os.path.join(TR, {"A": "mcp-Claude_Browser-blob-1795468641453-mx4aj1.jpg", "B": "mcp-Claude_Browser-blob-1795457183609-wsmcqz.jpg"}[OPT])
RED = RGBColor(0xFF, 0, 0)

R = json.load(open(os.path.join(HERE, f"results_{OPT}.json"), encoding="utf-8"))
AMP = R["amp"]
IS_A = OPT == "A"
MDIR = os.path.join(HERE, "matlab")
_log = open(os.path.join(MDIR, "sim_antenna.log"), encoding="utf-8", errors="replace").read()
_m = re.search(r"Dmax = ([\d.]+) dBi at az = ([-\d.]+) deg, el = ([-\d.]+) deg", _log)
_b = re.search(r"HPBW azimuth plane = ([\d.]+) deg, elevation plane = ([\d.]+) deg", _log)
SIM = dict(d=float(_m.group(1)), az=float(_m.group(2)), el=float(_m.group(3)), bw_az=float(_b.group(1)), bw_el=float(_b.group(2)))
SIM["ap"] = SIM["d"] + 10 * __import__("math").log10(0.55)
C, ROWS, M, ALT = R["common"], R["rows"], R["main"], R["alt"]
d = docx.Document(SRC)
f4 = lambda v: f"{v:.4f}"


def set_cell(cell, text, red=False, bold=None, size=None):
    p = cell.paragraphs[0]
    for extra in cell.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
        run = runs[0]
    else:
        run = p.add_run(text)
    run.font.color.rgb = RED if red else RGBColor(0, 0, 0)
    if bold is not None:
        run.bold = bold
    if size:
        run.font.size = Pt(size)


def cells(row):
    seen, out = [], []
    for c in row.cells:
        if c._tc not in seen:
            seen.append(c._tc)
            out.append(c)
    return out


class Cursor:
    def __init__(self, element):
        self.el = element

    def para(self, text="", bold=False, red=False, italic=False, center=False, size=None, after=4):
        p = OxmlElement("w:p")
        self.el.addnext(p)
        self.el = p
        para = Paragraph(p, d._body)
        if text:
            r = para.add_run(text)
            r.bold = bold
            r.italic = italic
            if red:
                r.font.color.rgb = RED
            if size:
                r.font.size = Pt(size)
        para.paragraph_format.space_after = Pt(after)
        para.paragraph_format.keep_with_next = bool(bold)
        if center:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return para

    def picture(self, path, width):
        para = self.para(center=True, after=2)
        para.paragraph_format.keep_with_next = True
        para.add_run().add_picture(path, width=Inches(width))
        return para

    def caption(self, text):
        return self.para(text, italic=True, center=True, size=9, after=8)

    def table(self, data, widths, header=True, size=8):
        t = d.add_table(rows=len(data), cols=len(data[0]))
        tbl = t._tbl
        pr = tbl.tblPr
        b = OxmlElement("w:tblBorders")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{side}")
            e.set(qn("w:val"), "single")
            e.set(qn("w:sz"), "4")
            e.set(qn("w:color"), "808080")
            b.append(e)
        pr.append(b)
        for i, row in enumerate(data):
            tr = t.rows[i]
            if i == 0 and header:
                hdr = OxmlElement("w:tblHeader")
                tr._tr.get_or_add_trPr().append(hdr)
            cant = OxmlElement("w:cantSplit")
            tr._tr.get_or_add_trPr().append(cant)
            for j, value in enumerate(row):
                c = tr.cells[j]
                c.width = Inches(widths[j])
                p = c.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(str(value))
                run.font.size = Pt(size)
                if i == 0 and header:
                    run.bold = True
                    shade = OxmlElement("w:shd")
                    shade.set(qn("w:val"), "clear")
                    shade.set(qn("w:color"), "auto")
                    shade.set(qn("w:fill"), "FFF2CC")
                    c._tc.get_or_add_tcPr().append(shade)
        self.el.addnext(tbl)
        self.el = tbl
        return t


def find_para(pattern):
    for p in d.paragraphs:
        if re.search(pattern, p.text):
            return p
    raise KeyError(pattern)


# Cover
for p in d.paragraphs[:30]:
    for run in p.runs:
        if run.text.strip() == "Y" and "Design" in p.text:
            run.text = "10.59625"
            run.font.color.rgb = RGBColor(0, 0, 0)
        elif run.text.strip().startswith("Area1"):
            run.text = "UST Manila "
            run.font.color.rgb = RGBColor(0, 0, 0)
        elif run.text.strip().startswith("Area2"):
            run.text = " Valenzuela City"
            run.font.color.rgb = RGBColor(0, 0, 0)
        elif run.text.strip() == "Y" and "Group" in p.text:
            run.text = " 5"
            run.font.color.rgb = RGBColor(0, 0, 0)
        elif run.text.strip() == "Z":
            run.text = "B"
            run.font.color.rgb = RGBColor(0, 0, 0)

T = d.tables
# Executive summary
summary = [
    f"A fixed point-to-point microwave link is needed between UST Manila and Valenzuela City. The {C['d_km']:.4f} km path must carry a 10.59625 GHz signal with line-of-sight, Fresnel clearance, and enough fade margin for reliable communication.",
    (f"The link uses 1.8 m parabolic antennas, 2 W input power, WR-90 waveguide, and a low noise amplifier. The antennas are mounted at {f4(M['h_ant_a'])} m and {f4(M['h_ant_b'])} m above sea level with a {M['tilt_deg']:.4f}° tilt, so Site A needs no added tower and Site B needs a {f4(M['tower_b'])} m tower." if IS_A else f"The link uses 1.8 m parabolic antennas, 2 W input power, WR-90 waveguide, and a low noise amplifier. The minimum antenna height is {f4(M['hmin'])} m, requiring {f4(M['tower_a'])} m and {f4(M['tower_b'])} m towers at Sites A and B."),
    "The design uses the assigned NTC microwave channel, a k = 4/3 standard atmosphere, 60% first Fresnel zone clearance, and the free-space path loss model. Component values follow manufacturer specification sheets.",
    "Main constraints are dense Manila high-rises, a 15 to 20 m ridge in Caloocan, limited rooftop space, waveguide loss along tall towers, and building heights approximated at 2.5 m per floor because local structures are not rendered in 3D.",
]
for row, text in zip(T[2].rows, summary):
    set_cell(row.cells[1], text)

# Table 1
t = T[3]
for row_i, left, right, pending in [
    (2, "0.9", f"{f4(C['theta'])}°", False),
    (3, "0.63", f"{SIM['bw_az']:.4f}° (azimuth plane), {SIM['bw_el']:.4f}° (elevation plane)", False),
    (4, "90", f"{f4(C['ad_db'])} dBi", False),
    (5, "10.59625", f"{f4(SIM['d'])} dBi", False),
    (6, "10.09625 to 11.09625 GHz, 50 MHz steps", f"az = {SIM['az']:.2f}°, el = {SIM['el']:.2f}°", False),
]:
    c = cells(t.rows[row_i])
    set_cell(c[1], left)
    set_cell(c[3], right, red=pending)

# Table 2
t = T[4]
c = cells(t.rows[2]); set_cell(c[1], "UST Manila"); set_cell(c[3], "Valenzuela City")
c = cells(t.rows[3]); set_cell(c[1], ROWS[0]["lat"] + ", " + ROWS[0]["lon"]); set_cell(c[3], "14°40'08.72\"N, 120°59'11.05\"E")
c = cells(t.rows[4]); set_cell(c[1], "Rooftop of the UST Frassati Building" if IS_A else "Rooftop of the Buenaventura Garcia Paredes, O.P. (BGPOP) Building"); set_cell(c[3], "Rooftop of a 6-storey Fini Homes building, Ramon Delfin St., Marulas")
c = cells(t.rows[5]); set_cell(c[1], f"{ROWS[0]['floors']} floors × 2.5 m = {ROWS[0]['floors'] * 2.5:g} m"); set_cell(c[3], "6 floors × 2.5 m = 15 m")
c = cells(t.rows[6]); set_cell(c[-1], f"{f4(C['d_km'])} km")
c = cells(t.rows[7]); set_cell(c[-1], "8-storey building under construction on Asuncion St (between P17 and P18), Maranatha/PMCC tower (between P5 and P6), mid-rise block (P2), low-rise buildings (P14, P15), and the 15 to 20 m ridge (P12 to P17)" if IS_A else "Pacific Icon Residences 2 (P2), Chinese General Hospital (P7), 4th St. building (P13), 11th Ave. building (P15), Manila Central University (P17)")

# Table 3
t = T[5]
for r in ROWS:
    c = cells(t.rows[r["n"] + 1])
    vals = [str(r["n"]), f"{f4(r['d1'])} km", f"{f4(r['d2'])} km", f"{f4(r['elev'])} m", f"{f4(r['bulge'])} m", f"{f4(r['f60'])} m", f"{f4(r['the'])} m"]
    for cell, value in zip(c, vals):
        set_cell(cell, value, size=8.5)

# Table 4
t = T[6]
c = cells(t.rows[2]); set_cell(c[-1], f"{f4(M['h_ant_a'])} m (Site A), {f4(M['h_ant_b'])} m (Site B), tilted" if M.get("tilted") else f"{f4(M['hmin'])} m")
c = cells(t.rows[3]); set_cell(c[1], f"{f4(ROWS[0]['elev'])} m"); set_cell(c[2], f"{f4(ROWS[-1]['elev'])} m")
c = cells(t.rows[4]); set_cell(c[1], f"{f4(M['tower_a'])} m"); set_cell(c[2], f"{f4(M['tower_b'])} m")

# Table 5
t = T[7]
new_tr = copy.deepcopy(t.rows[8]._tr)
t.rows[8]._tr.addnext(new_tr)
vals = {
    2: ("ANDREW VHLP6-11W/A [1]", "10.000 to 11.700 GHz", "44 dBi (mid band)"),
    3: (None, None, "0 dB (not listed)"),
    4: ("ATM WR-90, copper RG-52/U [2]", "8.20 to 12.40 GHz", f"{C['wg_db_m']:.4f} dB/m"),
    5: (None, None, f"A: {f4(M['len_a'])} m; B: {f4(M['len_b'])} m"),
    6: (f"{AMP['name']} [3]", AMP["band"], f"{AMP['gain']:g} dB (min)"),
    7: (None, None, f"{AMP['nf']:g} dB (max)"),
    8: ("Fairview FMWCA1107, antenna side [4]", "8.2 to 12.4 GHz", "0.2 dB"),
    9: ("Fairview FMWCA1025 + FMAD1245 SMA male-male adapter, amplifier side [5], [7]", "8.2 to 12.4 GHz", "0.3 + 0.21 = 0.51 dB"),
}
for i, (model, band, value) in vals.items():
    c = cells(t.rows[i])
    if model:
        set_cell(c[1], model, size=9)
        set_cell(c[2], band, size=9)
    set_cell(c[-1], value, size=9)

for i, name in ((2, 'Parabolic Reflector Antenna'), (4, 'Rectangular Waveguide'), (6, 'Amplifier'), (8, 'Connector'), (9, 'Connector')):
    set_cell(cells(t.rows[i])[0], name, size=8)

# Remove completed instructions and keep what the group still has to do
done = [r"^Tabulate and explain", r"^Make sure to include appropriate units", r"^Add figure numbers", r"^Graph and explain",
        r"^Add legend", r"^Show the 20 points", r"^Include map images", r"^When selecting the values", r"^If you use more than one",
        r"^Compute the required length", r"^Calculate the requested", r"^Compute FSL", r"^Compare the total loss", r"^Calculate FM",
        r"^Compare the power gain", r"^Compare the RSL", r"^Don.t forget", r"^Include screenshots of the specification",
        r"^Include any other information", r"^Use IEEE reference format", r"^Include the following", r"^Links where"]
done += [r"^Include and explain the screenshots of the Matlab", r"^Compare the theoretical and experimental"]
if IS_A:
    done.append(r"^Overlay the radiation")
for p in list(d.paragraphs):
    if any(re.search(x, p.text.strip()) for x in done):
        p._p.getparent().remove(p._p)

# Section 1
cur = Cursor(T[3]._tbl)
cur.para()
cur.para("Theoretical computation", bold=True)
cur.para("λ = c / fc = (3 × 10⁸) / (10.59625 × 10⁹) = 0.028312 m, rounded to 0.0283 m as in the handwritten solution")
cur.para(f"AD = (πD / λ)² = [π(1.8) / {C['lam']:.4f}]² = {f4(C['ad_lin'])} = {f4(C['ad_db'])} dBi")
cur.para(f"Θh = 70λ / D = 70({C['lam']:.4f}) / 1.8 = {f4(C['theta'])}°")
cur.para("Simulation setup", bold=True)
cur.para("Software: MATLAB R2025b Update 7 (25.2.0.3360999) with Antenna Toolbox, using the reflectorParabolic object with a dipole exciter and the MoM-PO solver.")
cur.para("Computer: Intel Core i5-9400 CPU at 2.90 GHz (6 cores), 20 GB RAM, Windows 11 Pro.")
cur.para("Antenna parameters: radius = 0.9 m, focal length = 0.63 m, tilt = 90° about the x-axis, feed offset = [0 0 0], fc = 10.59625 GHz. The antenna was saved as 4ECEB_Group5_Antenna.mat.")
for fn, cap in (("antenna_geometry.png", "Figure 1. Parabolic reflector antenna geometry in MATLAB"),
                ("pattern_3d.png", "Figure 2. 3D directivity pattern at 10.59625 GHz"),
                ("pattern_azimuth.png", f"Figure 3. Azimuth pattern at el = {SIM['el']:.2f}° with the cursor at the maximum directive gain"),
                ("pattern_elevation.png", f"Figure 4. Elevation pattern at az = {SIM['az']:.2f}° with the cursor at the maximum directive gain")):
    cur.picture(os.path.join(MDIR, fn), 5.0 if "3d" in fn or "geometry" in fn else 4.2)
    cur.caption(cap)
cur.para("Experimental values", bold=True)
cur.para(f"Maximum directive gain = {f4(SIM['d'])} dBi at az = {SIM['az']:.2f}°, el = {SIM['el']:.2f}°. The main beam points along the -y axis, which matches the 90° tilt about the x-axis.")
cur.para(f"Half-power beamwidth = {SIM['bw_az']:.4f}° in the azimuth plane and {SIM['bw_el']:.4f}° in the elevation plane.")
cur.para("Comparison with theory", bold=True)
cur.para(f"Directive gain: {f4(SIM['d'])} dBi simulated versus {f4(C['ad_db'])} dBi theoretical, a difference of {f4(C['ad_db'] - SIM['d'])} dB. In linear terms, the simulated directive gain is {10 ** ((SIM['d'] - C['ad_db']) / 10) * 100:.4f}% of the theoretical value. The theoretical formula assumes uniform aperture illumination, while the dipole feed tapers the illumination and spills some power past the reflector edge.")
cur.para(f"Beamwidth: {SIM['bw_az']:.4f}° and {SIM['bw_el']:.4f}° simulated versus {f4(C['theta'])}° theoretical. The two planes differ because the dipole feed pattern is not rotationally symmetric.")

# Section 2 map
cur = Cursor(T[4]._tbl)
cur.para()
im = Image.open(MAP_SHOT).convert("RGB")
crop = im.crop((170, 110, 640, 665) if IS_A else (0, 103, im.width, 665))
map_path = os.path.join(HERE, f"map_points_{OPT}.jpg")
crop.save(map_path, quality=92)
cur.picture(map_path, 4.8 if IS_A else 5.8)
cur.caption(f"Figure 5. Straight-line path and points from UST {'Frassati' if IS_A else 'BGPOP'} to Fini Homes in Google Earth")
if IS_A:
    cur.picture(os.path.join(HERE, "map_overlay_A.png"), 4.8)
    cur.caption(f"Figure 6. Simulated azimuth patterns at both sites, each pointed at the other site, with the 6,661.37 m distance")
    cur.para("Reflection question: The azimuth pattern is used for the overlay. Google Maps shows the horizontal plane, and the azimuth pattern is the cut in that same plane, so it shows how the beam is pointed from one site toward the other. The elevation pattern describes the vertical plane, which a flat map cannot show.")

# Path profile figure before Table 3
anchor = find_para(r"^Path Profile")
cur = Cursor(anchor._p)
cur.picture(os.path.join(HERE, "path_profile_A.png" if IS_A else "path_profile.png"), 6.5)
cur.caption("Figure 7. Path profile showing all 20 points, THE, and the minimum antenna height")

# Worked point
p2 = ROWS[14] if IS_A else ROWS[1]
sample = "P15" if IS_A else "P2"
cur = Cursor(T[5]._tbl)
cur.para()
cur.para("Sample computation at the highest intermediate point (P15)" if IS_A else "Sample computation at the governing point (P2)", bold=True)
cur.para(f"helevation = {p2['ground']:.2f} + {p2['floors']}(2.5) = {f4(p2['elev'])} m")
cur.para(f"hearth bulge = d1d2 / 12.75 = ({f4(p2['d1'])})({f4(p2['d2'])}) / 12.75 = {f4(p2['bulge'])} m")
cur.para(f"F1 = 17.3√[d1d2 / (f(d1 + d2))] = 17.3√[({f4(p2['d1'])})({f4(p2['d2'])}) / (10.59625 × {f4(C['d_km'])})] = {f4(p2['f1'])} m")
cur.para(f"0.6F1 = 0.6({f4(p2['f1'])}) = {f4(p2['f60'])} m")
cur.para(f"THE = {f4(p2['elev'])} + {f4(p2['bulge'])} + {f4(p2['f60'])} = {f4(p2['the'])} m")
if IS_A:
    cur.para("Near-line obstruction check", bold=True)
    cur.para("The Maranatha/PMCC tower lies between P5 and P6, with its west corner at the path line (d1 = 1.6630 km). Using 9 floors from Street View: THE = 4.35 + 9(2.5) + 0.6519 + 3.5620 = 31.0639 m, which is below the " + f"{f4(M['h_ant_a'] + (M['h_ant_b'] - M['h_ant_a']) * 1.6630 / C['d_km'])}" + " m height of the tilted line of sight at that point.")

# Towers
cur = Cursor(T[6]._tbl)
cur.para()
if M.get("tilted"):
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
    cur.para(f"hantenna(min) = maximum THE = {f4(M['hmin'])} m (P{M['governing']})")
    cur.para(f"htower,A = {f4(M['hmin'])} - {f4(ROWS[0]['elev'])} = {f4(M['tower_a'])} m")
    cur.para(f"htower,B = {f4(M['hmin'])} - {f4(ROWS[-1]['elev'])} = {f4(M['tower_b'])} m")

# Equipment notes
cur = Cursor(T[7]._tbl)
cur.para()
cur.para(f"Waveguide loss: 2.995 dB/100 ft ÷ 30.48 m = {C['wg_db_m']:.4f} dB/m, using the listed value closest to fc (12.4 GHz).")
cur.para(f"Waveguide length: LA = {f4(M['tower_a'])} + 3 = {f4(M['len_a'])} m; LB = {f4(M['tower_b'])} + 3 = {f4(M['len_b'])} m")
cur.para(f"Power gain of simulated antenna: AP = AD + 10log(0.55) = {f4(SIM['d'])} - 2.5964 = {f4(SIM['ap'])} dBi, compared with 44 dBi from the specification sheet.")

# Link budget
anchor = find_para(r"^FSL, RSL, and FM")
cur = Cursor(anchor._p)
th = M["fm_theory"]
cur.para("Free-space loss", bold=True)
cur.para(f"FSL = 20log(4π/c) + 20log(fHz) + 20log(D) = 20log[4π/(3 × 10⁸)] + 20log(10.59625 × 10⁹) + 20log({C['d_m']:.2f}) = {f4(C['fsl'])} dB")
cur.para("Received signal level", bold=True)
cur.para(f"Pin = 10log(2000 mW) = {f4(C['pin'])} dBm")
cur.para(f"GTotal = 2(44) + {AMP['gain']:g} - {f4(M['wg_a'])} - {f4(M['wg_b'])} - {f4(M['conn'])} - 0 = {f4(M['g_total'])} dB")
cur.para(f"RSL = {f4(C['pin'])} + {f4(M['g_total'])} - {f4(C['fsl'])} = {f4(M['rsl_out'])} dBm at the output of the Site B amplifier")
cur.para(f"RSL at the amplifier input = {f4(M['rsl_out'])} - {AMP['gain']:g} = {f4(M['rsl_in'])} dBm. The input is below the +{AMP['max_in']:g} dBm maximum, and the output is below the +{AMP['p1db']:g} dBm P1dB.")
cur.para(f"RSL with the simulated antenna (AP = {f4(SIM['ap'])} dBi at both sites) = {f4(M['rsl_out'])} - 2(44 - {f4(SIM['ap'])}) = {f4(M['rsl_out'] - 2 * (44 - SIM['ap']))} dBm. It is {f4(2 * (44 - SIM['ap']))} dB lower than with the ANDREW antenna, which has a higher power gain.")
cur.para("Microwave versus fiber loss", bold=True)
cur.para(f"Microwave loss = FSL + waveguide + connectors = {f4(C['fsl'])} + {f4(M['wg_a'] + M['wg_b'])} + {f4(M['conn'])} = {f4(M['micro_loss'])} dB")
cur.para(f"Fiber length = 8.9 km road route + {ROWS[0]['obstruction'] / 1000:.4f} km + {ROWS[-1]['obstruction'] / 1000:.4f} km vertical = {f4(M['fiber_len'])} km")
cur.para(f"Fiber loss = 0.22 dB/km × {f4(M['fiber_len'])} km = {f4(M['fiber_loss'])} dB at 1550 nm [6], excluding splices and connectors")
cur.para("Experimental fade margin", bold=True)
cur.para(f"N = 10log(kTB / 1 mW) = 10log[(1.38 × 10⁻²³)(290)(2.5 × 10⁶) / 10⁻³] = {f4(M['n'])} dBm")
cur.para("T = 290 K is the standard noise reference temperature. B = 2.5 MHz is the spacing between the assigned 4ECE-B channels.")
cur.para(f"PR(th) = {f4(M['n'])} + 10 + {AMP['nf']:g} = {f4(M['pth'])} dBm")
cur.para(f"FM = {f4(M['rsl_out'])} - ({f4(M['pth'])}) = {f4(M['fm'])} dB")
cur.para("Theoretical fade margin", bold=True)
cur.para("A = 1 (average terrain, mixed urban path with a moderate ridge) and B = 0.5 (hot, humid area), from the M3B lecture table.")
tbl_rows = [["Reliability", "FM (dB)", "Experimental FM meets it?"]]
for k, label in (("99", "99%"), ("99.9", "99.9%"), ("99.99", "99.99%"), ("99.999", "99.999%")):
    tbl_rows.append([label, f4(th[k]), "Yes"])
cur.table(tbl_rows, [2.0, 2.0, 2.5], size=9)
cur.caption("Table 6. Theoretical fade margin at each reliability")
cur.para("System reliability", bold=True)
cur.para(f"1 - R = 10^[(30log D + 10log(6ABf) - 70 - FM) / 10] = 10^[({f4(M['fm_base'])} - {f4(M['fm'])}) / 10] = {M['unreliability']:.4e}")
cur.para(f"R = 1 - {M['unreliability']:.4e} ≈ 99.999999999999%, so the design exceeds all four reliability targets.")

# Appendix
anchor = find_para(r"^Specification Sheets")
cur = Cursor(anchor._p)
specs = [
    ("antenna_VHLP6-11W-A_p1.png", "Figure A1. ANDREW VHLP6-11W/A antenna specification sheet [1]"),
    ("lna_ERZ-LNA-0800-1220-26-2_p1.png" if IS_A else "lna_LNA-30-08001200-15-15P_p1.png", f"Figure A2. {AMP['name']} specification sheet [3]"),
    ("adapter_FMWCA1107_p1.png", "Figure A3. Fairview FMWCA1107 adapter specification sheet [4]"),
    ("adapter_FMWCA1025_p1.png", "Figure A4. Fairview FMWCA1025 adapter specification sheet [5]"),
    ("adapter_FMAD1245_p1.png", "Figure A5. Fairview FMAD1245 SMA male-male adapter specification sheet [7]"),
    ("fiber_G652D_p1.png", "Figure A6. Prysmian G.652.D fiber cable specification sheet [6]"),
]
for fn, cap in specs:
    cur.picture(os.path.join(HERE, "specs", fn), 5.6)
    cur.caption(cap)
cur.para("[ADD: screenshot of the WR-90 row from the ATM waveguide table in reference [2].]", red=True)

anchor = find_para(r"^Other information")
cur = Cursor(anchor._p)
data = [["Pt", "Latitude", "Longitude", "Ground (m)", "Floors", "Obstruction", "Floor basis"]]
for r in ROWS:
    data.append([r["n"], r["lat"], r["lon"], f"{r['ground']:.2f}", r["floors"], r["desc"], r["evidence"]])
cur.table(data, [0.3, 1.05, 1.1, 0.6, 0.45, 1.75, 1.25], size=7.5)
cur.caption("Table A1. Coordinates, ground elevations, and floor counts for all 20 points")
cur.para("DRAFT NOTES (delete before submission)", bold=True, red=True)
NOTES_COMMON = [
    "Member Attestation still says no AI was used. Update it to match what the professor allowed before anyone signs.",
    "B = 2.5 MHz is inferred from the spacing of the 4ECE-B channels in guideline Table 4. Confirm it against the NTC Microwave Channel Plan.",
    "The ANDREW sheet does not list the antenna's feed interface, so confirm that the antenna-side adapter fits.",
    "The waveguide adapter and amplifier are both SMA female, so a 0.21 dB SMA male-male adapter was added at each site.",
    f"FM follows the guideline's RSL at the amplifier output. Referred to the amplifier input, FM = {f4(M['fm_in'])} dB.",
]
if IS_A:
    NOTES = [
        "This is OPTION A: UST Frassati to Fini Homes.",
        f"Tilted mounting is used, as guideline Part 3, item 9 allows. If the professor requires equal antenna heights, the Site B tower becomes {f4(M['flat_tower_b'])} m and the link budget must be redone.",
        f"The tilt is set by the building under construction on Asuncion St (8 floors counted in May 2026 Street View). It is not in the February 2026 satellite image. If it ends up taller, each extra floor raises the Site B antenna by about {2.5 * C['d_km'] / M['tilt_point']['d1']:.2f} m.",
        f"Guideline step 7 can also be read as counting an amplifier at both sites. That gives RSL = {f4(M['rsl_out'] + AMP['gain'])} dBm and FM = {f4(M['fm'] + AMP['gain'])} dB, but the 2 W input exceeds this LNA's +10 dBm maximum input, so confirm the intended reading with the professor.",
        f"Floor counts at P2 to P19 are satellite estimates. The tightest sampled point now has {f4(min(c_['margin'] for c_ in M['clearance'] if c_['name'].startswith('P') and c_['name'] not in ('P1', 'P20')))} m of spare clearance, so a single wrong floor count there would not change the design.",
        f"The Maranatha/PMCC floor count is from Street View. It has {f4(next(c_['margin'] for c_ in M['clearance'] if c_['name'] == 'M'))} m of spare clearance below the tilted line.",
        "D = 6,661.37 m is computed from the two pin coordinates. The drawn Google Earth line reads 6,660.58 m because of small click placement differences.",
        "The 8.9 km fiber road distance was reused from the BGPOP route. Measure the road route from Frassati before finalizing.",
    ] + NOTES_COMMON
else:
    NOTES = [
        "This is OPTION B: UST BGPOP to Fini Homes.",
        f"Biggest design issue: P2 forces {f4(M['tower_a'])} m and {f4(M['tower_b'])} m towers. Option A (Frassati) avoids P2.",
        f"Guideline step 7 can also be read as counting an amplifier at both sites. That gives RSL = {f4(M['rsl_out'] + 30)} dBm and FM = {f4(M['fm'] + 30)} dB, but it would overdrive this LNA, so confirm the intended reading with the professor.",
        "Verify every floor count marked as an estimate in Table A1.",
        "P2 is treated as blocking because the line runs within a few meters of Pacific Icon Residences 2. Its 26 floors come from one property listing.",
        f"If the group proves the line clears P2, the governing point becomes P15: hantenna(min) = {f4(ALT['hmin'])} m, towers = {f4(ALT['tower_a'])} m (A) and {f4(ALT['tower_b'])} m (B), RSL = {f4(ALT['rsl_out'])} dBm. That RSL exceeds the +15 dBm P1dB, so the amplifier would need to change.",
        "The 2 W is treated as the Site A transmit power, because the selected LNA is rated for only +13 dBm input. Only the Site B amplifier gain is counted.",
    ] + NOTES_COMMON
for note in NOTES:
    cur.para("• " + note, red=True, size=9.5, after=2)

anchor = find_para(r"^References")
cur = Cursor(anchor._p)
refs = [
    "[1] ANDREW, an Amphenol Company, “VHLP6-11W/A product specifications,” Mar. 12, 2025. [Online]. Available: https://www.andrew.com/globalassets/digizuite/471721-p360-vhlp6-11w-a-external.pdf",
    "[2] ATM Microwave, “Rectangular waveguide information.” [Online]. Available: https://www.atmmicrowave.com/tech-notes/rectangular-waveguide-information/",
    "[3] ERZIA Technologies, “ERZ-LNA-0800-1220-26-2 low noise amplifier,” Rev. 1.2. [Online]. Available: https://www.erzia.com/wp-content/uploads/ERZ-LNA-0800-1220-26-2_R1.2.pdf" if IS_A else "[3] Narda-MITEQ, “LNA-30-08001200-15-15P low noise amplifier,” Rev. 1.2. [Online]. Available: https://www.nardamiteq.com/docs/LNA-30-08001200-15-15P.PDF",
    "[4] Fairview Microwave, “FMWCA1107 data sheet,” Rev. 1.0, 2020. [Online]. Available: https://fairviewmicrowave.com/images/productPDF/FMWCA1107.pdf",
    "[5] Fairview Microwave, “FMWCA1025 data sheet,” Rev. 1.0, 2018. [Online]. Available: https://fairviewmicrowave.com/images/productPDF/FMWCA1025.pdf",
    "[6] Prysmian Group, “G652D cable datasheet,” 2021. [Online]. Available: https://ec.prysmian.com/sites/ec.prysmian.com/files/media/documents/G652D.pdf",
    "[7] Fairview Microwave, “FMAD1245 data sheet,” Rev. 1.1, 2020. [Online]. Available: https://www.fairviewmicrowave.com/content/dam/infinite-electronics/product-assets/fairview-microwave/product-datasheets/FMAD1245.pdf",
]
if not IS_A:
    refs.append("[8] iRealtee, “Pacific Icon Residences 2.” [Online]. Available: https://irealtee.com/properties/pacific-icon-residences-2-sampaloc-manila")
for ref in refs:
    cur.para(ref, size=9.5, after=3)

d.save(DST)
print("saved", DST)

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
DST = r"C:\UST\TRANSMA PROJECT\4ECEB_Group5_Report_DRAFT.docx"
MAP_SHOT = r"C:\Users\Lenovo\.claude\projects\C--UST-TRANSMA-PROJECT\84d6406d-f149-4c45-afef-396d97e96f97\tool-results\mcp-Claude_Browser-blob-1795457183609-wsmcqz.jpg"
RED = RGBColor(0xFF, 0, 0)

R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
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
    "A fixed point-to-point microwave link is needed between UST Manila and Valenzuela City. The 6.6877 km path must carry a 10.59625 GHz signal with line-of-sight, Fresnel clearance, and enough fade margin for reliable communication.",
    f"The link uses 1.8 m parabolic antennas, 2 W input power, WR-90 waveguide, and a low noise amplifier. The minimum antenna height is {f4(M['hmin'])} m, requiring {f4(M['tower_a'])} m and {f4(M['tower_b'])} m towers at Sites A and B.",
    "The design uses the assigned NTC microwave channel, a k = 4/3 standard atmosphere, 60% first Fresnel zone clearance, and the free-space path loss model. Component values follow manufacturer specification sheets.",
    "Main constraints are dense Manila high-rises, a 15 to 20 m ridge in Caloocan, limited rooftop space, waveguide loss along tall towers, and building heights approximated at 2.5 m per floor because local structures are not rendered in 3D.",
]
for row, text in zip(T[2].rows, summary):
    set_cell(row.cells[1], text)

# Table 1
t = T[3]
for row_i, left, right, pending in [
    (2, "0.9", f"{f4(C['theta'])}°", False),
    (3, "0.63", "[PENDING MATLAB]", True),
    (4, "90", f"{f4(C['ad_db'])} dBi", False),
    (5, "10.59625", "[PENDING MATLAB]", True),
    (6, "10.09625 to 11.09625 GHz, 50 MHz steps", "[PENDING MATLAB] Expected near az = -90°, el = 0°", True),
]:
    c = cells(t.rows[row_i])
    set_cell(c[1], left)
    set_cell(c[3], right, red=pending)

# Table 2
t = T[4]
c = cells(t.rows[2]); set_cell(c[1], "UST Manila"); set_cell(c[3], "Valenzuela City")
c = cells(t.rows[3]); set_cell(c[1], "14°36'31.23\"N, 120°59'17.80\"E"); set_cell(c[3], "14°40'08.72\"N, 120°59'11.05\"E")
c = cells(t.rows[4]); set_cell(c[1], "Rooftop of the Buenaventura Garcia Paredes, O.P. (BGPOP) Building"); set_cell(c[3], "Rooftop of a 6-storey Fini Homes building, Ramon Delfin St., Marulas")
c = cells(t.rows[5]); set_cell(c[1], "12 floors × 2.5 m = 30 m"); set_cell(c[3], "6 floors × 2.5 m = 15 m")
c = cells(t.rows[6]); set_cell(c[-1], f"{f4(C['d_km'])} km")
c = cells(t.rows[7]); set_cell(c[-1], "Pacific Icon Residences 2 (P2), Chinese General Hospital (P7), 4th St. building (P13), 11th Ave. building (P15), Manila Central University (P17)")

# Table 3
t = T[5]
for r in ROWS:
    c = cells(t.rows[r["n"] + 1])
    vals = [str(r["n"]), f"{f4(r['d1'])} km", f"{f4(r['d2'])} km", f"{f4(r['elev'])} m", f"{f4(r['bulge'])} m", f"{f4(r['f60'])} m", f"{f4(r['the'])} m"]
    for cell, value in zip(c, vals):
        set_cell(cell, value, size=8.5)

# Table 4
t = T[6]
c = cells(t.rows[2]); set_cell(c[-1], f"{f4(M['hmin'])} m")
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
    6: ("Narda-MITEQ LNA-30-08001200-15-15P [3]", "8.0 to 12.0 GHz", "30 dB (min)"),
    7: (None, None, "1.5 dB (max)"),
    8: ("Fairview FMWCA1107, antenna side [4]", "8.2 to 12.4 GHz", "0.2 dB"),
    9: ("Fairview FMWCA1025, amplifier side [5]", "8.2 to 12.4 GHz", "0.3 dB"),
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
for p in list(d.paragraphs):
    if any(re.search(x, p.text.strip()) for x in done):
        p._p.getparent().remove(p._p)

# Section 1
cur = Cursor(T[3]._tbl)
cur.para()
cur.para("Theoretical computation", bold=True)
cur.para(f"λ = c / fc = (3 × 10⁸) / (10.59625 × 10⁹) = {C['lam']:.6f} m")
cur.para(f"AD = (πD / λ)² = [π(1.8) / {C['lam']:.6f}]² = {f4(C['ad_lin'])} = {f4(C['ad_db'])} dBi")
cur.para(f"Θh = 70λ / D = 70({C['lam']:.6f}) / 1.8 = {f4(C['theta'])}°")

# Section 2 map
cur = Cursor(T[4]._tbl)
cur.para()
im = Image.open(MAP_SHOT).convert("RGB")
crop = im.crop((0, 103, im.width, 665))
map_path = os.path.join(HERE, "map_points.jpg")
crop.save(map_path, quality=92)
cur.picture(map_path, 5.8)
cur.caption("Figure 1. Straight-line path and points from UST BGPOP to Fini Homes in Google Earth")

# Path profile figure before Table 3
anchor = find_para(r"^Path Profile")
cur = Cursor(anchor._p)
cur.picture(os.path.join(HERE, "path_profile.png"), 6.5)
cur.caption("Figure 2. Path profile showing all 20 points, THE, and the minimum antenna height")

# Worked point
p2 = ROWS[1]
cur = Cursor(T[5]._tbl)
cur.para()
cur.para("Sample computation at the governing point (P2)", bold=True)
cur.para(f"helevation = 2.77 + 26(2.5) = {f4(p2['elev'])} m")
cur.para(f"hearth bulge = d1d2 / 12.75 = ({f4(p2['d1'])})({f4(p2['d2'])}) / 12.75 = {f4(p2['bulge'])} m")
cur.para(f"F1 = 17.3√[d1d2 / (f(d1 + d2))] = 17.3√[({f4(p2['d1'])})({f4(p2['d2'])}) / (10.59625 × {f4(C['d_km'])})] = {f4(p2['f1'])} m")
cur.para(f"0.6F1 = 0.6({f4(p2['f1'])}) = {f4(p2['f60'])} m")
cur.para(f"THE = {f4(p2['elev'])} + {f4(p2['bulge'])} + {f4(p2['f60'])} = {f4(p2['the'])} m")

# Towers
cur = Cursor(T[6]._tbl)
cur.para()
cur.para(f"hantenna(min) = maximum THE = {f4(M['hmin'])} m (P2)")
cur.para(f"htower,A = {f4(M['hmin'])} - {f4(ROWS[0]['elev'])} = {f4(M['tower_a'])} m")
cur.para(f"htower,B = {f4(M['hmin'])} - {f4(ROWS[-1]['elev'])} = {f4(M['tower_b'])} m")

# Equipment notes
cur = Cursor(T[7]._tbl)
cur.para()
cur.para(f"Waveguide loss: 2.995 dB/100 ft ÷ 30.48 m = {C['wg_db_m']:.4f} dB/m, using the listed value closest to fc (12.4 GHz).")
cur.para(f"Waveguide length: LA = {f4(M['tower_a'])} + 3 = {f4(M['len_a'])} m; LB = {f4(M['tower_b'])} + 3 = {f4(M['len_b'])} m")
cur.para(f"Power gain of simulated antenna: AP = AD + 10log(0.55) = [PENDING MATLAB]. Using the theoretical AD as a reference only: {f4(C['ad_db'])} - 2.5964 = {f4(C['ap_theory'])} dBi, compared with 44 dBi from the specification sheet.", red=True)

# Link budget
anchor = find_para(r"^FSL, RSL, and FM")
cur = Cursor(anchor._p)
th = M["fm_theory"]
cur.para("Free-space loss", bold=True)
cur.para(f"FSL = 20log(4π/c) + 20log(fHz) + 20log(D) = 20log[4π/(3 × 10⁸)] + 20log(10.59625 × 10⁹) + 20log({C['d_m']:.2f}) = {f4(C['fsl'])} dB")
cur.para("Received signal level", bold=True)
cur.para(f"Pin = 10log(2000 mW) = {f4(C['pin'])} dBm")
cur.para(f"GTotal = 2(44) + 30 - {f4(M['wg_a'])} - {f4(M['wg_b'])} - {f4(M['conn'])} - 0 = {f4(M['g_total'])} dB")
cur.para(f"RSL = {f4(C['pin'])} + {f4(M['g_total'])} - {f4(C['fsl'])} = {f4(M['rsl_out'])} dBm at the output of the Site B amplifier")
cur.para(f"RSL at the amplifier input = {f4(M['rsl_out'])} - 30 = {f4(M['rsl_in'])} dBm. The output stays below the +15 dBm P1dB.")
cur.para(f"RSL with the simulated antenna = [PENDING MATLAB]. Reference using theoretical AD and 55% efficiency: {f4(M['rsl_ref'])} dBm.", red=True)
cur.para("Microwave versus fiber loss", bold=True)
cur.para(f"Microwave loss = FSL + waveguide + connectors = {f4(C['fsl'])} + {f4(M['wg_a'] + M['wg_b'])} + {f4(M['conn'])} = {f4(M['micro_loss'])} dB")
cur.para(f"Fiber length = 8.9 km road route + 0.030 km + 0.015 km vertical = {f4(M['fiber_len'])} km")
cur.para(f"Fiber loss = 0.22 dB/km × {f4(M['fiber_len'])} km = {f4(M['fiber_loss'])} dB at 1550 nm [6], excluding splices and connectors")
cur.para("Experimental fade margin", bold=True)
cur.para(f"N = 10log(kTB / 1 mW) = 10log[(1.38 × 10⁻²³)(290)(2.5 × 10⁶) / 10⁻³] = {f4(M['n'])} dBm")
cur.para("T = 290 K is the standard noise reference temperature. B = 2.5 MHz is the spacing between the assigned 4ECE-B channels.")
cur.para(f"PR(th) = {f4(M['n'])} + 10 + 1.5 = {f4(M['pth'])} dBm")
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
cur.para("R ≈ 99.999999999999%, so the design exceeds all four reliability targets.")

# Appendix
anchor = find_para(r"^Specification Sheets")
cur = Cursor(anchor._p)
specs = [
    ("antenna_VHLP6-11W-A_p1.png", "Figure A1. ANDREW VHLP6-11W/A antenna specification sheet [1]"),
    ("lna_LNA-30-08001200-15-15P_p1.png", "Figure A2. Narda-MITEQ LNA-30-08001200-15-15P specification sheet [3]"),
    ("adapter_FMWCA1107_p1.png", "Figure A3. Fairview FMWCA1107 adapter specification sheet [4]"),
    ("adapter_FMWCA1025_p1.png", "Figure A4. Fairview FMWCA1025 adapter specification sheet [5]"),
    ("fiber_G652D_p1.png", "Figure A5. Prysmian G.652.D fiber cable specification sheet [6]"),
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
for note in [
    "Member Attestation still says no AI was used. Update it to match what the professor allowed before anyone signs.",
    f"Biggest design issue: P2 forces {f4(M['tower_a'])} m and {f4(M['tower_b'])} m towers. Frassati to Fini Homes may avoid P2 and would need about {60.04 - 19.97:.2f} m at Fini and no Frassati tower, but that line has not been traced and Frassati's 23 floors need confirming.",
    f"Guideline step 7 can also be read as counting an amplifier at both sites. That gives RSL = {f4(M['rsl_out'] + 30)} dBm and FM = {f4(M['fm'] + 30)} dB, but it would overdrive this LNA, so confirm the intended reading with the professor.",
    "B = 2.5 MHz is inferred from the spacing of the 4ECE-B channels in guideline Table 4. Confirm it against the NTC Microwave Channel Plan.",
    "Verify every floor count marked as an estimate in Table A1.",
    "P2 is treated as blocking because the line runs within a few meters of Pacific Icon Residences 2. Its 26 floors come from one property listing.",
    f"If the group proves the line clears P2, the governing point becomes P15: hantenna(min) = {f4(ALT['hmin'])} m, towers = {f4(ALT['tower_a'])} m (A) and {f4(ALT['tower_b'])} m (B), RSL = {f4(ALT['rsl_out'])} dBm. That RSL exceeds the +15 dBm P1dB, so the amplifier would need to change.",
    "The 2 W is treated as the Site A transmit power, because the selected LNA is rated for only +13 dBm input. Only the Site B amplifier gain is counted.",
    f"FM follows the guideline's RSL at the amplifier output. Referred to the amplifier input, FM = {f4(M['fm_in'])} dB.",
    "The ANDREW sheet does not list the antenna's feed interface, so confirm that the antenna-side adapter fits.",
]:
    cur.para("• " + note, red=True, size=9.5, after=2)

anchor = find_para(r"^References")
cur = Cursor(anchor._p)
refs = [
    "[1] ANDREW, an Amphenol Company, “VHLP6-11W/A product specifications,” Mar. 12, 2025. [Online]. Available: https://www.andrew.com/globalassets/digizuite/471721-p360-vhlp6-11w-a-external.pdf",
    "[2] ATM Microwave, “Rectangular waveguide information.” [Online]. Available: https://www.atmmicrowave.com/tech-notes/rectangular-waveguide-information/",
    "[3] Narda-MITEQ, “LNA-30-08001200-15-15P low noise amplifier,” Rev. 1.2. [Online]. Available: https://www.nardamiteq.com/docs/LNA-30-08001200-15-15P.PDF",
    "[4] Fairview Microwave, “FMWCA1107 data sheet,” Rev. 1.0, 2020. [Online]. Available: https://fairviewmicrowave.com/images/productPDF/FMWCA1107.pdf",
    "[5] Fairview Microwave, “FMWCA1025 data sheet,” Rev. 1.0, 2018. [Online]. Available: https://fairviewmicrowave.com/images/productPDF/FMWCA1025.pdf",
    "[6] Prysmian Group, “G652D cable datasheet,” 2021. [Online]. Available: https://ec.prysmian.com/sites/ec.prysmian.com/files/media/documents/G652D.pdf",
    "[7] iRealtee, “Pacific Icon Residences 2.” [Online]. Available: https://irealtee.com/properties/pacific-icon-residences-2-sampaloc-manila",
]
for ref in refs:
    cur.para(ref, size=9.5, after=3)

d.save(DST)
print("saved", DST)

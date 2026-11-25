"""Fill Section 2 (Option A, Frassati to Fini) into a copy of the group's latest document."""
import json
import os
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.text.paragraph import Paragraph

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC, DST = sys.argv[1], sys.argv[2]
R = json.load(open(os.path.join(HERE, "results_A.json"), encoding="utf-8"))
C, ROWS, M = R["common"], R["rows"], R["main"]
f4 = lambda v: f"{v:.4f}"
d = docx.Document(SRC)
BLACK = RGBColor(0, 0, 0)


def set_cell(cell, text, size=None):
    p = cell.paragraphs[0]
    for extra in cell.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    runs = [r for r in p.runs]
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
        run = runs[0]
    else:
        run = p.add_run(text)
    run.font.color.rgb = BLACK
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

    def para(self, text="", bold=False, italic=False, center=False, size=None, after=4):
        p = OxmlElement("w:p")
        self.el.addnext(p)
        self.el = p
        para = Paragraph(p, d._body)
        if text:
            r = para.add_run(text)
            r.bold, r.italic = bold, italic
            r.font.color.rgb = BLACK
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

    def caption(self, text):
        self.para(text, italic=True, center=True, size=9, after=8)

    def table(self, data, widths, size=8.5):
        t = d.add_table(rows=len(data), cols=len(data[0]))
        pr = t._tbl.tblPr
        b = OxmlElement("w:tblBorders")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{side}")
            e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "808080")
            b.append(e)
        pr.append(b)
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                c = t.rows[i].cells[j]
                c.width = Inches(widths[j])
                p = c.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(str(value))
                run.font.size = Pt(size)
                run.bold = i == 0
        self.el.addnext(t._tbl)
        self.el = t._tbl


# Locate Section 2 and its tables by caption text, not by index
paras = d.paragraphs
start = next(i for i, p in enumerate(paras) if p.text.strip().startswith("Section 2."))
end = next(i for i, p in enumerate(paras) if p.text.strip().startswith("Section 3."))


def table_named(prefix):
    for t in d.tables:
        if t.rows[0].cells[0].text.strip().startswith(prefix):
            return t
    raise KeyError(prefix)


t2, t3, t4 = table_named("Table 2."), table_named("Table 3."), table_named("Table 4.")

# Table 2
c = cells(t2.rows[2]); set_cell(c[1], "UST Manila"); set_cell(c[3], "Valenzuela City")
c = cells(t2.rows[3]); set_cell(c[1], f"{ROWS[0]['lat']}, {ROWS[0]['lon']}"); set_cell(c[3], f"{ROWS[-1]['lat']}, {ROWS[-1]['lon']}")
c = cells(t2.rows[4]); set_cell(c[1], "Rooftop of the UST Frassati Building"); set_cell(c[3], "Rooftop of a 6-storey Fini Homes building, Marulas")
c = cells(t2.rows[5]); set_cell(c[1], "23 floors × 2.5 m = 57.5 m"); set_cell(c[3], "6 floors × 2.5 m = 15 m")
c = cells(t2.rows[6]); set_cell(c[-1], f"{f4(C['d_km'])} km")
c = cells(t2.rows[7]); set_cell(c[-1], "8-storey building under construction on Asuncion St (between P17 and P18), Maranatha/PMCC tower (between P5 and P6), mid-rise block (P2), low-rise buildings (P14, P15), and the 15 to 20 m ridge (P12 to P17)")

# Table 3
for r in ROWS:
    vals = [str(r["n"]), f"{f4(r['d1'])} km", f"{f4(r['d2'])} km", f"{f4(r['elev'])} m", f"{f4(r['bulge'])} m", f"{f4(r['f60'])} m", f"{f4(r['the'])} m"]
    for cell, v in zip(cells(t3.rows[r["n"] + 1]), vals):
        set_cell(cell, v, size=9)

# Table 4
c = cells(t4.rows[2]); set_cell(c[-1], f"{f4(M['h_ant_a'])} m (Site A), {f4(M['h_ant_b'])} m (Site B), tilted")
c = cells(t4.rows[3]); set_cell(c[1], f"{f4(ROWS[0]['elev'])} m"); set_cell(c[2], f"{f4(ROWS[-1]['elev'])} m")
c = cells(t4.rows[4]); set_cell(c[1], f"{f4(M['tower_a'])} m"); set_cell(c[2], f"{f4(M['tower_b'])} m")

# Remove finished Section 2 instructions, keep the handwritten-computation reminders
keep = re.compile(r"^Include and explain the screenshots of handwritten")
for p in paras[start:end]:
    reds = [r for r in p.runs if r.text.strip() and r.font.color is not None and r.font.color.rgb is not None and str(r.font.color.rgb) != "000000"]
    if reds and p.text.strip() and not keep.search(p.text.strip()):
        p._p.getparent().remove(p._p)

# Site locations: discussion, map, overlay, reflection answer
cur = Cursor(t2._tbl)
cur.para(f"Discussion: Site A is on the rooftop of the UST Frassati Building, and Site B is on the rooftop of a 6-storey Fini Homes building in Valenzuela. The straight-line distance between the sites is {f4(C['d_km'])} km. Building heights use 2.5 m per floor.")
cur.picture(os.path.join(HERE, "map_points_A.jpg"), 4.8)
cur.caption("Figure 2.1: Straight-line path and the 20 points from UST Frassati to Fini Homes in Google Earth")
cur.para("Discussion: Points P2 to P19 are spaced about 350.60 m apart along the straight line between the sites.")
cur.picture(os.path.join(HERE, "map_overlay_A.png"), 4.8)
cur.caption("Figure 2.2: Simulated azimuth patterns at both sites, each pointed at the other site, with the 6.6614 km distance")
cur.para("Discussion: Each antenna's main lobe is pointed at the other site, so the maximum directive gain lies along the path.")
cur.para("Reflection question: The azimuth pattern is used for the overlay. Google Maps shows the horizontal plane, and the azimuth pattern is the cut in that same plane, so it shows how the beam is pointed from one site toward the other. The elevation pattern describes the vertical plane, which a flat map cannot show.")

# Path profile figure right after the Path Profile heading
heading = next(p for p in d.paragraphs if p.text.strip() == "Path Profile")
cur = Cursor(heading._p)
cur.picture(os.path.join(HERE, "path_profile_A.png"), 6.3)
cur.caption("Figure 2.3: Path profile showing all 20 points, THE, and the minimum antenna height")
cur.para(f"Discussion: The ground rises from about 2.5 m near UST to a 15 to 20 m ridge between P12 and P17, then drops near the Tullahan River. The dashed red line is the tilted line of sight from {f4(M['h_ant_a'])} m at Frassati to {f4(M['h_ant_b'])} m at Fini Homes. It stays at or above THE at every point and the near-line buildings, and just touches the THE of the building under construction on Asuncion St.")

# Sample computation and near-line check after Table 3
p = ROWS[14]
cur = Cursor(t3._tbl)
cur.para("Sample computation at the highest intermediate point (P15)", bold=True)
cur.para(f"helevation = {p['ground']:.2f} + {p['floors']}(2.5) = {f4(p['elev'])} m")
cur.para(f"hearth bulge = d1d2 / 12.75 = ({f4(p['d1'])})({f4(p['d2'])}) / 12.75 = {f4(p['bulge'])} m")
cur.para(f"F1 = 17.3√[d1d2 / (f(d1 + d2))] = 17.3√[({f4(p['d1'])})({f4(p['d2'])}) / (10.59625 × {f4(C['d_km'])})] = {f4(p['f1'])} m")
cur.para(f"0.6F1 = 0.6({f4(p['f1'])}) = {f4(p['f60'])} m")
cur.para(f"THE = {f4(p['elev'])} + {f4(p['bulge'])} + {f4(p['f60'])} = {f4(p['the'])} m")
cur.para("Near-line obstruction check", bold=True)
cur.para("The Maranatha/PMCC tower lies between P5 and P6, with its west corner at the path line (d1 = 1.6630 km). Using 9 floors from Street View: THE = 4.35 + 9(2.5) + 0.6519 + 3.5620 = 31.0639 m, which is below the " + f"{f4(M['h_ant_a'] + (M['h_ant_b'] - M['h_ant_a']) * 1.6630 / C['d_km'])}" + " m height of the tilted line of sight at that point.")

# Tower computation after Table 4
g = M["tilt_point"]
cur = Cursor(t4._tbl)
cur.para("Tilted antenna mounting (guideline Part 3, item 9)", bold=True)
cur.para(f"With equal antenna heights, both antennas would sit at the maximum THE of {f4(M['hmin'])} m (P1), which needs a {f4(M['flat_tower_b'])} m tower at Site B. The antennas are instead mounted at an angle, keeping line of sight and clearance from every THE.")
cur.para("Two buildings between the sampled points were also checked because they sit within the 0.6F1 clearance of the line:")
for e in M["extras"]:
    cur.para(f"• {e['name']} = {e['label']}: d1 = {f4(e['d1'])} km, THE = {e['ground']:.2f} + {e['floors']}(2.5) + {f4(e['bulge'])} + {f4(e['f60'])} = {f4(e['the'])} m")
cur.para(f"Site A antenna height: hA = THE at P1 = {f4(M['h_ant_a'])} m, so htower,A = {f4(M['h_ant_a'])} - {f4(ROWS[0]['elev'])} = {f4(M['tower_a'])} m")
cur.para("For each point, the straight line from Site A must stay at or above THE: hA - (hA - hB)(d1 / D) ≥ THE, so hB ≥ hA - (hA - THE)(D / d1).")
cur.para(f"The largest required hB is at {g['name']}: hB = {f4(M['h_ant_a'])} - ({f4(M['h_ant_a'])} - {f4(g['the'])})({f4(C['d_km'])} / {f4(g['d1'])}) = {f4(M['h_ant_b'])} m")
cur.para(f"htower,B = {f4(M['h_ant_b'])} - {f4(ROWS[-1]['elev'])} = {f4(M['tower_b'])} m")
cur.para(f"Tilt angle = tan⁻¹[(hA - hB) / D] = tan⁻¹[({f4(M['h_ant_a'])} - {f4(M['h_ant_b'])}) / {C['d_m']:.2f}] = {M['tilt_deg']:.4f}°, downward at Site A and upward at Site B")
cur.para(f"Justification: the ANDREW VHLP6-11W/A antenna mount has a ±5° fine elevation adjustment, so a {M['tilt_deg']:.4f}° tilt is within its range. The tilt is also smaller than half of the antenna's vertical beamwidth (1° on the specification sheet, 0.9200° simulated), and each antenna is aimed directly at the other.")
data = [["Point", "d1 (km)", "THE (m)", "Line of sight (m)", "Clearance above THE (m)"]]
for c_ in M["clearance"]:
    data.append([c_["name"], f4(c_["d1"]), f4(c_["the"]), f4(c_["line"]), f4(c_["margin"])])
cur.table(data, [0.6, 1.1, 1.3, 1.6, 1.9])
cur.caption("Table 4.1. Clearance of the tilted line of sight at all 20 points and the two near-line buildings")
cur.para(f"Discussion: Site A needs no added tower, only a rooftop mount on the Frassati Building. Site B needs a {f4(M['tower_b'])} m mast on the Fini Homes rooftop instead of a {f4(M['flat_tower_b'])} m tower. The building under construction on Asuncion St (N) sets the tilt because the line of sight just touches its THE.")

d.save(DST)
print("saved", DST)

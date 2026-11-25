"""Create build_opt.py from build_doc.py so Options A and B share one verified template builder."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "build_doc.py"), encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)


rep('DST = r"C:\\UST\\TRANSMA PROJECT\\4ECEB_Group5_Report_DRAFT.docx"',
    'OPT = os.environ["OPT"]\nDST = {"A": r"C:\\UST\\TRANSMA PROJECT\\4ECEB_Group5_Report_OPTION_A_Frassati.docx", "B": r"C:\\UST\\TRANSMA PROJECT\\4ECEB_Group5_Report_OPTION_B_BGPOP.docx"}[OPT]')
rep('MAP_SHOT = r"C:\\Users\\Lenovo\\.claude\\projects\\C--UST-TRANSMA-PROJECT\\84d6406d-f149-4c45-afef-396d97e96f97\\tool-results\\mcp-Claude_Browser-blob-1795457183609-wsmcqz.jpg"',
    'TR = r"C:\\Users\\Lenovo\\.claude\\projects\\C--UST-TRANSMA-PROJECT\\84d6406d-f149-4c45-afef-396d97e96f97\\tool-results"\nMAP_SHOT = os.path.join(TR, {"A": "mcp-Claude_Browser-blob-1795468641453-mx4aj1.jpg", "B": "mcp-Claude_Browser-blob-1795457183609-wsmcqz.jpg"}[OPT])')
rep('R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))',
    'R = json.load(open(os.path.join(HERE, f"results_{OPT}.json"), encoding="utf-8"))\nAMP = R["amp"]\nIS_A = OPT == "A"')
rep('"A fixed point-to-point microwave link is needed between UST Manila and Valenzuela City. The 6.6877 km path',
    'f"A fixed point-to-point microwave link is needed between UST Manila and Valenzuela City. The {C[\'d_km\']:.4f} km path')
rep('''f"The link uses 1.8 m parabolic antennas, 2 W input power, WR-90 waveguide, and a low noise amplifier. The minimum antenna height is {f4(M['hmin'])} m, requiring {f4(M['tower_a'])} m and {f4(M['tower_b'])} m towers at Sites A and B.",''',
    '''(f"The link uses 1.8 m parabolic antennas, 2 W input power, WR-90 waveguide, and a low noise amplifier. The minimum antenna height is {f4(M['hmin'])} m. The Frassati rooftop already reaches this height, so Site A needs no added tower and Site B needs a {f4(M['tower_b'])} m tower." if IS_A else f"The link uses 1.8 m parabolic antennas, 2 W input power, WR-90 waveguide, and a low noise amplifier. The minimum antenna height is {f4(M['hmin'])} m, requiring {f4(M['tower_a'])} m and {f4(M['tower_b'])} m towers at Sites A and B."),''')
rep('''set_cell(c[1], "14°36'31.23\\"N, 120°59'17.80\\"E")''', '''set_cell(c[1], ROWS[0]["lat"] + ", " + ROWS[0]["lon"])''')
rep('set_cell(c[1], "Rooftop of the Buenaventura Garcia Paredes, O.P. (BGPOP) Building")',
    'set_cell(c[1], "Rooftop of the UST Frassati Building" if IS_A else "Rooftop of the Buenaventura Garcia Paredes, O.P. (BGPOP) Building")')
rep('set_cell(c[1], "12 floors × 2.5 m = 30 m")',
    'set_cell(c[1], f"{ROWS[0][\'floors\']} floors × 2.5 m = {ROWS[0][\'floors\'] * 2.5:g} m")')
rep('set_cell(c[-1], "Pacific Icon Residences 2 (P2), Chinese General Hospital (P7), 4th St. building (P13), 11th Ave. building (P15), Manila Central University (P17)")',
    'set_cell(c[-1], "Maranatha/PMCC tower (between P5 and P6), mid-rise block (P2), low-rise buildings (P14, P15), and the 15 to 20 m ridge (P12 to P17)" if IS_A else "Pacific Icon Residences 2 (P2), Chinese General Hospital (P7), 4th St. building (P13), 11th Ave. building (P15), Manila Central University (P17)")')
rep('6: ("Narda-MITEQ LNA-30-08001200-15-15P [3]", "8.0 to 12.0 GHz", "30 dB (min)"),',
    '6: (f"{AMP[\'name\']} [3]", AMP["band"], f"{AMP[\'gain\']:g} dB (min)"),')
rep('7: (None, None, "1.5 dB (max)"),', '7: (None, None, f"{AMP[\'nf\']:g} dB (max)"),')
rep('9: ("Fairview FMWCA1025, amplifier side [5]", "8.2 to 12.4 GHz", "0.3 dB"),',
    '9: ("Fairview FMWCA1025 + FMAD1245 SMA male-male adapter, amplifier side [5], [7]", "8.2 to 12.4 GHz", "0.3 + 0.21 = 0.51 dB"),')
rep('crop = im.crop((0, 103, im.width, 665))', 'crop = im.crop((170, 110, 640, 665) if IS_A else (0, 103, im.width, 665))')
rep('map_path = os.path.join(HERE, "map_points.jpg")', 'map_path = os.path.join(HERE, f"map_points_{OPT}.jpg")')
rep('cur.picture(map_path, 5.8)', 'cur.picture(map_path, 4.8 if IS_A else 5.8)')
rep('cur.caption("Figure 1. Straight-line path and points from UST BGPOP to Fini Homes in Google Earth")',
    'cur.caption(f"Figure 1. Straight-line path and points from UST {\'Frassati\' if IS_A else \'BGPOP\'} to Fini Homes in Google Earth")')
rep('cur.picture(os.path.join(HERE, "path_profile.png"), 6.5)',
    'cur.picture(os.path.join(HERE, "path_profile_A.png" if IS_A else "path_profile.png"), 6.5)')
rep('p2 = ROWS[1]', 'p2 = ROWS[14] if IS_A else ROWS[1]\nsample = "P15" if IS_A else "P2"')
rep('cur.para("Sample computation at the governing point (P2)", bold=True)',
    'cur.para("Sample computation at the highest intermediate point (P15)" if IS_A else "Sample computation at the governing point (P2)", bold=True)')
rep('''cur.para(f"helevation = 2.77 + 26(2.5) = {f4(p2['elev'])} m")''',
    '''cur.para(f"helevation = {p2['ground']:.2f} + {p2['floors']}(2.5) = {f4(p2['elev'])} m")''')
rep('''cur.para(f"THE = {f4(p2['elev'])} + {f4(p2['bulge'])} + {f4(p2['f60'])} = {f4(p2['the'])} m")''',
    '''cur.para(f"THE = {f4(p2['elev'])} + {f4(p2['bulge'])} + {f4(p2['f60'])} = {f4(p2['the'])} m")
if IS_A:
    cur.para("Near-line obstruction check", bold=True)
    cur.para("The Maranatha/PMCC tower lies between P5 and P6, with its west corner at the path line (d1 = 1.6630 km). Using 9 floors from Street View: THE = 4.35 + 9(2.5) + 0.6519 + 3.5620 = 31.0639 m, which is below the 60.0400 m minimum antenna height.")''')
rep('''cur.para(f"hantenna(min) = maximum THE = {f4(M['hmin'])} m (P2)")''',
    '''cur.para(f"hantenna(min) = maximum THE = {f4(M['hmin'])} m (P{M['governing']})")''')
rep('''cur.para(f"GTotal = 2(44) + 30 - ''', '''cur.para(f"GTotal = 2(44) + {AMP['gain']:g} - ''')
rep('''cur.para(f"RSL at the amplifier input = {f4(M['rsl_out'])} - 30 = {f4(M['rsl_in'])} dBm. The output stays below the +15 dBm P1dB.")''',
    '''cur.para(f"RSL at the amplifier input = {f4(M['rsl_out'])} - {AMP['gain']:g} = {f4(M['rsl_in'])} dBm. The input is below the +{AMP['max_in']:g} dBm maximum, and the output is below the +{AMP['p1db']:g} dBm P1dB.")''')
rep('''cur.para(f"Fiber length = 8.9 km road route + 0.030 km + 0.015 km vertical = {f4(M['fiber_len'])} km")''',
    '''cur.para(f"Fiber length = 8.9 km road route + {ROWS[0]['obstruction'] / 1000:.4f} km + {ROWS[-1]['obstruction'] / 1000:.4f} km vertical = {f4(M['fiber_len'])} km")''')
rep('''cur.para(f"PR(th) = {f4(M['n'])} + 10 + 1.5 = {f4(M['pth'])} dBm")''',
    '''cur.para(f"PR(th) = {f4(M['n'])} + 10 + {AMP['nf']:g} = {f4(M['pth'])} dBm")''')
rep('cur.para("R ≈ 99.999999999999%, so the design exceeds all four reliability targets.")',
    '''cur.para(f"R = 1 - {M['unreliability']:.4e} ≈ 99.999999999999%, so the design exceeds all four reliability targets.")''')
rep('("lna_LNA-30-08001200-15-15P_p1.png", "Figure A2. Narda-MITEQ LNA-30-08001200-15-15P specification sheet [3]"),',
    '("lna_ERZ-LNA-0800-1220-26-2_p1.png" if IS_A else "lna_LNA-30-08001200-15-15P_p1.png", f"Figure A2. {AMP[\'name\']} specification sheet [3]"),')
rep('("fiber_G652D_p1.png", "Figure A5. Prysmian G.652.D fiber cable specification sheet [6]"),',
    '("adapter_FMAD1245_p1.png", "Figure A5. Fairview FMAD1245 SMA male-male adapter specification sheet [7]"),\n    ("fiber_G652D_p1.png", "Figure A6. Prysmian G.652.D fiber cable specification sheet [6]"),')

notes = r'''NOTES_COMMON = [
    "Member Attestation still says no AI was used. Update it to match what the professor allowed before anyone signs.",
    "B = 2.5 MHz is inferred from the spacing of the 4ECE-B channels in guideline Table 4. Confirm it against the NTC Microwave Channel Plan.",
    "The ANDREW sheet does not list the antenna's feed interface, so confirm that the antenna-side adapter fits.",
    "The waveguide adapter and amplifier are both SMA female, so a 0.21 dB SMA male-male adapter was added at each site.",
    f"FM follows the guideline's RSL at the amplifier output. Referred to the amplifier input, FM = {f4(M['fm_in'])} dB.",
]
if IS_A:
    NOTES = [
        "This is OPTION A: UST Frassati to Fini Homes.",
        "The Site A tower is 0 m because the Frassati rooftop sets the minimum height. The antenna still needs a rooftop mount, and only the 3 m horizontal waveguide run is counted there.",
        f"Guideline step 7 can also be read as counting an amplifier at both sites. That gives RSL = {f4(M['rsl_out'] + AMP['gain'])} dBm and FM = {f4(M['fm'] + AMP['gain'])} dB, but the 2 W input exceeds this LNA's +10 dBm maximum input, so confirm the intended reading with the professor.",
        "Floor counts at P2 to P19 are satellite estimates. A sampled point would need more than 14 floors to change the minimum antenna height.",
        "The Maranatha/PMCC floor count is from Street View. It would need more than 20 floors to change the result.",
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
'''
s, n = re.subn(r'for note in \[.*?\]:\n    cur\.para\("• " \+ note, red=True, size=9\.5, after=2\)\n', lambda _: notes, s, flags=re.S)
assert n == 1

refs = r'''refs = [
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
for ref in refs:'''
s, n = re.subn(r'refs = \[.*?\]\nfor ref in refs:', lambda _: refs, s, flags=re.S)
assert n == 1
open(os.path.join(HERE, "build_opt.py"), "w", encoding="utf-8").write(s)
print("patched")

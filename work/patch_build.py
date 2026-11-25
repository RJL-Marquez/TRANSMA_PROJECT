import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b, 1)
rep("for p in d.paragraphs[:12]:", "for p in d.paragraphs[:30]:")
rep("        para.paragraph_format.space_after = Pt(after)\n", "        para.paragraph_format.space_after = Pt(after)\n        para.paragraph_format.keep_with_next = bool(bold)\n")
rep("# Remove completed instructions", "for i, name in ((2, 'Parabolic Reflector Antenna'), (4, 'Rectangular Waveguide'), (6, 'Amplifier'), (8, 'Connector'), (9, 'Connector')):\n    set_cell(cells(t.rows[i])[0], name, size=8)\n\n# Remove completed instructions")
rep('    "Verify every floor count marked as an estimate in Table A1.",\n', '''    "Member Attestation still says no AI was used. Update it to match what the professor allowed before anyone signs.",
    f"Biggest design issue: P2 forces {f4(M['tower_a'])} m and {f4(M['tower_b'])} m towers. Frassati to Fini Homes may avoid P2 and would need about {60.04 - 19.97:.2f} m at Fini and no Frassati tower, but that line has not been traced and Frassati's 23 floors need confirming.",
    f"Guideline step 7 can also be read as counting an amplifier at both sites. That gives RSL = {f4(M['rsl_out'] + 30)} dBm and FM = {f4(M['fm'] + 30)} dB, but it would overdrive this LNA, so confirm the intended reading with the professor.",
    "B = 2.5 MHz is inferred from the spacing of the 4ECE-B channels in guideline Table 4. Confirm it against the NTC Microwave Channel Plan.",
    "Verify every floor count marked as an estimate in Table A1.",
''')
open(p, "w", encoding="utf-8").write(s)

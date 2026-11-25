"""Add MATLAB simulation results to build_opt.py (run after patch_options.py)."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "build_opt.py")
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)


rep('IS_A = OPT == "A"', r'''IS_A = OPT == "A"
MDIR = os.path.join(HERE, "matlab")
_log = open(os.path.join(MDIR, "sim_antenna.log"), encoding="utf-8", errors="replace").read()
_m = re.search(r"Dmax = ([\d.]+) dBi at az = ([-\d.]+) deg, el = ([-\d.]+) deg", _log)
_b = re.search(r"HPBW azimuth plane = ([\d.]+) deg, elevation plane = ([\d.]+) deg", _log)
SIM = dict(d=float(_m.group(1)), az=float(_m.group(2)), el=float(_m.group(3)), bw_az=float(_b.group(1)), bw_el=float(_b.group(2)))
SIM["ap"] = SIM["d"] + 10 * __import__("math").log10(0.55)''')
rep('(3, "0.63", "[PENDING MATLAB]", True),',
    '(3, "0.63", f"{SIM[\'bw_az\']:.4f}° (azimuth plane), {SIM[\'bw_el\']:.4f}° (elevation plane)", False),')
rep('(5, "10.59625", "[PENDING MATLAB]", True),', '(5, "10.59625", f"{f4(SIM[\'d\'])} dBi", False),')
rep('(6, "10.09625 to 11.09625 GHz, 50 MHz steps", "[PENDING MATLAB] Expected near az = -90°, el = 0°", True),',
    '(6, "10.09625 to 11.09625 GHz, 50 MHz steps", f"az = {SIM[\'az\']:.2f}°, el = {SIM[\'el\']:.2f}°", False),')
rep('''cur.para(f"Θh = 70λ / D = 70({C['lam']:.6f}) / 1.8 = {f4(C['theta'])}°")''',
    '''cur.para(f"Θh = 70λ / D = 70({C['lam']:.6f}) / 1.8 = {f4(C['theta'])}°")
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
cur.para(f"Directive gain: {f4(SIM['d'])} dBi simulated versus {f4(C['ad_db'])} dBi theoretical, a difference of {f4(C['ad_db'] - SIM['d'])} dB. The theoretical formula assumes uniform aperture illumination, while the dipole feed tapers the illumination and spills some power past the reflector edge.")
cur.para(f"Beamwidth: {SIM['bw_az']:.4f}° and {SIM['bw_el']:.4f}° simulated versus {f4(C['theta'])}° theoretical. The two planes differ because the dipole feed pattern is not rotationally symmetric.")''')
rep("Figure 1. Straight-line", "Figure 5. Straight-line")
rep("Figure 2. Path profile", "Figure 7. Path profile")
s, n = re.subn(r'(cur\.caption\(f"Figure 5\. Straight-line[^\n]*\n)', lambda m: m.group(1) + '''if IS_A:
    cur.picture(os.path.join(HERE, "map_overlay_A.png"), 4.8)
    cur.caption(f"Figure 6. Simulated azimuth patterns at both sites, each pointed at the other site, with the 6,661.37 m distance")
    cur.para("Reflection question: The azimuth pattern is used for the overlay. Google Maps shows the horizontal plane, and the azimuth pattern is the cut in that same plane, so it shows how the beam is pointed from one site toward the other. The elevation pattern describes the vertical plane, which a flat map cannot show.")
''', s)
assert n == 1
rep('r"^Links where"]', 'r"^Links where"]\ndone += [r"^Include and explain the screenshots of the Matlab", r"^Compare the theoretical and experimental"]\nif IS_A:\n    done.append(r"^Overlay the radiation")')
s, n = re.subn(r'cur\.para\(f"Power gain of simulated antenna:.*?red=True\)\n',
               lambda _: 'cur.para(f"Power gain of simulated antenna: AP = AD + 10log(0.55) = {f4(SIM[\'d\'])} - 2.5964 = {f4(SIM[\'ap\'])} dBi, compared with 44 dBi from the specification sheet.")\n', s)
assert n == 1
s, n = re.subn(r'cur\.para\(f"RSL with the simulated antenna = \[PENDING MATLAB\].*?red=True\)\n',
               lambda _: 'cur.para(f"RSL with the simulated antenna (AP = {f4(SIM[\'ap\'])} dBi at both sites) = {f4(M[\'rsl_out\'])} - 2(44 - {f4(SIM[\'ap\'])}) = {f4(M[\'rsl_out\'] - 2 * (44 - SIM[\'ap\']))} dBm. It is {f4(2 * (44 - SIM[\'ap\']))} dB lower than with the ANDREW antenna, which has a higher power gain.")\n', s)
assert n == 1
rep("""cur.para(f"λ = c / fc = (3 × 10⁸) / (10.59625 × 10⁹) = {C['lam']:.6f} m")""",
    """cur.para("λ = c / fc = (3 × 10⁸) / (10.59625 × 10⁹) = 0.028312 m, rounded to 0.0283 m as in the handwritten solution")""")
assert s.count("{C['lam']:.6f}") == 2
s = s.replace("{C['lam']:.6f}", "{C['lam']:.4f}")
rep("""a difference of {f4(C['ad_db'] - SIM['d'])} dB.""",
    """a difference of {f4(C['ad_db'] - SIM['d'])} dB. In linear terms, the simulated directive gain is {10 ** ((SIM['d'] - C['ad_db']) / 10) * 100:.4f}% of the theoretical value.""")
open(p, "w", encoding="utf-8").write(s)
print("sim patched")

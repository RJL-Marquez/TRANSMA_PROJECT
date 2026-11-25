import re
src = open("plot_a.py", encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith('ax.annotate("N:'):
        lines[i] = 'ax.annotate("P17 sets the tilt\n(line just clears its THE)", (g["d1"], g["the"]), xytext=(g["d1"] - 2.4, 50),'
src = "\n".join(lines)
rep = [
 ('"results_A.json"', '"results_M.json"'),
 ('label="THE of near-line buildings (M, N)"', 'label="THE of near-line structures (M: Maranatha tower, L: LRT-1 viaduct)"'),
 ('xytext=(5.95, 28)', 'xytext=(6.15, 12)'),
 ('"Path Profile: UST Frassati (Site A) to Fini Homes, Valenzuela (Site B)"', '"Path Profile: UST Frassati (Site A) to Metro Industries, Valenzuela (Site B)"'),
 ('"path_profile_A.png"', '"path_profile_M.png"'),
]
for a, b in rep:
    assert a in src, a
    src = src.replace(a, b)
assert "P17 sets the tilt" in src
open("plot_m.py", "w", encoding="utf-8").write(src)

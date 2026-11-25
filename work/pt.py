"""Usage: pt.py N s  -> coordinate of point N shifted s metres along the line (north positive)."""
import json, sys
L = json.load(open(__file__.replace("pt.py", "metro_line.json")))
n, s = int(sys.argv[1]), float(sys.argv[2])
d1 = (n - 1) / 19 * L["D"] + s
t = d1 / L["D"]
A, B = L["A"], L["B"]
print(f"P{n}: d1 = {d1:.1f} m -> {A[0] + t*(B[0]-A[0]):.7f}, {A[1] + t*(B[1]-A[1]):.7f}")

"""Line from the group's Frassati pin to Metro Industries (84 Ramon Delfin), with evenly spaced reference spots."""
import json, math, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from draft_points import vincenty, dms, to_dms  # noqa
A = (dms(14, 36, 32.71), dms(120, 59, 31.75))
B = (dms(14, 40, 17.32), dms(120, 59, 12.63))
D = vincenty(*A, *B)
az = math.degrees(math.atan2((B[1]-A[1])*math.cos(math.radians(A[0])), B[0]-A[0])) % 360
print(f"D = {D:.2f} m, heading {az:.2f} deg, even spacing {D/19:.2f} m")
def at(t):
    return A[0] + t*(B[0]-A[0]), A[1] + t*(B[1]-A[1])
rows=[]
for i in range(20):
    la, lo = at(i/19)
    rows.append(dict(n=i+1, t=i/19, lat=la, lon=lo))
    print(i+1, f"{la:.7f}, {lo:.7f}", f"{vincenty(*A, la, lo) if i else 0:.1f}")
json.dump(dict(A=A, B=B, D=D, rows=rows), open(os.path.join(HERE, "metro_line.json"), "w"), indent=1)

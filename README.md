# TRANSMA Project: ECE21129 Microwave Link Design (4ECE-B, Group 5)

A 10.59625 GHz point-to-point microwave link from the UST Frassati Building (Site A) to Metro Industries, 84 Ramon Delfin St, Marulas, Valenzuela (Site B). Due **November 27, 2026**.

Start with **[WHERE_WE_LEFT_OFF.md](WHERE_WE_LEFT_OFF.md)**. It has the current numbers, the open tasks, and how to rerun everything.

## Current design at a glance

| Item | Value |
|---|---|
| Path length | 6.9270 km |
| Antenna heights A / B (tilted) | 59.9700 m / 29.1511 m |
| Towers A / B | 0.0000 m / 5.6711 m (flat method would need 36.4900 m) |
| Tilt | 0.2549° |
| RSL at amplifier output | 13.6878 dBm |
| Fade margin | 111.4856 dB |

![Path profile](report/path_profile_M.png)

## Folders

| Folder | What is inside |
|---|---|
| `report/` | Report files. **`4ECEB_Group5_Report_Metro_Section2.docx`** is the group's latest export with Section 2 filled for Metro Industries; `_preview.pdf` is the same file rendered. `Section2_Metro_Text.md` is the Section 2 text for pasting into Google Docs; `Section2_Metro_Industries.md` is the same with figures. Also the `.mat` deliverable and older option drafts (Fini Homes Site B) |
| `figures/` | Map, pattern overlay, path profile, and MATLAB pattern images. `_M` = Metro Industries (current), `_A` = Frassati to Fini (old Option A), `_B` = BGPOP to Fini (old Option B) |
| `specs/` | Specification sheet images for the appendix (antenna, adapters, amplifiers, fiber) |
| `notes/` | AI use log, Option A vs B comparison, guideline rules, project setup, and site-selection history |
| `work/` | Python scripts, point data, results JSON, and the MATLAB simulation (`work/matlab/sim_antenna.m`) |

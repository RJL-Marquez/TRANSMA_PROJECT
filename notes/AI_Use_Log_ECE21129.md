# AI Use Log: ECE21129 Design Project, 4ECE-B Group 5

Tool: Claude Code (Claude Opus 5.5), desktop app
Dates: November 23 to 26, 2026 (entries 14 to 21 on November 26)

This log summarizes the prompts. Copy the exact wording from the chat if your professor needs it verbatim.

| # | What the group asked | What the AI produced | What the group must verify or do |
|---|---|---|---|
| 1 | Read the guidelines and report template | Summary of requirements and assigned values | Check values against the latest guideline revision |
| 2 | Check the groupmate's MATLAB antenna script | List of errors and a corrected script | Run it, save the `.mat`, and capture Antenna Designer results |
| 3 | Explain how to get elevation and building height | Google Earth method using floors × 2.5 m | Follow the guideline method |
| 4 | Research and compare Valenzuela and UST sites | Candidate ranking, distances, and clearance estimates | Confirm the final site pair |
| 5 | Trace the straight line between candidate sites | Obstruction checks in Google Earth | Confirm clearances |
| 6 | Add the 20 path points in the TRANSMA project | Placemarks P2 to P19 with ground elevations | Check placemarks and floor counts |
| 7 | Continue the computations using the guidelines and lecture PDFs | Path profile, tower heights, equipment selection, FSL, RSL, FM, fiber comparison, and reliability | Recompute by hand and include the handwritten solutions |
| 8 | Fill in a separate copy of the template | `4ECEB_Group5_Report_DRAFT.docx` | Reword all text, replace pending items, and remove draft notes |
| 9 | Trace Frassati to Fini as a second option and keep BGPOP | Placemarks F2 to F19, `FINI to FRASSATI` line, and building checks | Confirm Frassati floors and floor estimates |
| 12 | Review the group's Section 1 and add Section 2 to a copy of the group's document | `4ECEB_Group5_Report_with_Section2.docx` and a list of Section 1 fixes | Apply the Section 1 fixes in the group's own words |
| 13 | Trace Frassati to Metro Industries (84 Ramon Delfin) with 20 points placed on the tallest roofs near an even spacing, and fill the Section 2 tables | Google Earth pins M2 to M19 and LRT EDSA, `4ECEB_Group5_Report_Metro_Section2.docx` with Tables 2 to 4.1, map, overlay, and path profile | Confirm Metro Industries' floor count, P17's floor count, and the LRT-1 viaduct height in Street View; do the handwritten computations |
| 11 | Run the MATLAB antenna simulation on the group's PC | `4ECEB_Group5_Antenna.mat`, pattern figures, Table 1 values, and the map overlay | Capture Antenna Designer screenshots if the professor wants them from the app |
| 10 | Check the amplifier and make Frassati Option A and BGPOP Option B | Amplifier and connector update, `4ECEB_Group5_Report_OPTION_A_Frassati.docx`, `4ECEB_Group5_Report_OPTION_B_BGPOP.docx`, and `Option_A_vs_B_Comparison.md` | Recheck the computations, reword all text, and remove draft notes |

| 14 | Clone the repo, then build a step-by-step solutions document for every Section 2 table | Solutions builder (`work/docgen/`), path profile script `work/section2_path_profile.py` | Check each step by hand |
| 15 | Add a safety margin above THE | 2.5 m (one floor) margin on both antennas; masts and tilt recomputed | Group chose 2.5 m on both antennas |
| 16 | Split the handwritten solutions among the five members | `report/4ECEB_Group5_Section2_Task_Distribution.docx` (checklist, solutions to copy, scan boxes) | Each member writes and scans their part |
| 17 | Check Section 2 and Section 3 against the guideline PDF | Earth bulge corrected to d1·d2/(12.75k), k = 4/3; RSL taken at the Site B amplifier output; B = 2.5 MHz from the channel spacing | Group confirmed the corrections |
| 18 | Recount Site B from Street View | Site B counted as 6 floors at the pin (5-storey building + rooftop structure); P20, mast and waveguide recomputed | Group confirmed the count |
| 19 | Shorten the tower computations | h_B from P17 only and a 2-row clearance check instead of the 20-row and 22-row tables | None |
| 20 | Draft Section 3 (equipment, FSL, RSL, FM) in a separate file | `report/4ECEB_Group5_Section3_DRAFT.docx`, `work/section3_calc.py`; equipment from spec sheets and the ATM waveguide table | Add the missing spec sheets, write the computations by hand, reword in the group's own words |
| 21 | Review the group's own Section 2 paragraphs | Fixes (distance typo, 6 floors, figure numbering) and talking points; draft coordinates and notes for a point table | Group writes the final text |

Not done by AI: MATLAB simulation results, handwritten computations, Introduction, Conclusion, member details, and signatures.

// Section 3 (Link Budget) draft, separate from the main report. Data: work/results_S3.json
process.env.SEC2_DATA = process.env.SEC2_DATA || __dirname + "/sec2_steps.json";
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, ShadingType, BorderStyle } = require("docx");
const { docOptions, p, h1, h2, h3, bullet, formula, table, caption, runs, BODY } = require("./build_solutions.js");

const [, , resPath, outPath] = process.argv;
const R = JSON.parse(fs.readFileSync(resPath, "utf8"));
const E = R.equip, G = R.given;
const f4 = (x) => x.toFixed(4), f2 = (x) => x.toFixed(2);
const C = [];
const note = (s) => new Paragraph({
  children: runs(s, { size: 20 }), spacing: { before: 80, after: 120 },
  shading: { type: ShadingType.CLEAR, fill: "FFF2CC", color: "auto" },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: "BF9000", space: 8 } }, indent: { left: 240 },
});
const step = (rows) => table([2300, 4926, 1800], ["Step", "Working", "Answer"], rows, { mathCol: 1, align: ["l", "l", "r"], hl: new Set([rows.length - 1]) });

// ---------------- title ----------------
C.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Section 3. Link Budget (Draft)")] }));
C.push(p("ECE21129 Microwave Link Design · 4ECE-B Group 5 · UST Frassati Building (Site A) to Metro Industries, Valenzuela (Site B)", { color: "404040" }));
C.push(p("This is a working draft kept separate from the main report. It follows Section 3 of the design project guidelines (items 1 to 13) and the template's instructions. Every equipment value comes from a specification sheet; the distance and tower heights come from Section 2 (with the 12.75k earth bulge and the 2.5 m margin). Hand calculations use four decimal places and metric units.", { after: 120 }));
C.push(note("Still to do before this goes into the report: (1) add three spec sheets to the appendix: the WR-90 rows of the ATM waveguide table, the VHLP6-11W-6WH/A product page, and the Pasternack PE-W90SF006-12 data sheet; (2) write the computations in Part 2 by hand and insert the pictures with figure numbers and captions; (3) put the explanations in the group's own words. The compliance checklist at the end maps every guideline item to this draft."));

// ---------------- Part 1 ----------------
C.push(h1("Part 1. List of Equipment"));
C.push(h2("1.1 System setup at each site"));
C.push(p("The guideline's setup (its Figure 2) has, at each site, the antenna on a mast, a rectangular waveguide running down the mast and 3 m across to a cabinet, connectors at both ends, and the amplifier in the cabinet at the bottom of the mast. The signal path is:"));
C.push(table([1500, 7526], ["Site", "Signal path"], [
  ["Site A (transmit)", `Transmitter, 2 W → FMAD1245 SMA male-male → FMWCA1025 WR-90 to SMA adapter → WR-90 waveguide, ${f4(R.len_a)} m → PE-W90SF006-12 flexible section (CPR-90G) → VHLP6-11W-6WH/A antenna`],
  ["Site B (receive)", `VHLP6-11W-6WH/A antenna → PE-W90SF006-12 flexible section (CPR-90G) → WR-90 waveguide, ${f4(R.len_b)} m → FMWCA1025 WR-90 to SMA adapter → FMAD1245 SMA male-male → ERZIA low noise amplifier (RSL is taken at its output)`],
], { boldCol: 0 }));

C.push(h2("1.2 Table 5. Equipment Information"));
C.push(table([1500, 2300, 1400, 2026, 1800], ["Equipment", "Brand/Model", "Frequency Band", "Parameter", "Value*"], [
  ["Parabolic reflector antenna", "ANDREW (Amphenol) VHLP6-11W-6WH/A, 1.8 m [1]", "10.000 – 11.700 GHz", "Power gain (mid band)", `${f4(E.ant_gain)} dBi`],
  ["", "", "", "Installation loss", "0.0000 dB (not listed)"],
  ["Rectangular waveguide", "ATM WR-90, copper, RG-52/U [2]", "8.20 – 12.40 GHz", "Loss per unit length", `${E.wg_db_100ft} dB/100 ft = ${f4(E.wg_db_m)} dB/m`],
  ["", "", "", "Required length", `A: ${f4(R.len_a)} m, B: ${f4(R.len_b)} m`],
  ["Amplifier", "ERZIA ERZ-LNA-0800-1220-26-2 [3]", "8 – 12.2 GHz", "Amplifier gain (min)", `${f4(E.amp_gain)} dB`],
  ["", "", "", "Noise figure (max)", `${f4(E.amp_nf)} dB`],
  ["Connector (antenna to waveguide)", "Pasternack PE-W90SF006-12, WR-90 flexible section, CPR-90G both ends [7]", "8.2 – 12.4 GHz", "Connector loss (max)", `${f4(E.conn_ant)} dB`],
  ["Connector (waveguide to amplifier)", "Fairview FMWCA1025, WR-90 UG-135/U to SMA female [4]", "8.2 – 12.4 GHz", "Connector loss (typ)", `${f4(E.conn_wg)} dB`],
  ["Connector (SMA to SMA)", "Fairview FMAD1245, SMA male-male [5]", "DC – 26.5 GHz", "Connector loss (max)", `${f4(E.conn_sma)} dB`],
], { align: ["l", "l", "l", "l", "r"] }));
C.push(p("*Values per piece, at each site. Values are those closest to the center frequency of 10.59625 GHz, as the template asks.", { italics: true, color: "555555", before: 60 }));

C.push(h2("1.3 Why each part was chosen"));
C.push(h3("Antenna"));
C.push(p(`The VHLP6-11W/A family covers 10.000 – 11.700 GHz, which includes 10.59625 GHz, and its 1.8 m diameter is the same as the simulated reflector (radius 0.9 m). The sheet gives 43.2 dBi (low band), 44 dBi (mid band) and 44.8 dBi (top band). The band's midpoint is 10.85 GHz; 10.59625 GHz is 0.2538 GHz from it and 0.5963 GHz from the 10.000 GHz low edge, so the mid band gain of 44 dBi is used. The sheet lists no installation loss, so 0 dB is used (guideline item 1). The -6WH/A variant is ordered because it has a CPR90G waveguide flange; its electrical specifications are the same as the base VHLP6-11W/A sheet. The mount allows ±5° of fine elevation adjustment, which covers the ${f4(R.tilt)}° tilt from Section 2.`));
C.push(h3("Waveguide"));
C.push(p(`Rectangular waveguide is used, as the guideline asks. WR-90 (RG-52/U) is the size whose recommended TE10 range, 8.20 – 12.40 GHz, contains 10.59625 GHz; its TE10 cut-off is 6.560 GHz (also listed in the M05A lecture). Copper is chosen over aluminum (RG-67/U) because it has lower loss. ATM lists the theoretical attenuation as 4.238 dB/100 ft at 8.20 GHz and 2.995 dB/100 ft at 12.40 GHz. 10.59625 GHz is 1.8038 GHz from 12.40 GHz and 2.3963 GHz from 8.20 GHz, so the 12.40 GHz value is the closest: 2.995 / 30.48 = ${f4(E.wg_db_m)} dB/m.`));
C.push(h3("Amplifier"));
C.push(p(`The ERZIA low noise amplifier covers 8 – 12.2 GHz. Its sheet gives a gain of 25 dB (min), 26 dB (typ) and 28 dB (max), and a noise figure of 1.6 (min), 1.8 (typ) and 2.2 dB (max). The worst case is used: 25 dB gain and 2.2 dB noise figure. Its RF ports are SMA female.`));
C.push(h3("Connectors"));
C.push(p(`Antenna to waveguide: the antenna's waveguide port is a CPR90G flange. The Pasternack PE-W90SF006-12 is a 12 in (304.8 mm) WR-90 flexible section with a CPR-90G flange on both ends, so it matches the antenna on one side and the waveguide (ordered with a CPR-90G flange at the top; copper WR-90 is offered with CPR-90G flanges in the ATM table) on the other. Being flexible, it also absorbs the small misalignment from the ${f4(R.tilt)}° tilt and mast movement. Its sheet gives VSWR 1.07:1 and a maximum insertion loss of 0.9 dB, which is used.`));
C.push(p("Waveguide to amplifier: the bottom of the waveguide has a UG-39/U square cover flange, which has the same size and bolt pattern as the UG-135/U flange of the Fairview FMWCA1025 (WR-90 to SMA female, 0.3 dB typical). Both the FMWCA1025 and the amplifier have SMA female ports, so a Fairview FMAD1245 SMA male-male adapter (0.21 dB maximum) joins them. At Site A the same pair connects the transceiver to the waveguide. All connectors are 50 Ω SMA or WR-90, so the impedances match (VSWR 1.07:1 to 1.25:1 on the sheets)."));

C.push(h2("1.4 Power gain: specification sheet vs simulated antenna"));
C.push(formula("G_{p} = D_{max} + 10 log_{10}(η)", "η = 0.55"));
C.push(step([
  ["Simulated D_{max}", "MATLAB Antenna Designer (Section 1)", `${f4(R.sim_dmax)} dBi`],
  ["10 log_{10}(0.55)", "10 log_{10}(0.55)", `${f4(10 * Math.log10(0.55))} dB`],
  ["Simulated G_{p}", `${f4(R.sim_dmax)} + (${f4(10 * Math.log10(0.55))})`, `${f4(R.sim_gain)} dBi`],
]));
C.push(p(`The commercial antenna's 44.0000 dBi is ${f4(E.ant_gain - R.sim_gain)} dB higher than the simulated antenna's ${f4(R.sim_gain)} dBi. Both are 1.8 m dishes. The commercial antenna's efficiency is higher than the assumed 55%, and the simulated reflector uses only the default feed and the three assigned parameters.`, { before: 80 }));

C.push(h2("1.5 Required waveguide length"));
C.push(formula("L = h_{tower} + 3 m", "vertical run up the mast + 3 m horizontal run to the cabinet"));
C.push(step([
  ["Site A", `${f4(R.tower_a)} + 3`, `${f4(R.len_a)} m`],
  ["Site B", `${f4(R.tower_b)} + 3`, `${f4(R.len_b)} m`],
]));

// ---------------- Part 2 ----------------
C.push(h1("Part 2. FSL, RSL, and FM"));
C.push(h2("2.1 Free space loss (item 6)"));
C.push(formula("FSL(dB) = 20 log_{10}(4π/c) + 20 log_{10}(f_{Hz}) + 20 log_{10}(D)", "D in metres"));
C.push(step([
  ["20 log_{10}(4π/c)", "20 log_{10}(4π / 3×10^{8})", `${f4(R.fsl_terms[0])} dB`],
  ["20 log_{10}(f)", "20 log_{10}(10.59625×10^{9})", `${f4(R.fsl_terms[1])} dB`],
  ["20 log_{10}(D)", `20 log_{10}(${f4(R.d_m)})`, `${f4(R.fsl_terms[2])} dB`],
  ["FSL", `${f4(R.fsl_terms[0])} + ${f4(R.fsl_terms[1])} + ${f4(R.fsl_terms[2])}`, `${f4(R.fsl)} dB`],
]));

C.push(h2("2.2 Total gain and received signal level (item 7)"));
C.push(formula("RSL(dBm) = P_{in}(dBm) + G_{Total}(dB) − FSL(dB)", "up to the output of the Site B amplifier"));
C.push(formula("G_{Total} = G_{A} + G_{B} + G_{amp} − L_{WG,A} − L_{WG,B} − L_{conn} − L_{install}"));
C.push(p(`The 2 W is the transceiver power fed into Site A's line (the guideline's P_in). Only the Site B amplifier's gain is counted: the RSL is taken at its output, as item 7 asks, and a low noise amplifier cannot take 2 W (33.0103 dBm) at its input, since its output saturates at about ${f2(E.amp_p1db)} dBm. Connector and waveguide losses are counted at both sites.`));
C.push(step([
  ["P_{in}", "10 log_{10}(2 W / 1 mW) = 10 log_{10}(2000)", `${f4(R.p_in)} dBm`],
  ["L_{WG,A}", `${f4(R.len_a)} m × ${f4(E.wg_db_m)} dB/m`, `${f4(R.wg_a)} dB`],
  ["L_{WG,B}", `${f4(R.len_b)} m × ${f4(E.wg_db_m)} dB/m`, `${f4(R.wg_b)} dB`],
  ["L_{conn}", `2 sites × (${f2(E.conn_ant)} + ${f2(E.conn_wg)} + ${f2(E.conn_sma)})`, `${f4(R.conn)} dB`],
  ["L_{install}", "2 × 0", "0.0000 dB"],
  ["G_{Total}", `${f2(E.ant_gain)} + ${f2(E.ant_gain)} + ${f2(E.amp_gain)} − ${f4(R.wg_a)} − ${f4(R.wg_b)} − ${f4(R.conn)} − 0`, `${f4(R.g_total)} dB`],
  ["RSL", `${f4(R.p_in)} + ${f4(R.g_total)} − ${f4(R.fsl)}`, `${f4(R.rsl)} dBm`],
]));
C.push(p(`Check: the amplifier input is ${f4(R.rsl)} − ${f2(E.amp_gain)} = ${f4(R.rsl_amp_in)} dBm, and its output, ${f4(R.rsl)} dBm, is below its minimum 1 dB compression point of ${f2(E.amp_p1db)} dBm, so the amplifier works in its linear range.`, { before: 80 }));

C.push(h2("2.3 RSL with the simulated antenna (item 8)"));
C.push(step([
  ["G_{Total,sim}", `${f4(R.sim_gain)} + ${f4(R.sim_gain)} + ${f2(E.amp_gain)} − ${f4(R.wg_a)} − ${f4(R.wg_b)} − ${f4(R.conn)}`, `${f4(R.g_total_sim)} dB`],
  ["RSL_{sim}", `${f4(R.p_in)} + ${f4(R.g_total_sim)} − ${f4(R.fsl)}`, `${f4(R.rsl_sim)} dBm`],
]));
C.push(p(`The simulated antenna gives an RSL ${f4(R.rsl - R.rsl_sim)} dB lower (twice the ${f4(E.ant_gain - R.sim_gain)} dB gain difference, since both sites use the same antenna). The link still works with the simulated antenna.`, { before: 80 }));

C.push(h2("2.4 Microwave vs fiber optic losses (item 9)"));
C.push(formula("L_{microwave} = FSL + L_{WG,A} + L_{WG,B} + L_{conn} + L_{install}"));
C.push(formula("L_{fiber} = α × (road distance + building heights)"));
C.push(step([
  ["L_{microwave}", `${f4(R.fsl)} + ${f4(R.wg_a)} + ${f4(R.wg_b)} + ${f4(R.conn)} + 0`, `${f4(R.micro_loss)} dB`],
  ["Fiber length", `${f2(E.road_km)} km road + (${f2(R.elev_a)} + ${f2(R.elev_b)}) m / 1000`, `${f4(R.fiber_len)} km`],
  ["L_{fiber}", `${f2(E.fiber_db_km)} dB/km × ${f4(R.fiber_len)} km (Prysmian G.652.D at 1550 nm [6])`, `${f4(R.fiber_loss)} dB`],
]));
C.push(p(`Road distance: Google Maps shortest road route from the Frassati pin to Metro Industries (via R-9), ${f2(E.road_km)} km. Building heights: Frassati 57.5 m and Metro Industries 15 m (5 storeys + rooftop structure), for the vertical runs. Splice and connector losses of the fiber are not included.`, { before: 80 }));
C.push(p(`Reflection: the fiber cable loses far less (${f4(R.fiber_loss)} dB vs ${f4(R.micro_loss)} dB) and is not affected by rain or obstructions, so it is better where a cable can be laid and maintained. The microwave link avoids digging and right-of-way permits along ${f2(E.road_km)} km of busy Manila and Caloocan roads, can be set up quickly on existing rooftops, and its antenna gains more than make up for the free space loss, so it suits links between buildings where laying cable is slow or expensive.`));

C.push(h2("2.5 Experimental fade margin (item 10)"));
C.push(formula("FM(dB) = RSL(dBm) − P_{R(th)}(dBm)"));
C.push(formula("P_{R(th)} = N(dBm) + SNR(dB) + NF(dB),   N(dBm) = 10 log_{10}(kTB / 1 mW)"));
C.push(step([
  ["kTB", `(1.38×10^{−23})(${G.T})(${G.B / 1e6}×10^{6})`, `${R.ktb.toExponential(4)} W`],
  ["N", `10 log_{10}(${R.ktb.toExponential(4)} / 10^{−3})`, `${f4(R.n_dbm)} dBm`],
  ["P_{R(th)}", `${f4(R.n_dbm)} + ${f2(G.snr)} + ${f2(E.amp_nf)}`, `${f4(R.p_th)} dBm`],
  ["FM", `${f4(R.rsl)} − (${f4(R.p_th)})`, `${f4(R.fm)} dB`],
]));
C.push(p(`Basis for T = 290 K: it is the standard reference temperature (17 °C) at which noise figures are specified, so it matches the amplifier's noise figure. Using Manila's warmer ambient (about 301 K, 28 °C) would raise N by only 10 log(301/290) = 0.1617 dB. Basis for B = 2.5 MHz: the guideline says the channel bandwidth follows the NTC microwave channel plan, and the 4ECE-B assigned center frequencies are spaced 2.5 MHz apart (10586.25, 10588.75, 10591.25 MHz …), so each channel is 2.5 MHz wide. SNR = 10 dB is given by the guideline. With the simulated antenna, FM = ${f4(R.rsl_sim)} − (${f4(R.p_th)}) = ${f4(R.fm_sim)} dB.`, { before: 80 }));

C.push(h2("2.6 Theoretical fade margin at four reliabilities (item 11)"));
C.push(formula("FM(dB) = 30 log_{10}(D) + 10 log_{10}(6ABf) − 10 log_{10}(1 − R) − 70", "D in km, f in GHz"));
C.push(step([
  ["30 log_{10}(D)", `30 log_{10}(${f4(R.d_km)})`, `${f4(R.base_terms[0])} dB`],
  ["10 log_{10}(6ABf)", `10 log_{10}(6 × ${G.A} × ${G.Bf} × ${G.f_ghz})`, `${f4(R.base_terms[1])} dB`],
  ["Sum of the R-independent terms", `${f4(R.base_terms[0])} + ${f4(R.base_terms[1])} − 70`, `${f4(R.base)} dB`],
]));
C.push(table([2000, 4226, 1500, 1300], ["Reliability R", "−10 log_{10}(1 − R)", "FM (dB)", "Met?"],
  R.fm_theory.map((x) => [`${(x.R * 100).toFixed(3).replace(/0+$/, "").replace(/\.$/, "")}%`, `−10 log_{10}(${(1 - x.R).toExponential(0)}) = ${f4(x.term)}`, f4(x.fm), x.meets ? "Yes" : "No"]),
  { mathCol: 1, align: ["l", "l", "r", "c"] }));
C.push(p("A negative or small theoretical value means fading at that reliability needs little or no margin over a path this short; the requirement grows by 10 dB for every extra 9 in the reliability.", { before: 80 }));
C.push(p(`Basis for A = 1: the path crosses flat to gently rolling urban ground (2.47 m to about 20 m along the path, Section 2), which is "average terrain" in the M03B lecture table, not water or smooth flat land (A = 4) or mountains (A = 0.25). Basis for B = 0.5: Metro Manila is a hot, humid area, the worst weather condition in that table for this site.`, { before: 80 }));

C.push(h2("2.7 Comparison and reliability (items 12 and 13)"));
C.push(p(`The experimental fade margin of ${f4(R.fm)} dB is larger than the theoretical fade margin at all four reliabilities (the largest is ${f4(R.fm_theory[3].fm)} dB at 99.999%), so the design meets 99.999% reliability. The margin is large because the 7 km path is short, both antennas have about 44 dBi of gain, and the amplifier adds 25 dB.`));
C.push(formula("10 log_{10}(1 − R) = 30 log_{10}(D) + 10 log_{10}(6ABf) − 70 − FM"));
C.push(step([
  ["10 log_{10}(1 − R)", `${f4(R.base)} − ${f4(R.fm)}`, `${f4(R.base - R.fm)} dB`],
  ["1 − R", `10^{(${f4(R.base - R.fm)}/10)}`, R.unrel.toExponential(4)],
  ["R", `(1 − ${R.unrel.toExponential(4)}) × 100%`, "≈ 100.0000%"],
]));
C.push(p("This equation only models multipath fading. At 10.6 GHz, heavy tropical rain also attenuates the signal, so the real availability during typhoons would be lower than this figure; the large margin is what protects the link in that case.", { before: 80 }));

C.push(h2("2.8 Summary of Section 3 values"));
C.push(table([5026, 2000, 2000], ["Quantity", "Commercial antenna", "Simulated antenna"], [
  ["Free space loss, FSL", `${f4(R.fsl)} dB`, `${f4(R.fsl)} dB`],
  ["Input power, P_{in}", `${f4(R.p_in)} dBm`, `${f4(R.p_in)} dBm`],
  ["Antenna power gain (each)", `${f4(E.ant_gain)} dBi`, `${f4(R.sim_gain)} dBi`],
  ["Waveguide loss A / B", `${f4(R.wg_a)} / ${f4(R.wg_b)} dB`, "same"],
  ["Connector loss (both sites)", `${f4(R.conn)} dB`, "same"],
  ["Total gain, G_{Total}", `${f4(R.g_total)} dB`, `${f4(R.g_total_sim)} dB`],
  ["Received signal level, RSL", `${f4(R.rsl)} dBm`, `${f4(R.rsl_sim)} dBm`],
  ["Receiver sensitivity, P_{R(th)}", `${f4(R.p_th)} dBm`, `${f4(R.p_th)} dBm`],
  ["Experimental fade margin", `${f4(R.fm)} dB`, `${f4(R.fm_sim)} dB`],
  ["Microwave system loss", `${f4(R.micro_loss)} dB`, ""],
  ["Fiber optic system loss", `${f4(R.fiber_loss)} dB`, ""],
], { boldCol: 0, align: ["l", "r", "r"] }));

// ---------------- appendix ----------------
C.push(h1("Specification sheets for the appendix"));
C.push(table([700, 4626, 3700], ["Ref.", "Sheet", "Status"], [
  ["[1]", "ANDREW VHLP6-11W/A antenna (pages 1–2)", "Have: specs/antenna_VHLP6-11W-A_p1.png, _p2.png. Add the -6WH/A product page showing the CPR90G flange."],
  ["[2]", "ATM rectangular waveguide table, WR-90 rows (atmmicrowave.com, Tech Notes, Rectangular Waveguide Information)", "Need a screenshot"],
  ["[3]", "ERZIA ERZ-LNA-0800-1220-26-2", "Have: specs/lna_ERZ-LNA-0800-1220-26-2_p1.png"],
  ["[4]", "Fairview FMWCA1025", "Have: specs/adapter_FMWCA1025_p1.png (and p2)"],
  ["[5]", "Fairview FMAD1245", "Have: specs/adapter_FMAD1245_p1.png"],
  ["[6]", "Prysmian G.652.D fiber", "Have: specs/fiber_G652D_p1.png"],
  ["[7]", "Pasternack PE-W90SF006-12 WR-90 flexible section", "Need the data sheet page (pasternack.com, or the copy on alldatasheet.com)"],
], { align: ["c", "l", "l"] }));
C.push(p("No longer used: specs/adapter_FMWCA1107_p1/p2 (it converts waveguide to coax, which is not what the antenna side needs) and the two Narda-MITEQ amplifier sheets (an earlier option).", { italics: true, color: "555555", before: 80 }));

C.push(h1("References for this section"));
for (const s of [
  "[1] ANDREW, an Amphenol company, “VHLP6-11W/A 1.8 m | 6 ft ValuLine High Performance Low Profile Antenna,” product specifications, rev. Mar. 12, 2025.",
  "[2] ATM Microwave (Narda-MITEQ), “Rectangular Waveguide Information,” Tech Notes. [Online]. Available: https://www.atmmicrowave.com/tech-notes/rectangular-waveguide-information/",
  "[3] ERZIA, “ERZ-LNA-0800-1220-26-2 Low Noise Amplifier,” data sheet.",
  "[4] Fairview Microwave, “FMWCA1025 data sheet,” rev. 1.0, 2018.",
  "[5] Fairview Microwave, “FMAD1245 data sheet,” rev. 1.1, 2020.",
  "[6] Prysmian Group, “G652D: Properties of cable with standard Enhanced SM fibre,” 2021.",
  "[7] Pasternack, “PE-W90SF006-12 WR-90 Flexible Straight Waveguide Section, 12 Inch,” technical data sheet, rev. 1.0, 2014.",
  "[8] M. S. Matias and J. M. R. Reyes, “Microwave Communication,” ECE21129 Module 3B lecture, UST Electronics Engineering Department (fade margin, A and B factors, receiver threshold).",
  "[9] W. Tomasi, Electronic Communications Systems: Fundamentals Through Advanced, 5th ed. Pearson, 2004 (noise power at the 290 K reference temperature).",
]) C.push(p(s, { size: 19, after: 60 }));

C.push(h1("Guideline compliance checklist"));
C.push(table([3626, 3600, 1800], ["Guideline / template requirement", "Where it is met", "Status"], [
  ["1. Commercial antenna for the target frequency; power gain and installation loss from its sheet (0 dB if not listed)", "Table 5; 1.3 Antenna", "Done"],
  ["2. Rectangular (not elliptical) waveguide; WR number from the TE10 recommended range; loss per unit length", "Table 5; 1.3 Waveguide", "Done"],
  ["2. Waveguide length = tower height + 3 m horizontal", "1.5", "Done"],
  ["3. Amplifier gain and noise figure; amplifier at the bottom of the tower", "Table 5; 1.1; 1.3", "Done"],
  ["4. Connectors: (a) antenna to waveguide, (b) waveguide to amplifier, matched interfaces", "Table 5; 1.3 Connectors", "Done"],
  ["5. Complete the table of specifications, with units; values closest to f_c", "Table 5", "Done"],
  ["Template: compare spec-sheet power gain with the simulated antenna at 55% efficiency", "1.4", "Done"],
  ["6. FSL with 20log(4π/c) + 20log(f) + 20log(D), D from the 2D map distance", "2.1", "Done"],
  ["7. RSL up to the output of the Site B amplifier with 2 W input; G_Total includes amplifier, antenna, line, connector and installation terms", "2.2", "Done"],
  ["8. RSL with the simulated antenna (55% efficiency)", "2.3", "Done"],
  ["9. Microwave loss vs fiber (sheet attenuation × road distance + building heights); reflection question", "2.4", "Done"],
  ["10. Experimental FM; P_R(th) = N + SNR + NF with SNR = 10 dB; basis for the temperature", "2.5", "Done"],
  ["11. Theoretical FM at 99, 99.9, 99.99, 99.999%; bases/references for A and B (terrain, worst weather)", "2.6; refs [8]", "Done"],
  ["12. Compare experimental and theoretical FM; which reliability is met", "2.7", "Done"],
  ["13. System reliability from the experimental FM", "2.7", "Done"],
  ["Spec sheets in the appendix", "Appendix list", "3 sheets still to add"],
  ["Handwritten computations, four decimal places, metric units, with pictures, figure numbers and captions", "Part 2", "To do by the group"],
], { align: ["l", "l", "c"] }));

const doc = new Document(docOptions("4ECE-B Group 5 · Section 3 Link Budget (Draft)", C));
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(outPath, b); console.log("wrote", outPath, b.length); });

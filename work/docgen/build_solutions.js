// Build the Section 2 computations and solutions docx from sec2_steps.json
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, BorderStyle, Header, Footer, PageNumber, LevelFormat, VerticalAlign, TableLayoutType,
} = require("docx");

const dataPath = process.env.SEC2_DATA || process.argv[2], outPath = process.argv[3];
const d = JSON.parse(fs.readFileSync(dataPath, "utf8"));

const W = 9026; // A4 content width in DXA with 1 in margins
const BODY = "Calibri", MATH = "Cambria Math";
const f4 = (x) => x.toFixed(4), f6 = (x) => x.toFixed(6), f2 = (x) => x.toFixed(2);
const sgn6 = (x) => (x < 0 ? "(" + f6(x) + ")" : f6(x));
const rad = (x) => (x * Math.PI) / 180;

// "h_{elevation}" -> subscript, "x^{2}" -> superscript
function runs(s, o = {}) {
  const out = [];
  for (const part of String(s).split(/(_\{[^}]*\}|\^\{[^}]*\})/)) {
    if (!part) continue;
    const base = { font: o.font || BODY, size: o.size, bold: o.bold, italics: o.italics, color: o.color };
    if (part.startsWith("_{")) out.push(new TextRun({ ...base, text: part.slice(2, -1), subScript: true }));
    else if (part.startsWith("^{")) out.push(new TextRun({ ...base, text: part.slice(2, -1), superScript: true }));
    else out.push(new TextRun({ ...base, text: part }));
  }
  return out;
}
const p = (s, o = {}) => new Paragraph({ children: runs(s, o), spacing: { after: o.after ?? 120, before: o.before ?? 0 }, alignment: o.align, keepNext: o.keepNext });
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const h3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(t, { font: BODY }) });
const bullet = (s) => new Paragraph({ numbering: { reference: "bul", level: 0 }, children: runs(s), spacing: { after: 60 } });
// shaded formula line
const formula = (s, note) => new Paragraph({
  children: [...runs(s, { font: MATH, size: 23 }), ...(note ? runs("      " + note, { size: 19, italics: true, color: "555555" }) : [])],
  shading: { type: ShadingType.CLEAR, fill: "EEF2F8", color: "auto" },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: "2F5597", space: 8 } },
  indent: { left: 240 }, spacing: { before: 60, after: 60 },
});

const thin = { style: BorderStyle.SINGLE, size: 4, color: "A6A6A6" };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
function cell(content, width, o = {}) {
  // o.keep: keep this row with the next one
  const items = Array.isArray(content) ? content : [content];
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders, verticalAlign: VerticalAlign.CENTER,
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: items.map((s) => new Paragraph({ alignment: o.align, keepNext: o.keep, keepLines: true, children: runs(s, { size: o.size || 19, bold: o.bold, font: o.font }) })),
  });
}
// cols: widths; head: header strings; body: arrays of strings; opts.hl: set of row indexes to highlight; opts.align: per-col
function table(cols, head, body, o = {}) {
  const sum = cols.reduce((a, b) => a + b, 0);
  if (sum !== W) throw new Error("table width " + sum);
  const al = (i) => (o.align && o.align[i] === "c" ? AlignmentType.CENTER : o.align && o.align[i] === "r" ? AlignmentType.RIGHT : AlignmentType.LEFT);
  const rows = [new TableRow({ tableHeader: true, cantSplit: true, children: head.map((h, i) => cell(h, cols[i], { fill: "D9E2F3", bold: true, align: al(i), keep: o.keep })) })];
  body.forEach((r, ri) => rows.push(new TableRow({
    cantSplit: true,
    children: r.map((v, i) => cell(v, cols[i], { fill: o.hl && o.hl.has(ri) ? "FFF2CC" : undefined, align: al(i), bold: o.boldCol === i, font: o.mathCol === i ? MATH : undefined, keep: o.keep && ri < body.length - 1 })),
  })));
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cols, layout: TableLayoutType.FIXED, rows });
}
const caption = (s) => p(s, { bold: true, after: 80, before: 160, keepNext: true });
const spacer = () => new Paragraph({ children: [], spacing: { after: 80 } });

const C = [];
const marks = [];
const mark = (k) => marks.push([k, C.length]);
const D = d.D, DK = d.DK, F = d.F, g = d.geo;
const fD = F * DK;
const R = d.rows, last = R[R.length - 1];

// ---------------- Title ----------------
C.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Section 2. Path Planning: Computations and Solutions")] }));
C.push(p("ECE21129 Microwave Link Design · 4ECE-B Group 5 · UST Saint Pier Giorgio Frassati Building (Site A) to Metro Industries, 84 Ramon Delfin St, Marulas, Valenzuela (Site B)", { color: "404040" }));
C.push(p("This file shows how every value in Tables 2, 3 and 4 of the report, and the clearance check, was obtained, table by table. The working keeps 6 decimal places so that each sum comes out right; every final answer is rounded to 4 decimal places, the same as in the report. The design keeps a 2.5 m safety margin above every THE, added to both antennas (Part 3). Distances d₁, d₂ and D are in km inside the formulas unless a step says metres.", { after: 160 }));

// ---------------- Part 0 ----------------
mark("given");
C.push(h1("0. Given data and constants"));
C.push(table([1500, 3226, 2300, 2000], ["Symbol", "Meaning", "Value", "Source"], [
  ["f", "Operating (center) frequency", "10.59625 GHz", "Section 1"],
  ["h_{floor}", "Height per floor (Philippine buildings are not 3D in Google Earth)", "2.5 m", "Guideline"],
  ["12.75", "Earth bulge constant (d in km, result in m)", "12.75", "Guideline"],
  ["k", "Effective earth radius factor (standard atmosphere)", "4/3, so 12.75k = 17", "Guideline"],
  ["17.3", "Fresnel zone constant (d in km, f in GHz, result in m)", "17.3", "Guideline"],
  ["a", "WGS-84 equatorial radius", "6,378,137 m", "WGS-84 (Google Earth)"],
  ["f_{e}", "WGS-84 flattening", "1 / 298.257223563", "WGS-84"],
  ["e^{2}", "Eccentricity squared = f_{e}(2 − f_{e})", f6(d.E2) + "…", "Computed"],
  ["Site A", "Frassati Building rooftop", "14°36'32.71\"N 120°59'31.75\"E; ground 2.47 m; 23 floors", "Google Earth pin"],
  ["Site B", "Metro Industries rooftop", "14°40'17.32\"N 120°59'12.63\"E; ground 10.98 m; 5 storeys + 1-storey rooftop structure = 6 floors", "Google Earth pin, Street View"],
], { boldCol: 0 }));

mark("formulas");
C.push(h2("Quick formula sheet"));
C.push(table([2300, 4426, 2300], ["Quantity", "Formula", "Units"], [
  ["Building height", "floors × 2.5", "m"],
  ["h_{elevation}", "h_{earth contour} + h_{obstruction} = ground + floors × 2.5", "m"],
  ["d_{2}", "D − d_{1}", "km"],
  ["h_{earth bulge}", "d_{1}·d_{2} / (12.75k),  k = 4/3", "d in km → m"],
  ["F_{1}", "17.3 √[ d_{1}·d_{2} / (f·D) ],  D = d_{1} + d_{2}", "d in km, f in GHz → m"],
  ["Fresnel clearance", "0.6 F_{1}", "m"],
  ["THE", "h_{elevation} + h_{earth bulge} + 0.6F_{1}", "m"],
  ["h_{antenna} (equal heights)", "maximum THE of the 20 points + m", "m"],
  ["h_{tower}", "h_{antenna} − h_{elevation} of the site", "m"],
  ["Tilted line of sight at d_{1}", "h_{LOS} = h_{A} − (h_{A} − h_{B})(d_{1} / D)", "m"],
  ["Safety margin", "m = 2.5 m kept above every THE (one floor)", "m"],
  ["Site A antenna (tilted)", "h_{A} = THE(P1) + m", "m"],
  ["Lowest allowed h_{B}", "h_{B} ≥ h_{A} − (h_{A} − THE − m)(D / d_{1})  for every point", "m"],
  ["Tilt angle", "tan^{−1}[ (h_{A} − h_{B}) / D ],  D in m", "degrees"],
  ["Clearance above THE", "h_{LOS} − THE  (≥ m)", "m"],
], { mathCol: 1 }));

// ---------------- Part 1: Table 2 ----------------
mark("1");
C.push(h1("1. Table 2. Site Information"));
mark("1.1");
C.push(h2("1.1 Height of building and h-elevation at each site"));
C.push(formula("Height of building = floors × 2.5 m"));
C.push(bullet("Site A: 23 × 2.5 = 57.5000 m"));
C.push(bullet("Site B: (5 + 1) × 2.5 = 15.0000 m (5-storey block plus the 1-storey rooftop structure the mast stands on)"));
C.push(formula("h_{elevation} = h_{earth contour} + h_{obstruction}"));
C.push(bullet("Site A: h_{elevation} = 2.47 + 57.50 = 59.9700 m"));
C.push(bullet("Site B: h_{elevation} = 10.98 + 15.00 = 25.9800 m"));
C.push(p("These two values are reused in Tables 3 and 4.", { italics: true, color: "555555" }));

mark("1.2");
C.push(h2("1.2 Map coordinates: degrees-minutes-seconds to decimal degrees"));
C.push(formula("decimal degrees = deg + min/60 + sec/3600"));
const dd = (pp, h) => `${pp[0]} + ${pp[1]}/60 + ${pp[2].toFixed(2)}/3600`;
const sa = d.sites[0], sb = d.sites[1];
C.push(table([2600, 4426, 2000], ["Coordinate", "Working", "Decimal degrees"], [
  ["φ_{A} (Site A latitude)", dd(sa.latp), sa.lat.toFixed(7) + "°"],
  ["λ_{A} (Site A longitude)", dd(sa.lonp), sa.lon.toFixed(7) + "°"],
  ["φ_{B} (Site B latitude)", dd(sb.latp), sb.lat.toFixed(7) + "°"],
  ["λ_{B} (Site B longitude)", dd(sb.lonp), sb.lon.toFixed(7) + "°"],
], { mathCol: 1, align: ["l", "l", "r"] }));

mark("1.3");
C.push(h2("1.3 Distance between sites A and B"));
C.push(p("Over a 7 km path the Earth's ellipsoid is practically flat, so the distance can be found by turning the latitude and longitude differences into metres with the WGS-84 radii of curvature at the mean latitude, then using Pythagoras. This gives the same value as Vincenty's formula used in the project scripts and as the Google Earth ruler."));
C.push(formula("φ_{m} = (φ_{A} + φ_{B}) / 2"));
C.push(formula("M = a(1 − e^{2}) / (1 − e^{2} sin^{2}φ_{m})^{3/2}", "north-south radius of curvature"));
C.push(formula("N = a / √(1 − e^{2} sin^{2}φ_{m})", "east-west radius of curvature"));
C.push(formula("Δy = M · Δφ,   Δx = N · cos φ_{m} · Δλ", "Δφ, Δλ in radians"));
C.push(formula("D = √(Δx^{2} + Δy^{2})"));
const s2 = Math.sin(rad(g.phim)) ** 2;
C.push(caption("Solution"));
C.push(table([2300, 4926, 1800], ["Step", "Working", "Result"], [
  ["φ_{m}", `(${sa.lat.toFixed(7)} + ${sb.lat.toFixed(7)}) / 2`, g.phim.toFixed(7) + "°"],
  ["sin^{2}φ_{m}", `sin^{2}(${g.phim.toFixed(7)}°)`, s2.toFixed(9)],
  ["M", `6378137(1 − ${f6(d.E2)}) / (1 − ${f6(d.E2)} × ${s2.toFixed(6)})^{3/2}`, f2(g.M) + " m"],
  ["N", `6378137 / √(1 − ${f6(d.E2)} × ${s2.toFixed(6)})`, f2(g.N) + " m"],
  ["Δφ", `(${sb.lat.toFixed(7)} − ${sa.lat.toFixed(7)}) × π/180`, g.dphi.toExponential(6) + " rad"],
  ["Δλ", `(${sb.lon.toFixed(7)} − ${sa.lon.toFixed(7)}) × π/180`, g.dlam.toExponential(6) + " rad"],
  ["Δy (north)", `${f2(g.M)} × ${g.dphi.toExponential(6)}`, f4(g.dy) + " m"],
  ["Δx (east)", `${f2(g.N)} × cos(${g.phim.toFixed(4)}°) × (${g.dlam.toExponential(6)})`, f4(g.dx) + " m"],
  ["D", `√[(${f4(g.dx)})^{2} + (${f4(g.dy)})^{2}]`, f4(g.D) + " m"],
  ["D in km", `${f4(g.D)} / 1000`, (g.D / 1000).toFixed(4) + " km"],
], { mathCol: 1, hl: new Set([9]), align: ["l", "l", "r"] }));
C.push(p(`Answer: D = ${(D / 1000).toFixed(4)} km. Note: a spherical haversine with R = 6371 km gives about 6.961 km, about 0.5% too long for this north-south path, so it is not used.`, { before: 80 }));

mark("1.4");
C.push(h2("1.4 Pointing direction for the radiation pattern overlay (Figure 2.2)"));
C.push(p("Each antenna's main lobe is aimed along the path, so the azimuth pattern is rotated to these bearings (measured clockwise from true north)."));
C.push(formula("θ_{AB} = tan^{−1}(Δx / Δy)   (quadrant from the signs of Δx and Δy)"));
C.push(formula("θ_{BA} = θ_{AB} − 180°"));
const ang = Math.atan(g.dx / g.dy) * 180 / Math.PI;
C.push(table([1900, 4626, 2500], ["Step", "Working", "Result"], [
  ["tan^{−1}(Δx/Δy)", `tan^{−1}(${f4(g.dx)} / ${f4(g.dy)}) = tan^{−1}(${(g.dx / g.dy).toFixed(6)})`, f4(ang) + "°"],
  ["θ_{AB} (Site A → B)", `Δx < 0 and Δy > 0 → just west of north: 360° + (${f4(ang)}°)`, f4(g.az) + "° (N " + f4(-ang) + "° W)"],
  ["θ_{BA} (Site B → A)", `${f4(g.az)}° − 180°`, f4(g.az - 180) + "° (S " + f4(-ang) + "° E)"],
], { mathCol: 1, align: ["l", "l", "r"], keep: true }));

mark("1.5");
C.push(h2("1.5 Placing the 20 points on the path (Figure 2.1)"));
C.push(formula("even spacing = D / 19", "20 points make 19 gaps"));
C.push(bullet(`Even spacing = ${f4(D)} / 19 = ${f2(D / 19)} m`));
C.push(bullet("Even position of point k = (k − 1) × D / 19. Each pin was then slid up to 30 m along the line onto the tallest roof nearby, as the guideline asks."));
C.push(bullet("The d_{1} of each pin is found with the same method as section 1.3, from Site A to the pin's own coordinates."));
C.push(caption("d1 of the 18 intermediate points"));
C.push(table([560, 1500, 1580, 1080, 1000, 1110, 1110, 1086],
  ["Pt", "Latitude", "Longitude", "Δy (m)", "Δx (m)", "d_{1} (m)", "Even (m)", "Shift (m)"],
  d.d1rows.map((r) => [String(r.n), R[r.n - 1].lat, R[r.n - 1].lon, f2(r.dy), f2(r.dx), r.used.toFixed(1), f2(r.even), (r.shift >= 0 ? "+" : "") + f2(r.shift)]),
  { align: ["c", "l", "l", "r", "r", "r", "r", "r"] }));
C.push(p("d_{1} = √(Δx^{2} + Δy^{2}) for each point, rounded to 0.1 m and used as d_{1} in km in Table 3 (for example 355.6 m → 0.3556 km). Shift = d_{1} − even position. Point 1 is Site A (d_{1} = 0) and point 20 is Site B (d_{1} = D).", { before: 80 }));

mark("1.6");
C.push(h2("1.6 Table 2 completed"));
C.push(table([2600, 2600, 2600, 1226], ["Item", "Site A", "Site B", "From"], [
  ["Map coordinates", "14°36'32.71\"N 120°59'31.75\"E", "14°40'17.32\"N 120°59'12.63\"E", "Google Earth"],
  ["Height of building", "23 × 2.5 m = 57.5 m", "(5 + 1) × 2.5 m = 15 m", "1.1"],
  ["Ground elevation", "2.47 m", "10.98 m", "Google Earth"],
  ["h_{elevation}", "59.9700 m", "25.9800 m", "1.1"],
  ["Distance between A and B", "6.9270 km", "", "1.3"],
  ["Pointing bearing", f4(g.az) + "° (toward B)", f4(g.az - 180) + "° (toward A)", "1.4"],
], { boldCol: 0 }));

// ---------------- Part 2: Table 3 ----------------
mark("2");
C.push(h1("2. Table 3. Path Profile: Elevation, Earth Bulge, and Fresnel Clearance"));
mark("2.1");
C.push(h2("2.1 Formulas"));
C.push(formula("d_{2} = D − d_{1}", `D = ${f6(DK)} km`));
C.push(formula("h_{elevation} = h_{earth contour} + h_{obstruction} = ground + floors × 2.5"));
C.push(formula("h_{earth bulge} = d_{1}·d_{2} / (12.75k) = d_{1}·d_{2} / 17", "k = 4/3, d in km, answer in m"));
C.push(formula("F_{1} = 17.3 √[ d_{1}·d_{2} / (f·(d_{1} + d_{2})) ]", "f in GHz, d in km, answer in m"));
C.push(formula("THE = h_{elevation} + h_{earth bulge} + 0.6F_{1}"));
C.push(p(`Where 17.3 comes from: F₁ = √(λ·d₁·d₂ / D). With λ = 0.3/f (m, f in GHz) and d in km, F₁ = √(300·d₁·d₂ / (f·D)) = 17.32√(d₁·d₂ / (f·D)). Since d₁ + d₂ = D for every point, the denominator is the same everywhere: f·D = 10.59625 × ${f6(DK)} = ${f6(fD)}.`, { before: 80 }));

mark("2.2");
C.push(h2("2.2 Solution for each of the 20 points"));
C.push(p("At the two sites (P1 and P20) one of d₁ or d₂ is zero, so the earth bulge and the Fresnel zone are both zero and THE equals h_{elevation}."));
function pointTable(r, title) {
  const out = [h3(title)];
  const end = r.d1 === 0 || r.d2 === 0;
  const d1s = r.d1 === DK ? f6(r.d1) : f4(r.d1);
  const rows = [
    ["d_{2}", `D − d_{1} = ${f6(DK)} − ${d1s}`, f4(r.d2) + " km"],
    ["h_{elevation}", `${f2(r.ground)} + ${r.floors}(2.5) = ${f2(r.ground)} + ${f2(r.obst)}`, f4(r.elev) + " m"],
  ];
  if (end) {
    rows.push(["h_{earth bulge}", `(${f4(r.d1)})(${f4(r.d2)}) / [12.75(4/3)] = 0 / 17`, "0.0000 m"]);
    rows.push(["F_{1}", `17.3√[0 / ${f6(fD)}]`, "0.0000 m"]);
    rows.push(["0.6F_{1}", "0.6(0)", "0.0000 m"]);
    rows.push(["THE", `${f4(r.elev)} + 0 + 0`, f4(r.the) + " m"]);
  } else {
    rows.push(["h_{earth bulge}", `(${d1s})(${f6(r.d2)}) / [12.75(4/3)] = ${f6(r.prod)} / 17`, f4(r.bulge) + " m"]);
    rows.push(["F_{1}", `17.3√[${f6(r.prod)} / ${f6(fD)}] = 17.3√${f6(r.arg)} = 17.3(${f6(r.sq)})`, f4(r.f1) + " m"]);
    rows.push(["0.6F_{1}", `0.6(${f6(r.f1)})`, f4(r.f60) + " m"]);
    rows.push(["THE", `${f6(r.elev)} + ${f6(r.bulge)} + ${f6(r.f60)} = ${f6(r.the_hand)}`, f4(r.the) + " m"]);
  }
  out.push(table([1700, 5626, 1700], ["Quantity", "Substitution", "Answer"], rows, { mathCol: 1, hl: new Set([5]), align: ["l", "l", "r"], keep: true }));
  return out;
}
for (const r of R) {
  mark(`P${r.n}`);
  const fl = r.floors === 0 ? "open ground, 0 floors" : `${r.floors} floor${r.floors > 1 ? "s" : ""}`;
  C.push(...pointTable(r, `Point ${r.n}: d_{1} = ${f4(r.d1)} km · ${r.desc} (${fl})`));
}

mark("2.3");
C.push(h2("2.3 Near-line structures (checked in addition to the 20 points)"));
C.push(p("These two structures sit on or beside the line between points, so their THE is computed with the same formulas. Their d₁ is measured from Site A to the structure."));
for (const e of d.extras) { mark(e.name); C.push(...pointTable(e, `${e.name}: ${e.label}, d_{1} = ${f4(e.d1)} km`)); }

mark("2.4");
C.push(h2("2.4 Table 3 completed"));
C.push(table([560, 940, 940, 940, 720, 1300, 1230, 1100, 1296],
  ["Pt", "d_{1} (km)", "d_{2} (km)", "Ground (m)", "Floors", "h_{elevation} (m)", "h_{earth bulge} (m)", "0.6F_{1} (m)", "THE (m)"],
  [...R.map((r) => [String(r.n), f4(r.d1), f4(r.d2), f2(r.ground), String(r.floors), f4(r.elev), f4(r.bulge), f4(r.f60), f4(r.the)]),
   ...d.extras.map((e) => [e.name, f4(e.d1), f4(e.d2), f2(e.ground), String(e.floors), f4(e.elev), f4(e.bulge), f4(e.f60), f4(e.the)])],
  { align: ["c", "r", "r", "r", "c", "r", "r", "r", "r"], hl: new Set([0, 16]), boldCol: 8 }));
C.push(p("Highlighted: P1 has the highest THE (sets the equal-height antenna), and P17 sets the tilted line of sight (Part 3). M = Maranatha/PMCC tower, L = LRT-1 viaduct.", { before: 80, italics: true, color: "555555" }));

// ---------------- Part 3: Table 4 ----------------
const MG = d.margin, mg = f4(MG), hAs = f4(d.hA);
mark("3");
C.push(h1("3. Table 4. Antenna Heights"));
mark("3.1");
C.push(h2("3.1 Safety margin"));
C.push(p(`THE already keeps 0.6F₁ of the Fresnel zone and the earth bulge clear. On top of that, the design keeps an extra m = ${mg} m (one floor) above every THE, because the heights of P17 (4 floors) and the LRT-1 viaduct (12.5 m) are estimates from satellite and street imagery. The design target at every point is therefore THE + ${mg} m, and ${mg} m is added to both antenna heights.`));
C.push(formula(`design target = THE + m,   m = ${mg} m`));

mark("3.2");
C.push(h2("3.2 Equal-height method (for comparison)"));
C.push(formula("h_{antenna} = maximum THE of all 20 points + m"));
C.push(formula("h_{tower} = h_{antenna} − h_{elevation}"));
C.push(bullet(`Maximum THE = ${f4(d.hmin)} m at P${d.gov} (Site A rooftop itself), so h_{antenna} = ${f4(d.hmin)} + ${mg} = ${f4(d.hmin + MG)} m`));
C.push(bullet(`Site A: h_{tower} = ${f4(d.hmin + MG)} − ${f4(d.elevA)} = ${f4(d.hmin + MG - d.elevA)} m`));
C.push(bullet(`Site B: h_{tower} = ${f4(d.hmin + MG)} − ${f4(d.elevB)} = ${f4(d.flatB)} m`));
C.push(p(`A ${f4(d.flatB)} m tower at Site B is large, so the antennas are mounted with a tilt instead (guideline Part 3, item 9).`, { before: 60 }));

mark("3.3");
C.push(h2("3.3 Tilted mounting: finding the lowest Site B antenna height"));
C.push(p(`Site A's antenna sits ${mg} m above the THE of P1: h_{A} = ${f4(d.hmin)} + ${mg} = ${hAs} m. The straight line from h_{A} down to h_{B} must stay at least ${mg} m above THE at every point:`));
C.push(formula("h_{LOS}(d_{1}) = h_{A} − (h_{A} − h_{B})(d_{1} / D) ≥ THE + m"));
C.push(p(`Solving for h_{B} gives the lowest Site B height a point allows. Only the point where the line comes closest to THE limits h_{B}. The path profile (Figure 2.3) shows this is P17: it has a high THE (${f4(d.req.find((q) => q.name === "P17").the)} m) and sits close to Site B, where the tilted line is lowest. So only P17 needs to be worked out:`, { before: 60 }));
C.push(formula("h_{B} = h_{A} − (h_{A} − THE_{P17} − m)(D / d_{1,P17})"));
const top = d.req.find((q) => q.name === "P17");
C.push(bullet(`h_{B} = ${hAs} − (${hAs} − ${f4(top.the)} − ${mg})(${f6(DK)} / ${f4(top.d1)}) = ${hAs} − (${f6(top.diff)})(${f6(top.ratio)}) = ${f4(d.hB)} m`));
C.push(p(`Site B's own roof is ${f4(d.elevB)} m, and ${f4(d.hB)} m is above it, so h_{B} = ${f4(d.hB)} m. Part 4 checks the next-closest structure to confirm that P17 is the one that sets h_{B}.`, { before: 80 }));

mark("3.4");
C.push(h2("3.4 Tower heights"));
C.push(formula("h_{tower} = h_{antenna} − h_{elevation}"));
C.push(bullet(`Site A: h_{tower,A} = ${hAs} − ${f4(d.elevA)} = ${f4(d.towerA)} m (short mast on the Frassati roof)`));
C.push(bullet(`Site B: h_{tower,B} = ${f4(d.hB)} − ${f4(d.elevB)} = ${f4(d.towerB)} m (mast on the Metro Industries roof)`));

mark("3.5");
C.push(h2("3.5 Tilt angle and check"));
C.push(formula("tilt = tan^{−1}[ (h_{A} − h_{B}) / D ]", "D in metres"));
const rat = (d.hA - d.hB) / D;
C.push(bullet(`tilt = tan^{−1}[(${hAs} − ${f4(d.hB)}) / ${f4(D)}] = tan^{−1}(${f6(d.hA - d.hB)} / ${f4(D)}) = tan^{−1}(${rat.toFixed(8)}) = ${f4(d.tilt)}°`));
C.push(bullet(`Downward ${f4(d.tilt)}° at Site A and upward ${f4(d.tilt)}° at Site B. Adding the same ${mg} m to both antennas moves the whole line up without changing its slope, so the tilt is the same as without the margin.`));
C.push(bullet(`Check: ${f4(d.tilt)}° is within the ANDREW VHLP6-11W/A mount's ±5° fine elevation adjustment, and smaller than half the vertical beamwidth (1° / 2 = 0.5° on the spec sheet; 0.92° / 2 = 0.46° simulated).`));

mark("3.6");
C.push(h2("3.6 Table 4 completed"));
C.push(table([3026, 3000, 3000], ["Parameter", "Site A Tower", "Site B Tower"], [
  ["h_{antenna}", hAs + " m", f4(d.hB) + " m (tilted)"],
  ["h_{elevation}", f4(d.elevA) + " m", f4(d.elevB) + " m"],
  ["h_{tower}", f4(d.towerA) + " m", f4(d.towerB) + " m"],
  ["Safety margin above THE", mg + " m", mg + " m"],
  ["Tower with equal heights (not used)", f4(d.hmin + MG - d.elevA) + " m", f4(d.flatB) + " m"],
  ["Tilt angle", f4(d.tilt) + "° down", f4(d.tilt) + "° up"],
], { boldCol: 0, align: ["l", "r", "r"], keep: true }));

// ---------------- Part 4: Table 4.1 ----------------
mark("4");
C.push(h1("4. Clearance Check of the Tilted Line of Sight"));
C.push(p("No full clearance table is needed. The path profile (Figure 2.3) already shows the tilted line above THE everywhere; the only points that come close are P17, which sets h_{B}, and the LRT-1 viaduct. Checking those two is enough to prove the tilted mounting works."));
C.push(formula("s = (h_{A} − h_{B}) / D", "m per km"));
C.push(formula("h_{LOS} = h_{A} − s·d_{1},   Clearance = h_{LOS} − THE  (must be ≥ m)"));
C.push(bullet(`s = (${hAs} − ${f6(d.hB)}) / ${f6(DK)} = ${f6(d.hA - d.hB)} / ${f6(DK)} = ${f6(d.slope)} m/km`));
const ck = ["P17", "L"].map((n) => d.clear.find((c) => c.name === n));
C.push(table([700, 950, 3276, 1300, 1300, 1500],
  ["Pt", "d_{1} (km)", `h_{LOS} = ${hAs} − s·d_{1}`, "h_{LOS} (m)", "THE (m)", "Clearance (m)"],
  ck.map((c) => [c.name, f4(c.d1), `${hAs} − (${f6(d.slope)})(${f4(c.d1)}) = ${hAs} − ${f6(d.slope * c.d1)}`, f4(c.los), f4(c.the), `${f4(c.los)} − ${f4(c.the)} = ${f4(c.margin)}`]),
  { mathCol: 2, align: ["c", "r", "l", "r", "r", "r"], boldCol: 5, keep: true }));
const others = d.clear.filter((c) => !["P1", "P20", "P17", "L"].includes(c.name)).sort((a, b) => a.margin - b.margin);
C.push(p(`Both are at least ${mg} m: P17 has exactly ${mg} m (which is why it sets h_{B}) and the viaduct has ${f4(ck[1].margin)} m. Every other point clears THE by ${f4(others[0].margin)} m or more (${others[0].name} is the next closest), as Figure 2.3 shows.`, { before: 80 }));

mark("end");
const docOptions = (headerText, children) => ({
  creator: "4ECE-B Group 5",
  title: "Section 2 Path Planning Computations",
  styles: {
    default: { document: { run: { font: BODY, size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { font: BODY, size: 40, bold: true, color: "1F3864" }, paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: BODY, size: 30, bold: true, color: "1F3864" }, paragraph: { spacing: { before: 360, after: 140 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: BODY, size: 25, bold: true, color: "2F5597" }, paragraph: { spacing: { before: 240, after: 100 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: BODY, size: 21, bold: true, color: "404040" }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: headerText, size: 17, color: "808080" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ["Page ", PageNumber.CURRENT, " of ", PageNumber.TOTAL_PAGES], size: 17, color: "808080" })] })] }) },
    children,
  }],
});
// named slices of the solution content, so other documents can reuse exactly the same blocks
function block(key) {
  const i = marks.findIndex(([k]) => k === key);
  if (i < 0) throw new Error("no block " + key);
  return C.slice(marks[i][1], marks[i + 1][1]);
}
module.exports = { block, docOptions, d, W, runs, p, h1, h2, h3, bullet, formula, table, cell, caption, BODY, MATH, f4, f6 };
if (require.main === module) {
  const doc = new Document(docOptions("4ECE-B Group 5 · Section 2 Path Planning: Computations", C));
  Packer.toBuffer(doc).then((b) => { fs.writeFileSync(outPath, b); console.log("wrote", outPath, b.length); });
}

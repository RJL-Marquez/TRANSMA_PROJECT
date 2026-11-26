// Task distribution for the handwritten Section 2 solutions: checklist, solutions to copy, and space for scans.
process.env.SEC2_DATA = process.env.SEC2_DATA || process.argv[2];
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, BorderStyle, VerticalAlign, TableLayoutType, CheckBox, HeightRule, PageBreak,
} = require("docx");
const S = require("./build_solutions.js");
const { block, docOptions, d, W, runs, p, h1, h2, h3, bullet, formula, table, BODY, f4 } = S;
const outPath = process.argv[3];

// ------------------------------------------------------------------ the split
// Each task: code, short title, what to write, solution blocks (keys from build_solutions.js)
const PT = (code, n) => [code, `Point ${n}: d2, h_elevation, h_earth bulge, F1, 0.6F1, THE`, "2.2", [`P${n}`]];
const FORMULAS = (code) => [code, "Table 3 formulas (write once at the top of page 1)", "2.1", ["2.1"]];
const MEMBERS = [
  {
    name: "Marquez", role: "Table 2 (site information), then checks and compiles everyone's work",
    load: "6 short computations + final check",
    tasks: [
      ["MQ-1", "Building heights and h_elevation of both sites", "1.1", ["1.1"]],
      ["MQ-2", "Coordinates from degrees-minutes-seconds to decimal degrees", "1.2", ["1.2"]],
      ["MQ-3", "Distance between Sites A and B (D = 6.9270 km)", "1.3", ["1.3"]],
      ["MQ-4", "Pointing bearings for the radiation pattern overlay", "1.4", ["1.4"]],
      ["MQ-5", "Point spacing D/19 and the d1 table (write one full sample, P17: d1 = √(Δx² + Δy²))", "1.5", ["1.5"]],
      ["MQ-6", "Table 2 completed", "1.6", ["1.6"]],
    ],
  },
  {
    name: "Dimalanta", role: "Table 3, points 1 to 10",
    load: "10 points (P1 is a 1-line case)",
    tasks: [FORMULAS("DM-1"), ...[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n, i) => PT(`DM-${i + 2}`, n))],
  },
  {
    name: "Cabatian", role: "Table 3, points 11 to 20",
    load: "10 points (P20 is a 1-line case)",
    tasks: [FORMULAS("CB-1"), ...[11, 12, 13, 14, 15, 16, 17, 18, 19, 20].map((n, i) => PT(`CB-${i + 2}`, n))],
  },
  {
    name: "Rocero", role: "Near-line structures, Table 3 summary, Site B antenna height and the tilt angle",
    load: "2 structures + 1 table copy + about 5 lines",
    tasks: [
      ["RC-1", "Maranatha/PMCC tower (M): same 6 steps as a point", "2.3", ["M"]],
      ["RC-2", "LRT-1 viaduct (L): same 6 steps as a point", "2.3", ["L"]],
      ["RC-3", "Table 3 completed (copy the finished table)", "2.4", ["2.4"]],
      ["RC-4", "Safety margin (2.5 m) explanation", "3.1", ["3.1"]],
      ["RC-5", `Equal-height method (${f4(d.flatB)} m tower, for comparison)`, "3.2", ["3.2"]],
      ["RC-6", `Site B antenna height from P17 only: h_B = ${f4(d.hB)} m`, "3.3", ["3.3"]],
      ["RC-7", `Tilt angle (${f4(d.tilt)}°) and the mount/beamwidth check`, "3.5", ["3.5"]],
    ],
  },
  {
    name: "Manuel", role: "Tower heights, Table 4, and the clearance check (proof)",
    load: "towers + Table 4 + 2-row clearance check",
    tasks: [
      ["MN-1", `Tower heights (${f4(d.towerA)} m and ${f4(d.towerB)} m)`, "3.4", ["3.4"]],
      ["MN-2", "Table 4 completed", "3.6", ["3.6"]],
      ["MN-3", "Clearance check at P17 and the LRT-1 viaduct (2 rows, the proof for the tilt)", "4", ["4"]],
    ],
  },
];
const SCAN_BOXES = { Marquez: 2, Dimalanta: 3, Cabatian: 3, Rocero: 2, Manuel: 1 };

// ------------------------------------------------------------------ helpers
const thin = { style: BorderStyle.SINGLE, size: 4, color: "A6A6A6" };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
const box = () => new CheckBox({ checked: false, checkedState: { value: "2611", font: "MS Gothic" }, uncheckedState: { value: "2610", font: "MS Gothic" } });
function tcell(children, width, o = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders, verticalAlign: o.valign || VerticalAlign.CENTER, columnSpan: o.span,
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: Array.isArray(children) ? children : [children],
  });
}
const para = (s, o = {}) => new Paragraph({ alignment: o.align, keepNext: o.keepNext, children: runs(s, { size: o.size || 19, bold: o.bold, color: o.color, italics: o.italics }) });
const boxPara = () => new Paragraph({ alignment: AlignmentType.CENTER, children: [box()] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });
const sub = (s) => s.replace(/h_(\w+)/g, "h_{$1}").replace(/\bd([12])\b/g, "d_{$1}").replace(/F1\b/g, "F_{1}");
const FILL = { head: "D9E2F3", member: "E2EFDA" };

// ------------------------------------------------------------------ document
const C = [];
C.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Section 2 Handwritten Solutions: Task Distribution")] }));
C.push(p("ECE21129 Microwave Link Design · 4ECE-B Group 5 · UST Frassati Building (Site A) to Metro Industries, Valenzuela (Site B)", { color: "404040" }));
C.push(p("The report asks for screenshots of handwritten computations under Section 2 (Path Profile and Antenna Towers). This file splits that writing among the five members. Part 1 is the checklist, Part 2 has the exact solutions each member copies by hand, and Part 3 is where each member pastes the photos or scans of their pages. The project is due November 27, 2026.", { after: 160 }));

// ---------- Part 1: checklist
C.push(h1("Part 1. Checklist"));
C.push(h2("Who does what"));
C.push(table([1500, 4226, 3300], ["Member", "Covers", "Load"], MEMBERS.map((m) => [m.name, m.role, m.load]), { boldCol: 0 }));
C.push(h2("How to write the solutions"));
for (const s of [
  "Write in this order for every quantity: the formula, then the numbers substituted in, then the answer. Box or underline the final answer.",
  "Final answers to 4 decimal places in metric units (m, km), the same as the report. Copy the 6-decimal working in Part 2 so the sums come out right.",
  "At the top of every sheet write your name, your task codes (for example DM-3 to DM-6), and a page number.",
  "Use clean bond paper and dark ink. Take the photo straight on in good light, or scan it, so the numbers are readable.",
  "Tick a box in this checklist when that part is written and checked. Tick \"Scanned\" once its photo is pasted in Part 3.",
]) C.push(bullet(s));

const CW = [950, 1000, 4776, 1000, 1300];
const head = new TableRow({ tableHeader: true, children: ["Written", "Code", "What to write", "Ref.", "Scanned"].map((h, i) => tcell(para(h, { bold: true, align: i === 2 ? AlignmentType.LEFT : AlignmentType.CENTER }), CW[i], { fill: FILL.head })) });
const rows = [head];
for (const m of MEMBERS) {
  rows.push(new TableRow({ cantSplit: true, children: [tcell(para(`${m.name}: ${m.role}`, { bold: true, keepNext: true }), W, { fill: FILL.member, span: 5 })] }));
  m.tasks.forEach(([code, what, ref]) => rows.push(new TableRow({
    cantSplit: true,
    children: [tcell(boxPara(), CW[0]), tcell(para(code, { align: AlignmentType.CENTER, bold: true }), CW[1]), tcell(para(sub(what)), CW[2]),
      tcell(para(ref, { align: AlignmentType.CENTER }), CW[3]), tcell(boxPara(), CW[4])],
  })));
}
C.push(new Paragraph({ children: [], spacing: { after: 60 } }));
C.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: CW, layout: TableLayoutType.FIXED, rows }));
C.push(p("Ref. is the section number in Part 2 below (and in 4ECEB_Group5_Section2_Computations.docx).", { italics: true, color: "555555", before: 60 }));

C.push(h2("Group steps after the writing"));
const GW = [700, 6326, 2000];
const steps = [
  ["Every member's pages are photographed or scanned and pasted in Part 3", "Everyone"],
  ["Every boxed answer matches Tables 2, 3 and 4 and the clearance check in the report", "Marquez"],
  ["Pictures inserted in the report under \"Include and explain the screenshots of handwritten computations\" (Path Profile and Antenna Towers)", "Marquez"],
  ["A one-line explanation written under each picture, and the red reminder text deleted", "Marquez"],
];
C.push(new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: GW, layout: TableLayoutType.FIXED,
  rows: [new TableRow({ children: ["Done", "Step", "Who"].map((h, i) => tcell(para(h, { bold: true, align: i === 1 ? AlignmentType.LEFT : AlignmentType.CENTER }), GW[i], { fill: FILL.head })) }),
    ...steps.map(([s, who]) => new TableRow({ cantSplit: true, children: [tcell(boxPara(), GW[0]), tcell(para(s), GW[1]), tcell(para(who, { align: AlignmentType.CENTER }), GW[2])] }))],
}));

// ---------- Part 2: solutions to copy
C.push(pageBreak());
C.push(h1("Part 2. Solutions to Copy"));
C.push(p("Each member's section starts on a new page and has everything needed for their task codes: the formulas, the substitution, and the answer. The numbers are the same as in the report; do not round in the middle of a step."));
C.push(...block("formulas"));
const shared = new Set();
for (const m of MEMBERS) {
  C.push(pageBreak());
  C.push(h1(`${m.name}: ${m.role}`));
  C.push(p(`Task codes ${m.tasks[0][0]} to ${m.tasks[m.tasks.length - 1][0]}. Load: ${m.load}.`, { color: "555555", italics: true }));
  for (const [code, what, , keys] of m.tasks) {
    C.push(new Paragraph({
      keepNext: true, spacing: { before: 200, after: 60 },
      shading: { type: ShadingType.CLEAR, fill: "FFF2CC", color: "auto" },
      children: [new TextRun({ text: `${code}  `, bold: true, font: BODY, size: 21, color: "7F6000" }), ...runs(sub(what), { size: 21, bold: true })],
    }));
    for (const k of keys) {
      // a block can only be placed once in a document; rebuild duplicates (the 2.1 formulas) from scratch
      if (shared.has(k)) {
        C.push(...block2_1());
      } else {
        shared.add(k);
        C.push(...block(k));
      }
    }
  }
}
function block2_1() {
  const DK = d.DK, fD = d.F * DK;
  return [
    h2("2.1 Formulas"),
    formula("d_{2} = D − d_{1}", `D = ${DK.toFixed(6)} km`),
    formula("h_{elevation} = h_{earth contour} + h_{obstruction} = ground + floors × 2.5"),
    formula("h_{earth bulge} = d_{1}·d_{2} / (12.75k) = d_{1}·d_{2} / 17", "k = 4/3, d in km, answer in m"),
    formula("F_{1} = 17.3 √[ d_{1}·d_{2} / (f·(d_{1} + d_{2})) ]", "f in GHz, d in km, answer in m"),
    formula("THE = h_{elevation} + h_{earth bulge} + 0.6F_{1}"),
    p(`Since d₁ + d₂ = D for every point, the denominator is the same everywhere: f·D = 10.59625 × ${DK.toFixed(6)} = ${fD.toFixed(6)}.`, { before: 80 }),
  ];
}

// ---------- Part 3: space for scans
C.push(pageBreak());
C.push(h1("Part 3. Scanned Handwritten Solutions"));
C.push(p("Paste each page as a picture inside a box (Insert > Pictures, then set the picture to fit the box width). Each box grows to fit its picture. If you need more boxes, copy a row and paste it below."));
MEMBERS.forEach((m, mi) => {
  const codes = `${m.tasks[0][0]} to ${m.tasks[m.tasks.length - 1][0]}`;
  const n = SCAN_BOXES[m.name];
  if (mi > 0) C.push(pageBreak());
  C.push(h2(`${m.name}: ${codes}`));
  C.push(new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W], layout: TableLayoutType.FIXED,
    rows: Array.from({ length: n }, (_, i) => new TableRow({
      height: { value: i === 0 ? (mi === 0 ? 10400 : 11800) : 12800, rule: HeightRule.ATLEAST },
      children: [new TableCell({
        width: { size: W, type: WidthType.DXA }, verticalAlign: VerticalAlign.TOP,
        borders: { top: { style: BorderStyle.DASHED, size: 6, color: "8EA9DB" }, bottom: { style: BorderStyle.DASHED, size: 6, color: "8EA9DB" }, left: { style: BorderStyle.DASHED, size: 6, color: "8EA9DB" }, right: { style: BorderStyle.DASHED, size: 6, color: "8EA9DB" } },
        margins: { top: 80, bottom: 80, left: 100, right: 100 },
        children: [
          new Paragraph({ children: runs(`${m.name} · page ${i + 1} of ${n}`, { size: 18, bold: true, color: "2F5597" }) }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 2400 }, children: runs("Paste the photo or scan here", { size: 20, color: "A6A6A6", italics: true }) }),
        ],
      })],
    })),
  }));
});

const doc = new Document(docOptions("4ECE-B Group 5 · Section 2 Handwritten Solutions: Task Distribution", C));
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(outPath, b); console.log("wrote", outPath, b.length); });

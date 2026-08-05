#!/usr/bin/env node
/**
 * Tilstandsscanning af fiskeriprojektets dashboard.
 * Rapporterer drift mellem projektet på disken og DATA i arbejdsgrundlag.html.
 *
 *   node scan.mjs [projektrod]
 *
 * Rapport, ikke gate — exit er altid 0 medmindre filerne slet ikke findes.
 */
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import { execSync } from "node:child_process";

const ROOT = process.argv[2] ||
  "/Users/kasperlandsvig/Documents/Claude Cowork/Kasper Private/Fiskeri Styrelsen";
const HTML = join(ROOT, "arbejdsgrundlag.html");
const LEGAL = join(ROOT, "Legal docs");

if (!existsSync(HTML)) {
  console.error(`FEJL: fandt ikke ${HTML}`);
  console.error("Er projektroden flyttet? Angiv den som argument.");
  process.exit(1);
}

const sh = (cmd) => { try { return execSync(cmd, { cwd: ROOT, encoding: "utf8", stdio: ["pipe", "pipe", "pipe"] }).trim(); } catch { return ""; } };
const H = (t) => console.log("\n" + t + "\n" + "-".repeat(t.length));
const bullet = (s) => console.log("  " + s);

/* ---------- Udtræk DATA. Linjeforankret: strengen 'const DATA = {' findes også
   som brødtekst i vedligeholdelsespanelet. ---------- */
const lines = readFileSync(HTML, "utf8").split("\n");
const s = lines.findIndex((l) => l.trimEnd() === "const DATA = {");
let e = -1;
for (let i = s + 1; i < lines.length; i++) if (lines[i] === "};") { e = i; break; }
if (s === -1 || e === -1) { console.error("FEJL: kunne ikke afgrænse DATA-blokken"); process.exit(1); }

let DATA;
try { DATA = Function(lines.slice(s, e + 1).join("\n") + "\nreturn DATA;")(); }
catch (err) { console.error("FEJL: DATA kunne ikke parses —", err.message); process.exit(1); }

const antalSp = (DATA.questions || []).reduce((a, g) => a + (g.items?.length || 0), 0);
const huller = (DATA.chain || []).filter((c) => !c.gf || !c.dk);

console.log("=".repeat(64));
console.log("TILSTANDSSCANNING — fiskeriprojektets dashboard");
console.log("=".repeat(64));

H("Dashboardets indhold");
bullet(`DATA-blok: linje ${s + 1}–${e + 1} (${e - s + 1} linjer)`);
bullet(`chain ${DATA.chain?.length}  ·  terms ${DATA.terms?.length} (legal ${DATA.terms?.filter((t) => t.t === "legal").length}, jargon ${DATA.terms?.filter((t) => t.t === "jargon").length})`);
bullet(`conflicts ${DATA.conflicts?.length}  ·  deadlines ${DATA.deadlines?.length}  ·  corpus ${DATA.corpus?.length}`);
bullet(`spørgsmål ${antalSp}  ·  corrections ${DATA.corrections?.length}  ·  gaps ${DATA.gaps?.length}`);
bullet(`huller i kæden: ${huller.length}/${DATA.chain?.length}`);
bullet(`ansættelsesvindue: ${DATA.window?.from} → ${DATA.window?.to}`);

/* ---------- Validering ---------- */
H("Validering");
const vPath = join(ROOT, "scripts", "validate.mjs");
if (existsSync(vPath)) {
  const out = sh(`node "${vPath}" 2>&1`);
  const sidste = out.split("\n").filter(Boolean).slice(-1)[0] || "(intet output)";
  bullet(sidste);
  const fejl = out.split("\n").filter((l) => l.includes("FEJL:"));
  if (fejl.length) fejl.slice(0, 8).forEach((l) => bullet(l.trim()));
} else {
  bullet("scripts/validate.mjs findes ikke — kør den ikke, men nævn det");
}

/* ---------- Drift: filer på disken vs. DATA.corpus ---------- */
H("Drift mellem Legal docs/ og DATA.corpus");
const kendte = new Set((DATA.corpus || []).map((d) => d.path).filter(Boolean));
const paaDisken = [];
const walk = (dir) => {
  if (!existsSync(dir)) return;
  for (const n of readdirSync(dir)) {
    if (n.startsWith(".")) continue;
    const p = join(dir, n);
    if (statSync(p).isDirectory()) walk(p);
    else paaDisken.push(relative(LEGAL, p));
  }
};
["eu", "dk", "vejledninger"].forEach((d) => walk(join(LEGAL, d)));

const nye = paaDisken.filter((p) => !kendte.has(p));
const forsvundne = [...kendte].filter((p) => p && !p.startsWith("—") && !existsSync(join(LEGAL, p)));

if (!nye.length && !forsvundne.length) bullet("ingen drift — alle kildedokumenter er registreret");
if (nye.length) {
  bullet(`${nye.length} fil(er) på disken UDEN post i DATA.corpus:`);
  nye.slice(0, 15).forEach((p) => bullet("    + " + p));
  if (nye.length > 15) bullet(`    … og ${nye.length - 15} mere`);
}
if (forsvundne.length) {
  bullet(`${forsvundne.length} post(er) i DATA.corpus UDEN fil på disken:`);
  forsvundne.forEach((p) => bullet("    − " + p));
}

/* ---------- Bilag: er de koblet på? ---------- */
H("Bilagsudtrækket");
const felt = join(LEGAL, "bilag", "feltkatalog.csv");
if (!existsSync(felt)) {
  bullet("Legal docs/bilag/ findes ikke — bilagsudtrækket er ikke kørt");
} else {
  const rk = readFileSync(felt, "utf8").split("\n").filter((l) => l.trim()).length - 1;
  const kode = existsSync(join(LEGAL, "bilag", "kodelister"))
    ? readdirSync(join(LEGAL, "bilag", "kodelister")).filter((f) => f.endsWith(".csv")).length : 0;
  bullet(`feltkatalog.csv: ${rk} rækker  ·  kodelister: ${kode} filer`);
  // Reel kobling = en chain-post peger på et bilag i sin hjemmel eller gennemførelse.
  // Løs omtale i prosa tæller ikke, derfor to separate tal.
  const koblet = (DATA.chain || []).filter((c) => /bilag/i.test(`${c.eu} ${c.gf || ""}`)).length;
  const omtalt = (JSON.stringify(DATA).match(/bilag/gi) || []).length;
  bullet(`chain-poster der henviser til et bilag: ${koblet}/${DATA.chain?.length}`);
  bullet(`ordet "bilag" i DATA i alt: ${omtalt} forekomst(er) (prosa medregnet)`);
  if (!koblet) bullet("→ feltkataloget er endnu ikke koblet på sporbarhedskæden");
}

/* ---------- Ordliste: CSV vs DATA.terms ---------- */
H("Ordliste");
const csv = join(LEGAL, "ordliste", "ordliste.csv");
if (existsSync(csv)) {
  const rk = readFileSync(csv, "utf8").split("\n").filter((l) => l.trim()).length - 1;
  const d = rk - (DATA.terms?.length || 0);
  bullet(`ordliste.csv ${rk} rækker vs DATA.terms ${DATA.terms?.length}` +
    (d === 0 ? "  → i sync" : `  → AFVIGER med ${d > 0 ? "+" : ""}${d}`));
} else bullet("ordliste.csv findes ikke");

/* ---------- PROJEKT.md ---------- */
H("PROJEKT.md (manager-agentens tilstand — læs, rediger ikke)");
const pj = join(ROOT, "PROJEKT.md");
if (existsSync(pj)) {
  const txt = readFileSync(pj, "utf8");
  const sek = (navn) => {
    const m = txt.match(new RegExp(`##\\s*\\d*\\.?\\s*${navn}([\\s\\S]*?)(?=\\n##\\s|$)`, "i"));
    return m ? m[1].trim() : "";
  };
  const ver = sek("Verificeret");
  const tom = /^\*?[^*]*Endnu intet bekræftet|^\*.*\*$/i.test(ver) || ver.length < 40;
  bullet(`Verificeret: ${tom ? "stadig tomt — intet bekræftet indefra endnu" : "HAR INDHOLD → afklaringer kan være besvaret, tjek DATA.questions"}`);
  const naeste = sek("Næste skridt").split("\n").filter((l) => /^\s*\d\./.test(l));
  if (naeste.length) { bullet("Næste skridt ifølge manager-agenten:"); naeste.forEach((l) => bullet("    " + l.trim())); }
} else bullet("PROJEKT.md findes ikke");

/* ---------- Git ---------- */
H("Git");
if (!sh("git rev-parse --is-inside-work-tree")) {
  bullet("ikke et git-repo — ingen fortrydelsesmulighed, overvej git init");
} else {
  const dirty = sh("git status --porcelain");
  bullet(dirty ? `${dirty.split("\n").length} uncommittede ændring(er):` : "arbejdstræet er rent");
  if (dirty) dirty.split("\n").slice(0, 12).forEach((l) => bullet("    " + l));
  const sidsteDash = sh('git log -1 --format="%h %ad %s" --date=short -- arbejdsgrundlag.html');
  bullet(`sidste commit på dashboardet: ${sidsteDash || "(ingen)"}`);
  const siden = sh('git log --oneline "$(git log -1 --format=%H -- arbejdsgrundlag.html)"..HEAD 2>/dev/null');
  if (siden) { bullet(`commits siden da (${siden.split("\n").length}):`); siden.split("\n").slice(0, 10).forEach((l) => bullet("    " + l)); }
}

console.log("\n" + "=".repeat(64));
console.log("Scanning færdig. Læs AGENTS.md i projektroden før du redigerer DATA.");
console.log("=".repeat(64));

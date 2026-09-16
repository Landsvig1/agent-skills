---
name: html-interactive-decisions
description: Generer eller rediger selvstændige, interaktive single-file HTML/CSS/JS fagsystem-artefakter, beslutningsoplæg, lovkonflikt-inspektorer og krydskontrol-workbenches til Fiskeristyrelsen under Miljøministeriet. ALTID KUN PÅ DANSK. Autentisk dansk embeds-DNA med officiel Miljøministeriet-palette (#0E472F skovgrøn, #14643C handlingsgrøn, #F0F4F1 lys salvie), Raleway/Inter typografi, EU-Kontrolforordning (1224/2009, 2023/2842, 2025/2196), FOS/VMS-sporing og e-logbog. 100% offline, zero-Node.js, corporate-safe og udstyret med dansk udklipsholder-eksport til fagsystemer og journalisering. Brug altid denne skill når brugeren nævner "/html-interactive-decisions", "html-interactive-decisions", eller beder om fagsystem-beslutningsflader for Fiskeristyrelsen eller Miljøministeriet.
---

# HTML Interactive Decisions (Fiskeristyrelsen & Miljøministeriet Standard)

En specialiseret fagsystem-skill til at skabe rolige, autoritative og interaktive single-file HTML/CSS/JS fagsystem-artefakter, tilsynsværktøjer, lovkonflikt-inspektorer og krydskontrol-workbenches til **Fiskeristyrelsen under Miljøministeriet**.

Udviklet specifikt til restriktive arbejdscomputere uden Node.js, offline anvendelse og sikker journalisering i statslige fagsystemer.

---

## 0. Ufravigeligt Sprogkrav: ALTID KUN DANSK (ALWAYS DANISH ONLY)

**Enhver artefakt genereret for Fiskeristyrelsen SKAL være 100% på dansk:**
* **Dokumentsprog**: `<html lang="da-DK">` er obligatorisk.
* **UI-elementer & Knapper**: Alle knapper, faneblade, labels, badges, tooltips og hjælpetekster skal være på formelt dansk embedsmandssprog.
  - Skriv **"Kopier Afgørelse til Udklipsholder"** (ALDRIG "Copy to clipboard").
  - Skriv **"✓ Kopieret til Udklipsholder"** (ALDRIG "Copied").
  - Skriv **"Alle Sager" / "Oversigt"** (ALDRIG "All" / "Overview").
  - Skriv **"Sagsnotat & Bemærkninger"** (ALDRIG "Notes" / "Comments").
* **Ingen engelske placeholders**: Undgå standard AI-engelsk i mock-data, sagsnumre og fritekstfelter.
* **Fagtermer**: Brug styrelsens korrekte danske termer: *Tilsynsnotat*, *Kontrolsag*, *Bødeforelæg*, *Partshøring*, *Fartøjsovervågning (FOS)*, *E-logbog*, *Margentolerance*, *Landingsdeklaration*, *Vejekontrol*, *Kystlog*.

---

## 1. Retskilder & Domænekontekst

Artefakter bygger på det faktiske EU- og nationale retsgrundlag:
* **(EU) 1224/2009**: Kontrolforordningen (Grundlæggende kontrolprincipper, logbogspligt art. 14, FOS/VMS art. 9, vejekrav art. 60).
* **(EU) 2023/2842**: Den nye ændringsforordning (Trinvis implementering 2026/2027/2028, REM/CCTV, udvidet e-sporing for små fartøjer).
* **(EU) 2025/2196**: Gennemførelsesforordning for datavalidering & krydskontrol (Art. 49–53: Automatiseret krydstjek mellem e-log, FOS-spor og salgsnotaer).
* **Nationale Bekendtgørelser (fx BEK 1421)**: Særregler, kystfiskerordninger (Kystlog for fartøjer < 12m), biologiske fredningsbælter og redskabsrestriktioner.
* **10% Margentolerance**: Grænsen for skippers skønnede vægt mod faktisk vejet landing jf. art. 14, stk. 3.

---

## 2. Miljøministeriets Visuelle DNA (Design Tokens)

Ingen AI-slop, ingen neon-elementer og ingen tunge portaler. Rolig, præcis institutionel autoritet:

```css
:root {
  --bg: #f8faf8;                  /* Lys nordisk tåge med let organisk skær */
  --surface: #ffffff;             /* Rent hvidt karton/panel */
  --surface-subtle: #f0f4f1;      /* Dæmpet salvie (mim.dk --color-light--3) */
  --border: #e1e7e2;              /* Diskret mineralgrænse */
  --border-strong: #cbd6cd;       /* Aktiv / hover-kant */
  --border-focus: #0e472f;        /* Miljøministeriets dybe skovgrønne */
  
  --text: #19211c;                /* Dyb koksgrå */
  --text-muted: #4e5e54;          /* Skifergrå til hjælpetekst */
  --text-dim: #718177;            /* Dæmpet grå til metadata */
  
  /* Officielle Miljøministeriet brand-farver */
  --mim-green: #0e472f;           /* Dyb ministeriel skovgrøn */
  --mim-action: #14643c;          /* Primær knap og aktiv markering */
  --mim-action-hover: #0b3d28;
  --mim-tint: #e6eee4;            /* Badge- og fremhævningsbaggrund */
  --mim-border-tint: #c5d7c3;
  --ink-inverted: #ffffff;
  
  /* Tilsynsstatus */
  --crit: #b91c1c; --crit-tint: #fee2e2;
  --warn: #b45309; --warn-tint: #fef3c7;
  --ok: #15803d;   --ok-tint: #dcfce7;

  /* Typografi: mim.dk officiel parring */
  --font-display: 'Raleway', 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
  
  --radius-sm: 4px;
  --radius: 8px;
}
```

---

## 3. Fem ufravigelige regler for artefakter

1. **ALTID DANSK (da-DK)**: 100% rent dansk sprog i alle titler, knapper, notater og udklipsholder-eksport.
2. **Single-file & Zero-Node**: 100% selvkørende i én `.html`-fil. CSS i `<style>`, JS i `<script>`, ikoner som inlinet `<svg>`. Ingen eksterne afhængigheder eller build-tools.
3. **Ingen Tailwind CDN**: `cdn.tailwindcss.com` er strengt forbudt. Brug ren, vedligeholdelsesfri CSS med CSS-variabler.
4. **Mandatory Round-Trip Export**: Enhver artefakt med interaktive felter (radioknapper, sagsbehandler-notat, tolerance-skydere) skal indeholde en fastbundet handlingslinje med en dansk "Kopier Afgørelse som Markdown"-knap (`navigator.clipboard.writeText(...)`), så konklusionen let overføres til fagsystem eller tilsynsnotat.
5. **Præcis Retskildereference**: Ingen fiktive regler. Henvis altid til eksakte artikler i (EU) 1224/2009, 2023/2842, 2025/2196 eller specifikke bekendtgørelser.

---

## 4. Standard Dansk Embeds-Boilerplate

```html
<!DOCTYPE html>
<html lang="da-DK" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Miljøministeriet · Fiskeristyrelsen — [Dansk Titel]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* Indsæt design tokens herover */
  </style>
</head>
<body>
  <nav class="masthead">
    <div style="font-weight: 700; color: var(--mim-green); text-transform: uppercase; font-size: 0.85rem;">
      Miljøministeriet · Fiskeristyrelsen
    </div>
    <div style="font-size: 0.82rem; color: var(--text-dim);">Fagsystem · Offline Dokument</div>
  </nav>

  <header style="margin-bottom: 2.5rem;">
    <h1 style="font-family: var(--font-display); font-size: 2.2rem; margin-bottom: 0.5rem;">[Dansk Titel]</h1>
    <p style="color: var(--text-muted); max-width: 68ch;">[Faglig indledning på formelt dansk]</p>
  </header>

  <main>
    <!-- Interaktivt tilsynsindhold på dansk -->
  </main>

  <aside class="export-dock">
    <span id="dock-status">Klar til journalisering</span>
    <button id="btn-export" class="btn-action">Kopier Tilsynsnotat til Udklipsholder</button>
  </aside>

  <script>
    document.getElementById('btn-export').addEventListener('click', async (e) => {
      const payload = `### Fiskeristyrelsen Tilsynsnotat (${new Date().toISOString().slice(0, 10)})\n\n[Dansk sagsafgørelse]`;
      await navigator.clipboard.writeText(payload);
      const btn = e.currentTarget;
      btn.textContent = '✓ Kopieret til Udklipsholder';
      setTimeout(() => btn.textContent = 'Kopier Tilsynsnotat til Udklipsholder', 2000);
    });
  </script>
</body>
</html>
```

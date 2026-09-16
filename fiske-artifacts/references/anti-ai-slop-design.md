# Reference: Nordic Institutional Restraint (Miljøministeriet / Fiskeristyrelsen Standard)

A refined aesthetic specifically calibrated for Danish public sector agencies, ministries, and regulatory authorities (specifically **Fiskeristyrelsen under Miljøministeriet**). 

It tilts the Scandinavian minimalist baseline toward the quiet, authoritative visual language of Danish state institutions (`mim.dk`): signature deep forest green, soft mineral mist, Raleway/Inter typography, and functional legibility.

---

## 1. Core Visual DNA & Design Tokens

### The Miljøministeriet Palette (Subtly Tilted Baseline)
```css
:root {
  --bg: #f8faf8;                  /* Crisp Nordic mist with subtle organic warmth */
  --surface: #ffffff;             /* Clean paper canvas */
  --surface-subtle: #f0f4f1;      /* Soft sage tint (mim.dk --color-light--3) */
  --border: #e1e7e2;              /* Muted mineral border */
  --border-strong: #cbd6cd;       /* Active / hover border */
  --border-focus: #0e472f;        /* Deep Miljøministeriet green focus */
  
  --text: #19211c;                /* Deep charcoal with slight pine warmth */
  --text-muted: #4e5e54;          /* Weathered slate for descriptions */
  --text-dim: #718177;            /* Soft sage-gray for metadata */
  
  /* Signature Miljøministeriet Brand Tokens */
  --mim-green: #0e472f;           /* Signature deep ministry forest green */
  --mim-action: #14643c;          /* Primary interactive button & active state */
  --mim-action-hover: #0b3d28;
  --mim-tint: #e6eee4;            /* Soft badge background */
  --mim-border-tint: #c5d7c3;
  --ink-inverted: #ffffff;

  /* Typography: Official mim.dk pairing */
  --font-display: 'Raleway', 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
  
  --radius-sm: 4px;
  --radius: 8px;
}

[data-theme="dark"] {
  --bg: #0d1712;                  /* Deep Nordic spruce */
  --surface: #13221b;             /* Dark slate well */
  --surface-subtle: #192c23;      /* Secondary surface */
  --border: #1f372c;              /* Whisper pine border */
  --border-strong: #2c4d3e;
  --border-focus: #82ba79;
  
  --text: #f2f7f4;
  --text-muted: #9bb1a4;
  --text-dim: #6d8577;
  
  --mim-green: #82ba79;
  --mim-action: #82ba79;
  --mim-action-hover: #a3d49b;
  --mim-tint: #1c3328;
  --mim-border-tint: #2a4c3c;
  --ink-inverted: #0d1712;
}
```

---

## 2. Institutional Balance & Craft Rules

1. **Subtle Tilt, Not a Government Portal Clone**:
   - Do **not** build heavy legacy portals with bloated multi-level megamenus.
   - Keep the artifact fast, responsive, single-file, and focused on decision-making.
   - Tilt subtly via the **color anchor** (deep forest green `#0E472F` instead of tech-blue) and **typography** (Raleway headings with clean Inter body).
2. **Authority Through Typographic Restraint**:
   - Use `font-family: var(--font-display)` for page headers, card titles, and modal headers.
   - Keep body text in `var(--font-sans)` with line-heights of 1.6 to ensure dense statutory text or regulatory notes are effortless to read.
3. **Institutional Badging**:
   - Badges use soft sage fills with subtle green borders:
     `background: var(--mim-tint); color: var(--mim-green); border: 1px solid var(--mim-border-tint);`
   - Useful for regulatory tags: `EU Forordning 1224/2009`, `National Bekendtgørelse`, `Miljøministeriet · Fiskeristyrelsen`.
4. **Docked Export Action**:
   - The pinned export tray uses solid Miljøministeriet green (`var(--mim-action)`) for the primary button, giving it dignified official weight.

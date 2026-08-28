# Reference: Danish Institutional Design Standard (Miljøministeriet & Miljøstyrelsen)

A refined visual specification calibrated for high-stakes executive, regulatory, and institutional presentations. It combines Scandinavian minimalism with the authoritative brand identity of **Miljøministeriet (`mim.dk`)** and **Miljøstyrelsen (`mst.dk/erhverv`)**.

---

## 1. Official Color Palette Tokens

```css
:root {
  /* Canvas & Foundations */
  --bg: #f8faf8;                  /* Warm Nordic mist / clean paper */
  --surface: #ffffff;             /* Crisp presentation card */
  --surface-subtle: #f0f4f1;      /* Soft sage tint (mim.dk --color-light--3) */
  --border: #e1e7e2;              /* Muted hairline border */
  --border-strong: #cbd6cd;       /* Active border */
  --border-focus: #0e472f;        /* Deep Miljøministeriet green */
  
  /* Ink & Typography */
  --text: #19211c;                /* Deep charcoal */
  --text-muted: #4e5e54;          /* Weathered slate for supporting copy */
  --text-dim: #718177;            /* Muted sage-gray for metadata */
  
  /* Ministry Brand Colors */
  --mim-green: #0e472f;           /* Signature Miljøministeriet deep forest green */
  --mim-action: #14643c;          /* Primary action button & active element */
  --mim-action-hover: #0b3d28;
  --mim-tint: #e6eee4;            /* Badge fill & soft pill accent */
  --mim-border-tint: #c5d7c3;
  --ink-inverted: #ffffff;
  
  /* Status Indicators */
  --crit: #b91c1c; --crit-tint: #fee2e2;
  --warn: #b45309; --warn-tint: #fef3c7;
  --ok: #15803d;   --ok-tint: #dcfce7;

  /* Typography: Official Danish Ministry Pairing */
  --font-display: 'Raleway', 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
}

[data-theme="dark"] {
  --bg: #0d1712;                  /* Deep Nordic spruce */
  --surface: #13221b;             /* Dark panel */
  --surface-subtle: #192c23;      /* Secondary surface */
  --border: #1f372c;
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

## 2. Anti-AI-Slop Craft Floor (Strict Bans)

1. **NO Monospace as Presentation Headings:**
   Monospace is exclusively for data citations, timestamps, and numbers. Headings must use `var(--font-display)` (`Raleway`).
2. **NO Eyebrows / Kickers with Pulsing Dots:**
   Avoid artificial uppercase kicker labels above slide titles. Let slide headlines state the conclusion directly.
3. **NO Neon Glowing Outlines or Cyberpunk Gradients:**
   Selections are indicated with a crisp hairline border or tactile 2px top rule.
4. **Line-Length Discipline on Slides:**
   Slide copy must never sprawl across the full width of wide 16:9 displays. Cap prose blocks at `max-width: 65ch` to preserve scannability from the back of the conference room.
5. **Mandatory Clipboard Export Action:**
   Any slide that accepts interactive inputs must provide an export button so changes made during executive discussion can be copied to clipboard as Markdown.

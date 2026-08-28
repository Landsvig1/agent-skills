# Reference: Scandinavian Minimalist Enterprise Design System

A refined aesthetic specifically calibrated for senior engineering, architecture, and corporate decision surfaces. It eliminates common "AI-slop" design tropes (dark terminal neon, glowing cyan borders, gratuitous gradients, and monospace headings) in favor of the quiet, tactile dignity of physical paper and refined print.

---

## 1. Core Visual DNA & Design Tokens

### The Warm Paper & Charcoal Baseline
```css
:root {
  --bg: #faf9f6;                  /* Warm bone paper canvas */
  --surface: #ffffff;             /* Clean card surface */
  --surface-subtle: #f4f3ef;      /* Soft parchment tint */
  --border: #e6e4df;              /* Muted hairline border */
  --border-strong: #d3d0c9;       /* Active / hover border */
  --border-focus: #18181b;        /* Deep ink focus */
  
  --text: #18181b;                /* Deep charcoal ink */
  --text-muted: #52525b;          /* Weathered slate for descriptions */
  --text-dim: #71717a;            /* Neutral gray for metadata */
  
  --ink: #18181b;
  --ink-inverted: #faf9f6;

  --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
  
  --radius-sm: 4px;
  --radius: 8px;
}

[data-theme="dark"] {
  --bg: #121316;                  /* Deep matte charcoal */
  --surface: #191a1e;             /* Dark panel */
  --surface-subtle: #202227;      /* Secondary surface */
  --border: #282a30;              /* Quiet border */
  --border-strong: #383a42;
  --border-focus: #faf9f6;
  
  --text: #f4f4f5;
  --text-muted: #a1a1aa;
  --text-dim: #71717a;
  
  --ink: #f4f4f5;
  --ink-inverted: #121316;
}
```

---

## 2. Universal Craft Floor Rules (Strict Bans)

1. **NO Eyebrows / Kickers Above Headings**:
   Never put a small uppercase label with a glowing dot above an `<h1>` (e.g. `• REAL-TIME FLEET ANALYTICS`). Let the heading speak for itself.
2. **NO Monospace as UI Headings**:
   Monospace is exclusively for code symbols, git commit hashes, IP addresses, and tabular numbers. Headings and body text must always use sans-serif typography.
3. **NO Neon Borders or Glow Effects**:
   Never use cyan/magenta/green neon outlines (`box-shadow: 0 0 15px rgba(...)`). Selection must be indicated by a subtle hairline border or a tactile 2px top rule (`border-top: 2px solid var(--ink)`).
4. **Line-Length Discipline**:
   Prose and analytical descriptions must be capped at `max-width: 65ch` to guarantee readability.
5. **Mandatory Pinned Export Dock**:
   Every interactive decision surface must include a pinned bottom dock with a `Copy Decisions as Markdown` button using `navigator.clipboard.writeText(...)`.

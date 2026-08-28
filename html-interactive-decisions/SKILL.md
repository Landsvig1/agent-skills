---
name: html-interactive-decisions
description: Generate or edit standalone, highly interactive, Scandinavian minimalist single-file HTML/CSS/JS applications, prototypes, dashboard designs, visual reports, and technical decision matrices. 100% zero-build, zero-Node.js, offline-first, and corporate-safe. Make sure to use this skill whenever the user mentions "html-interactive-decisions", "/html-interactive-decisions", "HTML artifact", "visual prototype", "single-page mockup", "HTML dashboard", "zero-JS interactive UI", asks to compare architectural tradeoffs, needs a regulatory/code review diff surface, or wants an interactive tool in a standalone HTML file.
---

# HTML Interactive Decisions (Enterprise Scandinavian Minimalist Standard)

A specialized skill for building high-craft, quiet, and interactive single-file HTML/CSS/JS applications, prototypes, decision surfaces, and architectural/technical reviews.

Designed specifically for restricted enterprise environments, work laptops without Node.js, and offline usage. Artifacts open directly via `file:///` in Chrome, Edge, or Safari with zero build steps, zero npm dependencies, and zero corporate proxy blocks.

---

## 1. When to Reach for HTML vs. Stay in Markdown

Markdown is optimized for linear reading; HTML is an **ephemeral decision surface** that provides spatial layout, side-by-side comparisons, and real interactivity.

### Reach for HTML when:
- **Architecture & Vendor Comparisons (>2 options)**: Comparing database engines, cloud providers, or technical options side-by-side.
- **Reviewing Diffs / Checklists**: Collapsible comments, severity badges, and triage checkboxes.
- **Interactive Tuning**: Sliders, filters, calculators, or toggles that affect recommendations.
- **Information Density**: Clean data tables, blueprint schematics, and tabbed deep-dives.
- **Decision Capture**: The user needs to manipulate state and copy the result back to the AI prompt.

### Stay in Markdown when:
- Short conversational answers, terminal commands, or single code snippets.
- Simple summaries (<3 bullet points) or linear prose.
- Files intended strictly for git version-controlled text documentation (e.g. project READMEs).

---

## 2. Universal Zero-Node & Corporate-Safe Rules

Every artifact produced by this skill must satisfy these five rules:

1. **100% Single-File & Zero-Node**: No bundler, no `npm install`, no Vite, no Parcel. CSS resides in `<style>`, JS in `<script>`, and graphics as inline `<svg>` or `data:` URIs. Opens directly from disk (`file://`).
2. **Offline & Proxy Immune (No External Scripts)**:
   - **NO Tailwind CDN (`cdn.tailwindcss.com`)**: Strictly forbidden due to 3MB runtime JIT overhead, FOUC, and CSP blocking.
   - **System Font First with Webfont Enhancement**: Always include native system fonts (`system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`) in font stacks.
   - **Inlined Icons & Geometry**: Embed vector SVGs directly (see `references/anti-ai-slop-design.md`).
3. **The Mandatory Round-Trip Export Contract**:
   Every artifact with interactive inputs (radios, checkboxes, sliders, notes) **must** include a pinned export bar (`Copy Decisions as Markdown` / `Copy as Prompt`) using `navigator.clipboard.writeText(...)` so the user's decisions flow back into the agent context.
4. **Scandinavian Minimalist Dignity**:
   - **Warm Bone Paper Canvas**: `#FAF9F6` background, `#FFFFFF` cards, `#E6E4DF` hairlines, `#18181B` deep charcoal text.
   - **No Eyebrows / Kickers**: Never put a small uppercase label with a glowing dot above an `<h1>`. Let the title speak.
   - **No Neon Cyberpunk / Glassmorphism**: Avoid dark terminal neon, gratuitous blurred cards, or gradient text.
   - **Air & Restraint**: Generous margins, line-lengths under 65ch, and weights focused on 500, 600, and 700.
5. **HTML Unslop (Zero AI Tells):**
   Strictly enforce [`references/html-unslop.md`](references/html-unslop.md):
   - Zero decorative emojis in titles, section headings, or bullets.
   - Zero badge/pill overload on non-alert content.
   - Zero puffery words (*paradigmeskift, banebrydende, revolutionerende, flagskib, state-of-the-art, 10x*).
   - Zero em-dashes (`—`). Use periods, commas, or colons before lists.
   - Plain, sober, factual voice without contrast framing ("ikke bare X, men Y").

6. **Output Routing**:
   Save all artifacts to:
   `/Users/kasperlandsvig/Documents/Claude Cowork/agy outputs/HTML_Artifacts/<filename>.html`
   Use clean kebab-case names (e.g., `db-vendor-matrix.html`, `cloud-finops-calculator.html`).

---

## 3. Standard Scandinavian Minimalist Boilerplate

```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Artifact Title]</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  <style>
    /* 1. Scandinavian Minimalist Design Tokens */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    
    :root {
      --bg: #faf9f6;
      --surface: #ffffff;
      --surface-subtle: #f4f3ef;
      --border: #e6e4df;
      --border-strong: #d3d0c9;
      --border-focus: #18181b;
      
      --text: #18181b;
      --text-muted: #52525b;
      --text-dim: #71717a;
      
      --ink: #18181b;
      --ink-inverted: #faf9f6;

      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
      
      --radius-sm: 4px;
      --radius: 8px;
    }

    [data-theme="dark"] {
      --bg: #121316;
      --surface: #191a1e;
      --surface-subtle: #202227;
      --border: #282a30;
      --border-strong: #383a42;
      --border-focus: #faf9f6;
      
      --text: #f4f4f5;
      --text-muted: #a1a1aa;
      --text-dim: #71717a;
      
      --ink: #f4f4f5;
      --ink-inverted: #121316;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 3.5rem 2rem 8rem;
      max-width: 1080px;
      margin: 0 auto;
      -webkit-font-smoothing: antialiased;
    }

    /* Masthead */
    .masthead {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.25rem;
      margin-bottom: 3.5rem;
    }
    .persona-badge { font-size: 0.8rem; color: var(--text-dim); font-weight: 500; }
    .persona-badge strong { color: var(--text); font-weight: 600; }

    /* Header */
    .header-area { margin-bottom: 3rem; }
    h1 {
      font-size: clamp(2rem, 3.4vw, 2.75rem);
      font-weight: 700;
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 0.75rem;
      color: var(--text);
    }
    .lead-text {
      font-size: 1.1rem;
      color: var(--text-muted);
      max-width: 68ch;
      line-height: 1.65;
    }

    /* Grid */
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 4rem; }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 2rem 1.75rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      cursor: pointer;
      transition: border-color 0.2s ease;
    }
    .card:hover { border-color: var(--border-strong); }
    .card.selected { border-color: var(--border-focus); }
    .card.selected::before {
      content: "";
      position: absolute;
      top: -1px;
      left: 1.5rem;
      right: 1.5rem;
      height: 2px;
      background: var(--ink);
    }

    /* Pinned Export Dock */
    .export-dock {
      position: fixed;
      bottom: 2rem;
      left: 50%;
      transform: translateX(-50%);
      width: calc(100% - 4rem);
      max-width: 900px;
      background: var(--surface);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius);
      padding: 0.9rem 1.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
      z-index: 50;
    }
    .btn-export {
      background: var(--ink);
      color: var(--ink-inverted);
      border: none;
      font-family: var(--font-sans);
      font-weight: 500;
      font-size: 0.85rem;
      padding: 0.65rem 1.25rem;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: opacity 0.15s ease;
    }
    .btn-export:hover { opacity: 0.88; }
  </style>
</head>
<body>

  <header class="masthead">
    <div class="persona-badge"><strong>[Persona Name]</strong> · [Role Title]</div>
    <div style="font-size: 0.82rem; color: var(--text-dim);">Single-file · Corporate-Safe</div>
  </header>

  <section class="header-area">
    <h1>[Main Title]</h1>
    <p class="lead-text">[Clear, senior-level briefing explaining the problem and decision parameters.]</p>
  </section>

  <main class="grid">
    <!-- Comparison Cards -->
  </main>

  <aside class="export-dock" aria-label="Action Bar">
    <div id="dock-summary">Status: Option Selected</div>
    <button class="btn-export" id="btn-export">Copy Decision as Markdown</button>
  </aside>

  <script>
    document.getElementById('btn-export').addEventListener('click', async (e) => {
      const md = `### Executive Architecture Decision (${new Date().toISOString().slice(0, 10)})\n\n[Decision Details]`;
      await navigator.clipboard.writeText(md);
      const btn = e.currentTarget;
      btn.textContent = '✓ Copied to Clipboard';
      setTimeout(() => btn.textContent = 'Copy Decision as Markdown', 2000);
    });
  </script>
</body>
</html>
```

---

## 4. Category Archetype References

| Category | Reference Guide | When to Use |
| :--- | :--- | :--- |
| **Decisions & Tradeoffs** | [`references/decision-and-tradeoffs.md`](references/decision-and-tradeoffs.md) | Multi-vendor matrix, database engine comparisons, cloud egress calculators. |
| **Code Review & Diffs** | [`references/code-review-and-diff.md`](references/code-review-and-diff.md) | Architecture refactoring reviews, regulatory statutory diffs. |
| **Dashboards & Tools** | [`references/dashboards-and-tools.md`](references/dashboards-and-tools.md) | Quiet data tables, capacity allocators, audit finding triages. |
| **Visual Design & Icons** | [`references/anti-ai-slop-design.md`](references/anti-ai-slop-design.md) | Scandinavian minimalist tokens, system font fallbacks, 0kb inlined SVG geometry. |

---

## 5. Verification & Sanity Check

```bash
python3 scripts/lint-artifact.py <path-to-file.html>
```

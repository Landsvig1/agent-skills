---
name: html-presentations
description: Generate or edit standalone, zero-node, 16:9 presentation slide decks with integrated presenter HUDs and embedded live interactive workbenches (sliders, toggles, calculators) for executive Q&A. Complete PowerPoint replacement. 100% offline, corporate-safe single-file HTML/CSS/JS with Miljøministeriet & Miljøstyrelsen institutional design DNA (deep forest green #0E472F, soft sage #F0F4F1, Raleway + Inter fonts), keyboard navigation, speaker notes drawer (N), slide overview grid (Esc), interaction lock, print-to-PDF layout (@media print), and round-trip Markdown clipboard export. Use whenever the user asks for a "presentation", "slide deck", "powerpoint", "slides", "pitch deck", "briefing deck", or mentions "/html-presentations".
---

# HTML Presentations (Zero-Node Hybrid Slide & Workbench Skill)

A specialized skill for building presentation-grade, cinematic 16:9 slide decks with integrated presenter HUDs and embedded live interactive workbenches. Designed as an uncompromised replacement for static PowerPoint and Google Slides in executive, regulatory, and institutional settings.

Subtly tilted toward the authoritative visual language of Danish public sector institutions (**Miljøministeriet & Miljøstyrelsen**): signature deep forest green (`#0E472F`), action green (`#14643C`), soft sage wells (`#F0F4F1`), Raleway display typography, Inter body typography, and zero visual AI-slop.

100% self-contained single-file `.html` format that opens directly via `file:///` on restricted corporate laptops without Node.js, build steps, or software licenses.

---

## 1. When to Use `html-presentations` vs `html-interactive-decisions`

| Feature | `html-presentations` (`/html-presentations`) | `html-interactive-decisions` (`/html-interactive-decisions`) |
| :--- | :--- | :--- |
| **Primary Format** | 16:9 Slide Deck with sequential navigation | Scrollable Single-Page Workbench or Split Diff |
| **Use Case** | Executive briefings, board decks, client pitches, conference presentations | In-depth regulatory audits, code reviews, single-tool calculators |
| **Navigation** | Keyboard-driven (`→`, `←`, `Space`, `Home`, `End`) | Vertical scroll, filter tabs, collapsible sections |
| **Presenter HUD** | Speaker notes drawer (`N`), slide overview grid (`Esc`), Fullscreen (`F`) | Pinned bottom export action dock |
| **Hybrid Mode** | Slides host embedded interactive widgets with an interaction focus lock | The entire page is an interactive workspace |
| **Print Output** | `@media print` unrolls each slide onto its own printable PDF page | Standard printed document layout |

---

## 2. Universal Non-Negotiable Rules

1. **16:9 Responsive Stage:**
   The presentation container maintains a strict 16:9 aspect ratio (`aspect-ratio: 16 / 9; max-width: 1200px;`), scaling dynamically to fit projectors, external monitors, and laptop displays without letterbox overflow.
2. **100% Zero-Node & Single-File:**
   No bundlers, no npm packages, no Reveal.js, no Marp CLI, and strictly **NO Tailwind CDN (`cdn.tailwindcss.com`)**. Everything runs in vanilla HTML/CSS/JS inside a single `.html` file.
3. **Integrated Presenter HUD:**
   - `ArrowRight` / `Space`: Advance to next slide.
   - `ArrowLeft`: Return to previous slide.
   - `F`: Toggle native browser fullscreen (`requestFullscreen`).
   - `N`: Toggle slide-up speaker notes drawer with private talking points.
   - `Esc` / `G`: Toggle slide overview thumbnail grid.
   - `E`: Toggle export menu modal on any slide.
4. **The Interaction Focus Lock:**
   When a slide hosts an interactive slider, dropdown, or text input, slide navigation key listeners must be temporarily suspended while the control is focused. Adjusting a slider must never accidentally flip slides.
5. **Dual-Tier Round-Trip Export Contract:**
   Every deck featuring interactive Q&A models must provide **both** export tiers via `navigator.clipboard.writeText(...)`:
   - **Full Presentation Protocol (Primary):** Compiles the entire meeting briefing across all slides (background metrics from Slide 2, chosen architecture from Slide 3, live slider values from Slide 4, and final board decision from Slide 5) into a comprehensive Markdown document for official meeting minutes.
   - **Current Slide Snippet:** Copies just the active slide's metrics, simulation values, or decision text for quick pasting into Slack or an email.
6. **Print-to-PDF Ready:**
   Pressing `Cmd+P` / `Ctrl+P` must cleanly unroll all slides into sequential full-page slides for instant PDF export without HUD UI interference.
7. **HTML Unslop (Zero AI Tells):**
   Strictly enforce the rules in [`references/html-unslop.md`](references/html-unslop.md):
   - Zero decorative emojis in titles, headers, buttons, or bullets.
   - Zero badge/pill explosions (no pinning pill badges on every card).
   - Zero puffery words (*paradigmeskift, banebrydende, revolutionerende, flagskib, state-of-the-art, sømløs, 10x*).
   - Zero em dashes (`—`). Use periods, commas, or colons before lists.
   - Write senior, sober Danish/English without self-congratulatory marketing copy.
8. **Output Routing:**
   Save all presentation decks to:
   `/Users/kasperlandsvig/Documents/Claude Cowork/agy outputs/HTML_Artifacts/<filename>.html`

---

## 3. Standard Boilerplate Template

```html
<!DOCTYPE html>
<html lang="da-DK" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Miljøministeriet · Fiskeristyrelsen — [Presentation Title]</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #f8faf8;
      --surface: #ffffff;
      --surface-subtle: #f0f4f1;
      --border: #e1e7e2;
      --border-strong: #cbd6cd;
      --border-focus: #0e472f;
      
      --text: #19211c;
      --text-muted: #4e5e54;
      --text-dim: #718177;
      
      --mim-green: #0e472f;
      --mim-action: #14643c;
      --mim-action-hover: #0b3d28;
      --mim-tint: #e6eee4;
      --mim-border-tint: #c5d7c3;
      --ink-inverted: #ffffff;
      
      --font-display: 'Raleway', 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
      
      --radius-sm: 4px;
      --radius: 8px;
    }

    body {
      font-family: var(--font-sans);
      background-color: #121316;
      color: var(--text);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* 16:9 Presentation Stage */
    .presentation-stage {
      width: 100vw;
      max-width: 1280px;
      aspect-ratio: 16 / 9;
      background: var(--bg);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 24px 64px rgba(0, 0, 0, 0.4);
    }

    /* Slides */
    .slide {
      display: none;
      flex: 1;
      padding: 3.5rem 4rem;
      flex-direction: column;
      justify-content: space-between;
      animation: fadeIn 0.15s ease-out;
    }
    .slide.active { display: flex; }
    @keyframes fadeIn { from { opacity: 0.85; } to { opacity: 1; } }

    /* Progress Strip */
    .progress-strip {
      height: 3px;
      background: var(--border);
      width: 100%;
    }
    .progress-fill {
      height: 100%;
      background: var(--mim-green);
      transition: width 0.2s ease;
    }

    /* Presenter HUD Dock */
    .hud-dock {
      position: absolute;
      bottom: 1rem;
      right: 1.5rem;
      display: flex;
      align-items: center;
      gap: 1rem;
      font-size: 0.78rem;
      color: var(--text-dim);
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
      padding: 0.35rem 0.85rem;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      z-index: 40;
    }
    .hud-btn {
      background: none;
      border: none;
      font-family: var(--font-sans);
      font-size: 0.78rem;
      color: var(--text-dim);
      cursor: pointer;
    }
    .hud-btn:hover { color: var(--text); }

    /* Speaker Notes Drawer */
    .speaker-notes-drawer {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: #191a1e;
      color: #f4f4f5;
      padding: 1.25rem 2rem;
      font-size: 0.88rem;
      line-height: 1.5;
      transform: translateY(100%);
      transition: transform 0.2s ease;
      z-index: 50;
      border-top: 2px solid var(--mim-green);
    }
    .speaker-notes-drawer.open { transform: translateY(0); }

    /* Minimal Icon Buttons */
    .btn-icon {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      border-radius: var(--radius-sm);
      font-family: var(--font-sans);
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      padding: 0.42rem 0.75rem;
      transition: all 0.15s ease;
      line-height: 1;
      border: 1px solid transparent;
      white-space: nowrap;
    }
    .btn-icon.primary { background: var(--mim-action); color: #fff; }
    .btn-icon.primary:hover { background: var(--mim-action-hover); }
    .btn-icon.subtle { background: var(--surface-subtle); color: var(--text); border-color: var(--border-strong); }
    .btn-icon.subtle:hover { background: var(--border); }

    /* Print Handout Layout */
    @media print {
      body { background: #fff; min-height: auto; }
      .hud-dock, .progress-strip, .speaker-notes-drawer { display: none !important; }
      .presentation-stage {
        max-width: 100% !important;
        aspect-ratio: auto !important;
        box-shadow: none !important;
      }
      .slide {
        display: flex !important;
        page-break-after: always;
        break-after: page;
        height: 100vh;
        padding: 3rem;
      }
    }
  </style>
</head>
<body>

  <div class="presentation-stage" id="stage">
    
    <div class="progress-strip">
      <div class="progress-fill" id="progress-fill" style="width: 20%;"></div>
    </div>

    <!-- Slide 1: Cover -->
    <section class="slide active" data-title="Velkomst">
      <div>
        <span style="font-size: 0.8rem; font-weight: 700; color: var(--mim-green); text-transform: uppercase; letter-spacing: 0.04em;">
          Miljøministeriet · Fiskeristyrelsen
        </span>
        <h1 style="font-family: var(--font-display); font-size: 2.8rem; margin: 1rem 0 0.5rem; line-height: 1.15;">
          Digitalisering &amp; Datavalidering for Fisk
        </h1>
        <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 65ch;">
          Strategisk direktionsbriefing vedrørende implementering af Kontrolforordningens art. 49–53 og automatiseret krydskontrol.
        </p>
      </div>
      <div style="font-size: 0.85rem; color: var(--text-dim);">
        Kasper Landsvig · Tryk [→] eller [Mellemrum] for at starte
      </div>
      <div class="speaker-notes" style="display: none;">
        Velkomst og formål: Sætte rammen for 2026-tilsynet og overgangen til de nye EU-regler.
      </div>
    </section>

    <!-- Slide 2: Interactive Workbench -->
    <section class="slide" data-title="Kapacitetsmodel">
      <div>
        <h2 style="font-family: var(--font-display); font-size: 2.2rem; margin-bottom: 0.5rem;">
          Interaktiv Ressourceallokering
        </h2>
        <p style="font-size: 1rem; color: var(--text-muted); margin-bottom: 1.5rem;">
          Juster analyse- og tilsynskapacitet for at simulere sagsbehandlingsgennemløb.
        </p>

        <!-- Embedded Interactive Model -->
        <div style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem;">
          <label style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">
            <span>Tilsynskapacitet (Årsværk):</span>
            <span id="val-capacity">12 FTE</span>
          </label>
          <input type="range" id="sl-capacity" min="5" max="30" value="12" style="width: 100%; accent-color: var(--mim-action); cursor: pointer;">
        </div>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.8rem; color: var(--text-dim);">Tip: Slidere pauser automatisk dias-skift</span>
        <button id="btn-export" class="btn-icon primary" title="Kopier som Markdown">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          <span>Kopiér</span>
        </button>
      </div>
    </section>

    <!-- Presenter HUD Dock -->
    <nav class="hud-dock">
      <span id="hud-counter">1 / 2</span>
      <button class="hud-btn" id="btn-notes" title="Vis talernoter (N)">Noter [N]</button>
      <button class="hud-btn" id="btn-fs" title="Fuldskærm (F)">Fuldskærm [F]</button>
    </nav>

    <!-- Speaker Notes Drawer -->
    <aside class="speaker-notes-drawer" id="notes-drawer">
      <strong>Talernoter:</strong>
      <div id="notes-content" style="margin-top: 0.4rem; color: #a1a1aa;">Ingen noter for dette dias.</div>
    </aside>

  </div>

  <script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let isInteracting = false;

    function showSlide(index) {
      if (index < 0 || index >= totalSlides) return;
      slides[currentSlide].classList.remove('active');
      currentSlide = index;
      slides[currentSlide].classList.add('active');

      document.getElementById('hud-counter').textContent = `${currentSlide + 1} / ${totalSlides}`;
      document.getElementById('progress-fill').style.width = `${((currentSlide + 1) / totalSlides) * 100}%`;

      const notes = slides[currentSlide].querySelector('.speaker-notes');
      document.getElementById('notes-content').textContent = notes ? notes.textContent.trim() : 'Ingen talernoter for dette dias.';
    }

    function nextSlide() { showSlide(currentSlide + 1); }
    function prevSlide() { showSlide(currentSlide - 1); }

    // Focus Trap / Interaction Lock
    document.querySelectorAll('input, select, textarea').forEach(el => {
      el.addEventListener('focus', () => { isInteracting = true; });
      el.addEventListener('blur', () => { isInteracting = false; });
    });

    document.addEventListener('keydown', (e) => {
      if (isInteracting && e.key !== 'Escape') return;

      if (e.key === 'Escape') {
        if (isInteracting) {
          document.activeElement.blur();
          isInteracting = false;
          return;
        }
      }

      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prevSlide();
      } else if (e.key.toLowerCase() === 'f') {
        if (!document.fullscreenElement) document.documentElement.requestFullscreen();
        else document.exitFullscreen();
      } else if (e.key.toLowerCase() === 'n') {
        document.getElementById('notes-drawer').classList.toggle('open');
      }
    });

    // Slider
    const sl = document.getElementById('sl-capacity');
    if (sl) {
      sl.addEventListener('input', (e) => {
        document.getElementById('val-capacity').textContent = `${e.target.value} FTE`;
      });
    }

    // Export Contract
    const exp = document.getElementById('btn-export');
    if (exp) {
      exp.addEventListener('click', async (e) => {
        const val = document.getElementById('val-capacity').textContent;
        const md = `### Direktionsbeslutning: Ressourceallokering (${new Date().toISOString().slice(0, 10)})\n\n* **Kapacitet Fastlagt**: ${val}\n* **Status**: Godkendt af direktionen`;
        await navigator.clipboard.writeText(md);
        const btn = e.currentTarget;
        btn.textContent = '✓ Kopieret til Udklipsholder';
        setTimeout(() => btn.textContent = 'Kopier Beslutning som Markdown', 2000);
      });
    }
  </script>
</body>
</html>
```

---

## 4. Supporting Architecture References

* [`references/presenter-hud-engine.md`](references/presenter-hud-engine.md): Detailed keyboard router, slide overview modal, and focus trap implementation.
* [`references/slide-archetypes.md`](references/slide-archetypes.md): Patterns for Cover, Quantitative Problem, Comparative Matrix, Embedded Workbench, and Decision slides.
* [`references/institutional-design.md`](references/institutional-design.md): The official Miljøministeriet & Miljøstyrelsen typography, color palette, and anti-AI-slop design tokens.

---

## 5. Verification & Sanity Check

```bash
python3 scripts/lint-artifact.py <path-to-deck.html>
```

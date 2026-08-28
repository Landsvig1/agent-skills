# Reference: Presenter HUD & Navigation Engine

A zero-dependency vanilla JavaScript engine (<130 lines) providing presentation-grade navigation, presenter notes, slide overview grids, and interaction locks for embedded live workbenches.

---

## 1. Core Architecture

The presentation container uses a fixed 16:9 aspect ratio (`aspect-ratio: 16 / 9`) centered on the screen.
Only the active slide (`.slide.active`) is rendered.

```
┌─────────────────────────────────────────────────────────────┐
│ Progress Strip (e.g. 3 of 8 · 37%)                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                      Active 16:9 Slide                      │
│                                                             │
│    [ Slide Content or Live Interactive Workbench ]          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Pinned Presenter Dock (Keyboard shortcuts hint & Jump menu) │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Keyboard Control Map

| Key | Action | Engine Handling |
| :--- | :--- | :--- |
| `→` / `Space` / `PgDn` | Next Slide | Advances active index; suppressed if interaction lock is active. |
| `←` / `PgUp` | Previous Slide | Decrements active index; suppressed if interaction lock is active. |
| `Home` / `End` | First / Last Slide | Jumps to slide 0 or slide N-1. |
| `F` | Toggle Fullscreen | Calls `document.documentElement.requestFullscreen()`. |
| `N` | Toggle Speaker Notes | Slides up the hidden bottom presenter notes drawer. |
| `Esc` / `G` | Toggle Slide Grid | Opens thumbnail overview grid for rapid non-linear jumping. |
| `E` | Toggle Export Menu | Opens dual-tier export modal (Full Deck Protocol vs Current Slide). |
| `Tab` / Click input | Interaction Lock | Disables slide keybindings while manipulating sliders or textareas. |

---

## 3. The Interaction Focus Lock

When an embedded slide contains interactive controls (sliders, inputs, dropdowns), using the arrow keys to adjust a slider could accidentally advance the presentation.

The engine traps focus:
```javascript
let isInteracting = false;

document.querySelectorAll('input, select, textarea, [contenteditable="true"]').forEach(el => {
  el.addEventListener('focus', () => { isInteracting = true; });
  el.addEventListener('blur', () => { isInteracting = false; });
});

document.addEventListener('keydown', (e) => {
  // If the user is actively adjusting an input, let standard input keys pass
  if (isInteracting && e.key !== 'Escape') {
    return;
  }
  
  if (e.key === 'Escape') {
    if (isInteracting) {
      document.activeElement.blur();
      isInteracting = false;
      return;
    }
    toggleOverviewGrid();
    return;
  }

  // Slide navigation
  if (e.key === 'ArrowRight' || e.key === ' ') {
    e.preventDefault();
    nextSlide();
  } else if (e.key === 'ArrowLeft') {
    e.preventDefault();
    prevSlide();
  } else if (e.key.toLowerCase() === 'f') {
    toggleFullscreen();
  } else if (e.key.toLowerCase() === 'n') {
    toggleNotes();
  }
});
```

---

## 4. Speaker Notes Drawer (`N` Key)

Each slide can optionally define a hidden `.speaker-notes` element:
```html
<section class="slide" data-title="Problem Frame">
  <h2>The Regulatory Challenge</h2>
  <p>Main visible content...</p>

  <div class="speaker-notes" style="display: none;">
    <strong>Talking Points:</strong>
    <ul>
      <li>Emphasize that 85% of audit findings stem from missing e-log reconciliation.</li>
      <li>Anticipate objection from CFO regarding initial hardware cost.</li>
    </ul>
  </div>
</section>
```

When the presenter presses `N`, the engine copies the active slide's `.speaker-notes` into a persistent HUD drawer that slides up from the bottom of the screen.

---

## 5. Print & PDF Handout View (`@media print`)

```css
@media print {
  body {
    padding: 0;
    background: #ffffff;
  }
  .hud-progress, .hud-dock, .slide-grid-modal, .speaker-notes-drawer {
    display: none !important;
  }
  .presentation-stage {
    display: block !important;
    width: 100% !important;
    height: auto !important;
  }
  .slide {
    display: flex !important;
    opacity: 1 !important;
    page-break-after: always;
    break-after: page;
    width: 100% !important;
    height: 100vh !important;
    box-sizing: border-box;
    padding: 3rem;
  }
}
```
Pressing `Cmd+P` / `Ctrl+P` renders all slides sequentially into an executive PDF presentation handout.

---

## 6. Dual-Tier Export Engine (Full Protocol vs. Current Slide)

Presenters and committees need two distinct export capabilities:
1. **Full Presentation Executive Protocol (`isFull = true`):**
   Gathers data across ALL slides:
   - Meeting header (Subject, Authority, Presenter, Date)
   - Baseline metrics from problem slides
   - Selected architecture or model from comparison cards
   - Live workbench slider inputs and recalculated values from simulation slides
   - Final committee verdict / decision radio value
   - Pinned into a single, cohesive Markdown briefing ready for official minutes.
2. **Current Slide Snippet (`isFull = false`):**
   Extracts only the metrics, formula result, or talking points of the currently visible slide for quick pasting into Slack, Teams, or an email reply.

```javascript
async function handleExport(isFull, btnTrigger) {
  const md = isFull ? getFullPresentationMarkdown() : getCurrentSlideMarkdown();
  await navigator.clipboard.writeText(md);

  if (btnTrigger) {
    const orig = btnTrigger.innerHTML;
    btnTrigger.textContent = isFull ? '✓ Hele Protokollen Kopieret' : '✓ Dias Kopieret';
    setTimeout(() => { btnTrigger.innerHTML = orig; }, 2200);
  }
}
```
Available via:
- Slide 5: Prominent primary button ("Kopier Hele Præsentationen") and secondary button ("Kopier Kun Dette Dias").
- Presenter HUD Dock: "Eksport [E]" button opening a modal with both options on any slide.
- Keyboard: `E` key toggles the export modal instantly.

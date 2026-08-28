# Reference: Slide Archetypes for Hybrid Presentations

Five battle-tested slide patterns that balance executive clarity with deep interactive capability.

---

## Archetype 1: Institutional Title / Cover Slide
* **Purpose:** Establish solemn institutional authority and set the context.
* **Layout:** Centered or left-aligned masthead with official institutional branding, large clean display heading (`Raleway`), executive subtitle, author/role metadata, and a subtle keyboard hint.
* **Key Elements:**
  - Official badge (`Miljøministeriet · Fiskeristyrelsen` or `Executive Briefing`).
  - Single strong headline (no tech jargon in the title).
  - Date and presenter attribution.

---

## Archetype 2: Quantitative Problem Frame Slide
* **Purpose:** Anchor the presentation on observable metrics, regulatory friction, or commercial urgency.
* **Layout:** 2-column or 3-column split:
  - Left: Narrative challenge, regulatory citation, and core operational bottleneck.
  - Right: High-impact KPI block (e.g. `47m Outage`, `€1.45M Pipeline At Risk`, `26.4% Margenafvigelse`).

---

## Archetype 3: Comparative Trade-Off Matrix Slide
* **Purpose:** Present 2–3 competing strategic options without favoring one prematurely.
* **Layout:** 3 structured cards side-by-side:
  - Header: Option Name & Architectural Approach.
  - Cost / Effort Block: Implementation weeks or projected cloud burn.
  - Trade-offs list: Pro/con analysis.
  - Selection indicator: Radio button allowing the presenter or committee to select an option live during discussion.

---

## Archetype 4: Embedded Interactive Workbench Slide (Hybrid Mode)
* **Purpose:** The core differentiator over PowerPoint. A fully functional calculation model embedded directly on the slide canvas.
* **Layout:**
  - Top: Parameter sliders (e.g., FTE capacity, fleet size, egress traffic, budget threshold).
  - Center: Live recalculating table, comparison gauge, or visual meter.
  - Bottom: Real-time summary metric (e.g., `Result: 40 Weeks Buffer · €1.2M Impact`).
  - Presenter interaction lock: Inputs trap focus so using arrow keys adjusts values instead of flipping slides.

---

## Archetype 5: Executive Decision Request Slide
* **Purpose:** Close the briefing by driving alignment and capturing decisions.
* **Layout:**
  - Clear decision prompt: Three explicit resolution choices (e.g. `Approve Full Roadmap`, `Phase Delivery to Q2`, `Reject Scope`).
  - Next steps timeline: 30 / 60 / 90 day milestones.
  - Dual-Tier Export Affordances: Elevated into the card header (`[↓ Dias]` and `[↓ Fuld]`), cleanly separated from the bottom edge.
  - HUD Dock Clearance: Always elevate action buttons into card headers or preserve at least 200px clearance from the bottom-right corner, ensuring slide interactive elements never collide or interfere with the fixed Presenter HUD dock (`.hud-dock`).

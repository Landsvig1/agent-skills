# `html-presentations` (Zero-Node Hybrid Slide & Workbench Skill)

> Generate or edit standalone, zero-node, 16:9 presentation slide decks with integrated presenter HUDs and embedded live interactive workbenches (sliders, toggles, calculators) for executive Q&A. Complete PowerPoint replacement.

## Overview

A specialized skill for building presentation-grade, cinematic 16:9 slide decks with integrated presenter HUDs and embedded live interactive workbenches. Designed as an uncompromised replacement for static PowerPoint and Google Slides in executive, regulatory, and institutional settings.

Subtly calibrated to the authoritative visual language of Danish public sector institutions (**Miljøministeriet & Miljøstyrelsen**): signature deep forest green (`#0E472F`), action green (`#14643C`), soft sage wells (`#F0F4F1`), Raleway display typography, Inter body typography, and zero visual AI-slop.

## Core Features

- **100% Zero-Node & Single-File**: Opens directly via `file:///` on restricted corporate laptops without Node.js, build steps, or software licenses.
- **Integrated Presenter HUD**: Keyboard-driven navigation (`ArrowRight`, `Space`), Fullscreen (`F`), Speaker Notes Drawer (`N`), Slide Overview Grid (`Esc` / `G`), and Export Menu (`E`).
- **The Interaction Focus Lock**: Adjusting embedded sliders, text fields, or toggles temporarily suspends slide navigation listeners so controls can be manipulated without accidentally advancing slides.
- **Dual-Tier Round-Trip Export Contract**: One-click Markdown export of both the full meeting briefing protocol and individual slide snippets via `navigator.clipboard.writeText(...)`.
- **Print & PDF Mode**: `@media print` unrolls all slides sequentially for clean `Cmd+P` executive handouts.
- **HTML Unslop Enforced**: Zero decorative emojis in headings, zero badge explosions, zero puffery adjectives, and zero em-dash connectors.

## File Structure

```text
html-presentations/
├── SKILL.md
├── README.md
├── evals/
│   └── evals.json
├── references/
│   ├── html-unslop.md
│   ├── institutional-design.md
│   ├── presenter-hud-engine.md
│   └── slide-archetypes.md
└── scripts/
    └── lint-artifact.py
```

## Verification

Validate generated presentation decks against zero-node, corporate-safe presentation standards:

```bash
python3 scripts/lint-artifact.py <path-to-deck.html>
```

## License

Internal Custom Skills © [Kasper Landsvig / aiauto.dk](https://aiauto.dk). All rights reserved.

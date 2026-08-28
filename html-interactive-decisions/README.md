# `html-interactive-decisions` (Scandinavian Minimalist Enterprise Decision & Prototype Skill)

> Generate or edit standalone, highly interactive, quiet single-file HTML/CSS/JS applications, prototypes, dashboard designs, visual reports, and technical decision matrices.

## Overview

A specialized skill for building high-craft, quiet, and interactive single-file HTML/CSS/JS applications, prototypes, decision surfaces, and architectural/technical reviews.

Designed specifically for restricted enterprise environments, work laptops without Node.js, and offline usage. Artifacts open directly via `file:///` in Chrome, Edge, or Safari with zero build steps, zero npm dependencies, and zero corporate proxy blocks.

## Core Features

- **100% Zero-Node & Single-File**: Opens directly from disk (`file://`) with zero npm, bundler, or build dependencies.
- **Corporate & Proxy Safe**: Strictly no Tailwind CDN runtime overhead or blocked third-party dependencies.
- **Mandatory Round-Trip Export Contract**: Interactive decision surfaces (radios, sliders, triage checklists) provide a one-click clipboard export (`navigator.clipboard.writeText`) to format decisions directly back into Claude/agent markdown.
- **Scandinavian Minimalist Dignity**: Warm paper canvas (`#FAF9F6`), clean hairlines (`#E6E4DF`), deep charcoal text (`#18181B`), and system-first typography.
- **HTML Unslop Enforced**: Zero decorative emojis in titles, zero badge explosions, zero marketing puffery words, and zero mid-sentence em-dash drama connectors.

## File Structure

```text
html-interactive-decisions/
├── SKILL.md
├── README.md
├── evals/
│   └── evals.json
├── references/
│   ├── anti-ai-slop-design.md
│   ├── code-review-and-diff.md
│   ├── dashboards-and-tools.md
│   ├── decision-and-tradeoffs.md
│   └── html-unslop.md
└── scripts/
    └── lint-artifact.py
```

## Verification

Validate generated artifacts against zero-node, corporate-safe standards:

```bash
python3 scripts/lint-artifact.py <path-to-file.html>
```

## License

Internal Custom Skills © [Kasper Landsvig / aiauto.dk](https://aiauto.dk). All rights reserved.

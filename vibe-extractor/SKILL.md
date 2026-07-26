---
name: vibe-extractor
description: Extracts design systems, aesthetics, and UI/UX rules from highly acclaimed target websites and distills them into pure, reusable design blueprints without domain-specific content.
---

# Vibe Extractor (/vibe-extractor)

## Overview
This skill acts as a world-class reverse-engineer for web design. It takes a target site or aesthetic, strips away all text, images, and specific features, and extracts the underlying design matrix (typography, spacing, color scales, micro-interactions). The goal is to produce a "blueprint" that makes a new project look as though a top-tier design team spent 3 months perfecting it.

## Core Workflow

### 1. Targeting
- If provided a URL: Immediately target that URL.
- If provided an aesthetic (e.g., "Stripe-like SaaS"): Use `exa-web-search` to find 2-3 highly acclaimed, modern examples of that design.
- **Extraction**: Use `firecrawl-scrape` (or the native Antigravity `antigravity-cmd-design-review` skill) to analyze the DOM structure, CSS tokens, layout techniques, and color palettes.

### 2. Abstraction (The Clean Room)
- Strip out all original text, brand names, product features, and images.
- Distill the raw data into strict **Design Principles**:
  - **Color Palette**: Identify primary, secondary, accents, and background gradients (convert to HSL/Hex).
  - **Typography**: Note font stacks, h1-h6 hierarchies, tracking, and line heights.
  - **Layout**: Document grid systems, max-widths, padding scales, and component borders.
  - **Interactions**: Extract transition timings, hover states, glassmorphism filters, and shadow elevations.

### 3. Production
Output two specific artifacts into the `Gem-CLI Outputs/HTML_Artifacts/` directory (or the active project):
1. **`design-blueprint.md`**: A strategic breakdown of *why* the design works, psychological rules of the UI, and the exact design tokens.
2. **`design-system.html`**: A standalone HTML document defining pure vanilla CSS variables (`:root`) and a few blank, unstyled structural examples (e.g., a blank hero, a blank bento-grid). No Tailwind yet—pure CSS tokens.

### 4. Implementation Readiness
- Conclude by providing a short summary of the extracted vibe.
- Provide instructions for passing `design-blueprint.md` to the `frontend-ui-engineering` skill to apply the new theme to the user's active codebase.

## Usage Commands
- `/vibe-extractor <URL or Aesthetic>`: Executes the end-to-end extraction pipeline.

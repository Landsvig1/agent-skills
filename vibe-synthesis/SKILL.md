---
name: vibe-synthesis
description: Synthesizes a mathematically optimal shadcn/ui design system by analyzing the top 3 competitors in an industry or niche using Exa.
---

# Vibe Synthesis (/vibe-synthesis)

## Overview
This skill acts as an industry-level design engineer. Instead of copying a single site, it analyzes the top tier of an entire industry to extract baseline UX expectations and premium outliers. It then compiles these into a ready-to-use `shadcn/ui` theme.

## Core Workflow

### 1. Triangulated Targeting (Exa)
- Input: An industry, niche, or aesthetic (e.g., "Developer Tools", "Fintech Dashboard").
- Action: Use the `exa-web-search` skill to find the 3 best-in-class, highly acclaimed sites in that niche.
- **Extraction (Chrome DevTools MCP)**:
  - Do NOT use Firecrawl (it returns markdown and loses CSS).
  - Instead, use the `chrome-devtools` MCP to navigate to each of the 3 URLs in a live browser.
  - Execute JavaScript via the MCP to extract exact `getComputedStyle()` tokens directly from the rendering engine. Specifically target:
    - `<button>` and `<a>` elements to find exact RGB/Hex brand colors, border-radii, and paddings.
    - `<h1>` through `<p>` to map font-families, font weights, and typographic scales.
    - `.card` or layout containers for exact `box-shadow` elevations and background colors.

### 2. Competitive Abstraction
- Compare the extracted data across the 3 sites to find the intersection of design choices.
- Identify:
  - **The Baseline**: Common UI patterns, standard color ratios, and expected layouts.
  - **The Premium Outliers**: Unique typographic scales, unique background gradients, or specific border treatments that elevate the design.
- Abstract these into a single, cohesive hybrid design matrix.

### 3. Native `shadcn/ui` Theming
- Map the hybrid design matrix directly to `shadcn/ui` design tokens.
- Generate two specific output files:
  1. A complete `tailwind.config.ts` (with custom colors, border radii, and extend properties).
  2. A `globals.css` file containing the exact `:root` CSS variables mapped to shadcn's expected variable names (e.g., `--primary`, `--muted`, `--ring`).

### 4. Handoff
- Pass the generated configuration files to the `frontend-ui-engineering` skill for instant implementation into the user's active Next.js project.

## Usage Commands
- `/vibe-synthesis <Industry/Niche>`: Executes the multi-competitor extraction and shadcn mapping pipeline.

---
name: vibe-vision
description: Surgically reverse-engineers the exact visual hierarchy and micro-interaction physics of a target URL using multimodal analysis, live DOM interception, and auto-generates Framer Motion React components.
---

# Vibe Vision (/vibe-vision)

## Overview
This skill is a surgical reverse-engineering tool for a single, high-fidelity target. It goes beyond basic CSS scraping by combining multimodal vision analysis with live Chrome DevTools interception. It extracts the exact mathematical truth of animations (springs, beziers) and outputs fully wired, accessibility-corrected Framer Motion React components.

## Core Workflow

### 1. Multimodal & Live Capture
- Input: A single specific target URL.
- **Visual & Motion Context**: Execute `antigravity-cmd-design-review` and `antigravity-cmd-record` to capture the holistic aesthetic, optical alignment, and video of the micro-interactions.
- **Direct Physics Interception**: Use the `chrome-devtools` MCP to attach to the live page. Inject a `MutationObserver` and listen to `TransitionEvent` and `AnimationEvent` APIs. Scrape the exact `cubic-bezier` curves, duration timings, and transform matrices directly from the rendering engine as they fire.

### 2. Deep Documentation & Autonomous Agent-in-the-Loop Review
- **CRITICAL STOP**: Do not write any HTML or React code yet.
- You must first exhaustively document everything into a `vibe-matrix.md` artifact.
- The Matrix must include:
  - **Color Math**: Exact HSL scales for primary, secondary, backgrounds, and borders.
  - **Typography Math**: Font-family stacks, exact `rem` sizing, and line-heights.
  - **Spatial Math**: The precise padding scales, max-widths, and grid gaps.
  - **Physics Math**: The exact easing curves, spring stiffness/damping, and transition durations mapped to specific triggers (hover, active, scroll).
- **Agent-in-the-Loop Review**: Do not wait for human approval. Instead, invoke the `doubt-driven-development` skill to conduct a fresh-context, adversarial review of your `vibe-matrix.md`. 
  - The reviewer agent must verify if the physics and layouts are mathematically complete and coherent.
  - If the reviewer finds gaps (e.g., missing hover states, inconsistent typography, or unrealistic bezier curves), you must iterate and fix the matrix.
  - Only proceed to prototyping once the adversarial review is passed.

### 3. The "Better Than Original" Audit (a11y)
- Pass the extracted visual tokens through the `a11y-debugging` skill.
- Evaluate the target site's contrast ratios and focus states.
- If the target has poor accessibility (e.g., low-contrast text on glassmorphism), mathematically shift the HSL lightness to pass WCAG AAA standards while preserving the original aesthetic intent. Update the Matrix.

### 4. Rapid Prototyping
- Generate an isolated, playable HTML/CSS/JS prototype artifact of the specific interaction (e.g., a standalone floating button or bento card).
- Save this artifact to `Gem-CLI Outputs/HTML_Artifacts/` so the user can instantly test the extracted physics in their browser.

### 5. Production Component Generation
- Generate fully functional, production-ready React components (e.g., `BentoCard.tsx`, `HeroSection.tsx`).
- Wrap the interactive elements in `<motion.div>` tags (Framer Motion).
- Pre-wire all the exact extracted physics (stiffness, damping, mass, bezier curves) from the Vibe Matrix into the `initial`, `animate`, and `exit` states of the component.
- Pass the final components to the `frontend-ui-engineering` skill to integrate them into the user's active codebase.

### 6. Blueprint Sanitization (The Final Prompt)
- Before concluding, sanitize the `vibe-matrix.md` and any final outputs into a pure **Design Prompt**.
- **Remove all origins**: Erase any mention of the original target URL, company name, or brand.
- **Remove meta-commentary**: Do not write "We extracted this color palette from..." or "We verified the contrast ratios". 
- **Absolute Abstraction**: The document must read as an authoritative, standalone design system specification (e.g., "The primary color is HSL(X, Y, Z)", "Cards use a cubic-bezier(X) hover state"). 
- The goal is to produce a clean, stateless prompt that can be injected blindly into any future AI session to perfectly recreate the vibe without any historical baggage.

## Usage Commands
- `/vibe-vision <Specific URL>`: Executes the complete end-to-end multimodal capture, physics interception, a11y correction, component generation, and final sanitization pipeline.

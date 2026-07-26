---
name: html-artifacts
description: Generate or edit standalone, highly interactive, premium single-file HTML/CSS/JS visualizations, prototypes, dashboards, and UI experiments (stored under agy outputs/HTML_Artifacts/). Make sure to use this skill whenever the user mentions "HTML artifact", "visual prototype", "single-page mockup", "HTML dashboard", "zero-JS interactive UI", or asks to generate an interactive web UI/mockup in a standalone HTML file, even if they don't explicitly name a specific folder or tool.
---

# HTML Artifacts

A specialized skill for building mind-blowing, ultra-premium, interactive single-file HTML/CSS/JS applications, prototypes, dashboard designs, and UI/UX experiments. These artifacts serve to showcase state-of-the-art native browser capabilities and offer the user an immediate "wow" factor upon load.

---

## 1. Output Routing

- All standalone HTML artifacts must be written to:
  `/Users/kasperlandsvig/Documents/Claude Cowork/agy outputs/HTML_Artifacts/<filename>.html`
- Do not save them in temporary folders, `.gemini/`, or project subdirectories unless specifically requested.
- Ensure `<filename>` is clean, kebab-case, and descriptive (e.g., `modern-auth-flow.html`, `interactive-speculation-rules-hud.html`).

---

## 2. Design System & Aesthetics Guidelines

Every HTML artifact must look exceptionally polished, feeling like a premium SaaS application or a highly curated design showcase.

### Styling Core Principles
- **No Tailwind CSS**: Use vanilla CSS in a `<style>` tag for maximum flexibility and clean, unbloated stylesheet architecture.
- **Modern HSL-Based Design Systems**: Utilize CSS variables mapped to HSL colors for dynamic, unified palettes. Implement smooth gradients, subtle glowing accents, and premium glassmorphism borders (`rgba(255, 255, 255, 0.08)`).
- **Typography**: Import modern web typography via Google Fonts (e.g., `Plus Jakarta Sans`, `Outfit`, or `Geist Sans`). Use appropriate sizing, letter-spacing, and line-heights.
- **Glassmorphism**: Use `backdrop-filter: blur(12px) saturate(180%);` for overlay cards.
- **Modern Icons**: Embed inline vector SVGs or load a lightweight icon library like Lucide (`https://unpkg.com/lucide@latest`).

---

## 3. Implementation of Cutting-Edge Platform Features (2026 Baseline)

Leverage the latest native CSS and browser APIs to eliminate bulky framework dependencies.

### Inline Conditionals
- **CSS `if()`**: Use inline conditional values for style queries, media queries, and support checks without duplicating rulesets.
  ```css
  button {
    background-color: if(style(--variant: outline): transparent; else: var(--accent));
    width: if(media(max-width: 600px): 100%; else: auto);
  }
  ```

### Scope Isolation
- **CSS `@scope`**: Scope styles to a specific DOM subtree to avoid leaking selectors or needing complex BEM naming conventions.
  ```css
  @scope (.card) to (.card-footer) {
    button {
      color: var(--accent);
    }
  }
  ```

### Scroll-Driven Animations
- **Scroll & View Timelines**: Trigger and map animations to scroll progress or element visibility natively.
  ```css
  .scroll-progress-bar {
    animation: scale-x linear both;
    animation-timeline: scroll();
  }
  .fade-in-on-scroll {
    view-timeline-name: --item-reveal;
    animation: fade-in linear both;
    animation-timeline: --item-reveal;
    animation-range: entry 10% cover 30%;
  }
  ```

### Native Grid Masonry
- **CSS Grid Lanes**: Implement masonry layouts cleanly without JavaScript.
  ```css
  .grid-masonry {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    grid-template-rows: masonry;
    gap: 1.5rem;
  }
  ```

### Interactive Overlays (Popovers & Dialogs)
- **Popover API**: Use the `popover` attribute for stateless floating widgets.
- **`<dialog>` Elements**: Use `<dialog>` and `dialog.showModal()` for modal dialogs to gain native focus-trapping and Esc-key dismiss.
- **Anchor Positioning**: Position popovers and floating cards relative to their triggers natively.
  ```css
  .trigger { anchor-name: --my-trigger; }
  .popover {
    position-anchor: --my-trigger;
    position-area: bottom right;
  }
  ```

### Transitions & Starting Styles
- **Discrete Property Transitions**: Smoothly animate elements going to/from `display: none` or top-layer states using `transition-behavior: allow-discrete`.
- **Starting Style**: Set entry values for newly opened/rendered elements.
  ```css
  .element {
    transition: opacity 0.3s ease, display 0.3s ease allow-discrete, overlay 0.3s ease allow-discrete;
  }
  @starting-style {
    .element:popover-open { opacity: 0; transform: translateY(-8px); }
  }
  ```

---

## 4. Standard 2026 HTML Template Structure

Use the following boilerplate. It incorporates native scroll-driven animations, popovers, anchor positioning, and `@starting-style` transitions.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Premium 2026 Showcase - [Title Name]</title>
  
  <!-- Modern Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    /* 1. Design System & CSS Reset */
    :root {
      --bg-base: hsl(240 10% 4%);
      --bg-surface: hsl(240 10% 9% / 0.7);
      --border-color: hsl(240 10% 20% / 0.4);
      --text-primary: hsl(240 5% 96%);
      --text-secondary: hsl(240 5% 65%);
      --accent: hsl(250 85% 60%);
      --accent-glow: hsl(250 85% 60% / 0.15);
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-base);
      color: var(--text-primary);
      font-family: var(--font-sans);
      min-height: 100vh;
      overflow-x: hidden;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
    }

    /* 2. Scroll-Driven Reading Progress Bar (Pure CSS) */
    .scroll-progress {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--accent), hsl(280 85% 60%));
      transform-origin: left;
      scale: 0 1;
      z-index: 1000;
      animation: grow-progress linear both;
      animation-timeline: scroll();
    }

    @keyframes grow-progress {
      to { scale: 1 1; }
    }

    /* 3. Layout Structure */
    header {
      padding: 1.5rem 2rem;
      border-bottom: 1px solid var(--border-color);
      backdrop-filter: blur(12px);
      background-color: hsl(240 10% 4% / 0.5);
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    main {
      flex: 1;
      padding: 3rem 2rem;
      max-width: 1200px;
      margin: 0 auto;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 3rem;
    }

    /* 4. Anchor-positioned popover with starting-style transitions */
    .menu-trigger {
      anchor-name: --nav-menu-trigger;
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 0.5rem 1rem;
      border-radius: 6px;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    .menu-trigger:hover {
      background-color: hsl(240 10% 12%);
    }

    .dropdown-menu {
      margin: 0;
      inset: auto;
      position-anchor: --nav-menu-trigger;
      position-area: bottom right;
      position-try-fallbacks: flip-block, flip-inline;
      
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      backdrop-filter: blur(16px);
      padding: 0.5rem;
      border-radius: 8px;
      min-width: 200px;
      box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
      
      /* Animation Setup */
      opacity: 0;
      transform: translateY(-8px) scale(0.98);
      transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), display 0.2s ease allow-discrete, overlay 0.2s ease allow-discrete;
    }

    .dropdown-menu:popover-open {
      opacity: 1;
      transform: translateY(8px) scale(1);
    }

    @starting-style {
      .dropdown-menu:popover-open {
        opacity: 0;
        transform: translateY(-8px) scale(0.98);
      }
    }

    /* 5. Scroll-driven Card Reveal (Pure CSS) */
    .reveal-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 2rem;
      border-radius: 12px;
      view-timeline-name: --card-reveal;
      animation: card-slide-up linear both;
      animation-timeline: --card-reveal;
      animation-range: entry 5% cover 25%;
    }

    @keyframes card-slide-up {
      from {
        opacity: 0;
        transform: translateY(40px) scale(0.97);
      }
      to {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
  </style>
</head>
<body>

  <div class="scroll-progress"></div>

  <header>
    <div class="logo" style="font-weight: 600; letter-spacing: -0.02em;">Premium 2026 HUD</div>
    <button class="menu-trigger" popovertarget="nav-menu">Open Menu</button>
    <div id="nav-menu" popover class="dropdown-menu">
      <div style="padding: 0.5rem; font-size: 0.85rem; color: var(--text-secondary);">Native Popover & Anchor</div>
      <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 0.5rem 0;">
      <a href="#" style="display: block; padding: 0.5rem; color: var(--text-primary); text-decoration: none; font-size: 0.9rem;">Option 1</a>
      <a href="#" style="display: block; padding: 0.5rem; color: var(--text-primary); text-decoration: none; font-size: 0.9rem;">Option 2</a>
    </div>
  </header>

  <main>
    <section class="reveal-card">
      <h2>Scroll-Driven Card Reveal</h2>
      <p style="color: var(--text-secondary); margin-top: 0.5rem;">This panel animates and scales up smoothly when scrolled into view, driven purely by CSS view-timelines.</p>
    </section>
  </main>

  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    lucide.createIcons();
  </script>
</body>
</html>
```

---

## 5. Workflow Verification

Before returning the file to the user:
1. **Self-Review**: Run the code mentally or via checking for valid CSS/HTML syntax. Verify that no placeholders are used.
2. **Micro-interactivity Check**: Verify that hover styles, popover triggers, entry/exit transitions, and native elements behave smoothly.
3. **Provide Links**: Print the clickable absolute link to the file on the user's filesystem using `file://` formatting (e.g., `[view page](file:///Users/kasperlandsvig/Documents/Claude%20Cowork/agy%20outputs/HTML_Artifacts/example.html)`).

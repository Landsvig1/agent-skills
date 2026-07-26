---
name: framer-motion
description: Expert guidance, best practices, and standard patterns for building high-performance, fluid animations using Framer Motion in React/Next.js.
---

# Framer Motion Expert (/framer-motion)

## Overview
This skill acts as the source of truth for implementing fluid, mathematically precise animations in React using Framer Motion. It ensures animations are performant (GPU-accelerated), accessible, and cleanly orchestrated. Use this skill whenever the user asks to animate components, add micro-interactions, or when building output for the `vibe-vision` skill.

## Core Directives

### 1. Performance First (Hardware Acceleration)
- **Rule**: ONLY animate `transform` (e.g., `x`, `y`, `scale`, `rotate`) and `opacity`. 
- **Anti-pattern**: NEVER animate `width`, `height`, `top`, `left`, or `box-shadow` unless absolutely necessary, as these trigger expensive browser layout/paint calculations.
- **Layout Animations**: When dimensions *must* change, use the `layout` prop (`<motion.div layout>`) which performs FLIP animations under the hood to simulate layout changes using hardware-accelerated transforms.

### 2. Spring Physics > Durations
- **Rule**: Default to `type: "spring"` instead of `type: "tween"`. Springs feel organic and interruptible.
- **Standard Spring**: `transition={{ type: "spring", stiffness: 300, damping: 30 }}`
- **Bouncy Spring**: `transition={{ type: "spring", stiffness: 400, damping: 10 }}`

### 3. Orchestration via Variants
- Always use the `variants` prop when coordinating complex, multi-element animations (e.g., a staggered list reveal).
- Define variants outside the component render to prevent re-creation on every render.
```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};
```

### 4. Exit Animations
- To animate components when they are removed from the React tree, wrap them in `<AnimatePresence>`.
- The child must have an `exit` prop (e.g., `exit={{ opacity: 0, scale: 0.95 }}`) and a unique `key`.

### 5. Scroll & Interpolation
- When tying animations to scroll position, use `useScroll` and `useTransform`.
- **Warning**: Do not put state variables tied to `useScroll` directly into the dependency array of a `useEffect` unless strictly necessary, as it fires constantly. Pass the `MotionValue` directly to the `<motion.div style={{ y: yRange }}>` to bypass React rendering entirely.

### 6. Accessibility (Prefers Reduced Motion)
- Respect user OS settings. Hook into `useReducedMotion()` from framer-motion.
- If `true`, downgrade complex physics to a simple opacity fade, or remove the animation entirely.

## Integration with `/vibe-vision`
When generating components from `/vibe-vision`, ensure the extracted cubic-beziers or physics are injected perfectly into the `transition` object of the primary `<motion.div>`.

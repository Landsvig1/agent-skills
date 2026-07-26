---
name: web-performance
description: >
  Audit and optimize website performance and Core Web Vitals (LCP, INP, CLS) for
  Next.js/Vercel sites: images, fonts, bundle size, rendering strategy, caching, and
  third-party scripts. Use this skill whenever the user mentions performance, speed,
  slow pages, Lighthouse, PageSpeed, Core Web Vitals, LCP, INP, CLS, bundle size,
  optimization, or "make it faster" — and proactively before launches and after adding
  heavy features (image galleries, embeds, large dependencies, client-side data
  fetching).
---

# Web Performance & Core Web Vitals (Next.js)

Measure first, fix the biggest lever, re-measure. Most perf work fails by optimizing
things that were never the bottleneck — the audit decides where the time goes.

## Targets (2026 thresholds)

| Metric | Good | Notes |
|---|---|---|
| LCP | < 2.0 s | tightened from 2.5 s in 2026; 2.0–2.5 s is now "needs improvement" |
| INP | < 200 ms | most commonly failed vital; full ranking signal |
| CLS | < 0.1 | |
| TTFB | < 800 ms | not a CWV but gates LCP |

Field data (real users) decides pass/fail — lab runs (Lighthouse) are for diagnosis.
Sources: Vercel Speed Insights, Chrome UX Report / PageSpeed Insights "field data"
section, or `useReportWebVitals` shipped to your analytics.

## Phase 1: Audit

1. **Field data:** PageSpeed Insights for the top 3–5 URL types (home, content page,
   product/app page). Note which metric fails and on which device class (it's
   usually mobile).
2. **Lab diagnosis** for failing pages: Lighthouse in Chrome devtools (mobile,
   throttled). Read the *opportunities* and the LCP element + its request waterfall.
3. **Bundle:** `ANALYZE=true` with `@next/bundle-analyzer`. Flag any client chunk
   > ~200 kB gz, duplicate libs, moment/lodash-style full imports, heavy components
   marked `"use client"` that could be server components.
4. **Third parties:** devtools coverage + network tab — script weight, blocking time
   per third party. This is where INP usually dies.
5. **Build output:** `next build` route table — which routes are static (○), ISR (◐),
   dynamic (ƒ)? Pages that *could* be static but render dynamically (a stray
   `cookies()` call, fetch with `no-store`) waste the easiest TTFB win available.

Report: each failing metric → suspected cause → expected impact of fix → effort.
Fix in impact order, one change at a time, re-measure between.

## Phase 2: Fix by metric

### LCP (< 2.0 s)

- LCP element is almost always a hero image or heading. Image: `next/image` with
  `priority`, correct `sizes`, AVIF/WebP (automatic), and *no* lazy-loading on it.
  Preload if it's a CSS background (prefer `<Image fill>` instead).
- TTFB: make the route static or ISR if its content allows; on Vercel that means
  cache-hit responses in tens of ms. Check for accidental dynamic rendering (audit
  §5). For personalized shells, stream: static layout + `<Suspense>` around the
  dynamic part so first paint doesn't wait for the DB.
- Fonts: `next/font` (self-hosted, zero layout shift, no render-blocking request to
  Google — also a GDPR win). Subset to latin + the needed extras.
- Strip render-blocking third-party CSS/JS from the critical path; `next/script`
  `afterInteractive` or `lazyOnload` for everything non-essential.

### INP (< 200 ms)

- Cut main-thread work: less client JS. Default to Server Components; `"use client"`
  only at interactive leaves. `next/dynamic` for modals, editors, charts, maps —
  anything below the fold or behind a click.
- Long tasks: break up heavy handlers; debounce inputs that trigger work.
- Third-party scripts are the top INP killer — lazy-load chat widgets behind a fake
  button, façade YouTube embeds (`lite-youtube` pattern), remove tag-manager zombies.
- Hydration cost: a giant client tree hydrating = terrible first-interaction INP.
  The fix is architectural (server components), not micro-optimization.

### CLS (< 0.1)

- Every image/video/embed gets explicit dimensions (`next/image` enforces this).
- Reserve space for late content: ads, banners, consent dialogs (render the consent
  banner as overlay/fixed, never pushing content down).
- `next/font` kills font-swap shift. Avoid injecting content above existing content
  after load.

### Caching & data

- Static where possible; ISR (`revalidate`) for content that changes hourly/daily;
  `fetch` cache options + tags (`revalidateTag`) for granular invalidation.
- Don't fetch client-side what the server already knew — waterfalls of
  `useEffect`+fetch are both slow and an INP tax. Move reads into server components,
  parallelize with `Promise.all`.
- Set `Cache-Control` on your own API routes/handlers serving public data;
  `stale-while-revalidate` is a good default for public data.

## Phase 3: Verify and keep it fast

- Re-run PageSpeed/Lighthouse on the same URLs; compare before/after numbers in the
  report to the user. Field data takes ~28 days to fully refresh — say so.
- Wire continuous monitoring: Vercel Speed Insights or `useReportWebVitals` → your
  analytics events, so regressions surface without anyone remembering to check.
- Guardrails in CI if the project warrants it: bundle-size budget
  (`size-limit`/bundle-analyzer diff) and a Lighthouse CI run on PRs.
- The cheapest performance win is the dependency you don't add. When reviewing PRs,
  question every new client-side package > 20 kB.

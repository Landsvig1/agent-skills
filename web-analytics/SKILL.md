---
name: web-analytics
description: >
  Choose, implement, and audit website analytics in a privacy-compliant (EU/Denmark)
  way for Next.js sites: cookieless analytics (Plausible, Umami, Vercel Analytics),
  GA4 with Consent Mode v2, custom event tracking, conversions, and UTM hygiene. Use
  this skill whenever the user mentions analytics, tracking, GA4, Google Analytics,
  Plausible, Umami, PostHog, page views, conversions, funnels, measuring traffic or
  user behavior, or asks "how is my site doing" / "who visits my site" — and whenever
  adding marketing pages whose performance will need measuring.
---

# Web Analytics (privacy-first, Next.js)

Get useful measurement without legal exposure or consent-banner data loss. Decide the
tool first — that decision determines whether a consent banner is needed at all, and
banner-gated analytics typically loses ~half of all traffic data to "Reject".

## Step 1: Choose the stack

Decision order for an EU/Danish site:

1. **Cookieless analytics** (default recommendation): Plausible (EU-hosted, paid),
   Umami (self-host free or cloud), or Vercel Web Analytics (zero-config on Vercel).
   No cookies, no personal data stored, no consent banner needed for analytics, no
   US-transfer problem, and you measure 100% of visitors instead of the consenting
   half. Sufficient for: traffic, sources, top pages, countries, devices, custom
   events, simple funnels/goals.
2. **PostHog (EU cloud)** when you need product analytics: session replay, feature
   flags, deep funnels, cohorts. Cookieless mode available; replay and
   identified-user tracking need consent — gate those features, not the basics.
3. **GA4** only when the user specifically needs Google Ads integration or
   cross-platform reporting. Then: Consent Mode v2 is mandatory (EEA), the banner is
   mandatory, and note that Danish DPA practice has been hostile to GA even with
   mitigations — flag the residual risk and prefer server-side tagging through an
   EU-region tagging server if they insist.

Whichever is chosen, coordinate with the gdpr-privacy-terms skill: cookieless tools
still belong in the privacy policy (legitimate-interest, aggregate stats); GA4
requires consent category "statistics" wired into the consent banner.

## Step 2: Implement (Next.js App Router)

**Vercel Analytics:** `pnpm add @vercel/analytics` → `<Analytics />` in root layout.
Add `@vercel/speed-insights` while you're there (feeds the web-performance skill).

**Plausible/Umami:** load via `next/script` with `strategy="afterInteractive"` in the
root layout. Self-hosted Umami on the user's own domain also dodges adblockers.
Optionally proxy the script through a rewrite (`/stats/script.js → plausible.io/...`)
for the same reason — fine for cookieless tools, do not do this to smuggle GA past
blockers.

**GA4 path:** consent default *denied* before any Google script, gtag loaded only
after "statistics" consent, `gtag('consent', 'update', ...)` on change. The consent
banner integration pattern is in the gdpr-privacy-terms skill
(`../gdpr-privacy-terms/references/consent-nextjs.md` when installed alongside).

**SPA navigation:** verify page views fire on client-side route changes. Plausible
and Umami handle this automatically; for hand-rolled senders, hook `usePathname()`
in a client component.

## Step 3: Events and conversions

Measure decisions, not vanity. Define 3–7 events that map to what the site is *for*:

```
signup_completed, contact_form_sent, checkout_completed, demo_booked,
newsletter_subscribed, download_clicked
```

- Plausible: `plausible('signup_completed', { props: { plan: 'pro' } })` — set up as
  Goals in the dashboard. Umami: `umami.track('signup_completed', {...})`.
- Fire events server-side where truth lives (e.g., after Stripe webhook confirms
  payment) when the provider supports an events API — client-side conversion events
  undercount.
- **Never put personal data in event names or props** — no emails, names, user IDs,
  free-text input. Use plan names, counts, booleans, categories.
- UTM hygiene: tag all owned campaign links (`utm_source/medium/campaign`,
  consistent lowercase taxonomy); cookieless tools read UTMs without consent issues.

## Step 4: Audit an existing setup

When reviewing a site that already has analytics:

1. Network tab on a fresh profile: what fires before consent? (GA/Meta firing
   pre-consent is the most common critical finding — hand to gdpr-privacy-terms.)
2. Duplicate tracking — GA4 + Vercel + an old GTM container all at once is common;
   pick the stack deliberately, remove the rest.
3. Event audit: are defined events actually firing? (Trigger each one, watch the
   network tab.) Are conversions tracked anywhere, or only page views?
4. PII leak check: inspect event payloads and URLs sent to the provider — emails in
   query strings (`?email=...` on thank-you pages) leak into analytics; strip or
   redact such params.
5. Data quality: localhost/preview deployments excluded? Own visits excluded? Bot
   filtering on?

## Verification

After setup: visit the site in a fresh profile, confirm exactly the intended
requests fire (and nothing before consent where consent is required); trigger each
custom event once and confirm it appears in the dashboard; deploy-preview traffic
excluded; the analytics provider is named in the privacy policy. Then check the
dashboard after 48h — a setup nobody looks at is a setup to delete.

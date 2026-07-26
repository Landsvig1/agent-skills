# Consent management in Next.js (App Router) — direct implementation

A minimal, compliant consent system without a third-party CMP. Three pieces: consent
state, a banner/settings UI, and script gating.

## 1. Consent state

Store choices in a first-party cookie (itself strictly necessary, no consent needed):

```ts
// lib/consent.ts
export type ConsentCategories = {
  necessary: true;            // always true, not toggleable
  functional: boolean;
  statistics: boolean;
  marketing: boolean;
};

export type ConsentRecord = {
  categories: ConsentCategories;
  timestamp: string;          // ISO
  policyVersion: string;      // bump when cookie policy changes -> re-prompt
};

export const CONSENT_COOKIE = "site-consent";
export const POLICY_VERSION = "2026-06-01";
```

Read it server-side with `cookies()` so the first paint already knows the state (no
banner flash for returning visitors, no tracker requests before hydration).

## 2. Banner + settings

Requirements the UI must satisfy (these are the legally load-bearing parts):

- First layer has three equally-weighted actions: **Accept all**, **Reject all**,
  **Settings**. Reject must not be hidden behind Settings.
- Settings layer: one toggle per category, all defaulting to **off** (necessary shown
  but locked on). Short purpose description per category + link to cookie policy.
- A persistent way to reopen settings: footer link "Cookie settings" on every page.
- On change: write the cookie, log the consent (see §4), and **reload or re-evaluate
  gated scripts** so withdrawal takes effect immediately.
- Re-prompt when `policyVersion` in the cookie ≠ current `POLICY_VERSION`.

Don't block the page behind the banner (cookie walls are non-compliant in DK), and
don't nag — if the user rejected, respect it; re-asking on every page view undermines
"freely given".

## 3. Script gating

The most common compliance bug: scripts in `layout.tsx` load unconditionally. Gate them:

```tsx
// components/GatedScripts.tsx (client component)
"use client";
import Script from "next/script";
import { useConsent } from "./ConsentProvider";

export function GatedScripts() {
  const { categories } = useConsent();
  return (
    <>
      {categories.statistics && (
        <Script src="https://plausible.io/js/script.js" data-domain="example.dk" />
      )}
      {categories.marketing && (
        /* marketing pixels only here */
        null
      )}
    </>
  );
}
```

For embeds (YouTube, maps, social), use a click-to-load façade: render a static
placeholder with a "Load content from YouTube — this sends data to Google" button.
The click is itself valid consent for that embed.

If using Google services despite the transfer concerns, implement **Consent Mode v2**:
set `gtag('consent', 'default', {...denied})` before any Google script, update on
consent. Note to the user that Danish DPA practice has ruled against GA even with
these mitigations — cookieless analytics is the safer recommendation.

## 4. Consent logging

Log every consent action (grant, change, withdrawal) server-side — an API route that
appends `{ anonymousId, categories, timestamp, policyVersion, userAgent }` to a table.
Don't log IP with it (that would create a new personal-data problem); a random
first-party ID stored alongside the consent cookie is enough to evidence the choice.
Retention: keep logs as long as you'd need to demonstrate compliance (a few years).

## 5. Testing

Fresh incognito profile:

1. Load page → Network tab shows zero tracker domains; cookies show only the consent
   cookie and strictly-necessary ones.
2. Reject all → same as above, banner gone, choice persisted.
3. Accept "statistics" only → analytics requests appear, marketing domains still absent.
4. Footer → Cookie settings → withdraw → tracking requests stop.
5. Bump `POLICY_VERSION` → banner reappears.

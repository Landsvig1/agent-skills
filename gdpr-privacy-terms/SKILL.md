---
name: gdpr-privacy-terms
description: >
  Audit and implement GDPR compliance, cookie consent, privacy policies, and terms of
  service for websites — EU/Denmark-first, Next.js-aware. Use this skill whenever the
  user mentions GDPR, privacy, cookies, consent, cookie banner, privacy policy, terms
  of service, ToS, legal pages, data protection, Datatilsynet, tracking compliance, or
  asks to "make the site compliant" or "add legal pages" — even if they don't name a
  specific regulation. Also trigger when adding any third-party script (analytics, ads,
  chat widgets, embeds) since those have consent implications.
---

# GDPR, Privacy & Terms of Service

Make a website lawful to operate in the EU, with Denmark's stricter cookie regime as the
baseline. Two phases: **audit** (find what the site actually does with data) then
**implement** (consent, legal pages, data-handling fixes). Always audit first — policies
that don't match reality are worse than no policies, because they're provably false.

**Disclaimer to surface to the user:** this skill produces solid drafts and technically
correct implementations, but it is not legal advice. Recommend a lawyer review for
anything commercial.

## Legal baseline (Denmark/EU, current as of mid-2026)

- Two laws apply to cookies in Denmark: **cookiebekendtgørelsen** (Danish ePrivacy
  implementation, supervised by Digitaliseringsstyrelsen) and **GDPR** (supervised by
  Datatilsynet). Datatilsynet made cookie consent an enforcement priority for 2026.
- Consent must be **prior, informed, per-purpose, and freely given**. No pre-ticked
  boxes, no consent-by-scrolling, no cookie walls. "Reject all" must be as easy as
  "Accept all" — same layer, same visual weight.
- **Strictly necessary** cookies/storage are exempt (session, auth, cart, CSRF tokens,
  load balancing, consent choice itself) — as long as the data isn't reused for
  anything else.
- Consent must be **withdrawable as easily as it was given** (persistent
  link/button to reopen settings) and **logged** (what was shown, what was chosen, when).
- GDPR applies to all personal data, not just cookies: forms, accounts, server logs
  with IPs, emails sent, payment data, anything in your database.

## Phase 1: Audit

Scan the codebase and produce a findings report before changing anything.

1. **Inventory trackers and third parties.** Grep for script tags, `next/script`,
   known SDK imports and domains: `googletagmanager`, `google-analytics`, `gtag`,
   `fbq`/`facebook`, `hotjar`, `clarity`, `intercom`, `plausible`, `umami`, `posthog`,
   `sentry`, `stripe`, `youtube.com/embed`, `fonts.googleapis.com`. Each one is either
   strictly necessary, or it needs consent, or it should be removed/replaced.
2. **Inventory personal data flows.** Forms (what fields, where does the data go),
   auth/user tables, emails, payment processors, server/edge logs, error trackers
   (Sentry et al. capture IPs and sometimes request bodies). For Supabase: list tables
   holding personal data and check retention.
3. **Check what exists.** Consent banner present? Does it actually *block* scripts
   before consent, or just decorate? (Most fail here — scripts loaded in layout fire
   regardless.) Legal pages present, and do they match the inventory from steps 1–2?
4. **Check transfers.** Any data going to US providers? Note which (GA4 is the common
   offender — see the web-analytics skill for cookieless alternatives that sidestep
   the issue entirely).

Report findings as: **Critical** (tracking without consent, no legal pages, false
claims in existing policy) / **Should fix** (withdrawal not easy, missing purposes,
no consent logging) / **Nice to have**.

## Phase 2: Implement

### Consent management

Preferred order for getting consent right:

1. **Avoid needing it.** Replace GA4 with cookieless analytics, self-host fonts
   (`next/font` does this automatically), use façade patterns for embeds (click-to-load
   YouTube). A site with only strictly-necessary storage needs **no banner at all** —
   this is the best UX and the strongest compliance position.
2. **If consent is needed**, either use a CMP (Cookiebot, Cookie Information, Usercentrics
   — sensible for commercial sites that need audit trails) or implement it directly.
   For direct implementation in Next.js, see `references/consent-nextjs.md` for a
   complete pattern: consent state in a cookie, scripts gated behind consent state,
   per-purpose toggles (necessary / functional / statistics / marketing), reopen-settings
   footer link, and consent logging.

The non-negotiables either way: nothing non-essential loads before consent; reject is
one click on the first layer; choices are per-purpose; withdrawal is one click away
site-wide; consents are logged with timestamp and policy version.

### Legal pages

Generate from the audit inventory, never from generic boilerplate — every processor
and purpose named in the policy must exist in the code, and vice versa. Use
`references/policy-templates.md` for section-by-section skeletons of:

- **Privacy policy** (GDPR Art. 13/14 disclosures: controller identity, purposes,
  legal bases, recipients/processors, transfers, retention, data subject rights,
  complaint right to Datatilsynet)
- **Cookie policy** (table of actual cookies: name, provider, purpose, expiry —
  generate this table from the audit, keep it next to the consent config so they
  can't drift apart)
- **Terms of service** (scope, accounts, acceptable use, payment terms if any, IP,
  liability limits, governing law — Danish law/venue for DK businesses)

For Danish audiences, produce both Danish and English versions. Route them at
`/privacy`, `/cookies`, `/terms` (plus `/privatlivspolitik` etc. if the site is
Danish-first) and link all three plus "Cookie settings" in the footer.

### Data-handling fixes

- Data subject rights: ensure you can actually export and delete a user's data
  (Supabase: write the queries now, not when the first request arrives).
- Retention: add cleanup jobs for logs and stale accounts; document the periods.
- Minimization: drop form fields and DB columns nobody uses.
- Processor agreements: note which vendors need a DPA (most have standard ones —
  Vercel, Supabase, Stripe do).

## Verification checklist

After implementing, verify in a real browser: open devtools → Application → cookies
and Network tab on a fresh profile. Before any consent: only strictly-necessary
cookies, no requests to tracker domains. Reject all: same. Accept statistics only:
analytics fires, marketing doesn't. Withdraw: tracking stops on next navigation.
Legal pages reachable from every page, and every third party in the Network tab
appears in the cookie policy table.

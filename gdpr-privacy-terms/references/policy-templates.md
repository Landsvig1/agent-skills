# Legal page skeletons (EU/Denmark)

Fill every bracket from the audit inventory. Never ship a section describing
processing that doesn't happen, or omit one that does. Produce Danish + English for
Danish-market sites.

## Privacy policy (GDPR Art. 13/14)

1. **Controller** — legal name, CVR number (DK), address, contact email. If a DPO is
   appointed (rarely required for small sites), their contact.
2. **What we collect and why** — one block per processing purpose, each with:
   data categories, purpose, legal basis (consent / contract / legitimate interest /
   legal obligation), retention period. Typical blocks: account data, contact-form
   submissions, order & payment data, analytics, marketing, server logs.
3. **Recipients & processors** — name actual vendors (e.g., Vercel for hosting,
   Supabase for database, Stripe for payments, [analytics provider]). Note DPAs are
   in place.
4. **Transfers outside EU/EEA** — name the mechanism per vendor (adequacy decision,
   SCCs, EU–US Data Privacy Framework participation). If none apply: don't use the
   vendor.
5. **Your rights** — access, rectification, erasure, restriction, portability,
   objection, withdraw consent. How to exercise (email). Right to complain to
   Datatilsynet (datatilsynet.dk) — naming the DK authority is expected practice.
6. **Cookies** — short paragraph linking to the cookie policy.
7. **Changes** — versioning; material changes announced. Show "last updated" date.

## Cookie policy

1. What cookies/local storage are and that similar technologies are covered.
2. **The table** — generate from the audit, one row per cookie/storage key:
   `name | provider | purpose | type (necessary/functional/statistics/marketing) | expiry`.
   Keep this table in a data file shared with the consent banner config so the policy
   and the banner can't drift apart.
3. How to change or withdraw consent (the footer "Cookie settings" link) and how to
   delete cookies in the browser.
4. Per-purpose consent explanation matching the banner categories exactly.

## Terms of service

1. **Who we are & scope** — service description, company identity, CVR.
2. **Accounts** — eligibility (18+, or note parental consent rules), accuracy,
   security responsibility, termination conditions (both directions).
3. **Acceptable use** — prohibited conduct; right to suspend.
4. **Payments** (if any) — prices incl. VAT, billing cycle, renewal, cancellation.
   For consumers: 14-day withdrawal right (fortrydelsesret) under Danish consumer
   law, and the digital-content exception when delivery starts immediately with
   acknowledgment.
5. **Intellectual property** — what's ours, license to use the service, what users
   grant us over their content (keep it minimal and purpose-bound).
6. **Disclaimers & liability** — "as is" within what Danish/EU consumer law allows;
   liability cap for B2B. Consumer rights cannot be waived — say so explicitly rather
   than pretending otherwise.
7. **Governing law & venue** — Danish law; consumers can also use their local courts
   and the EU ODR platform / Mæglingsteamet & Forbrugerklagenævnet for disputes.
8. **Changes** — notice period for material changes; continued use = acceptance only
   after notice.

## Tone and format

Plain language beats legalese — GDPR explicitly requires "concise, transparent,
intelligible" information. Short sections, descriptive headings, tables where they
help. A policy a normal person can read in five minutes is both more compliant and
more trustworthy than ten pages of boilerplate.

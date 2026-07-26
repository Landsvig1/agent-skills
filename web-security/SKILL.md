---
name: web-security
description: >
  Audit and harden the security of Next.js/Vercel websites: security headers and CSP,
  authentication, API route protection, input validation, Supabase Row Level Security,
  secrets handling, and dependency vulnerabilities. Use this skill whenever the user
  mentions security, hardening, vulnerabilities, CSP, headers, XSS, CSRF, injection,
  rate limiting, auth review, RLS, leaked secrets, or pentest prep — and also before
  any launch/deploy of a site, or whenever building auth, payment, file-upload, or
  user-input features, even if the user doesn't say "security".
---

# Web Security (Next.js / Vercel / Supabase)

Audit first, then fix in severity order. The goal is a site where the *default* path
is safe: validation at every boundary, least privilege everywhere, and no security
decision left to "remembering to be careful".

## Phase 1: Audit

Work through these and produce a findings report (Critical / High / Medium / Low):

1. **Secrets.** Grep for keys in the repo (`sk_live`, `SUPABASE_SERVICE_ROLE`, `AKIA`,
   `-----BEGIN`, `.env` committed?). Check that only `NEXT_PUBLIC_*` vars are truly
   public-safe — the service-role key in client code is the classic catastrophic one.
2. **Headers.** `curl -sI https://site.dk` — look for CSP, HSTS,
   X-Content-Type-Options, X-Frame-Options/frame-ancestors, Referrer-Policy,
   Permissions-Policy. Missing CSP on a site with auth is High.
3. **API routes & server actions.** For every route handler and server action: does it
   authenticate? authorize (right user, not just *a* user)? validate input with a
   schema? Server actions are public HTTP endpoints — treat them exactly like API
   routes, never assume "only my UI calls this".
4. **Supabase RLS.** `select * from pg_tables where rowsecurity = false` on public
   schema tables = Critical. Then review policies: a policy of `true` for select on a
   table with personal data is a leak. Run Supabase's advisors
   (`get_advisors`) if MCP access is available.
5. **Injection surfaces.** Raw SQL string interpolation, `dangerouslySetInnerHTML`,
   unsanitized markdown/HTML rendering, `eval`/`new Function`, file uploads without
   type/size checks, redirects built from query params (open redirect).
6. **Dependencies.** `pnpm audit` / `npm audit`; flag criticals with known exploits.
   Check Next.js version against recent CVEs (middleware/proxy auth-bypass class bugs
   have happened — pin to a patched release).
7. **Abuse controls.** Rate limiting on auth endpoints, contact forms, anything that
   sends email or costs money (LLM API calls!). CAPTCHA or proof-of-work on signup if
   bot abuse is plausible.

## Phase 2: Harden

### Security headers

Two implementation tiers — pick based on the site:

**Tier 1 — static-friendly (most sites):** headers in `next.config.js` `headers()`.
Includes a solid CSP without nonces (allows `'self'` + named third parties,
`frame-ancestors 'none'`, etc.). Works with SSG/ISR. See
`references/headers-config.md` for the copy-paste config and per-directive reasoning.

**Tier 2 — strict nonce-based CSP:** generate a per-request nonce in middleware
(`middleware.ts`; renamed `proxy.ts` from Next.js 16). Stronger XSS protection, but
forces dynamic rendering — no SSG/ISR for nonce'd pages. Use for authenticated apps,
not content sites. Pattern in `references/headers-config.md`.

Either way: `unsafe-eval` may be needed in dev (HMR/DevTools) — branch on
`NODE_ENV` so it never ships to production. Verify the result at
securityheaders.com and with a manual click-through (CSP breakage shows in console).

### Input validation

Validate at every trust boundary with zod (or equivalent): API routes, server
actions, webhooks, URL/search params used in queries. Parse, don't sanitize —
`schema.parse(body)` and reject, rather than trying to clean bad input. Length-limit
all strings. For webhooks (Stripe etc.) verify signatures before parsing.

### Auth & session

- Use a maintained library/provider (Supabase Auth, Auth.js, Clerk) — never hand-roll
  password storage or session tokens.
- Authorization on every request server-side. UI hiding is not authorization. The
  pattern to enforce: a `requireUser()` / `requireOwner(resource)` helper called at
  the top of every protected handler, so review = grep for handlers missing it.
- Cookies: `httpOnly`, `secure`, `sameSite: 'lax'` (or `strict`); short-lived access
  + refresh rotation if hand-managing (prefer not to).
- Don't do auth checks *only* in middleware/proxy — middleware bypass CVEs exist;
  middleware is for redirects/UX, the route handler is the security boundary.

### Supabase RLS

RLS on for every table in exposed schemas, no exceptions. Policy patterns:

```sql
alter table profiles enable row level security;
create policy "own rows" on profiles for select using (auth.uid() = user_id);
create policy "own rows write" on profiles for update using (auth.uid() = user_id);
```

Service-role key only in server code, never `NEXT_PUBLIC_`. Storage buckets get
policies too — public buckets leak by URL guessing. Re-run advisors after changes.

### Rate limiting & abuse

Vercel: `@upstash/ratelimit` with Redis, or Vercel WAF rules. Limit by IP *and* by
user where authenticated. Tight limits on: login, signup, password reset, contact/
email-sending endpoints, anything calling paid APIs. Return 429 with `Retry-After`.

### Secrets & supply chain

- `.env*` in `.gitignore`; secrets in Vercel env vars; rotate anything ever committed
  (treat as burned — history is forever).
- `server-only` package import in modules that must never reach the client bundle.
- Lockfile committed; Dependabot/Renovate on; `pnpm audit` in CI failing on critical.

## Verification

After hardening: re-run the audit list top to bottom; hit securityheaders.com (aim
A); attempt your own bypasses — call a protected API route with no cookie via curl,
try another user's resource ID (IDOR), submit oversized/malformed payloads, check a
fresh clone for secrets. For auth changes, test the *negative* cases explicitly:
logged-out, wrong user, expired session.

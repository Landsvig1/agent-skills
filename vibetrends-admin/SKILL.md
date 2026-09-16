---
name: vibetrends-admin
description: Navigation and administration guide for the vibetrends.dk community platform (Next.js 16 + Supabase). Use when an agent needs to find its way around the codebase, add or change content, touch the schema, or reason about the submission review gate.
---

# VibeTrends.dk Admin Skill

Orientation for agents maintaining and evolving `vibetrends.dk`. Verified
against the repo on 2026-08-14. Where this file and the repo disagree, the
repo wins — and fix this file.

Read the project's `AGENTS.md` too. It carries the PR quality bar and the
migration access rules, and it is the stricter document.

## Architecture

- **Frontend**: Next.js 16 (App Router), React 19, Tailwind CSS 4, shadcn/ui.
  This is not the Next.js in your training data — read
  `node_modules/next/dist/docs/` before writing framework code.
- **Backend**: Supabase (Postgres + Auth + Storage). There is no
  GitHub-as-a-backend and no `src/data/db.json`; that architecture and
  `src/lib/github.ts`'s Octokit backend were removed. `src/lib/github.ts`
  still exists but serves repo metadata, not persistence.
- **Deploy**: Vercel, push to `main` for production.
- **Theme**: light off-white. `--background (#FAF9F6)`,
  `--accent-primary (#264021)`. Mascot is the Koala
  (`src/app/components/KoalaIcon.tsx`).
- **Env**: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`,
  `DATABASE_URL`.

## Data layer

Everything reads and writes through `src/lib/db.ts`, over the clients in
`src/lib/supabase-server.ts` (server client, the anon read client
`supabasePublic`, and `getAuthUser()`) and `src/lib/supabase.ts` (browser).

Tables: `skills`, `vibes`, `agents`, `forum_threads`, `forum_replies`,
`blog_posts`. Upvotes live in per-entity join tables (`skill_upvotes`,
`vibes_upvotes`, `agent_upvotes`, `thread_upvotes`, `reply_upvotes`), toggled
via an RPC, with counts maintained by `SECURITY DEFINER` triggers.

**There is no `cli` or `mcp` table.** `/cli` and `/mcp` are both views onto
`agents`, discriminated by `category`, which is
`'CLI' | 'MCP Server' | 'Host'`. `getCli()` filters to `'CLI'`,
`getMcpServers()` to `'MCP Server'`, and the generic agents list excludes
`'MCP Server'`. The detail pages check `category` themselves and 404 on a
mismatch, which is what stops an MCP server rendering under `/cli`. Submit
schemas (`src/lib/schemas.ts`) accept only `'CLI' | 'MCP Server'`.

Bilingual columns use `_da` / `_en` suffixes.

### `description_da` is nullable, and null is a real state

On `skills`, `vibes`, and `agents`, null `description_da` means "not
translated yet". Read paths coalesce to `description_en` through
`withEnglishFallback` in `src/lib/db.ts`, so a Danish visitor sees the English
original rather than an empty card.

- **Never write the English string into `description_da`.** It makes "has a
  Danish translation" and "has an English copy" indistinguishable and
  permanently disables the fallback. Migration
  `20260804000000_description_da_nullable.sql` exists to clean up exactly
  that, across 118 rows.
- Pass the optional `descriptionDa` field only with a real translation. Omit
  it (or send `""`) and the row correctly stores null.
- Backfill: `npm run backfill:danish -- --export work.json`, translate, get a
  Danish speaker to approve, then `--apply work.json`. The apply pass refuses
  passthroughs, mispaired translations, and partial files.
- Doc bodies (`skills.doc_markdown`, fetched `SKILL.md`) stay English.

## The submission review gate

`src/lib/reviewGate.ts` plus migration `20260813000000_review_state.sql`.
Read the module before touching any write path — its header explains the
distinction it is shaped to protect.

- `POST /api/agentauth` mints an anonymous identity with no signup. Rows from
  **bearer-token** callers land as `review_state = 'pending'` and are excluded
  from every public read: catalog, `/api` responses, feed, and sitemap.
- Cookie (magic-link) callers publish directly — they already cleared a real
  auth flow and the honeypot.
- Two separate questions: `reviewStateForWrite()` decides *who* gets held,
  `isGateEnabled()` decides *which tables hide pending rows*. They are not the
  same set. The forum carries the column but ships with its gate off
  (`FORUM_GATE_ENABLED = false`) so the one hub a visitor can fill isn't
  strangled at its first thread.
- A held submission returns **202** with a `PendingSubmission` body, not the
  created entity. Returning the row would tell a truthful agent something
  false.
- Approval path: `.github/workflows/submission-review.yml` turns each pending
  row into a PR; merging or closing it calls back into
  `scripts/review-queue.mjs` (`list` / `manifest` / `approve` / `reject`).
  The manifest has to be judgeable from the PR diff alone, since the row is
  unpublished and its detail page 404s.
- `visibleOnly(query, table)` is the read-side narrowing helper.

## Migrations

**`supabase db push` and the Supabase MCP do not work on this project** (the
MCP connector is authed to a different org, and the DB has no
`supabase_migrations` tracking table). `psql` is not installed locally. Use:

```bash
node --env-file=.env.local scripts/apply-migration.mjs supabase/migrations/<file>.sql
```

Because nothing tracks applied state, **every migration must be idempotent and
reversible** — re-runs and a future `db push` must both be safe. Always pass
`ssl: { rejectUnauthorized: false }` in any hand-rolled `pg` client, and fall
back to the IPv4 pooler when the IPv6-only direct host is unreachable. Full
detail in `AGENTS.md`.

**Order matters: ship the tolerant read code before the migration.** Doing it
the other way took search down for ~15 minutes once already, and the
`review_state` migration's header documents the one matrix cell that is unsafe.

## Auth and security

- **Auth**: Supabase sessions (email OTP magic links + Google/GitHub OAuth).
  Client state in `src/app/components/AuthProvider.tsx`.
- **Server identity**: routes resolve the user via `getAuthUser()`, and
  bearer callers via `resolveRequestIdentity()`. There is **no** `x-username`
  header — never trust client-supplied identity.
- **Authorization is RLS**, not route code: public read, authenticated insert
  with `auth.uid() = user_id`, owner-only update/delete. Delete routes report
  whether a row was actually removed.
- All POST/DELETE routes validate with Zod (`src/lib/schemas.ts`) and check
  the honeypot (`src/lib/honeypot.ts`). Rate limiting in `src/lib/rate-limit.ts`.

## UI/UX standards

- **Buttons**: `.btn-primary` / `.btn-secondary`.
- **Modals**: render outside `<header>` (see `Header.tsx`) or the
  `backdrop-filter` trap eats them.
- **Icons**: `KoalaIcon` for brand, `lucide-react` for UI actions.
- **Language**: the UI is **Danish-only**. PR #94 (Aug 2026) deleted the da/en
  toggle, `LanguageProvider`, the translations dictionary and the `vibe_lang`
  cookie; UI strings are hardcoded Danish and server code calls the data layer
  with a literal `'da'`. Do not reintroduce a toggle or `t()`-style indirection
  without an explicit decision to reverse #94 — and note that the old `t()` was
  never memoized, so any `useCallback`/`React.memo` chain built on it was a
  no-op (see `AGENTS.md`). The DB keeps its `_da`/`_en` column pairs, so
  re-adding English is a UI decision, not a migration. Code and commits in
  English.
- **The hub boards are one shared surface.** `/skills`, `/vibes`, `/cli`,
  `/mcp` and `/forum` share tab and board conventions. Never change one hub's
  default view or tab order alone — they get compared side by side, and the
  drift is immediately visible.
- `src/lib/hubContent.ts` decides whether a hub "has content" for the sitemap,
  robots meta, and header nav. It **fails open** on a read error, deliberately:
  wrongly deindexing a live hub takes a Google re-crawl to undo.

## SEO

- Dynamic pages MUST implement `generateMetadata` from the async `db.ts`
  helpers.
- Every content page injects JSON-LD (`src/lib/jsonLd.ts`).
- Detail pages are indexed and ranking as of August 2026, so **URL changes are
  no longer cheap** — slugs (`src/lib/slug.ts`, `catalog_slugs` migrations) are
  stable identifiers, not cosmetic.

## Scripts

`scripts/`: `apply-migration.mjs`, `review-queue.mjs`, `generate-index.js`
(regenerates `public/semantic-index.json` at build), `refresh-skill-docs.mjs`,
`backfill-danish-descriptions.mjs`, `backfill-slugs.mjs`,
`seed-content-updated-at.mjs`, `seed-e2e-fixtures.mjs`.

**`seed-e2e-fixtures.mjs` writes to the live database.** Running it by hand
leaves visible fixture rows on `/vibes` and `/cli`; teardown does not run
standalone.

## Tests

`npm run test:unit` (Vitest), `npm run test:e2e` (Playwright),
`npm run typecheck`, `npm run lint`. The e2e suite shares one fixture DB, so
overlapping PRs cancel each other's run — re-trigger rather than debug.

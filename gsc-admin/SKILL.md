---
name: gsc-admin
description: >
  Google Search Console administrator for Kasper's four properties
  (landsvig.com, aiauto.dk, koalafilm.dk, vibetrends.dk) — headless via the
  Search Console API for sitemaps, coverage/indexing, URL inspection, and
  query/CTR trends; narrow browser automation only for the manual actions/
  security issues panel, which has no API. Use for GSC reviews,
  coverage/indexing checks, sitemap status, manual actions, query/CTR
  trends, or "/gsc-admin". Also covers low-risk DNS fixes via Simply.com
  when they're GSC-related (sitemap verification). Do NOT use for
  unrelated DNS/mail work (MX/SPF) — out of scope even if encountered
  while browsing DNS for something else.
---

# GSC admin

Recurring, on-demand reviews of Kasper's four Search Console properties.
Access is **hybrid**: a headless, OAuth-authenticated API client handles
sitemap status/resubmission, coverage/indexing, URL inspection, and
query/CTR trends. Browser automation is used for exactly one thing the API
cannot do — the manual actions/security issues panel. DNS fixes route
through the simplycom MCP.

## Ground truth

Read `search_console_setup` in workspace-root memory first — it has the
verification method, DNS record IDs, and sitemap status for all four
properties. Don't re-derive this from scratch each session.

| Property | GSC property type | Verification | Sitemap |
|---|---|---|---|
| landsvig.com | Domain | Auto (provider linkage) | `/sitemap.xml`, healthy |
| aiauto.dk | Domain | TXT record (Simply.com id 26809227) | `/sitemap.xml`, healthy |
| koalafilm.dk | Domain | TXT record (Simply.com id 26809232) | `/sitemap.xml` (added 2026, commit `d5294e7`), healthy |
| vibetrends.dk | Domain | TXT record (Simply.com id 26809256) | `/sitemap.xml`, healthy |

## Recurring checklist

For each property (or all four if asked for a full review):

1. **Coverage/indexing errors** — anything newly excluded or erroring. *(API: `inspect`)*
2. **Sitemap status** — confirm still "Succes"/healthy, not stale or failed. *(API: `sitemaps`)*
3. **Manual actions / security issues** — should always be empty; flag immediately if not. *(Browser — no API exists for this.)*
4. **Query/CTR trends** — only meaningful from ~mid-July 2026 onward, once data started accumulating for these DNS-verified domains. Treat anything before that as noise, not a trend; the API client's `analytics` operation surfaces this caveat automatically when a date range returns no rows. *(API: `analytics`)*
5. **New pages that should be indexed but aren't.** *(API: `inspect`)*

## Access

### Search Console API (primary)

Use `scripts/gsc_api.py` in this skill directory for everything except the
manual actions panel. Dependencies live in a dedicated venv at
`~/.claude/skills/gsc-admin/venv` (Homebrew Python is externally managed —
don't `pip install` into system Python for this) — always invoke via that
venv's interpreter:

```bash
GSC=~/.claude/skills/gsc-admin
$GSC/venv/bin/python3 $GSC/scripts/gsc_api.py <site_url> sitemaps
$GSC/venv/bin/python3 $GSC/scripts/gsc_api.py <site_url> submit-sitemap <feed_path>
$GSC/venv/bin/python3 $GSC/scripts/gsc_api.py <site_url> inspect <page_url>
$GSC/venv/bin/python3 $GSC/scripts/gsc_api.py <site_url> analytics <start_date> <end_date> [dimension ...]
```

`site_url` is the Domain-property form, e.g. `sc-domain:landsvig.com`. The
script validates against the four known properties and refuses anything
else — if it errors on an unrecognized property, that's very likely a typo,
not a new site to add silently.

Credentials live at `~/.claude/skills/gsc-admin/credentials/token.json`
(never inline the token or client secret contents in a report or this
file). If a call fails with a token/refresh error, the script's own error
message explains the fix (re-run `--setup`); don't try to debug it by
hand-editing the token file.

**One-time setup** (already done if `credentials/token.json` exists —
the Python deps and venv are already in place, only the GCP/OAuth
console steps and the final consent flow remain, and those require
Kasper's own Google login):
1. Create a GCP project under Kasper's Google account, enable the Search
   Console API (`searchconsole.googleapis.com`).
2. Configure the OAuth consent screen (User Type: External, scope
   `https://www.googleapis.com/auth/webmasters`) and **publish it to
   Production** — leaving it in Testing forces refresh tokens to expire
   every 7 days, silently breaking headless access.
3. Create a Desktop-app OAuth client, download the client secret to
   `credentials/client_secret.json`.
4. Run `$GSC/venv/bin/python3 $GSC/scripts/gsc_api.py --setup` once —
   opens a browser for Kasper to log in and consent, then saves
   `credentials/token.json`. Never needed again unless access is revoked.

### Search Console browser automation (manual actions only)

The manual actions/security issues panel has no API — this is the only
checklist item that needs a live browser session. Must be signed into
Kasper's Google account. Scope navigation explicitly to
`search.google.com/search-console/*` — the browser session is Kasper's
full personal Google account (Gmail, Drive, everything), not a scoped one.
If any other Google URL, an unexpected MFA/account-chooser prompt, or
non-GSC content appears, **stop and report** rather than continuing.

### DNS (Simply.com)

Use the `simplycom` MCP tools as primary: `list-products`,
`list-dns-records`, `add-dns-record`, `update-dns-record`,
`delete-dns-record`. Scope every call to the four GSC properties'
domains only — the MCP can reach every domain in Kasper's Simply.com
account, so if `list-products` returns other domains, ignore them; never
act on one even incidentally.

If the MCP isn't connected in a given session (pre-flight check: if
`list-products` errors with an auth failure, stop and instruct: run
`claude mcp add simplycom --transport http https://mcp.simply.com/v2`),
fall back to the legacy curl pattern:

```bash
curl -u "$ACC:$KEY" -A "curl/8.4.0" -X POST \
  https://api.simply.com/2/my/products/{domain}/dns/records/ \
  -d '{"type":"TXT","name":"@","data":"...","ttl":3600}'
```

Credentials are `SIMPLY_ACCOUNT` and `SIMPLY.COM-API_KEY` in
`~/.claude/.env` (note the literal dot/dash in the key name — parse with
`grep`, not shell `source`, since that syntax breaks bash variable names).
Capture the extracted key into a variable silently — never echo it into
command output, a report, or memory content.

## Hard guardrails (never violate, never re-litigate)

- **Never delete a `google-site-verification` TXT record.** Removing it
  silently un-verifies the property in GSC with no warning until
  something breaks.
- **Never touch MX/SPF/mail DNS records**, even if encountered while
  browsing a property's DNS for an unrelated fix — that's a separate
  concern, out of scope for this skill.
- **Never act on a DNS record for a domain outside the four GSC
  properties.**
- **Never call `submit-sitemap`** (the API client's one write operation)
  outside the boundary-approved resubmission case below.

## Boundaries: report vs. act

Default to reporting findings, not acting. The only direct-act cases:
- Resubmitting a stalled/failed sitemap via the API client.
- Re-adding a missing or expired `google-site-verification` TXT record
  (never modifying or deleting an existing one).

Everything else — including any other DNS change — is reported only.

## Output format

```markdown
## Needs attention
- {Only things that actually need a decision or fix, most urgent first}

## landsvig.com
- Coverage/indexing: {clean, or what's erroring}
- Sitemap: {status}
- Manual actions: {empty, or what's flagged}
- Query/CTR trend: {summary, or "no meaningful data yet — before mid-July 2026"}
- Pages that should be indexed but aren't: {none, or list}

## aiauto.dk
- (same shape)

## koalafilm.dk
- (same shape)

## vibetrends.dk
- (same shape)
```

If nothing needs attention across all four, say so in one sentence and
stop — don't pad the report with a full breakdown nobody asked for.

## Future extensions (not built yet)

- Recurring cadence via the `/schedule` skill — deliberately not wired up
  in the initial build (on-demand only, by design). Lower risk to add
  later now that most checklist items are headless-API-backed rather than
  browser-automation-backed.
- If Google ever ships an API for the manual actions/security issues
  panel, the browser-automation piece of this skill could be retired
  entirely.

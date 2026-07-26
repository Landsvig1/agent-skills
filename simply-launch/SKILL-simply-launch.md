# Skill · simply-launch

Zero-to-live deployment protocol. Given a domain (registered at Simply.com) and a one-line
idea, provision a complete project stack in under 10 minutes.

---

## Prerequisites

Required in shell environment for every launch:
- `GITHUB_TOKEN` — GitHub PAT (scope: repo)
- `VERCEL_TOKEN` — Vercel API token

MCP connections (one-time setup via `claude mcp add`):
- `simplycom` — `https://mcp.simply.com/v2` (OAuth 2.1, handles DNS and domain lookup)

Conditionally required (see Step 3):
- `SUPABASE_ACCESS_TOKEN` — only if the DB tier is **Supabase** (supabase.com/dashboard/account/tokens)

Optionally required (see Step 6):
- `RESEND_API_KEY` — only if email forwarding is needed

> **Note:** Simply.com no longer requires SIMPLY_ACCOUNT or SIMPLY_API_KEY env vars.
> Authentication is handled by the simplycom MCP via OAuth 2.1. If the MCP is not yet
> connected, run: `claude mcp add simplycom --transport http https://mcp.simply.com/v2`

---

## Pre-flight checks

Before any other step, verify:

1. **simplycom MCP is connected** — if `list-products` errors with auth failure, stop and instruct:
   > Run `claude mcp add simplycom --transport http https://mcp.simply.com/v2` then re-run.

2. **Resolve `$GITHUB_USERNAME`** — fetch it once and store for use in Steps 2, 4, 7:
```bash
GITHUB_USERNAME=$(curl -s https://api.github.com/user \
  -H "Authorization: token $GITHUB_TOKEN" | jq -r '.login')
```
If this returns `null` or errors, stop: `GITHUB_TOKEN` is invalid or lacks `repo` scope.

---

## Step 0 · Assess DB need

Before doing anything else, read the idea description and classify it into one of three tiers:

| Tier | Signals in the idea | DB provisioned |
|------|---------------------|----------------|
| **none** | landing page, portfolio, static tool, countdown, link-in-bio, coming-soon | Skip Step 3 entirely |
| **vercel-postgres** | CRUD, user preferences, form submissions, simple data storage, waitlist, votes | Vercel Postgres via VERCEL_TOKEN |
| **supabase** | auth / login, file uploads, storage, multi-tenant, realtime, row-level security, "users can…" | Supabase project via SUPABASE_ACCESS_TOKEN |

Record your decision: `DB_TIER=none|vercel-postgres|supabase`

If `DB_TIER=supabase` and `SUPABASE_ACCESS_TOKEN` is absent from the environment, stop and report:
> ⛔ This idea needs Supabase but SUPABASE_ACCESS_TOKEN is not set. Export it to the shell and re-run.

---

## Step 1 · Verify domain ownership

Use the **simplycom MCP** `list-products` tool to list all products in the account.
Find the product whose domain matches `$DOMAIN`. Note its `product_id` — used in all DNS calls.

If the domain is not found: stop and report the available domains.

---

## Step 2 · Create GitHub repo + scaffold

1. Derive `$REPO_NAME` from the domain (strip TLD, replace dots with dashes, lowercase):
   e.g. `mysite.com` → `mysite-com`

2. Create a private repo via GitHub API and capture the repo ID:
```bash
REPO_RESPONSE=$(curl -s -X POST https://api.github.com/user/repos \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"'"$REPO_NAME"'","private":true,"auto_init":true}')

GITHUB_REPO_ID=$(echo "$REPO_RESPONSE" | jq -r '.id')
GITHUB_REPO_FULL=$(echo "$REPO_RESPONSE" | jq -r '.full_name')
```

3. Scaffold the repo using the GitHub Contents API (base64-encode each file):

**`app/layout.jsx`** — root layout with `<meta>` SEO tags, og:image stub, cookie consent banner component import

**`app/page.jsx`** — minimal landing page for the idea

**`app/privacy/page.jsx`** — GDPR privacy policy stub with data controller name and contact email

**`vercel.json`** — security headers:
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" }
      ]
    }
  ]
}
```

**`public/robots.txt`** — allow all, point to sitemap

**`public/sitemap.xml`** — stub with the root URL

Push each file via the GitHub Contents API:
```bash
CONTENT_B64=$(echo -n "$FILE_CONTENT" | base64)
curl -s -X PUT "https://api.github.com/repos/$GITHUB_REPO_FULL/contents/$FILE_PATH" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"scaffold: '"$FILE_PATH"'","content":"'"$CONTENT_B64"'"}'
```
Repeat for each file. Do NOT push all files in one call — use one PUT per file.

---

## Step 3 · Provision database (conditional)

### If DB_TIER = none
Skip this step. Write `DB_NOTE=no database provisioned` to the launch report.

### If DB_TIER = vercel-postgres
Create a Vercel Postgres store using the existing `VERCEL_TOKEN`. No new secret required.

```bash
STORE_RESPONSE=$(curl -s -X POST "https://api.vercel.com/v1/storage/stores" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"'"$REPO_NAME"'-db","type":"postgres","region":"iad1"}')

VERCEL_STORE_ID=$(echo "$STORE_RESPONSE" | jq -r '.store.id')
```

Connection strings (`POSTGRES_URL`, `POSTGRES_URL_NON_POOLING`, etc.) are auto-injected by Vercel when the store is linked — no manual env var injection needed.

### If DB_TIER = supabase
Create a new Supabase project via the Management API:

```bash
# Get org ID first
SUPABASE_ORG_ID=$(curl -s https://api.supabase.com/v1/organizations \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" | jq -r '.[0].id')

# Create project
SUPABASE_PROJECT=$(curl -s -X POST https://api.supabase.com/v1/projects \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'"$REPO_NAME"'",
    "organization_id": "'"$SUPABASE_ORG_ID"'",
    "plan": "free",
    "region": "eu-west-1",
    "db_pass": "'"$(openssl rand -base64 24)"'"
  }')

SUPABASE_PROJECT_ID=$(echo "$SUPABASE_PROJECT" | jq -r '.id')
```

Wait for project status to be `ACTIVE_HEALTHY` (poll every 10s, timeout 3 min):
```bash
until [ "$(curl -s "https://api.supabase.com/v1/projects/$SUPABASE_PROJECT_ID" \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" | jq -r '.status')" = "ACTIVE_HEALTHY" ]; do
  sleep 10
done
```

Retrieve keys:
```bash
SUPABASE_URL="https://$SUPABASE_PROJECT_ID.supabase.co"

SUPABASE_SERVICE_ROLE_KEY=$(curl -s \
  "https://api.supabase.com/v1/projects/$SUPABASE_PROJECT_ID/api-keys" \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" | \
  jq -r '.[] | select(.name=="service_role") | .api_key')
```

Inject `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` into Vercel env vars in Step 4.

---

## Step 4 · Create Vercel project

1. Create project from GitHub repo:
```bash
VERCEL_PROJECT=$(curl -s -X POST https://api.vercel.com/v9/projects \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'"$REPO_NAME"'",
    "framework": "nextjs",
    "gitRepository": { "type": "github", "repo": "'"$GITHUB_REPO_FULL"'" }
  }')

VERCEL_PROJECT_ID=$(echo "$VERCEL_PROJECT" | jq -r '.id')
```

2. Add custom domain and capture verification token:
```bash
DOMAIN_RESPONSE=$(curl -s -X POST \
  "https://api.vercel.com/v9/projects/$VERCEL_PROJECT_ID/domains" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"'"$DOMAIN"'"}')

VERCEL_VERIFY_VALUE=$(echo "$DOMAIN_RESPONSE" | \
  jq -r '.verification[] | select(.type=="TXT") | .value' 2>/dev/null || \
  echo "$DOMAIN_RESPONSE" | jq -r '.verificationRecord // empty')
```

3. If `DB_TIER = vercel-postgres`: link the storage store:
```bash
curl -s -X PUT \
  "https://api.vercel.com/v1/storage/stores/$VERCEL_STORE_ID/link" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$VERCEL_PROJECT_ID"'"}'
```

4. If `DB_TIER = supabase`: inject env vars:
```bash
for KEY_VAL in "SUPABASE_URL=$SUPABASE_URL" "SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY"; do
  KEY="${KEY_VAL%%=*}"
  VAL="${KEY_VAL#*=}"
  curl -s -X POST "https://api.vercel.com/v9/projects/$VERCEL_PROJECT_ID/env" \
    -H "Authorization: Bearer $VERCEL_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"key":"'"$KEY"'","value":"'"$VAL"'","type":"encrypted","target":["production","preview"]}'
done
```

---

## Step 5 · Set DNS records via Simply MCP

Use the **simplycom MCP** `add-dns-record` tool with the `product_id` from Step 1.
Add each record in the table below. The MCP tool parameters are self-describing.

| Type  | Name      | Data                                        | TTL  | Priority |
|-------|-----------|---------------------------------------------|------|----------|
| A     | @         | 76.76.19.19                                 | 3600 | —        |
| CNAME | www       | cname.vercel-dns.com                        | 3600 | —        |
| MX    | @         | feedback-smtp.eu-west-1.amazonses.com       | 3600 | 10       |
| TXT   | @         | `v=spf1 include:amazonses.com ~all`         | 3600 | —        |
| TXT   | `_vercel` | (value of `$VERCEL_VERIFY_VALUE` from Step 4) | 300 | —      |

If any record already exists (e.g. a conflicting A record), use the MCP `list-dns-records` tool
to inspect current records, then `update-dns-record` or `delete-dns-record` as needed before adding.

---

## Step 6 · Set up Resend email

> **Note:** `RESEND_API_KEY` is conditionally required. If absent, skip this step and note
> "Email not configured — export RESEND_API_KEY to shell to enable hello@{domain}" in the report.

1. Add domain to Resend and capture DKIM records:
```bash
RESEND_DOMAIN=$(curl -s -X POST https://api.resend.com/domains \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"'"$DOMAIN"'","region":"eu-west-1"}')
```

2. Add the DKIM TXT records returned by Resend using the **simplycom MCP** `add-dns-record` tool
   (same `product_id` as Step 5). The records are in `$RESEND_DOMAIN.records` — add each one.

3. Create inbound route to forward `hello@{domain}` to `klandsvig@gmail.com`:
```bash
curl -s -X POST https://api.resend.com/inbound/routes \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain":"'"$DOMAIN"'","to":"klandsvig@gmail.com"}'
```

---

## Step 7 · Trigger Vercel deploy

```bash
curl -s -X POST "https://api.vercel.com/v13/deployments" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'"$REPO_NAME"'",
    "gitSource": {
      "type": "github",
      "repoId": "'"$GITHUB_REPO_ID"'",
      "ref": "main"
    },
    "projectSettings": { "framework": "nextjs" }
  }'
```

---

## Step 8 · Write launch report

Print the following to stdout (do not assume a fixed filesystem path):

```
# Launch report: {domain}
Date: {date}
Idea: {idea}
DB tier: {none | vercel-postgres | supabase}

## Live URLs
- Site:  https://{domain}
- Repo:  https://github.com/{GITHUB_REPO_FULL}
- DB:    {store name / Supabase project URL / "none"}
- Email: hello@{domain} → klandsvig@gmail.com  (or "not configured")

## DNS records set
{table of records added in Steps 5–6}

## Vercel env vars set
{list, or "none beyond framework defaults"}

## Pending (async)
- DNS propagation: check https://dnschecker.org/#A/{domain}
- Vercel domain verification: auto-resolves after propagation
- Resend DKIM verification: auto-resolves after DNS propagates

## Manual steps (if any)
{list or "None"}
```

---

## Error reference

| Error | Likely cause | Fix |
|-------|-------------|-----|
| simplycom MCP auth failure | OAuth token expired or MCP not connected | Re-run `claude mcp add simplycom --transport http https://mcp.simply.com/v2` |
| Domain not found via `list-products` | Domain not in this Simply account | Check you're authenticated to the right account |
| `add-dns-record` fails — record exists | Conflicting record already present | Use `list-dns-records` then `delete-dns-record` first |
| `GITHUB_USERNAME` is null | Invalid token or missing `repo` scope | Regenerate PAT with `repo` scope |
| `GITHUB_REPO_ID` is null | Repo creation failed | Check token permissions; repo name may already exist |
| Vercel 403 on domain | Domain already on another Vercel project | Remove from old project first |
| Supabase project stuck `COMING_UP` > 5 min | Regional capacity | Retry with `region: us-east-1` |
| Resend inbound route 422 | Domain not verified yet | Re-run after DNS propagates (~30 min) |
| `DB_TIER=supabase` but no SUPABASE_ACCESS_TOKEN | Missing env var | Export to shell and re-run |

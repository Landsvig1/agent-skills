---
name: add-vibe
description: >
  Adds one or more entries to vibetrends.dk from a URL or GitHub repo —
  showcase projects (/vibes), agent skills (/skills), or CLI tools/MCP
  servers (/cli, /mcp) — auto-detected where possible, otherwise confirmed
  with the user. For a project: fetches the page to generate a description
  and title, takes a Playwright screenshot as thumbnail, then inserts it.
  For a repo containing one or more SKILL.md files: imports every detected
  skill as its own /skills entry in one pass. For a CLI tool or MCP server
  (an npm/pip/brew/cargo-installable tool, or something that self-describes
  as an MCP server): inserts it into /cli or /mcp with install command,
  requirements, and tags. Use this whenever working in the vibetrends-dk
  project and someone gives a URL or links to add — even if they just paste
  a URL without explanation. Also triggers on "add this to vibes", "add
  project", "vibes entry", "add to showcase", "add this skill", "add to
  /skills", "add this CLI", "add this MCP server", "add to /cli", "add to
  /mcp", "add this tool".
---

# add-vibe

Add one or more entries to vibetrends.dk from URLs. Given a URL, this skill
decides whether it's a showcase project, an agent-skill repo, or a CLI
tool/MCP server, then fetches, screenshots (projects only), and inserts
accordingly — all through the site's real authenticated API, not a direct
database write.

## Prerequisites (one-time setup)

1. Add `SUPABASE_SERVICE_ROLE_KEY` to `.env.local` (Supabase dashboard →
   Settings → API → service_role key). Used only for the Storage upload
   (project thumbnails) — unrelated to the bot account below.

2. Create the storage bucket:
   ```bash
   node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/setup-storage.mjs
   ```

3. Install Playwright's Chromium browser (if not already present):
   ```bash
   npx playwright install chromium
   ```

4. **Bot/curator account.** All inserts run through `POST /api/vibes` /
   `POST /api/skills` / `POST /api/agents` authenticated as a dedicated bot
   account (not a real contributor's account), so rows carry correct
   ownership and pass the same validation a human submission would.
   - Add `BOT_ACCOUNT_EMAIL` and `BOT_ACCOUNT_PASSWORD` to `.env.local`.
   - The account itself is a normal Supabase Auth user (created once via
     `supabase.auth.admin.createUser({ email, password, email_confirm: true })`
     using the service-role key) — no dashboard step is required beyond that,
     since email/password sign-in is already enabled on this project.
   - **Rotation:** generate a new password, update `BOT_ACCOUNT_PASSWORD` in
     `.env.local`. No code changes needed — the password is read from env at
     sign-in time on every script run (there's no cached/long-lived token to
     invalidate).
   - **If compromise is suspected:** first check recent `/vibes` and
     `/skills` rows for `user_id` matching the bot account (query
     `public.vibes`/`public.skills` via `DATABASE_URL`) to see what was
     inserted, then rotate the password.

If any of these aren't done yet, tell the user which step is missing before proceeding.

## Step 0 — Duplicate check (always, before any insert)

Nothing in the schema stops the same entry being inserted twice, and the
multi-skill path is the sharp edge: re-running this skill on a 14-skill repo
inserts 14 duplicate rows in one silent pass.

```bash
node --env-file=.env.local \
  ~/.claude/skills/add-vibe/scripts/check-existing.mjs \
  --catalog <skills|vibes|agents> --url "<URL>" [--title "<title>"]
```

Exit 0 = safe to insert, exit 2 = already there. For a skills repo, run it once
per detected `SKILL.md` (after Step 1a gives you the titles) — the script also
lists which skills from that repo are *already* imported, so a repo that gained
new skills since the last import only adds the new ones.

On a duplicate: don't insert, and don't "fix" it by tweaking the title. Report
the existing entry and its ID to the user.

## Step 1 — Detect: project, skill, or agent (CLI/MCP)?

**If the user's own request already names the catalog** ("add this CLI",
"put this under /mcp", "this is an MCP server", "add this skill") — skip
detection entirely and go straight to that path. Don't second-guess an
explicit instruction by re-deriving it from the repo/page.

Otherwise, for each URL:

**1a. Skill check (GitHub URLs only, mechanical).** Find the default branch
and list its tree:

```bash
DEFAULT_BRANCH=$(gh api repos/<owner>/<repo> --jq '.default_branch')
gh api "repos/<owner>/<repo>/git/trees/${DEFAULT_BRANCH}?recursive=1" \
  --jq '.tree[] | select(.path | test("SKILL\\.md$")) | select(.path | test("^\\.") | not) | .path'
```

(The `test("^\\.") | not` filter excludes hidden directories like `.agents/`
or `.claude/`, which tend to hold the repo's *own* dev tooling skills rather
than the skills it's actually publishing.)

- **One or more matches** → **skill path** (Step 2b). A single match is a
  single-skill repo; more than one is a multi-skill collection — both are
  handled the same way (one insert per match). Skill detection wins over
  agent detection below: a `SKILL.md`-bearing repo is a skill, full stop.
- **A `SKILL.md` exists but the repo is clearly a full application** with
  its own `package.json` build/dev scripts and a deployed homepage →
  genuinely ambiguous, ask the user which catalog it belongs in.

**1b. Agent (CLI/MCP) signal check** — only runs when 1a found no
`SKILL.md` match (or the URL isn't a GitHub repo at all). Unlike the
skill check, this is *not* a clean grep — a browser-based demo and an
installable CLI tool can look identical from a repo listing or a marketing
page, so lean on asking rather than guessing whenever it's unclear. Look for:

- A repo's `package.json` with a `bin` field, or a README/page that gives an
  install command (`npm install -g ...`, `pip install ...`, `brew install
  ...`, `cargo install ...`, `uvx ...`).
- The page/README explicitly describing itself as an "MCP server" or
  referencing "Model Context Protocol".
- Copy that frames the thing as something you *run in your terminal* or
  *connect your agent to*, rather than something you *visit* or *watch a
  demo of*.

If any of these signals are present, **ask the user to confirm** whether
this is a `/cli` or `/mcp` agent entry rather than a `/vibes` showcase
project — phrase it concretely, e.g. "This looks like an installable CLI
tool rather than a demo project — add it to /cli instead of /vibes?" A real
example from this project: a live marketing page for an npm-installable
video-editing tool was initially misrouted as a /vibes project screenshot
until the user corrected it — the page's own copy (`npm install -g ...`)
was the signal that should have triggered this question up front.

If confirmed → **agent path** (Step 2c).

**1c. Default.** No skill match, no agent signals → **project path**
(Step 2a). This is the fallback, unchanged from before.

## Step 2a — Project path (/vibes)

### Read and describe the page

Use `WebFetch` to fetch the URL. Extract:

- **Title**: from OG title or `<title>` tag. Strip trailing " | Site Name" suffixes. Keep it ≤ 60 chars and human-readable.
- **Description**: a single sentence explaining what the project *does* — what it is and what problem it solves. Think product tagline. No tech stack, no hype words ("revolutionary", "powerful"), no "This is a...". Just the point.

Good description: `"A CLI tool that watches your git commits and auto-generates changelogs."`
Bad description: `"An innovative platform that leverages AI to transform the way developers manage their workflow."`

### Screenshot

```bash
TIMESTAMP=$(date +%s)
npx playwright screenshot \
  --browser chromium \
  --viewport-size 1280,720 \
  --wait-for-timeout 2000 \
  "<URL>" "/tmp/vibe-${TIMESTAMP}.png"
```

### Insert

```bash
node --env-file=.env.local \
  ~/.claude/skills/add-vibe/scripts/add-vibe.mjs \
  --url "<URL>" \
  --title "<title>" \
  --desc "<description>" \
  --image "/tmp/vibe-${TIMESTAMP}.png"
```

This signs in as the bot account and POSTs to the real `/api/vibes`
endpoint (screenshot upload still uses the service-role key for Storage,
unchanged). The script prints the inserted project ID and a direct URL on
success.

### Danish-flags follow-up

**Auto-detect first, don't ask if the URL already tells you:** if the
project's URL host ends in `.dk`, set `is_danish: true` automatically —
no need to ask. That's a strong enough signal on its own (a `.dk` domain
means a Danish registrant). Still ask about `denmark_specific` though —
a `.dk` domain doesn't necessarily mean the *product* is Denmark-specific
(e.g. it could serve an international audience), so that flag stays a
judgment call.

For any URL that *isn't* `.dk`, ask the user whether this project is from a
Danish contributor, or specifically about/for Denmark. The `vibes` table has
the same two flags as
`agents` (`is_danish`, `denmark_specific`), `POST /api/vibes` doesn't expose
either, and they default to `false` on insert. This isn't cosmetic: `/vibes`
now defaults to a "Dansk" tab (same rollout as `/cli`, `/mcp`, `/skills`,
`/forum`) that only shows entries with `is_danish: true` — a project left at
the default is inserted successfully but invisible until a visitor switches
to "All". Confirmed 2026-07-13: a Danish CVR-data API (firmaapi.dk) was
inserted clean but didn't show up on `/vibes` until the flags were set
after the fact.

If the user confirms either applies, set it immediately as part of the same
insert (don't wait to be asked twice):

```bash
node --env-file=.env.local \
  ~/.claude/skills/add-vibe/scripts/set-flags.mjs \
  --catalog vibes --id "<inserted-id>" --danish [--denmark-specific]
```

`denmark_specific` implies `is_danish`, so `--denmark-specific` sets both —
the pair is never `(false, true)`.

## Step 2b — Skill path (/skills)

For each detected `SKILL.md` path from Step 1:

1. Read the file's frontmatter (`gh api repos/<owner>/<repo>/contents/<path> --jq '.content' | base64 -d`,
   or `WebFetch` the raw URL). Extract `name` and `description`.
2. Derive a title from `name` (title-case it if it's a kebab-case slug) and
   a one-sentence description from the frontmatter `description` (which is
   often written as agent-triggering instructions — compress it to a single
   plain-language sentence about what the skill does, same bar as project
   descriptions above).
3. Pick the best-fitting category from `SKILL_CATEGORY_SLUGS` (src/lib/skillCategories.ts)
   (`agent-methodology`, `frontend`, `backend-data`, `fullstack-devops`, `design-ux`,
   `growth-content`, `compliance`, `domain-data`) based on the skill's actual subject
   matter — e.g. a library/framework doc skill fits `frontend`/`backend-data`/
   `fullstack-devops` depending on layer, an external data/API lookup tool fits
   `domain-data`, and an agent planning/debugging/meta skill fits `agent-methodology`.
   Default to `agent-methodology` only when nothing else clearly fits.
4. **Build `--githubUrl` from the skill's own directory, not the repo root.**
   For a `SKILL.md` at `plugins/foo/skills/bar/SKILL.md` on branch `main`:
   ```
   https://github.com/<owner>/<repo>/tree/main/plugins/foo/skills/bar
   ```
   Only a `SKILL.md` sitting at the repo root gets a bare repo URL. This is not
   cosmetic: the `/skills/<id>` detail page resolves the skill's documentation
   from `github_url`, and when the URL names a subdirectory it searches *only*
   that directory — there is deliberately no fall back to the repo root
   (`src/lib/githubDocSource.ts`). A repo-root URL for a monorepo skill forces
   the page onto a slug-guessing heuristic, and when that misses, the skill
   shows the root README describing all 49 of its siblings instead. Step 1a
   already gave you both the branch and the exact path — use them.

5. Insert:
   ```bash
   node --env-file=.env.local \
     ~/.claude/skills/add-vibe/scripts/add-skill.mjs \
     --title "<title>" \
     --category "<topic-slug>" \
     --desc "<description>" \
     --githubUrl "https://github.com/<owner>/<repo>/tree/<branch>/<skill-dir>" \
     --source "https://github.com/<owner>/<repo>" \
     --tags "<comma,separated,tags>"
   ```
   (`--tags` is optional. `--source` is the repo root, for attribution; it
   defaults to `--githubUrl`, which is only correct for a single-skill repo.)

Repeat for every detected `SKILL.md` in the repo — all in one pass, without
asking the user to confirm each one individually.

### Danish-flags follow-up

`/skills` defaults to the same "Dansk" tab as the other hubs, filtering on
`is_danish = true` — so this step is **not** optional here just because the
original skill path never mentioned it. A Danish-authored skill left at the
default is inserted successfully and invisible on the page visitors land on.

Auto-detect where you can, otherwise ask once for the whole repo (skills from
one repo share an author, so this is one question, not one per skill):

```bash
node --env-file=.env.local \
  ~/.claude/skills/add-vibe/scripts/set-flags.mjs \
  --catalog skills --id "<inserted-id>" --danish
```

Add `--denmark-specific` when the skill is specifically about/for Denmark
(Danish law, CVR, Danish-language content). The script sets `is_danish`
implicitly in that case — the pair is never `(false, true)`.

## Step 2c — Agent path (/cli or /mcp)

Both routes are the same underlying `agents` table, filtered by `category`
— the only real decision is which category the entry is (`"CLI"` or
`"MCP Server"`; a third category, `"Host"`, exists in the schema but is a
connection target, not something you insert here — ask the user if it's
genuinely unclear which of CLI/MCP fits).

1. Read the page/repo (`WebFetch`, or `gh api` for a GitHub README) and extract:
   - **name** (≤ 100 chars).
   - **description** (10–500 chars): same factual, no-hype bar as project
     descriptions — what it does, how you run it, what it needs (API keys,
     runtime version, paid vs free). If setup takes more than one command,
     summarize the rest here rather than cramming it into `installCommand`.
   - **installCommand** (optional, ≤ 300 chars): the single copy-pasteable
     command, if there is one (e.g. `npm install -g some-tool`). This is
     rendered as a one-click "copy into your terminal" command, so the API
     rejects shell metacharacters (semicolon, `&`, `|`, backtick, `$`, `<`, `>`, or newlines) — if the real
     setup is `npm install -g x && x init`, put only `npm install -g x` here
     and mention the second step in the description instead.
   - **systemPrompt** (optional): free-text context — requirements,
     dependencies, licensing notes, anything that doesn't fit the
     one-sentence description.
   - **tags** (optional, max 10).
   - **sourceUrl** (optional): canonical repo/site, valid URL, ≤ 300 chars.
2. Insert:
   ```bash
   node --env-file=.env.local \
     ~/.claude/skills/add-vibe/scripts/add-agent.mjs \
     --name "<name>" \
     --category "<CLI|MCP Server>" \
     --desc "<description>" \
     --installCommand "<command>" \
     --systemPrompt "<text>" \
     --tags "<comma,separated,tags>" \
     --sourceUrl "<url>"
   ```
   Prints the inserted ID and a direct `/cli/<id>` or `/mcp/<id>` link.
3. **Danish-flags follow-up — ask, don't assume.** Ask the user whether this
   entry is from a Danish contributor, or specifically about Denmark. These
   two flags (`is_danish`, `denmark_specific`) aren't exposed by
   `POST /api/agents` at all, and they're not cosmetic: `/cli` and `/mcp`
   default to a "Dansk" tab that only shows entries with `is_danish: true` —
   an entry left at the default `false` is invisible until a visitor
   switches to the "All" view. If the user confirms either applies:
   ```bash
   node --env-file=.env.local \
     ~/.claude/skills/add-vibe/scripts/set-flags.mjs \
     --catalog agents --id "<inserted-id>" --danish [--denmark-specific]
   ```
   `denmark_specific` implies `is_danish`, so `--denmark-specific` sets both —
   the pair is never `(false, true)`.

## Step 3 — Summary

After all URLs/skills/agents are processed, print:
- How many projects, skills, and CLI/MCP agents were added
- Direct links: `https://vibetrends.dk/vibes/<id>`,
  `https://vibetrends.dk/skills/<id>`, `https://vibetrends.dk/cli/<id>`, or
  `https://vibetrends.dk/mcp/<id>` for each

## Error handling

**Playwright fails** (site blocks headless, times out, or blank screenshot):
Ask whether to skip this URL or proceed with a fallback thumbnail. If proceeding, omit `--image` — the script will use the default fallback image.

**Ambiguous detection** (Step 1): ask the user which catalog the repo belongs in rather than guessing. This applies doubly to the project-vs-agent split (Step 1b) since it has no mechanical check like the skill grep — when in doubt, ask.

**`installCommand` rejected for shell metacharacters** (Step 2c): the API rejects semicolon, `&`, `|`, backtick, `$`, `<`, `>`, or newlines in that field. Trim the command down to a single step (e.g. drop a trailing `&& x init`) and move the rest into the description — don't retry with the same string.

**Partial multi-skill import failure**: if one skill in a multi-skill repo fails to insert (bad category, network blip), report which ones succeeded and which failed — do not abort the remaining skills in the batch, and do not silently drop the failure either. Each skill's insert is independent (its own bot sign-in), so one failure never takes out the others.

**Script exits non-zero**:
Show the full error output. Don't continue to remaining URLs/skills until resolved.

**Duplicate found** (Step 0, exit code 2): stop for that URL. Report the
existing entry's title, ID and link. Never work around it by renaming the
entry — a near-duplicate row is worse than a rejected import. For a repo that
has genuinely gained new skills since the last import, insert only the ones
the script didn't list.

**Missing env vars**:
The script prints a clear error. Point the user to `.env.local` — the missing key is `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `BOT_ACCOUNT_EMAIL`, `BOT_ACCOUNT_PASSWORD`, or `DATABASE_URL` (the last one is used by `check-existing.mjs` and `set-flags.mjs` only).

**Bucket not found**:
Run `node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/setup-storage.mjs` first.

**Bot sign-in fails**:
Check `BOT_ACCOUNT_EMAIL`/`BOT_ACCOUNT_PASSWORD` in `.env.local` are current — the password may have been rotated. See Prerequisites above.

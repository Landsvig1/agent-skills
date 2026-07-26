---
name: projects-admin
description: >
  Read-only portfolio health check across Kasper's four live web projects —
  landsvig.com, vibetrends.dk, aiauto.dk, koalafilm.dk. Checks git state (uncommitted/
  unpushed work, leaked credentials in remotes), Vercel deploy health, Supabase
  advisors, and whether each project's CLAUDE.md/AGENTS.md is stale or wrong. Trigger
  whenever Kasper asks for a status check, portfolio review, "how are my sites doing",
  wants his projects audited, asks what's broken/stale/needs attention, or wants a
  recurring health check across his sites. This is diagnostic only — it never pushes,
  deploys, edits files, or writes to Supabase. Don't use it as a substitute for actually
  fixing something; use it to find out what needs fixing.
---

# Projects Admin

A portfolio-wide sweep across Kasper's four solo-founder sites. These are small
marketing/community sites, not enterprise systems — the point of this skill is
to surface the handful of things that actually need a human decision, not to
produce a wall of green checkmarks. If everything is fine, say so in one line.

**Hard rule: read-only.** Only run inspection commands (`git status`, `git log`,
reading files) and read-only MCP calls (list/get, never create/update/delete/push/deploy).
If you notice something that needs fixing, report it — don't fix it in this pass.

## The four projects

| Project | Path | GitHub remote | Vercel project name | Backend |
|---|---|---|---|---|
| landsvig.com | `projects/landsvig-com` | `Landsvig1/Landsvig.com` | `landsvig.com` | none (static + Resend email) |
| vibetrends.dk | `projects/vibetrends-dk` | `Landsvig1/Vibetrends.dk` | `vibetrends-dk` | Supabase (Postgres) |
| aiauto.dk | `projects/AiAuto` | `Landsvig1/AiAuto` | `ai-auto` | Supabase (leads table only) |
| koalafilm.dk | `projects/koalafilm` | `Landsvig1/Koalafilm` | `koalafilm` | local JSON (migrated off Supabase — check if that migration looks finished) |

All four share one Vercel team: `team_ripjlZeFprqucLRTvMbc07fo`. Paths are relative
to the Claude Cowork workspace root (`~/Documents/Claude Cowork/projects/`) — resolve
the absolute path for whatever environment you're running in; if a path doesn't
exist, say so rather than guessing another location.

**Don't trust each repo's local `.vercel/project.json` blindly.** It has been observed
stale at least once (AiAuto's local file pointed at a project ID that no longer
resolves under the team at all — the project was apparently recreated at some point
under a new ID/name). Always cross-check against a live `list_projects` call for the
team and match by name; if the name in the table above doesn't appear, search the
returned list for something close (e.g. spelling/hyphenation drift) before assuming
the mapping changed again. If the local file's project ID doesn't match anything
`list_projects` returns, that mismatch is itself a "needs attention" finding — it
usually means `vercel` CLI deploys from that machine are silently going nowhere,
or already went somewhere unexpected.

**Cross-account history gotcha:** these repos' git/Vercel history shows commits and
deployments under two different GitHub identities — `Sartrekant` (older) and
`Landsvig1` (current). That's expected and not itself a problem, but it's *why*
older docs/configs sometimes reference the wrong org — treat any doc referencing
`Sartrekant/...` as describing a pre-migration state, worth flagging as stale.

## Step 1 — Git state (all four)

For each repo, run:

```bash
git -C <path> status --short
git -C <path> log --oneline -3
git -C <path> log --oneline @{u}.. 2>/dev/null   # commits not yet pushed
git -C <path> remote -v
```

Look for:
- **Uncommitted changes or untracked files** — WIP that's been sitting there. Note what it looks like it's for (read filenames, don't need to read full diffs unless something looks off).
- **Unpushed commits** — local work that never made it to GitHub/Vercel.
- **Credentials embedded in the remote URL** (pattern: `https://user:TOKEN@github.com/...` or any `github_pat_...`/`ghp_...` string in the URL). This is a real secret sitting in plaintext in `.git/config` — flag it prominently and recommend rotating the token and switching to a credential helper, regardless of which repo it's in. Don't print the full token in your report; truncate it.

## Step 2 — Vercel deploy health (all four)

Find the Vercel MCP tools if they aren't already loaded — search for `list_projects`,
`get_deployment`, `list_deployments`, `get_runtime_errors` (they'll be under a server
whose tools are prefixed for Vercel). Use `list_projects` (scoped to the team above)
to resolve each project name to its ID, then pull the latest deployment for each and
check its state.

Pull the last ~20 deployments per project (`list_deployments`), not just the single
latest one — a single blocked/errored deployment could be a fluke, but if the last
several *in a row* share the same bad state, that's a pattern worth surfacing loudly.

Flag any state that isn't `READY`, including:
- `ERROR` — pull `get_deployment_build_logs` (or `get_runtime_errors` for a live
  site erroring post-deploy) for the specific failure line. Don't just report
  "it failed," report *why*.
- `BLOCKED` — this has been observed for real (koalafilm's last several *production*
  deployments came back `BLOCKED` in a row). Don't assume this means "same as
  ERROR" or wave it away as a preview-protection artifact — report the deployment
  IDs/timestamps and tell Kasper to check the Vercel dashboard for why (deployment
  protection, a required check, spend management pausing the project, etc.) since
  the root cause isn't visible from this MCP surface.
- `CANCELED`, or the newest entry stuck in `BUILDING`/`QUEUED` well past when a
  build should have finished.
- A latest deployment timestamp that's suspiciously old relative to the git log
  (suggests pushes aren't triggering deploys, or deploys are failing silently).

## Step 3 — Supabase advisors and stray project cleanup

koalafilm.dk migrated off Supabase to local JSON — confirm this is actually complete
by checking whether `@supabase/*` is still imported anywhere in `src/`. Also run
the Supabase MCP's `list_projects` and check whether a project named "Koalafilm"
(or similar) is still `ACTIVE_HEALTHY` — this has been observed to still be running
post-migration. An active, unused Supabase project is worth flagging (dead
infrastructure, possibly still billing) even though the app doesn't call it anymore.
landsvig.com never used Supabase, so skip it entirely.

For vibetrends.dk and aiauto.dk: **do not assume the Supabase MCP can see these
projects.** In practice it's been confirmed scoped to a different Supabase
organization than the one these two projects live in — vibetrends-dk's own
`AGENTS.md` documents this explicitly, and a real `list_projects` call returned
only unrelated projects, not vibetrends or aiauto. So: run `list_projects` first,
and only call `get_advisors` if a project genuinely matching that site's Supabase
ref turns up (cross-check against the `SUPABASE_URL`/project ref in the repo's
`.env.local` if present, not just by name). If no match appears, say so plainly —
"Supabase MCP isn't authed to this project's org, can't pull advisors this way" —
rather than silently skipping the check or guessing at a different project.

## Step 4 — Doc staleness (all four)

Read each project's `CLAUDE.md` (and `AGENTS.md` if `CLAUDE.md` just points to it).
A doc is stale if:
- It's a generic stub/template with no project-specific detail (e.g. just says
  "read README.md first" with no actual architecture notes).
- It references a git remote, org, or path that doesn't match what `git remote -v`
  actually shows.
- It describes a backend or stack the project has since moved off (e.g. still
  says "Supabase" when the code has migrated away).

This step matters because any future agent work on these repos leans on these docs —
a wrong doc actively misleads rather than just being unhelpful.

## Output format

Lead with what needs action. If nothing does, say so in one sentence and stop —
don't pad the report with a full per-project breakdown nobody asked for.

```markdown
## Needs attention
- {Only the things that actually need a decision or fix, most urgent first}

## landsvig.com
- Git: {clean, or what's outstanding}
- Deploy: {latest status}
- Docs: {fine, or what's stale}

## vibetrends.dk
- Git: ...
- Deploy: ...
- Supabase advisors: ...
- Docs: ...

## aiauto.dk
- (same shape)

## koalafilm.dk
- (same shape, note Supabase migration completeness)
```

Keep each bullet to one line unless something needs the detail (e.g. a build
error's actual message, or the exact secret-in-remote finding).

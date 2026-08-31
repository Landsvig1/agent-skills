---
name: bot-pr-review
description: >
  Daily PR triage for vibetrends.dk, the only repo this routine covers.
  Handles the three automated PR classes the repo actually produces:
  agent catalog submissions (`submission/*` branches, where merge means
  approve into the public catalog), the weekly hot-ranking PRs
  (`hot-ranking/YYYY-Www`, which routinely open duplicates), and the
  dormant coding-bot classes (Bolt/Sentinel/Jules). It closes clear
  rejects and duplicates on its own, and leaves genuine approval
  candidates open with a review comment for Kasper. Trigger whenever
  Kasper asks to check or review vibetrends PRs, drain the submission
  queue, clean up the PR backlog, asks what is waiting on the catalog,
  or wants a status check on the repo's open pull requests. Also runs
  nightly via bot_pr_review_daily.py on the Hermes VPS. Never acts on
  Kasper's own PRs.
compatibility: >
  Requires an authenticated `gh` CLI with merge and close permissions on
  Landsvig1/Vibetrends.dk, git with worktree support, and npm for
  typecheck/lint/test verification before any code merge.
---

# Vibetrends PR review

Scope: **one repo, `Landsvig1/Vibetrends.dk`.** Koalafilm and AiAuto were
dropped 2026-08-30 when everything was refocused on vibetrends.dk. Their
hard-won lessons are parked at the bottom of this file, not deleted, so
re-adding a repo is a matter of restoring a table row rather than
re-learning them. See `Agents/Hermes/FOCUS.md` for the wider focus ledger.

| Local path (Mac) | Local path (VPS) | Remote |
|---|---|---|
| `projects/vibetrends-dk` | `/home/administrator/vibetrends-dk` | `Landsvig1/Vibetrends.dk` |

Read `AGENTS.md` and `CLAUDE.md` in the repo before reviewing anything.
`AGENTS.md` carries the project's own PR quality bar, and several of the
reject criteria below are just that bar applied.

## Why this rewrite happened (read once, it explains the whole design)

Between late July and 2026-08-30 this routine ran every night and did
nothing at all. It was looking for `⚡ Bolt:`/`🛡️ Sentinel:` titles and
`^(jules|bolt|sentinel)[-/]` branches. Vibetrends has produced none since
late July. Every actually-open PR was a `submission/skills/*` branch,
which the old rules classified as "human, out of scope", so nine of them
accumulated over thirteen days while the log truthfully reported
"0 bot PRs, nothing to do".

That backlog then caused a second bug. The content loop
(`project_audit_loop.py --mode content`) dedupes candidates against the
live catalog, and a pending submission is not in the live catalog, so it
regenerated the same skills every run: `bot-pr-review` reached slug
`bot-pr-review-3` across PRs #152/#159/#164. The loop's own
`vibetrends_submitted.json` ledger was supposed to prevent exactly this,
but it lived under `knowledge/`, which the Mac pushes with
`rsync --delete`, so it was deleted twice a day. Fixed 2026-08-30 by
moving the ledger to `~/.hermes/state/`.

**The lesson to carry: a queue that nobody drains does not sit still, it
feeds back into whatever produces it.** When this routine reports "nothing
to do" on a repo that clearly has open PRs, that is a bug in the routine,
not a quiet day. Check what the open PRs actually are before believing it.

## Step 0: classify every open PR

```bash
gh pr list -R Landsvig1/Vibetrends.dk --state open \
  --json number,title,headRefName,createdAt,labels,files,mergeable
```

Assign every PR to exactly one class. If a PR matches none of them, it is
Class D by default (leave it alone) and say so in the report by name, so a
new automation class cannot silently go unhandled the way submissions did.

| Class | Identified by | This routine may |
|---|---|---|
| **A. Catalog submission** | branch `^submission/`, label `submission`, title `Submission: <name>` | close (reject) autonomously; never merge |
| **B. Hot ranking** | branch `^hot-ranking/\d{4}-W\d{2}` | close superseded duplicates; merge the surviving one only if CI is green |
| **C. Coding bot** | title starts `⚡ Bolt:` or `🛡️ Sentinel:`, or branch `^(jules|bolt|sentinel)[-/]` | full Step 3 pipeline (merge / fix / reject / escalate) |
| **D. Kasper's own** | anything else (`feature/*`, `fix/*`, `refactor/*`, `docs/*`, ...) | nothing, report only |

Class D is the safety default. `author.login`/`is_bot` is useless in this
repo: every PR is authored by `Landsvig1`, including the automated ones,
because the workflows use the owner's own token. Branch and label are the
only reliable signals.

## Step 1: Class A, catalog submissions

This is now the routine's main job. Read `.github/workflows/submission-review.yml`
and `submission-resolve.yml` in the repo for the mechanism; the short version:

- One PR per pending submission, opened every 15 minutes by a workflow.
- The PR body is a manifest at `submissions/<type>/<id>.md` and nothing else.
- **Merge means approve**: the entry becomes publicly visible in the catalog.
- **Close without merge means reject**: the DB row is deleted permanently.
- The `submission` label is load-bearing. `submission-resolve.yml` gates its
  entire job on it. Never remove it.

### The standing policy, decided by Kasper 2026-08-30

**Close clear rejects autonomously. Never merge an approval. Escalate every
genuine candidate to Kasper with a comment.**

The reason is not caution about the code, it is positioning: `PRODUCT.md`
bets vibetrends' whole pitch on "curated, never scraped", and the git
history of accepted manifests is that claim made auditable. An agent
approving agent-written entries into that catalog would hollow out the one
thing the product claims. Rejecting noise needs no such authority.

Do not re-litigate this per PR. Reject or escalate, never merge.

The single narrow exception is a PR whose row is *already live* in the
catalog, where merging records a decision the DB has already made rather
than making one. That exception is defined below, and it is evaluated
**after** the reject criteria, never before — see "Only after the criteria:
is the row already live?".

### Reject criteria (close it, with a specific reason)

Each of these is concrete and checkable. **Run all six before anything
else** — before the liveness lookup, before any judgement about whether the
PR is "really" a pending decision. Nothing short-circuits them. If none
apply, the PR is a candidate and goes to escalate.

1. **Duplicate of another open submission** for the same skill. Match on
   the manifest's `Kilde`/`GitHub` URL, and on title slug independently:
   the same skill has been submitted from two different URLs before
   (`simply-launch` as both `Landsvig1/agent-skills` and
   `Landsvig1/vibetrends-dk/.agents/skills/`), so URL matching alone
   misses real duplicates. Keep exactly one. **Criterion 2 decides which
   one whenever a slug suffix is present: keep the unsuffixed original,
   close the suffixed resubmissions.** The suffix is not a version, it is
   a collision artefact, and the original is the row the catalog will key
   on. Only when no suffix distinguishes them do you choose on manifest
   quality, tie-breaking to the newest. Close the others naming the
   winner.
2. **Slug carries a collision suffix** (`-2`, `-3`, ...) while an earlier
   submission of the same title is still open or already live. The suffix
   is direct evidence of the resubmission loop, not a distinct entry.
3. **`description_da` is a copy of the English text.** `AGENTS.md` is
   explicit: that column is nullable, null means "not translated yet", and
   read paths fall back through `withEnglishFallback` in `src/lib/db.ts`.
   Copying English in permanently disables the fallback and makes a real
   translation indistinguishable from a copy. Migration
   `20260804000000_description_da_nullable.sql` had to clean this up
   across 118 rows once already.
4. **Source URL is dead, private, or does not contain what the manifest
   claims.** Actually fetch it, every time. On 2026-08-30 three entries
   that were already live and public (`dk-techblog`, `gsc-admin`,
   `bot-pr-review`) pointed at
   `github.com/Landsvig1/vibetrends-dk/tree/main/.agents/skills/<name>`,
   which 404s twice over: the repo slug is `Vibetrends.dk`, not
   `vibetrends-dk`, and even corrected, `.agents/skills/` holds only
   `supabase`, `supabase-postgres-best-practices` and
   `vibetrends-analytics`. The content loop had invented a
   plausible-looking path. A URL that looks right is not a URL that
   resolves, and a fabricated source link in a catalog whose whole pitch
   is curation is worse than a missing one. A 404 is a reject, not an
   escalation — unless the row is already live, in which case it is an
   escalation, because the bad data is already public and unpublishing it
   is Kasper's call. This criterion is now also enforced mechanically by
   `.github/workflows/submission-urls.yml`, so a PR failing it shows a red
   `Submission URLs` check; that check failing is sufficient evidence, but
   its passing does not mean the page contains what the manifest claims.
5. **The entry is useful only to Kasper.** The catalog is public. A skill
   hardcoded to his own hosts, repos, or bot names has no value to a
   reader. The submission of this very skill (PR #164) says so in its own
   Danish description: "Uden nøjagtig samme bot-navngivning og
   repo-opsætning giver skillen ingen værdi til andre end Kasper." Take
   that at face value and close it.
6. **Category is not one of `SKILL_CATEGORY_SLUGS`**, or the entry is
   filed under the wrong hub (a CLI tool submitted to `/skills`).

Close with a reason that names the specific criterion:

```bash
gh pr close <n> -R Landsvig1/Vibetrends.dk \
  --comment "Closing: <criterion>, <the concrete evidence>." --delete-branch
```

Do not delete the branch if the workflow owns it and closing alone
resolves the row; check `submission-resolve.yml` first. When in doubt,
close without `--delete-branch`, the sweep handles it.

### Only after the criteria: is the row already live?

**This check runs LAST, not first, and it is a permission to merge only for
a PR that has already passed every criterion above.**

It used to run first, and that ordering is what put three entries with
fabricated source URLs into the public catalog on 2026-08-30 (PRs #152,
#160, #161, merged in a 12-second scripted batch). All three were already
live, so the fast path fired and returned "merge" before criterion 4 —
the one that says fetch the source URL every time — ever ran. Their
`Kilde`/`GitHub` URLs 404'd twice over. The criterion was written down,
correct, and never reached. **An exception evaluated before the checks it
is an exception to is not a fast path, it is a bypass.**

Look the entry up in the live catalog by the manifest's **ID**, not its
title:

```bash
curl -s https://vibetrends.dk/api/skills | \
  python3 -c "import sys,json;d=json.load(sys.stdin);items=d if isinstance(d,list) else d.get('items',[]);print([i for i in items if i.get('id')=='<manifest id>'])"
```

If the ID is already live, the row was approved out of band with
`node scripts/review-queue.mjs approve`, which sets `review_state` without
touching the PR. The PR is then an orphaned record, not a pending
decision, and merging it writes the manifest into git history — the
curation ledger `submission-review.yml` describes and `PRODUCT.md` leans
on for the "curated, never scraped" claim. Closing would leave a
permanent gap in that ledger for an entry that is publicly live.

So, in order:

1. **The PR failed a reject criterion AND the row is already live.**
   Do not merge. Do not close. **Escalate.** This is the dangerous case
   and the one that actually happened: a live row with a dead source URL
   is not a ledger gap to be tidied up, it is bad data already visible to
   the public, and merging only records the badness in git. The DB row
   needs unpublishing, which is Kasper's call and not this routine's.
   Comment with the criterion it failed and the evidence, and list it
   under "Needs your call".
2. **The PR passed every criterion AND the row is already live.** Merge
   it. The DB is already decided; the merge only records it. This is not
   approving.
3. **The PR passed every criterion and the row is NOT live.** That is a
   normal approval candidate. Escalate per the standing policy — never
   merge.

**Never `--admin`, anywhere in this routine.** Submission PRs used to be
permanently `BLOCKED` with zero checks, because `submission-review.yml`
opened them with the default `GITHUB_TOKEN` and GitHub does not trigger
`pull_request` workflows on `GITHUB_TOKEN`-authored events — so `--admin`
was the only way to merge one. That was fixed at the source: the workflow
now opens PRs with the `SUBMISSION_PR_TOKEN` PAT, so `quality`, `e2e` and
the `Submission URLs` check all run and report normally. A submission PR
that is still blocked now is blocked by a check that genuinely ran, and
forcing past that is exactly what `--admin` must never be used for. If
you find yourself reaching for it, the answer is escalate.

Criterion 4 is also machinery now, not just a written rule:
`.github/workflows/submission-urls.yml` runs
`scripts/check-submission-urls.mjs` on every PR and fails when a
manifest's `Kilde`/`GitHub`/`Demo`/`Billede` URL does not resolve. Still
fetch the URL yourself when reviewing — the workflow checks that a URL
resolves, not that the page contains what the manifest claims, which is
the other half of the criterion.


### Escalate criteria (leave open, comment, list in the report)

A submission that survives all six checks is a real candidate. Comment on
it with what you verified, so Kasper can approve by clicking merge without
re-deriving anything:

- the source URL you fetched and that it matches the manifest,
- whether `description_da` is a real translation or correctly omitted,
- whether the entry duplicates anything already live in the catalog
  (check `/api/skills`, `/api/vibes`, `/api/cli`, `/api/mcp-servers`),
- one line on who the entry is useful to, other than Kasper.

Then list it under "Needs your call" in Step 4 with the PR number.

### Volume rule for Class A

If more than **10** submission PRs are open, do not review them all. Do the
duplicate and slug-suffix passes across the whole set first (those are
mechanical and resolve the bulk), then review at most 6 of the survivors
in detail and say plainly in the report how many were left untouched. A
submission backlog growing faster than review capacity is itself the
signal worth reporting, and it means the content loop's volume cap needs
lowering rather than the review going faster.

## Step 2: Class B, hot-ranking PRs

`scan-hot-skills.yml` opens a `hot-ranking/<year>-W<week>` PR weekly, and
`resolve-hot-ranking.yml` cleans up. In practice it opens **duplicates for
the same week**, every week: W33 produced #145, #146, #148 all closed
against #150 merged; W34 produced #153, #155 closed against #157; W35
produced #163 closed against #168.

Handle it as pure mechanical cleanup:

1. Group open hot-ranking PRs by their `YYYY-Www` week key.
2. Within a week, keep the newest and close the rest as superseded,
   naming the survivor.
3. The survivor merges only if CI is green and the diff touches nothing
   outside the ranking data files. Anything else routes to Class C's
   review pipeline.
4. **If this recurs again, say so in the report every single run.** Three
   consecutive weeks of duplicates is a workflow concurrency bug worth
   fixing at the source (`scan-hot-skills.yml` needs a `concurrency:` group
   the way `submission-review.yml` has one), not a permanent cleanup chore
   for this routine. Do not fix the workflow unasked, that is outside
   scope, but do not let it go unreported either.

## Step 3: Class C, coding-bot PRs

Dormant since late July 2026, but the machinery stays because the bots can
be pointed back at this repo at any time. Everything below is unchanged
hard-won behaviour; it cost real debugging to learn.

### Skeptical review lens

**Never take the bot's own claims as evidence.** PR description
"Impact"/"Measurement" sections, `.jules/*.md` journal entries, and
benchmark tests that only `console.log` a number are the bot grading its
own homework. `AGENTS.md` requires a performance benchmark to make a real
assertion (a timing threshold, or a render/call-count check that fails on
regression), not a bare log line. Re-derive whether a claimed fix is real
by reading the code.

**Check whether the complexity is warranted for what vibetrends actually
is**: a small community and showcase site. A caching layer with an
eviction policy can be flawless code and still be bloat. Ask whether it
would earn its keep at 10x current traffic. If not, that is **reject**,
not merge, regardless of passing tests.

**Two repo-specific traps from `AGENTS.md`:**
- `LanguageProvider`'s `t` is **not memoized**. Any `useCallback`/
  `React.memo` optimization depending on `t` being referentially stable is
  silently broken (confirmed on PR #73). Reject memoization PRs built on
  that assumption, or require the upstream instability be fixed first.
- The extract-to-`<XCard />`-then-`React.memo` pattern has been hand-rolled
  6+ times (`SkillCard`, `ProjectCard`, `AgentCard`, `ThreadCard`, blog and
  forum cards) with no shared wrapper ever built. A 7th copy is a reject;
  a shared memoized list-card wrapper is the only acceptable version.

**Watch for drift across PRs, not just within one.** Several new
caching/memoization patterns or an expanding abstraction surface across
recent runs is architecture rot. Report the pattern in Step 4 even when
each individual PR looks fine.

### Pre-flight checks, in order

**Fetch fresh first.** `git fetch origin main <pr-branch>` before any
`merge-base` or `diff`. A stale local `origin/main` computes the wrong
merge-base and reviews the wrong diff.

**Never create a worktree from a bare branch name.** Always reset from the
remote ref, and record the SHA:

```bash
git worktree add <workspace>/.worktrees/<name> -B <local-name> origin/<pr-branch>
git rev-parse origin/<pr-branch>   # this is the reviewed SHA
```

`-B` force-resets past any stale local branch from an earlier run. Without
it, a run can review an old commit and report it as current fact
(Vibetrends #60 was reported as missing a fix the bot had already pushed).
Before any comment, merge, or close, re-run `git ls-remote origin <branch>`
and confirm the SHA still matches. If it moved, redo the review.

**Journal-file conflict.** The bot creates `.jules/bolt.md` or
`.jules/sentinel.md` as a new file on every branch, so once one PR merges,
every other open PR shows `CONFLICTING` on an otherwise clean diff. Check
with `git merge-tree $(git merge-base origin/main <branch>) origin/main
<branch>`. If the journal is the *only* collision, resolve by
concatenating both versions chronologically. If something else collides
too, handle that on its own merits first, and if it does not resolve
cleanly either way, escalate rather than inventing a third version.

**Staleness.** `git log origin/main --oneline -- <changed files>` for
commits after the PR opened. If main already covers the same intent
differently, close as superseded naming the commit.

**Main-drift silent-deletion check, mandatory for every PR regardless of
size.** A PR can merge with zero textual conflicts and still delete code
main added after the fork point. Vibetrends #60 would have cleanly merged
and silently deleted an entire `resolveAgentWriteLimit` rate limiter, a
real security regression.

1. `BASE=$(git merge-base origin/main origin/<pr-branch>)`
2. `git diff --name-only $BASE origin/main -- <PR's touched files>`. Empty
   means clear, move on.
3. For each such file, list top-level symbols main **added** since `$BASE`.
4. In a scratch worktree off `origin/main`, `git merge origin/<branch>
   --no-commit --no-ff`, then confirm every symbol from step 3 is still
   present by name. Discard the worktree either way, this is a probe.
5. Any missing symbol means the PR is **never auto-mergeable as-is**. Fix
   deliberately (merge main in, or cherry-pick the symbol back), re-verify,
   and only then proceed. If reconciling needs logic neither side proposed,
   escalate.

**Do not auto-rebase bot PRs** as blanket preprocessing. It rewrites the
bot's commits and invalidates every reviewed-SHA citation. Only touch a
branch's history for a concrete named problem.

**Lockfile drift.** This repo uses **npm** (`package-lock.json`). Never
allow `pnpm-lock.yaml`; `AGENTS.md` records it being stripped from or
causing rejection of at least five PRs, most recently #80. Strip it
unconditionally: `git rm --cached pnpm-lock.yaml && rm -f pnpm-lock.yaml`,
commit `chore: drop stray pnpm-lock.yaml (repo uses npm)`, push. Same
treatment for a `package-lock.json` regen when `package.json` itself did
not change; revert to main's version and prove it with
`npm ci`.

**Generated-artifact drift.** `playwright-report/`, `test-results/`,
`coverage/`, `*.log` dev-server output. If the PR *deletes* one, keep the
cleanup. If it *adds* one, skim it for anything secret-shaped first (a
dev-server log is exactly the kind of file that leaks a token), then strip
it the same way. If `.gitignore` lacks the pattern, note it in Step 4 but
do not edit `.gitignore` unasked.

**Compute size excluding that noise** before applying any heuristic:
`git diff ... -- . ':!package-lock.json' ':!pnpm-lock.yaml' ':!.jules'
':!playwright-report' ':!test-results' ':!*.log'`. A real PR once read as
9,162 lines raw and 193 lines clean.

**Volume governor.** If more than 5 Class C PRs are open, run the
mechanical cleanup on all of them but cap **actual merges at 3**. Fill
those slots with tiny/safe candidates before full-review candidates.
Past the cap, do a lighter read so the escalation comment is still
informed, and say "capped this run, not given the full review pass".

### Classification and outcomes

**Tiny/safe** requires all of: main-drift check clear; nothing on the
deny-list; net diff under ~150 lines and 5 files; CI green (or the only
red check fails identically on an unrelated open PR, which is the only
basis for calling something flaky); no merge conflicts.

**Deny-list, always routes to full review regardless of size:**
`supabase/migrations/**`; any path containing `auth`, `rate-limit`,
`security`, `payment`, `webhook`, or `admin`; `.github/workflows/**`; any
dependency version bump or lockfile change beyond the cleanup case; any
`**/api/**` file whose diff touches an auth check, permission check, or
input-validation boundary.

**A brand-new dependency always escalates**, even with a clean review. A
version bump is maintenance; a new dependency is a standing decision about
supply-chain surface and maintenance burden. That is Kasper's call.

Even for tiny/safe, read every hunk and the full enclosing function, and
apply the skeptical lens. Small and correct is not the same as warranted.

For full review, work in the worktree and invoke the `code-review` skill at
medium effort, then:

- **Bloat** (complexity unjustified at this project's scale, or justified
  only by a bot-authored claim): **reject**, whatever code-review found.
- **Sketchy but not clearly bloat** (clean review, but touches a
  foundational module, or the value tradeoff is genuinely close):
  **escalate**, never auto-merge.
- **Zero surviving findings and proportionate**: merge.
- **All findings CONFIRMED and none deny-listed**: fix them mirroring the
  repo's conventions, add a regression test per fix, run typecheck plus the
  affected tests, commit, push, then re-run code-review **once**. Clean
  means merge. Still dirty means stop, leave the fix pushed, report only.
  Do not loop.
- **Any finding only PLAUSIBLE, or touching a deny-listed concern**: never
  auto-fix-and-merge. Post findings and stop.
- **Circuit breaker**: if typecheck, lint, or tests fail after a fix,
  abort, discard the local fix commit, report what broke.

Always `git worktree remove --force` when done. Note it does not delete the
local branch, which is the residue behind the staleness bug. Periodically
`git branch -D` the leftovers for closed PRs.

## Step 4: reporting

**Language contract.** Every finding about what a PR does or does not do
must cite the reviewed SHA: "as of `a1b2c3d`, this branch builds its own
in-memory rate limiter", never a bare "this PR builds...". If you cannot
cite the SHA you verified against, you have not verified it.

**Per-PR comment** on everything touched, saying what was done and why.
For a closed submission, name the criterion and the evidence. For an
escalated submission, give Kasper the four verification points from Step 1
so merging is a one-click decision.

**Cross-repo summary**: append a dated section to
`docs/reports/pr-review-log.md` (on the VPS: `/home/administrator/docs/reports/`).
Report per class, not as one undifferentiated list:

```markdown
## 2026-08-31

### Needs your call
- #161 Submission: dk-techblog. Source verified, description_da is a real
  translation, nothing equivalent live. Merge to approve.

### Submissions
- 9 open at start, 5 closed (3 duplicate resubmissions of bot-pr-review,
  1 slug-suffix collision, 1 useful-only-to-Kasper), 1 escalated above,
  3 still queued.

### Hot ranking
- 0 open. (W35 duplicate pattern: third consecutive week, worth a
  concurrency group on scan-hot-skills.yml.)

### Coding bot
- 0 open. Dormant since late July.

### Kasper's own
- #167, #166 listed, untouched.

### Health
- Circuit breaker trips: none.
- Drift watch: nothing new.
```

Never report "nothing to do" without listing the open PR count by class.
A zero that is not broken down is exactly how the submission backlog went
unnoticed for weeks. If a class has 0 open PRs, print the 0.

## Parked: the other two repos

Dropped from scope 2026-08-30, restore by re-adding a table row in Step 0
and re-reading this section:

- **koalafilm.dk** (`projects/koalafilm`, `Landsvig1/Koalafilm`), npm.
  Reference case for the fake benchmark: PR #8, merged 2026-07-12,
  `console.log`ged "137x faster!" with no assertion and a comment claiming
  the lack of assertion was deliberate. Had a run of caching PRs (#6 db
  reads, #8 image URLs) worth watching for drift.
- **aiauto.dk** (`projects/AiAuto`, `Landsvig1/AiAuto`), **pnpm**, so the
  lockfile rule inverts there. PR #5 (2026-07-12) regenerated
  `pnpm-lock.yaml` dropping hundreds of transitive entries with
  `package.json` untouched; PR #4 committed a 24k-line
  `playwright-report/index.html` that swamped a real 14-line diff.

Both were on `⚡ Bolt:`/`🛡️ Sentinel:` PRs with no activity since late July.

---
name: bot-pr-review
description: >
  Daily triage of Kasper's coding bot's (Jules/Bolt/Sentinel) PRs across
  Koalafilm, Vibetrends.dk, and AiAuto — surfaces duplicate/stale bot PRs,
  merges the ones that are genuinely tiny and safe after a light diff read,
  runs the full code-review skill (with conditional auto-fix + re-review +
  merge) on anything larger or riskier, and rejects or escalates PRs that
  are technically fine but unwarranted bloat or a judgment call. Make sure
  to trigger this whenever Kasper asks to check/review the bot's PRs, clean
  up the PR backlog/merge queue, wants to know what Jules/Bolt/Sentinel has
  been up to, asks about open PRs across his projects, or wants a status
  check on any of the three repos' pull requests — even if he doesn't name
  the bot or this skill explicitly. Also runs automatically every morning
  via the bot-pr-review-daily scheduled task. Never touches PRs authored by
  Kasper himself (see the bot-identification rule below — author/is_bot is
  NOT a reliable signal here).
compatibility: >
  Requires an authenticated `gh` CLI with merge/close permissions on all
  three repos, git with worktree support, and each repo's own toolchain
  (npm for Koalafilm/Vibetrends.dk, pnpm for AiAuto) installed locally for
  typecheck/lint/test verification before merging.
---

# Bot PR review

Kasper runs a coding bot (Jules/Bolt/Sentinel-style tool) that opens PRs
daily against his 3 live-data projects. It authenticates through Kasper's
own GitHub identity, so `author.login`/`is_bot` on the PR is useless for
telling its PRs apart from Kasper's own — every PR shows `Landsvig1`. Bot
PRs are identified only by **title prefix** (`⚡ Bolt:` / `🛡️ Sentinel:`) or
**branch name** (`jules-`, `bolt-`/`bolt/`, `sentinel-` followed by a long
numeric ID). Anything that doesn't match either pattern is a human (Kasper's
own) PR — report it in the overview but never act on it.

**Hard rule**: only take actions this skill explicitly describes below
(comment, close-as-duplicate/superseded, close-as-bloat, escalate-for-
approval, merge, or push a fix commit to a bot's own PR branch). Never
touch Kasper's own PRs, never force-push, never apply a fix to something
outside the deny-list decision tree without stopping to report instead.

## Skeptical review lens — read before Step 2 or 3

Jules/Bolt/Sentinel run on a weaker model than whatever's running this
skill. That has two concrete consequences for how you review, not just
what you check:

**Never take the bot's own claims as evidence.** PR descriptions'
"Impact"/"Measurement" sections, `.jules/*.md` journal entries, and
benchmark tests that only `console.log` a number are the bot grading its
own homework — written by the same model that wrote the code. A test named
"performance benchmark" with no real assertion (Koalafilm #8, merged
2026-07-12, is the reference case: `console.log` a "137x faster!" line,
comment says logging-not-asserting is deliberate "to prevent flaky
pipeline failures") is not verification, it's marketing copy that happens
to live in a `.test.ts` file. Independently re-derive whether a claimed
fix/optimization is real by reading the code and reasoning about it (or
actually re-measuring) — never cite the PR's own narration as the reason
something is safe.

**Check whether the complexity is warranted for what this project
actually is**, not just whether it's technically correct. Read the
target repo's CLAUDE.md/AGENTS.md first — koalafilm.dk, vibetrends.dk, and
aiauto.dk are all small solo-founder marketing/community sites, not
high-traffic systems. A caching layer with an eviction policy, a new
abstraction, or a memoization scheme can be flawless code and still be
bloat if the project will never see the request volume that would make it
pay for itself. Ask: would this complexity earn its keep at 10x current
traffic? If the honest answer is "no, this solves a problem the project
doesn't have," it's bloat regardless of whether tests pass — route it to
**reject**, not merge (see Step 2/3 below).

**Watch for drift across PRs, not just within one.** A single
over-engineered PR is tolerable; ten of them over a month is architecture
rot an unattended pipeline can inflict without anyone noticing day-to-day.
If a repo has taken on several new caching/memoization patterns, growing
`.jules/*.md` journals, or expanding abstraction surface across recent
runs, say so in the Step 4 summary even if each individual PR this run
looks fine in isolation — that pattern itself is worth Kasper seeing.

## The three repos

| Project | Local path | GitHub remote |
|---|---|---|
| koalafilm.dk | `projects/koalafilm` | `Landsvig1/Koalafilm` |
| vibetrends.dk | `projects/vibetrends-dk` | `Landsvig1/Vibetrends.dk` |
| aiauto.dk | `projects/AiAuto` | `Landsvig1/AiAuto` |

Paths are relative to the Claude Cowork workspace root
(`~/Documents/Claude Cowork/`). If a new project starts getting bot PRs,
add it to this table rather than hard-coding a 4th special case anywhere
below.

## Step 1 — Overview

For each repo:

```bash
gh pr list -R Landsvig1/<Repo> --state open --json number,title,headRefName,createdAt,files
```

Classify each PR as **bot** (title starts `⚡ Bolt:` or `🛡️ Sentinel:`, OR
`headRefName` matches `^(jules|bolt|sentinel)[-/]`) or **human** (everything
else). List human PRs in the summary and stop there for those — out of
scope.

For the bot PRs, run these checks **before** any tiny/safe-vs-needs-review
classification:

**Duplicate/overlap check** — for any two open bot PRs in the same repo
whose `files` sets overlap, don't classify either yet. Pull both diffs
(`gh pr diff <n> -R <repo>`), read them, and decide: if one is a strict
superset/cleaner version of the other (more correct error handling, no
unrelated scope creep like a stray lockfile), keep it and close the other
with `gh pr close <n> --comment "Closing as duplicate of #<winner> — <one
concrete reason>" --delete-branch`. If genuinely unclear, leave both open
and note it in the report instead of guessing.

**Journal-file conflict** — the bot writes to `.jules/bolt.md` or
`.jules/sentinel.md` as a "new file" on every branch, so once any one PR
touching that file merges, every other still-open PR that also "creates"
it will show `mergeStateStatus: CONFLICTING` on an otherwise-clean diff.
This is not a real conflict — before concluding a PR is genuinely
conflicting, check whether the only colliding file is a `.jules/*.md`
journal: `git merge-tree $(git merge-base origin/main <branch>) origin/main
<branch>` (read-only, no working-tree changes) to see exactly what
conflicts. If it's just the journal, resolve by concatenating both
versions' entries (chronological order) once you're in Step 2/3's worktree
— don't let this trigger a staleness/duplicate judgment call on its own.

If the journal isn't the *only* thing conflicting — some other file
collides too — don't force the journal's easy resolution onto the whole
PR. Handle the non-journal conflict on its own merits first (staleness
check below, or a straight merge-conflict read if neither PR's change
strictly supersedes the other), and only fall back to the journal's
concatenation trick for that one file once the real conflict has its own
answer. A sandbox test run (2026-07-12) hit exactly this: a PR's branch
predated both the journal's first commit *and* an unrelated bugfix that
landed on main afterward touching the same function the PR itself
modified — two independent reasons to conflict, tangled in one diff. If
the non-journal conflict doesn't resolve cleanly either way (neither
version is a strict improvement, or reconciling them means writing new
code neither PR proposed), that unresolvable tangle is itself a reason to
escalate rather than merge — don't invent a third version of the fix
yourself to force a merge through.

**Staleness check** — for each remaining bot PR, check whether main has
independently solved the same problem since the PR's branch point:
`git -C <path> log origin/main --oneline -- <changed files>` for commits
after the PR opened. If the file(s) the PR touches have a materially
different implementation on main already covering the same intent, don't
force a merge-conflict resolution — close as superseded with a comment
naming the commit that already covers it, same as Koalafilm #2.

**Main-drift silent-deletion check — mandatory for every remaining PR,
regardless of size or how clean the diff looks.** A bot PR can merge with
zero textual conflicts and still silently delete code that main added
independently after the PR's fork point, if the PR's diff happens to
rewrite the region main's new code lives in without git treating it as a
conflicting hunk. This is not a hypothetical: Vibetrends.dk #60 (a DoS-fix
PR) would have cleanly merged and silently deleted an entire
`resolveAgentWriteLimit` cost-control rate-limiter that main had shipped
in the same file after the PR branched — a real security regression, and
the original review pass never ran a check that would have caught it.

For every PR still standing after the dedup/staleness checks above, before
Step 2's classification or Step 3's verdict:

1. `git fetch origin main <pr-branch>` (fresh, per the rule above).
2. `BASE=$(git merge-base origin/main origin/<pr-branch>)`.
3. List files main changed since the fork point that this PR also
   touches: `git diff --name-only $BASE origin/main -- <PR's touched files>`.
   If empty, this check is clear — main hasn't touched anything this PR
   also touches, skip to the next PR.
4. For each such file, list top-level symbols (functions, exported
   consts, classes) that main **added** since `$BASE` — grep the
   `git diff $BASE origin/main -- <file>` output for added lines matching
   a top-level declaration (e.g. `^\+\s*(export\s+)?(async\s+)?function
   \w+|^\+\s*export\s+const\s+\w+\s*=|^\+\s*class\s+\w+`, adapted to the
   file's language).
5. Simulate the merge: in a scratch worktree off current `origin/main`,
   `git merge origin/<pr-branch> --no-commit --no-ff`. Whether or not git
   reports a conflict, open the resulting file(s) and confirm every symbol
   found in step 4 is still present by name. Discard the scratch worktree
   either way (`git merge --abort` or just remove the worktree) — this is
   a probe, not a real merge.
6. If any symbol is missing from the simulated result: this PR is **never
   auto-mergeable as-is**, no matter what Step 2's size heuristic or
   Step 3's code-review pass conclude. Treat it the same as an
   unresolvable conflict tangle (see the journal-conflict section above):
   merge main into the PR branch (or cherry-pick the missing symbol back
   in) as a deliberate fix-commit, re-run the affected checks, and only
   proceed to merge if the fix is clean and verified — same discipline as
   Step 3's "fix them... commit, push, re-review" flow. If reconciling
   requires writing logic neither side proposed, escalate instead of
   guessing (same rule as the unresolvable-tangle case).

**Do not auto-rebase bot PRs as a blanket preprocessing step**, even
though this check makes main-drift a recurring problem for PRs that sit
open for days. Rebasing rewrites the bot's own commits — if the bot pushes
another commit to the same branch after an unprompted rebase, the next
push can conflict with or duplicate work in ways nobody is watching for,
and the rewritten SHAs stop matching what the reviewed-SHA citation
(above) or the bot's own PR history refers to. Only touch a PR branch's
history when this check (or Step 3's review) finds a concrete, named
problem to fix — never rebase speculatively just because main has moved.

**Lockfile drift** — if a bot PR's diff adds `pnpm-lock.yaml` or
`yarn.lock` in a repo whose own `package.json`/existing lockfile says
otherwise (check `ls package-lock.json bun.lockb yarn.lock pnpm-lock.yaml`
in the repo before this PR's branch), strip it unconditionally: clone/fetch
the PR branch, `git rm --cached <lockfile> && rm -f <lockfile>`, commit
`chore: drop stray <lockfile> (repo uses <real pm>)`, push to the PR
branch. This is pure cleanup — do it regardless of what tier the PR ends
up in. The same applies even when the lockfile matches the repo's real
package manager (e.g. a `pnpm-lock.yaml` regen in a pnpm repo) if
`package.json` itself didn't change — a lockfile can silently drop real
dependency entries with nothing to justify it (AiAuto #5, 2026-07-12: the
regen removed hundreds of transitive entries, `package.json` untouched).
Revert to main's version and confirm with `<pm> install --frozen-lockfile`
that it still installs clean — that's the proof nothing in the PR actually
needed the regen, not just an assumption.

**Generated-artifact drift** — bot PRs periodically commit build/test
output that was never meant to be tracked: `playwright-report/`,
`test-results/`, `*.log` dev-server output, `coverage/`. Hit twice on
2026-07-12 (AiAuto #4's `playwright-report/index.html` at 24k lines,
completely swamping the PR's real 14-line diff; AiAuto #5's
`next_start.log`). Handle case by case, not mechanically like the
lockfile: if the PR is *deleting* a previously-committed artifact, that's
a welcome cleanup, keep it. If it's *adding/modifying* one, strip it the
same way as a stray lockfile (`git rm --cached`, commit, push) — but
first skim the file for anything secret-shaped (API keys, tokens,
connection strings, env var dumps) before deciding to keep or discard it;
a dev-server log is exactly the kind of file that can leak something. If
a repo has no `.gitignore` entry for the pattern that just showed up,
note it in Step 4 — worth Kasper adding one so this stops recurring, but
don't edit `.gitignore` yourself unasked, that's outside this skill's
scope.

**Compute PR size for Step 2's classification excluding known noise** —
lockfiles, `.jules/*.md` journals, and generated artifacts inflate a raw
`gh pr diff | wc -l` by orders of magnitude and will wrongly push a
genuinely tiny change into needs-review, or worse, mask how large the
*real* change actually is once they're stripped. AiAuto #5 read as 9,162
lines raw; 193 lines once the noise above was removed. Always diff/count
with those paths excluded (`git diff ... -- . ':!pnpm-lock.yaml'
':!package-lock.json' ':!.jules' ':!playwright-report' ':!test-results'
':!*.log'`) before applying the ≤150-lines/≤5-files heuristic.

**Fetch `origin/main` fresh before computing any merge-base or diff** in
a worktree — a worktree created from a repo whose local `origin/main` ref
is stale will compute the wrong merge-base and review the wrong diff
(extra unrelated files, or a version of the PR's own changes that doesn't
match what's actually on the remote branch). AiAuto #5 hit this: a stale
local main showed 20 changed files where GitHub's own count was 10. Run
`git fetch origin main <pr-branch>` before any `git merge-base`/`git
diff` command, every time, not just when something looks off.

**Never create a worktree from a bare local branch name — always reset it
from the freshly-fetched remote ref, and record the exact SHA you
reviewed.** This skill runs headless, often as a fresh session per
invocation (a same-day "second opinion" re-run is a fresh process with no
memory of the last one). If the bot pushes a new commit to a PR branch
between two runs, and a run creates its worktree with plain `git worktree
add <path> <branch>`, git will happily reuse a stale local branch ref of
that name from a previous run instead of the branch's current tip —
producing a review of an old commit that gets reported as current fact.
(This happened for real: Vibetrends.dk #60 was reviewed against an early
commit that still had an in-memory rate limiter; the bot's own next
commit on the same branch had already fixed it to use `checkRateLimit()`,
but the report said the fix was "missing" and needed Kasper's attention —
because the review never looked at the branch's actual current HEAD.)

Fix: after `git fetch origin main <pr-branch>`, always create/reset the
worktree branch directly from the remote-tracking ref, never from a bare
branch name:

```bash
git worktree add <workspace>/.worktrees/<name> -B <local-branch-name> origin/<pr-branch>
```

The `-B` force-resets `<local-branch-name>` to match `origin/<pr-branch>`
exactly, even if a stale local branch of that name exists from an earlier
run. Immediately after, run `git rev-parse origin/<pr-branch>` and record
the short SHA — this is the **reviewed SHA** for this PR, and every
finding in Step 4 about this PR must cite it (see Step 4's language
contract below). Right before posting any comment or taking any merge/
close action on a PR, re-run `git ls-remote origin <pr-branch>` and
confirm the SHA still matches the reviewed SHA — if it doesn't (the bot
pushed again mid-review), the review is stale: re-fetch and redo the
review for that PR rather than acting on outdated findings.

**Volume governor** — after the checks above, count how many bot PRs are
left across all 3 repos combined. This routine has no mechanism to notice
"the bot had an unusually active/erratic day" other than counting — an
unattended pipeline that just grinds through however many PRs show up,
with no sense of "this is a lot," is exactly the derailing risk automation
introduces. If the combined count exceeds **8 in a single run**, or any
one repo alone has more than **5**, don't process them all normally:

- Step 1's cleanup (dedup/staleness/lockfile/artifacts) still runs on
  everything — it's mechanical and safe regardless of volume, and a
  sandbox test run (2026-07-12, 9 PRs in one repo) confirmed it resolves
  real PRs (duplicates, superseded, cleanups) before the cap ever matters.
- The cap applies to the **merge action specifically**, not to whether a
  PR gets looked at. A PR that Step 1 already resolves (duplicate,
  superseded) or that the deny-list/skeptical lens already rejects
  (bloat) doesn't consume a merge slot — those are "no" regardless of
  volume, not "capped." Reject-as-bloat and close-as-duplicate/superseded
  keep working normally at any volume.
- For PRs still standing after that, cap **actual merges at 3 per repo**
  this run. Fill those 3 slots with Step 2's tiny/safe candidates before
  Step 3's needs-review candidates — a tiny/safe PR takes a light diff
  read to clear, a needs-review PR takes a full code-review worktree
  cycle, and spending that cycle on a PR that's going to be escalated
  regardless of what it finds (because the cap is already spent) is pure
  waste. Once the merge cap is spent, don't run Step 3's full code-review
  pipeline on the remaining needs-review PRs either — do a lighter read
  (like Step 2's, diff plus the enclosing function, not the 8-agent
  fan-out) so the escalate comment is still informed, and say so: "capped
  this run, not given the full review pass."
- Auto-escalate everything past the cap ("high PR volume this run —
  capped at 3 automatic merges for koalafilm.dk, N PRs left for your
  review, full review not run on M of them due to the cap" in Step 4),
  and say so prominently in the summary. A sudden spike is itself a
  signal worth Kasper's attention, independent of whether each individual
  PR looks fine.

## Step 2 — Classify remaining bot PRs

A PR is **tiny/safe** only if ALL of:

- Passes the main-drift silent-deletion check above — no symbol main
  added since the fork point is missing from the simulated merge result.
  This gates tiny/safe regardless of how small or clean the diff itself
  looks; a 5-line PR that silently deletes a security control on merge is
  not safe.
- Diff touches nothing on the deny-list below.
- Net diff ≤ ~150 changed lines and ≤ 5 files (a triage heuristic, not
  proof of safety by itself — still read the diff, see below).
- CI is green, OR the only failing check is a test that ALSO currently
  fails **identically** (same test name/locator, visible in the failure
  log) on another open PR in the same repo that doesn't touch related
  code. That cross-check is the only basis for calling something "known
  flaky" — one red run alone is not enough, go find the second data point
  or treat it as real.
- No merge conflicts against the base branch (`gh pr view <n> --json
  mergeable,mergeStateStatus`).

**Deny-list — always routes to Step 3 (needs-review) regardless of size:**
- `supabase/migrations/**`
- any path/filename containing `auth`, `rate-limit`, `security`, `payment`,
  `webhook`, or `admin`
- `.github/workflows/**`, any `package.json` dependency version bump, any
  lockfile change beyond the Step 1 cleanup case
- any `**/api/**` file where the diff touches an auth check, permission
  check, or input-validation boundary — grep the diff for `auth`,
  `permission`, `RLS`, `validate`, `sanitize` as a fast pre-filter, then
  read the actual hunk before deciding

**A brand-new dependency (a `package.json` `dependencies`/
`devDependencies` key that didn't exist before, not just a version bump
on an existing one) always routes to Step 3's **escalate** outcome, even
if code-review finds nothing wrong with how it's used.** A version bump
is routine maintenance; a new dependency is a standing decision about
what this project is now willing to depend on — supply-chain surface,
bundle size, and a maintenance commitment that outlives the PR that added
it. That's Kasper's call, not something to wave through because the
import compiles and tests pass.

**Even for tiny/safe candidates, read the diff before merging.** This is a
lighter pass than Step 3's full code-review — no multi-agent fan-out — just
what worked tonight: read every hunk, Read the full enclosing function (not
just the diff context) for anything non-trivial, confirm the change does
what the title claims, and check it isn't reintroducing something already
fixed elsewhere in the repo's history. If anything reads oddly, downgrade
to Step 3 instead of merging on a hunch.

**Apply the skeptical review lens here too, before merging on "it's small
and correct" alone.** Small and correct is not the same as warranted. If
the diff adds a new cache/memoization/abstraction whose only justification
is a bot-authored performance claim, or grows the codebase's surface
(new files, new dependency, new pattern) without a correspondingly clear
improvement to correctness or user-visible behavior — that's **reject**,
not merge, even at 20 lines:
`gh pr close <n> --comment "Closing — adds <specific complexity> whose
justification (<the bot's claim>) doesn't hold up for this project's
actual scale/CLAUDE.md context. <one-line specific reason>." --delete-branch`

If the change is small, correct, and the complexity is genuinely
proportionate to a real problem (e.g. fixing a real bug, a real
user-visible perf issue, a real security gap) — that's a normal merge.
If you're genuinely unsure which side of that line it's on, don't guess:
route it to Step 3 and let the fuller review (including the escalation
option there) sort it out.

If it survives the deny-list, size check, CI check, the diff read, and the
skeptical lens: `gh pr merge <n> -R <repo> --merge --delete-branch`. If CI
is red only on the corroborated-flaky test, add `--admin` to bypass the
branch-protection gate for that one check, and say so explicitly in the PR
comment (Step 4).

## Step 3 — Needs-review PRs

The main-drift silent-deletion check above must already be clear (or its
fix-commit already applied and verified) before any outcome below is
reached — a PR that fails that check is never "zero findings, merge
directly" regardless of what code-review finds in this step.

Check out the PR branch in an isolated git worktree — `git worktree add
<workspace>/.worktrees/<name> <branch>` in the target repo, NOT the repo's
own local checkout under `projects/`, and NOT `EnterWorktree` (that tool
creates worktrees relative to whatever repo the session's own cwd is in,
which in this multi-repo workspace is the Cowork root, not the nested
project repo — it will silently worktree the wrong repo). Running plain
`git checkout -b <branch>` directly in `projects/<repo>` switches Kasper's
own local checkout to that branch — happened once already, caught
immediately because nothing was lost (already-pushed commits), but it's
exactly the kind of thing an unattended run has no one around to catch.
Always `git worktree add`, always under `<workspace>/.worktrees/`, always
`git worktree remove --force` when done (or `--force
--discard-changes` isn't needed if the branch's own work was already
pushed).

Invoke the `code-review` skill at medium effort against the PR's diff
(same 8-angle finder + 1-vote verify pipeline used on Vibetrends #54). Also
apply the skeptical review lens from above as you read the diff — the
code-review skill hunts for bugs and cleanup opportunities, it does not by
itself ask "is this complexity warranted for what this project is." That
judgment is yours to make here, on top of whatever the code-review pass
finds.

- **The change is bloat**: adds complexity (new cache/abstraction/
  dependency/pattern) whose justification doesn't hold up against the
  project's actual scale, or whose only "proof" is a bot-authored
  claim/unfalsifiable benchmark, or expands the codebase's surface without
  a clear correctness/UX payoff → **reject**, regardless of what
  code-review finds. Close with a specific, concrete reason (name the
  complexity, name why it doesn't pay for itself here):
  `gh pr close <n> --comment "..." --delete-branch`. This can apply even
  when the code itself has zero bugs — "correct" and "worth merging" are
  different questions.
- **The change is sketchy but not clearly bloat**: passes code-review
  (zero CONFIRMED findings) and isn't obviously unwarranted, but something
  still gives pause — it touches a shared/foundational module in a way
  future PRs will build on, it expands scope beyond what the title/fix
  claims, or the complexity/value tradeoff is genuinely close and you're
  not confident which way it should go even after the lens above →
  **escalate**. Never auto-merge. Comment on the PR naming the specific
  tension (what's good about it, what gives pause — be concrete, not
  "this seems risky"), leave it open, and flag it prominently in Step 4's
  summary under its own heading, not buried in the general list. This is
  the tier for "tests pass but Kasper should look at this himself before
  it ships" — distinct from needs-review's other outcomes, which the
  routine resolves on its own.
- **Zero findings survive verification, and the change is proportionate**
  (real bug fix, real user-visible perf/security fix, complexity matches
  the problem) → merge directly.
- **Findings survive, all CONFIRMED, none touch a deny-listed concern**
  (auth/migrations/payment/rate-limit/security/admin/webhook, same list as
  Step 2) → fix them: mirror the existing code's own conventions, add or
  extend a regression test for each fix, run typecheck + the affected test
  files locally in the worktree. If that all passes, commit, push to the
  PR branch, then **re-run the same code-review pass once more** against
  the updated diff.
  - Comes back clean → merge.
  - Still has surviving findings → stop. Do not loop. Fall back to
    report-only for this PR this run (Step 4), leaving the fix commit
    pushed (it's still an improvement) but the PR unmerged.
- **Any surviving finding is only PLAUSIBLE (not CONFIRMED), or touches a
  deny-listed concern even if it looks fixable** → never auto-fix-and-merge.
  Post the findings as a PR comment and stop. A routine running unattended
  at 4am does not get to make the auth/migrations/payment call Kasper made
  out loud tonight — that always waits for him.
- **Circuit breaker**: if typecheck, lint, or the affected tests fail after
  applying a fix, abort — discard the local fix commit (don't push a
  broken one), and fall back to report-only with a note explaining what
  broke.

Always `ExitWorktree` when done with a PR, whether merged or not. Note
`git worktree remove` deletes the worktree directory but does **not**
delete the local branch it was checked out from — that local branch ref
persists in the shared clone and is exactly the residue that caused the
staleness bug above. It's harmless as long as every future run sources
fresh from `origin/<pr-branch>` rather than reusing a branch by name, but
it does accumulate. Periodically (e.g. monthly, or whenever a run
notices several), delete merged/closed PRs' leftover local branches:
`git branch -D <name>` for branches whose PR is no longer open.

## Step 4 — Reporting

**Language contract — no finding is a claim about "this PR," it's a claim
about a specific commit.** Every finding that describes what a PR does or
doesn't do (contains a bug, is missing a fix, uses pattern X) must cite
the reviewed SHA recorded when its worktree was created (see the
fetch-fresh rule above): "as of `<short-sha>`, this branch builds its own
in-memory rate limiter" — not a bare "this PR builds its own in-memory
rate limiter." This is what makes a finding falsifiable and re-checkable
in a follow-up session, and it's what would have caught the Vibetrends.dk
#60 staleness bug immediately (the cited SHA would have visibly predated
the bot's fix commit). Never write "left for you" or any other
present-tense claim about a PR's state without a SHA attached — if you
can't cite the SHA you verified against, you haven't actually verified it
against the PR's current state, so re-fetch and check before reporting.

**Per-PR comment** — on every bot PR touched this run (merged, closed,
fix-pushed, or left with findings), comment with what was done and why:
- Merged: "Merged — [tiny/safe: diff read clean, CI green] or [code-review:
  zero findings survived / N findings fixed and re-reviewed clean]."
- Closed as duplicate/superseded: name the PR/commit it lost to.
- Closed as bloat: name the specific complexity added and why it doesn't
  pay for itself for this project (cite the CLAUDE.md context, not a
  vague "seems unnecessary").
- Escalated: name the specific tension — what's good about it, what gives
  pause. Kasper is the audience for this comment, not a log entry.
- Left open with findings: list them (file, line, one-line summary) so
  Kasper can act without re-deriving them.
- Fix pushed but not merged: what was fixed, why it's still waiting.

**Cross-repo summary** — append a dated section to
`docs/reports/pr-review-log.md` (create `docs/reports/` if it doesn't
exist) in the Claude Cowork workspace root. Give escalated PRs their own
heading so they can't be missed by skimming past a long "merged" list:

```markdown
## 2026-07-13

### Needs your call
- Vibetrends.dk #61 — adds a Redis-backed session cache. Tests pass, no
  bugs found, but it's a new infra dependency for a project with no
  existing cache layer — your call whether that's worth taking on.

### Everything else
- Koalafilm: 1 bot PR seen, #8 merged (tiny/safe).
- Vibetrends.dk: 2 bot PRs seen (#61 above, #59 closed as duplicate).
- AiAuto: 1 bot PR seen, #12 closed as bloat (memoized a pure function
  called once per page load — no realistic scale where this pays for
  itself; benchmark test only console.logged a number, no assertion).
- Circuit breaker trips: none.
- Drift watch: Koalafilm has now had 3 bot PRs in 2 weeks each adding a
  new caching layer (#6 db reads, #8 image URLs, this run's #12 rejected)
  — worth a look at whether the bot's default posture needs steering away
  from "cache everything" for this repo specifically.
```

Omit the "Needs your call" heading entirely on runs with nothing escalated
— don't print an empty section. Keep entries terse — this is a scan-the-
tail log, not a report. If a run finds nothing to do in a repo, still note
"0 bot PRs" rather than omitting the repo, so a gap doesn't read as "the
routine didn't run."

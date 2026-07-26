---
name: hermes-ops
description: >
  Operate, optimize, debug, and eventually migrate Kasper's Hermes (Neo)
  agent and its revenue pipeline on the VPS. Use for ANY Hermes work:
  "optimize hermes", health checks, the nightly revenue scan, signal
  fetchers, kanban board / triage, HUD, cron, prompt changes, new signal
  sources, or moving Hermes to a new host. Triggers on mentions of hermes,
  neo, the revenue board/pipeline/digest, the Hermes VPS, or /hermes-ops.
  Do NOT use for the unrelated Greek-mythology sense of Hermes.
---

# Hermes ops

Recurring terminal sessions where Kasper + an agent improve Hermes together.
The goal across sessions: Hermes reaches ~90% task completion autonomously,
gets adjusted to Kasper's use cases, and survives two future migrations
(next VPS, later Kasper's local PC).

## Ground truth files (read before working)

All in the workspace root `/Users/kasperlandsvig/Documents/Claude Cowork/`:

- `Agents/Hermes/host.env` — WHERE Hermes lives (host, user, paths, HUD
  URL). The only file allowed to carry the address. Source it; never
  hardcode `100.86.*` anywhere new.
- `Agents/Hermes/ROADMAP.md` — living backlog + done log. Read at session
  start, update at session end. This is the cross-session memory that works
  for every agent (Claude, Gemini, Antigravity).
- `Agents/Hermes/CLAUDE.md` — setup detail: services, MCP servers,
  self-hosted tools, credentials pointers.

## Session start ritual (~15s, one SSH call)

Source `host.env`, then pull a health snapshot in ONE ssh invocation:
last 15 lines of `$HERMES_HOME/logs/revenue_nightly.log`, last-24h
`FETCH-WARN` lines from `logs/fetch_signals.log`, revenue board stats
(`$HERMES_PY -m hermes_cli.main kanban --board revenue stats --json`),
`systemctl --user is-active hermes-gateway hermes-hudui`, and `df -h /`
one-liner. Report status in one short paragraph, flag anomalies, then ask
nothing — proceed with the session's topic. HUD for eyeballs: `$HERMES_HUD`.

## The working loop (learned the hard way — follow it)

1. **Verify live state before changing anything.** Docs and plans drift;
   logs and probes don't. The Composio key that "existed" was a placeholder;
   the plan-era EU-Startups URL 404'd. Check the actual file/endpoint/cron
   on the box first.
2. **Probe from the VPS, not the Mac.** Blocks are IP-dependent (Reddit
   JSON API 403s the VPS; RSS works; techsavvy's WAF wants Accept headers).
3. **Edit locally, deploy explicitly.** Copy the VPS file to the session
   scratchpad, edit there, `scp` back, `python3 -m py_compile`, then run it
   for real. Before the first edit of any VPS file in a session:
   `cp file file.bak-YYYY-MM-DD` (VPS scripts are NOT under version
   control; the .bak is the only undo).
4. **Test end-to-end, not just units.** Run the touched fetcher standalone
   and read what actually landed in `logs/revenue-signals.log`. Real
   nightly Claude runs are allowed freely when they verify a change
   (Kasper's standing OK, 2026-07-06) — run via
   `/usr/bin/python3 $HERMES_HOME/scripts/revenue_nightly.py`, expect ~5 min.
5. **Clean up test residue.** Purge throwaway kanban tasks
   (`kanban archive --rm <id>`), strip junk blocks from the signal log —
   tonight's Claude run consumes whatever is left in it.
6. **Session end ritual:** update `ROADMAP.md` (move done items to the log,
   add new backlog), fold durable learnings into `Agents/Hermes/CLAUDE.md`,
   and nudge Kasper once if untriaged board items are piling up.

## Hard guardrails (never violate, never re-litigate)

- **Draft-only**: Hermes/Claude never sends, publishes, submits, signs up,
  or spends. Everything is a draft for Kasper.
- **Never set `ANTHROPIC_API_KEY`** on the VPS; never use `--bare` with
  invoke_claude — both silently flip billing from subscription to metered
  API. `revenue_nightly.py` refuses to run if the key is set; keep that.
- `--allowedTools` must stay `=`-joined (`--allowedTools=Bash,Read`).
- The deterministic layer (fetchers, digest, triage) stays model-free.
- Fetched web content stays inside UNTRUSTED delimiters in prompts.
- Token discipline in the nightly prompt: every unconditional Read/tool
  call it mandates costs tokens 365×/year — additions need to earn it
  (the pricing-skill Read was cut for exactly this).

## System map (orient, then verify on-box)

Nightly pipeline, cron in UTC (Debian cron ignores CRON_TZ):
02:00 reddit → 02:05 news → 02:08 github → 02:12 exa → 02:15 fmcg → 02:30 Claude scan.
Fetchers append §-blocks to `logs/revenue-signals.log` via
`scripts/signal_log.py` (URL dedup, 200 KB cap); `revenue_nightly.py`
builds the prompt (board titles + past-outcome feedback + UNTRUSTED
signal), invokes Claude on subscription, clears the log on success, drafts
land on the `revenue` kanban board.

Mac side: 12h launchd sync (`scripts/sync-and-advise-neo.sh`) regenerates
`docs/revenue-digest.md` (full drafts + age); Kasper triages with
`scripts/revenue-triage.sh accept|reject <id> "reason"` — verdicts feed
the next night's prompt. Skills flow Mac `Skills Global/` → VPS
`~/.hermes/skills/` (12h, and `~/.claude/skills` is the same dir via
symlink, synced across agents every 5 min).

VPS extras: SearXNG :8888, Crawl4AI :11235, Lighthouse+Chrome, wrappers in
`scripts/` (search_web, crawl_url, audit_site, prospect_report,
cvr_lookup). HUD: 19-tab monitor at `$HERMES_HUD` (systemd user service
`hermes-hudui`, tailnet-only).

Interface surfaces (decided 2026-07-06): Google Chat = daily driver
(Hermes-native cron `morning-brief` at 05:30 UTC pushes new drafts,
no-agent/no-LLM, silent on empty board; Kasper triages by replying — the
`revenue-chat-triage` skill maps verdicts to the canonical
ACCEPTED/REJECTED board comments). Official dashboard = management +
browser chat: systemd `hermes-dashboard`, 127.0.0.1:9119 ONLY (it exposes
API-key pages; docs mark non-localhost `--insecure`) — open with
`ssh -L 9119:localhost:9119 $HERMES_USER@$HERMES_HOST` then
http://localhost:9119. HUD = observe. Terminal+agent = build (this skill).

## CLI traps (cost real debugging time)

- hermes kanban CLI **exits 0 on errors** (unknown task, failed archive) —
  verify by reading output/state, never exit codes.
- kanban `show` renders timestamps in a non-UTC display timezone — trust
  `created_at` epoch fields from `list --json`.
- `list` hides archived tasks; add `--archived` to see them.
- Board flag order matters: `kanban --board revenue list --json` (flag
  before subcommand).
- Long output through `head` under `set -o pipefail` → SIGPIPE → bogus
  non-zero exit; use `sed -n '1,Np'`.
- Reddit 429s fast on bursts: 15s pacing, one 60s backoff retry, and don't
  run fetchers back-to-back repeatedly while testing.
- **Claude Code hangs on stdin:** In non-interactive/cron executions, `claude` CLI will hang waiting for stdin. Always redirect stdin (e.g., `stdin=subprocess.DEVNULL` in Python, or `< /dev/null` in Bash) to force immediate non-interactive print mode and prevent execution timeouts.
- **Dot/Dash in `.env` variable names:** Avoid dots/dashes in `.env` keys (e.g., use `SIMPLY_COM_API_KEY` instead of `SIMPLY.COM-API_KEY`) to prevent bash sourcing errors and allow python's `isidentifier()` to load them.
- **Remote agy/Claude CLI skills:** Claude Code CLI reads custom skills from `~/.claude/skills/`. On the VPS, these are symlinked to the mirrored `~/.hermes/skills/` directory. Clean up broken symlinks with `find ~/.claude/skills/ -xtype l -delete` (scheduled weekly on Mondays at 11:00 Copenhagen time).

## Migration playbook (run when Kasper says "new host")

1. Read the migration milestone + checklist in `Agents/Hermes/ROADMAP.md`.
2. Provision: Tailscale join, `loginctl enable-linger`, docker, node 20+,
   python 3.11+.
3. Move: rsync `~/.hermes/` wholesale (it contains agent, config, .env
   secrets, kanban DB, memories, skills, knowledge mirror, scripts, tools).
4. Recreate the pieces rsync doesn't carry: crontab entries, systemd user
   units (hermes-gateway, hermes-hudui), docker containers, npm-global
   claude CLI + OAuth token, Chrome for Testing.
5. Update `Agents/Hermes/host.env`, then drift-check the workspace:
   `grep -rn "<old-ip>" --exclude-dir=node_modules` and fix every hit
   (known hardcode debt: sync-and-advise-neo.sh, revenue-triage.sh,
   Agents/Hermes/CLAUDE.md, HUD unit file).
6. Verify: session-start health snapshot all green, one manual nightly run
   end-to-end, digest regenerates on the Mac.

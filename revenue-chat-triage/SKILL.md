---
name: revenue-chat-triage
description: >
  Let Kasper triage revenue-board opportunities conversationally in chat.
  Use whenever Kasper's message accepts or rejects a revenue opportunity or
  reacts to the morning revenue brief — phrases like "accept t_xxx",
  "reject t_xxx because ...", "tag den" / "drop den" about a board item,
  "yes to the VVS pitch", "no to Serpier", or any verdict on a task from
  the revenue board. Only for the 'revenue' kanban board.
---

# Revenue chat triage

Kasper reviews drafted revenue opportunities by replying in chat. Your job:
map his verdicts onto the board in the EXACT format below — the nightly
scan reads these comments back as its feedback signal, so the wording is a
protocol, not a style choice.

## Accept

```
hermes kanban --board revenue comment <task_id> "ACCEPTED — Kasper will act on this draft."
hermes kanban --board revenue complete <task_id> --result accepted
```

## Reject

A reason is REQUIRED — it is the training signal that improves future
opportunities. If Kasper gave no reason, ask once ("Why not — one line is
enough?"), then:

```
hermes kanban --board revenue comment <task_id> "REJECTED: <his reason, one line>"
hermes kanban --board revenue archive <task_id>
```

## Outcome tracking (after accept)

Money starts where triage ends — when Kasper reports what happened to an
accepted item, log it on that task (works on done tasks too). Same
protocol discipline: exact uppercase prefixes, one comment per event.

- "sent the VVS pitch" / "sendt til X" →
  `hermes kanban --board revenue comment <id> "SENT <YYYY-MM-DD>"`
- "they replied" / "X vendte tilbage" →
  `hermes kanban --board revenue comment <id> "REPLIED: <one-line gist>"`
- "won it — 5.000 kr" / "de sagde ja" →
  `hermes kanban --board revenue comment <id> "WON: <amount + one-line terms>"`
- "no reply" / "died" / "lost" →
  `hermes kanban --board revenue comment <id> "LOST: <one-line reason if given>"`

Confirm back with the task title. If Kasper reports an outcome for a task
you can't find, list recent done tasks and ask which one he means.

## Rules

- Resolve fuzzy references ("the VVS one", "begge sponsor-pitches") against
  `hermes kanban --board revenue list` titles; if ambiguous, ask, never guess.
- Only touch tasks Kasper explicitly gave a verdict on. Never batch-triage
  unprompted, never triage on your own judgment.
- The kanban CLI exits 0 even on failures — verify with `show` after acting
  and confirm back in chat with the task TITLE (not just the id), e.g.
  "Archived: Pitch Flare a founding-partner sponsor spot — reason logged."
- ACCEPTED means Kasper will act himself. It does NOT authorize you to
  send, publish, submit, or spend anything — the draft-only guardrail
  stands. If he says "accept and send it", accept it, then remind him the
  sending step is his (or needs his explicit standing authorization he has
  not given).
- Danish or English both fine; write the REJECTED reason in the language
  Kasper used.

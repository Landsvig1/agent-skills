---
name: skill-creator-admin
description: Administrate and audit the cross-agent skills environment. Use this skill when checking the setup, synchronization, or structural integrity of custom skills across Claude, Gemini, Antigravity CLI, or project workspaces. Also trigger when the user mentions '/skill-creator-admin', 'sync skills', 'audit skills', or needs to diagnose broken symlinks or missing skill sync logs.
---

# Skill Creator Admin

This skill enables Antigravity / Gemini / Claude to audit, fix, and synchronize custom skills across all agents and projects.

## Skills Architecture

Skills are synchronized to flow seamlessly between Claude Code, Gemini CLI, Antigravity CLI, and local projects:

```
[Canonical Directory] (Claude Code)
~/.claude/skills/
   ▲
   │ (rsync via sync-skills.sh)
   ▼
[Workspace Global Link] (symlink in Claude Cowork root)
Documents/Claude Cowork/Skills Global/
   │
   ├─► [Workspace Mirror] (Gemini/Claude local agents root)
   │   Documents/Claude Cowork/Agents/skills/
   │
   └─► [Gemini Global Mirror] (symlinks)
       ~/.gemini/skills/ (also symlinked from ~/.gemini/antigravity-cli/skills)
```

## Audit & Sync Script

A Python utility is bundled inside this skill to automate auditing and fixing issues:
`/Users/kasperlandsvig/.claude/skills/skill-creator-admin/scripts/audit-sync.py`

### Usage

1. **Audit (Dry Run):**
   ```bash
   python3 "/Users/kasperlandsvig/.claude/skills/skill-creator-admin/scripts/audit-sync.py"
   ```
2. **Apply Automatic Fixes:**
   ```bash
   python3 "/Users/kasperlandsvig/.claude/skills/skill-creator-admin/scripts/audit-sync.py" --fix
   ```

## Key Tasks

### 1. Identify Stray Skills
If a skill is created directly in `~/.gemini/skills/` (physical folder) rather than `~/.claude/skills/`, it will not be backed up or synced to Claude Code. The audit script automatically detects these, consolidates them to the canonical folder, and replaces the target with a symlink.

### 2. Diagnose Cron Blockages (macOS)
On macOS, cron jobs are blocked from accessing `~/Documents/` by default due to TCC sandbox restrictions. If the sync log `/Users/kasperlandsvig/Documents/Claude Cowork/scripts/sync-skills.log` is stale, explain this to the user and guide them:
1. Open **System Settings** -> **Privacy & Security** -> **Full Disk Access**.
2. Click the `+` button.
3. Press `Cmd+Shift+G` and type `/usr/sbin/cron`.
4. Select `cron` and toggle it ON.

### 3. Flowing Skills to New Workspaces
Since Claude and Gemini load skills globally from `~/.claude/skills` and `~/.gemini/skills`, skills flow to any project automatically. To mirror them in a project-local agent setup:
1. Create a `Skills Global` symlink in the project root pointing to `/Users/kasperlandsvig/.claude/skills`.
2. Configure your sync script to copy from `Skills Global` to `Agents/skills/` or `.agents/skills/`.

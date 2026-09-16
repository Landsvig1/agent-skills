# vibetrends-admin

> **VibeTrends.dk Platform Administration Guide**  
> Custom Skill by [Kasper Landsvig / aiauto.dk](https://aiauto.dk)

## Overview

Guide and operational workflows for maintaining the VibeTrends.dk platform: Next.js 16 App Router, Supabase (Postgres + Auth + Storage), and the submission review gate.

## Key Capabilities

- Custom tailored for Kasper's AI automation & engineering workflow.
- High-efficiency execution with strict input validation and zero hardcoded secrets.
- Full compatibility across Claude Code, Antigravity (AGY), and Gemini CLI agents.

## Triggers & Invocation

Activate this skill in your agent prompt using any of the following triggers:
- `/vibetrends-admin`
- `vibetrends admin`
- `manage vibetrends`

## Prerequisites & Environment Variables

Ensure the following environment variables are configured in `.env.local` (see the project's `AGENTS.md`):

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `DATABASE_URL` (migrations, via `scripts/apply-migration.mjs`)

> **Security Note:** Never commit actual API keys or secret tokens to git repositories. Always load credentials from environment variables.

## File Structure

```text
vibetrends-admin/
├── SKILL.md
├── references/
├── assets/
└── README.md
```

## How It Works

1. **Trigger Detection:** The agent identifies intent from prompt keywords or explicit slash commands.
2. **Context & Execution:** The agent reads `SKILL.md` instructions and executes helper scripts located in `scripts/` (if present).
3. **Output:** Delivers structured responses, reports, or direct API/system actions.

## License

Internal Custom Skill — © vibetrends-admin by Kasper Landsvig / aiauto.dk. All rights reserved.

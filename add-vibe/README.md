# add-vibe

> **VibeTrends.dk Automated Entry Curator**  
> Custom Skill by [Kasper Landsvig / aiauto.dk](https://aiauto.dk)

## Overview

Automates adding vibes, skills, and agents to vibetrends.dk via authenticated API endpoints using dedicated bot credentials.

## Key Capabilities

- Custom tailored for Kasper's AI automation & engineering workflow.
- High-efficiency execution with strict input validation and zero hardcoded secrets.
- Full compatibility across Claude Code, Antigravity (AGY), and Gemini CLI agents.

## Triggers & Invocation

Activate this skill in your agent prompt using any of the following triggers:
- `/add-vibe`
- `add vibe`
- `add skill to vibetrends`
- `curate vibe`

## Prerequisites & Environment Variables

Ensure the following environment variables are configured in your `.env` or system environment:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `BOT_ACCOUNT_EMAIL`
- `BOT_ACCOUNT_PASSWORD`

> **Security Note:** Never commit actual API keys or secret tokens to git repositories. Always load credentials from environment variables.

## File Structure

```text
add-vibe/
├── SKILL.md
├── scripts/add-vibe.mjs
├── scripts/add-skill.mjs
├── scripts/add-agent.mjs
├── scripts/bot-auth.mjs
└── README.md
```

## How It Works

1. **Trigger Detection:** The agent identifies intent from prompt keywords or explicit slash commands.
2. **Context & Execution:** The agent reads `SKILL.md` instructions and executes helper scripts located in `scripts/` (if present).
3. **Output:** Delivers structured responses, reports, or direct API/system actions.

## License

Internal Custom Skill — © add-vibe by Kasper Landsvig / aiauto.dk. All rights reserved.

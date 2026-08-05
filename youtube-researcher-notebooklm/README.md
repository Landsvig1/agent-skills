# youtube-researcher-notebooklm

> **YouTube Video to NotebookLM Research Kit Generator**  
> Custom Skill by [Kasper Landsvig / aiauto.dk](https://aiauto.dk)

## Overview

Extracts video transcripts and synthesizes multi-format briefing documents into Google Docs & NotebookLM notebooks.

## Key Capabilities

- Custom tailored for Kasper's AI automation & engineering workflow.
- High-efficiency execution with strict input validation and zero hardcoded secrets.
- Full compatibility across Claude Code, Antigravity (AGY), and Gemini CLI agents.

## Triggers & Invocation

Activate this skill in your agent prompt using any of the following triggers:
- `/youtube-researcher-notebooklm`
- `research kit`
- `youtube to doc`

## Prerequisites & Environment Variables

Ensure the following environment variables are configured in your `.env` or system environment:

_None required (or optional context)_

> **Security Note:** Never commit actual API keys or secret tokens to git repositories. Always load credentials from environment variables.

## File Structure

```text
youtube-researcher-notebooklm/
├── SKILL.md
└── README.md
```

## How It Works

1. **Trigger Detection:** The agent identifies intent from prompt keywords or explicit slash commands.
2. **Context & Execution:** The agent reads `SKILL.md` instructions and executes helper scripts located in `scripts/` (if present).
3. **Output:** Delivers structured responses, reports, or direct API/system actions.

## License

Internal Custom Skill — © youtube-researcher-notebooklm by Kasper Landsvig / aiauto.dk. All rights reserved.

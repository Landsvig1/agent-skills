# Research2Podcast

> **Automated Topic Research to Podcast Converter**  
> Custom Skill by [Kasper Landsvig / aiauto.dk](https://aiauto.dk)

## Overview

Synthesizes online research into engaging, two-host podcast script audio overviews for NotebookLM.

## Key Capabilities

- Custom tailored for Kasper's AI automation & engineering workflow.
- High-efficiency execution with strict input validation and zero hardcoded secrets.
- Full compatibility across Claude Code, Antigravity (AGY), and Gemini CLI agents.

## Triggers & Invocation

Activate this skill in your agent prompt using any of the following triggers:
- `/research2podcast`
- `research to podcast`
- `make podcast script`

## Prerequisites & Environment Variables

Ensure the following environment variables are configured in your `.env` or system environment:

- `EXA_API_KEY`

> **Security Note:** Never commit actual API keys or secret tokens to git repositories. Always load credentials from environment variables.

## File Structure

```text
Research2Podcast/
├── SKILL.md
└── README.md
```

## How It Works

1. **Trigger Detection:** The agent identifies intent from prompt keywords or explicit slash commands.
2. **Context & Execution:** The agent reads `SKILL.md` instructions and executes helper scripts located in `scripts/` (if present).
3. **Output:** Delivers structured responses, reports, or direct API/system actions.

## License

Internal Custom Skill — © Research2Podcast by Kasper Landsvig / aiauto.dk. All rights reserved.

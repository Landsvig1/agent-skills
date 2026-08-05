# dra

> **dra Skill**  
> Agent Capability Module

## Overview

Deep Research Agent. Decomposes complex research queries into a local Blackboard State file inside the knowledge bank, spawns a ResearchSpecialist subagent to execute searches in parallel, validates findings via a ResearchDirector review cycle, and compiles a structured Obsidian source note pushed to the knowledge GitHub repository. Use this skill whenever the user asks for deep research, comprehensive analyses, market/topic reports, or uses the /dra or /DRA command.

## Triggers & Invocation

Activate this skill by referencing `dra` in prompt instructions or slash command `/name`.

## File Structure

```text
deep-research-agent/
├── SKILL.md
└── README.md
```

## Usage Guidelines

Refer to `SKILL.md` for full implementation guidelines, execution rules, and prompt specifications.

## License

MIT / Open Source / Proprietary Agent Skill.

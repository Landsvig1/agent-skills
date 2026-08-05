# ponytail-review

> **ponytail-review Skill**  
> Agent Capability Module

## Overview

Code review focused exclusively on over-engineering. Finds what to delete: reinvented standard library, unneeded dependencies, speculative abstractions, dead flexibility. One line per finding: location, what to cut, what replaces it. Use when the user says "review for over-engineering", "what can we delete", "is this over-engineered", "simplify review", or invokes /ponytail-review. Complements correctness-focused review, this one only hunts complexity.

## Triggers & Invocation

Activate this skill by referencing `ponytail-review` in prompt instructions or slash command `/name`.

## File Structure

```text
ponytail-review/
├── SKILL.md
└── README.md
```

## Usage Guidelines

Refer to `SKILL.md` for full implementation guidelines, execution rules, and prompt specifications.

## License

MIT / Open Source / Proprietary Agent Skill.

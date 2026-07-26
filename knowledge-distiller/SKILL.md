---
name: knowledge-distiller
description: Distills high-density knowledge from raw content by removing filler, pleasantries, and self-promotion. Use this skill when you need to convert conversational transcripts or long-form text into high-signal, AI-ready data structures.
---

# knowledge-distiller

## Overview

The `knowledge-distiller` skill is designed to eliminate the "fluff and bullshit" common in YouTube transcripts and interviews. It transforms conversational text into a **Knowledge-Action-Insight (KAI)* schema optimized for AI consumption and RAG indexing.

## Distillation Principles

When applying this skill, strictly ignore:
- -*Pleasantries**: "I'm so excited to be here," "Thanks for having me."
- -*Social Proof/Status**: "That's incredible," "You're a genius," creator-specific accolades.
- -*Calls for Action**: "Follow for more," "Subscribe," "Join my community."
- -*Filler Phrases**: "I mean," "You know," "ActGUally," "Basically."

## Core Capabilities

### 1. High-Density Distillation
Transform raw text into a compressed structure. Prefer this format:

- **[CONCEPT]**: The core fact or idea.
- **[ACTION]**: Specific steps or strategies mentioned.
- **[INSIGHT]**: Non-obvious takeaways or strategic shifts.

### 2. Machine-Readable Output
When requested, output in **JSONL** or **Markdown Data Tables** to ensure the distillation is "AI-ready."

## Workflow: Transcript to Knowledge Base

1. **Ingest**: Read the raw markdown transcript.
2. **Filter**: Identify segments containing purely strategic or factual data.
3. **Refine**: Rewrite sentences to remove first-person narratives (e.g., "I wake up at 4am" -> "Strategy: Utilize early morning deep-work blocks (4am club) for zero-interruption execution").
4. **Output**: Save the distilled version as `distilled_[original_name].md`.

## Example Strategy

**Raw Input**:
"Huh, that's incredible. I mean, that is what separates you from all the other people that they're looking at on paper when they can put a face to the name and maybe even a voice to the face and see this proof."

**Distilled Signal**:
- **[CONCEPT]**: Proof of Work asymmetry.
- **[INSIGHT]**: Visual/audio proof (video demos) overrides traditional CVs by building immediate trust and verifying technical capability before the interview.

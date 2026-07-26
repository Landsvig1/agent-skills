---
name: dra
description: Deep Research Agent. Decomposes complex research queries into a local Blackboard State file inside the knowledge bank, spawns a ResearchSpecialist subagent to execute searches in parallel, validates findings via a ResearchDirector review cycle, and compiles a structured Obsidian source note pushed to the knowledge GitHub repository. Use this skill whenever the user asks for deep research, comprehensive analyses, market/topic reports, or uses the /dra or /DRA command.
---

# Deep Research Agent (DRA)

Use this skill to execute comprehensive, high-fidelity research investigations integrated directly with the `knowledge` bank (Obsidian vault). The session is coordinated using an Orchestrator-Worker pattern via a local Blackboard State file (`knowledge/inbox/sessions/<slug>-state.json`) and commits updates to the `knowledge` GitHub repository.

---

## 1. Personas & Roles

*   **ResearchDirector (Orchestrator)**: Decomposes the research prompt, creates the blackboard state, spawns the worker, reviews findings, and compiles the final report using the Obsidian frontmatter template.
*   **ResearchSpecialist (Worker)**: Generates queries, performs semantic searches (Exa), triages targets, and extracts content (via Jina Reader or Firecrawl). Writes findings to the blackboard.

---

## 2. Core Workflow

### Step 1: Decomposition & Blackboard Initialization
The primary agent acts as the `ResearchDirector`.
1.  Decompose the research objective into atomic sub-questions.
2.  Initialize the blackboard JSON file at `/Users/kasperlandsvig/Documents/Claude Cowork/knowledge/inbox/sessions/<slug>-state.json`. Set the `status` to `"director_planning"`.

### Step 2: The User Gate
Present the proposed sub-questions clearly to the user. **You must pause execution** and ask:
> *"Here is the proposed research plan. Do you want to proceed with this direction, or adjust the sub-questions/sources?"*
**Do not invoke any subagents, search tools, or commit files until the user approves the plan.**

### Step 3: Multi-Persona Execution & Git Sync
Once approved, initialize the Git tracking inside `/Users/kasperlandsvig/Documents/Claude Cowork/knowledge`:
1.  Run `git add inbox/sessions/<slug>-state.json`
2.  Run `git commit -m "research: initialize session <slug>"`
3.  Run `git push`
4.  Define the `ResearchSpecialist` subagent using `define_subagent` and invoke it via `invoke_subagent` to process the questions.

### Step 4: Cost-Optimized Search Stack (Exa + Jina Reader)
The `ResearchSpecialist` executes searches using:
1.  **Exa API**: Retrieve the top 20 semantic results.
2.  **Triage**: Filter the snippets to select the top 3-5 high-signal URLs.
3.  **Jina Reader**: Fetch and parse page content using `https://r.jina.ai/<URL>`.
4.  **Firecrawl**: Use only as a fallback for dynamic, heavily protected JS websites.

### Step 5: Iterative Git Updates
Every time the `ResearchSpecialist` completes a sub-question:
1.  Write findings and source URLs back into `inbox/sessions/<slug>-state.json`.
2.  Mark status as `"completed"`.
3.  Run `git add inbox/sessions/<slug>-state.json`
4.  Run `git commit -m "research: update findings for <slug>"`
5.  Run `git push`

### Step 6: Verification & Review Loop
The `ResearchDirector` monitors the state. If a completed question lacks detail (confidence < 0.7), add follow-up questions to the blackboard and notify the Specialist.

### Step 7: Final Synthesis & Output Routing
Once all questions are complete:
1.  Generate the final Markdown file at `/Users/kasperlandsvig/Documents/Claude Cowork/knowledge/inbox/<yyyy-mm-slug>.md` using the Obsidian frontmatter template below.
2.  Set state status to `"completed"`.
3.  Run `git add inbox/sessions/<slug>-state.json inbox/<yyyy-mm-slug>.md`
4.  Run `git commit -m "research: complete report <slug>"`
5.  Run `git push`

---

## 3. Blackboard Schema (`inbox/sessions/<slug>-state.json`)

```json
{
  "objective": "Research target objective",
  "status": "in-progress",
  "sub_questions": [
    {
      "id": "q1",
      "question": "The specific sub-question text",
      "status": "pending",
      "queries": ["suggested search queries"],
      "findings": [
        {
          "source": "https://example.com/source",
          "fact": "Verifiable fact extracted by Specialist."
        }
      ]
    }
  ],
  "discovered_sources": [
    {
      "url": "https://example.com/source",
      "title": "Page Title"
    }
  ]
}
```

---

## 4. Report Structure (Obsidian Vault Source Template)

The generated report MUST follow this exact GFM layout with YAML frontmatter:

```markdown
---
type: source
source_kind: other
title: "Research Report: [Topic Name]"
author: "Deep Research Agent"
url: ""
date_published: yyyy-mm-dd
date_captured: yyyy-mm-dd
status: inbox
tags: [research, dra]
summary: "[3-5 sentence synthesis of key findings in the owner's own words]"
related: []
confidence: 0.9
---

# Research Report: [Topic Name]

## Executive Summary
[Concise overview of the key insights and conclusions.]

## Research Plan (Approved)
*   **Objective**: [Original user prompt]
*   **Sources Consulted**: [Summary of tools/databases queried]

## Detailed Findings
[Organized by sub-question or logical theme. Use headings, bullet points, and tables. Every claim must have an inline citation link, e.g., (Source Name)[URL].]

## Bibliography & Sources
*   [Title of Source 1](URL) — Brief description of relevance.
*   [Title of Source 2](URL) — Brief description of relevance.
```

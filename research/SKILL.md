---
name: research
description: Run a structured research project, market analysis, competitor analysis, literature review, technical fact-finding, or web scraping task. Make sure to use this skill whenever the user asks to research a topic, search the web, analyze competitors, find papers, scrape websites, compile research notes, or runs the /research command.
---

# General Research Skill

Use this skill to execute structured, high-fidelity research investigations, ranging from quick web queries to deep market, competitor, or academic synthesis. This skill coordinates available search and extraction tools (Exa, Firecrawl, Jina Reader) to produce comprehensive, citation-backed intelligence.

---

## 1. Research Modality Selection

Before executing, classify the task to select the optimal search stack:

| Modality | Use Case | Tool / Sub-Skill Recommendation |
| :--- | :--- | :--- |
| **Market / Competitor** | Company details, funding, competitors, industry trends | Use `exa-company-research` and `firecrawl-market-research`. |
| **People / Leads** | Finding key people, email contacts, LinkedIn profiling | Use `exa-people-research` and `exa-lead-generation`. |
| **Academic / Technical** | Research papers, technical specs, library docs | Use `exa-research-paper-search` and `exa-code-context`. |
| **General Web** | Recent news, blog posts, general facts | Use `exa-web-search` or `firecrawl-search`. |
| **Target Scraping** | Extracting specific URL content or whole websites | Use `firecrawl-scrape` or `firecrawl-crawl`. |
| **Deep Synthesis** | Complex, multi-faceted queries requiring validation | Use `firesearch` or spawn a `dra` (if vault integration needed). |

---

## 2. Core Execution Workflow

### Step 1: Decomposition & Planning
1. Break down the research objective into 3-5 specific, atomic sub-questions.
2. Define a list of initial search queries for each sub-question.
3. Identify the target entities, sources, or domains (e.g., industry reports, academic repositories, company blogs).

### Step 2: Search & Extraction Loop
For each sub-question:
1. **Search**: Query Exa or Firecrawl to retrieve top matching results.
2. **Triage**: Evaluate snippets to select the top 2-4 most relevant URLs.
3. **Extract**: Fetch full page markdown using Jina Reader (`https://r.jina.ai/<URL>`) or `firecrawl-scrape` (especially if JS-heavy).
4. **Log**: Record facts, data points, and their exact source URLs.

### Step 3: Validation & Refinement
Evaluate the collected facts against the research objectives:
- **Coverage**: Are all sub-questions answered with high-confidence data?
- **Recency**: Is the information up to date?
- **Verification**: If findings are thin or conflict, rephrase queries (using synonyms or specific domains) and repeat Step 2.

### Step 4: Premium Synthesis & Report Generation
Format the final output as a clean, structured Markdown report. Avoid vague summaries or placeholder text. Every claim must have an inline citation.

---

## 3. Standard Output Template

Save the output to `Gem-CLI Outputs/Research/<yyyy-mm-dd>_<slug>.md` or print it directly. Use the following template:

```markdown
# Research Report: [Subject / Topic Name]

## Executive Summary
[A concise, 3-5 sentence synthesis of the key findings and actionable takeaways.]

## Detailed Findings
### [Sub-Question or Theme 1]
[In-depth synthesis. Use tables, bullet points, or list structures to make data scannable. Include inline markdown links for every fact, e.g., (Source Name)(URL).]

### [Sub-Question or Theme 2]
[Detailed details...]

## Sources Consulted
* [Source Title](URL) - Brief description of what was extracted from this source.
```

---

## 4. Quality Bar & Rules

1. **Strict Citations**: Every single data point, metric, or major claim must be cited using a clickable markdown link. No general "Sources: [Google]" references.
2. **Fact-First**: Avoid AI filler phrases ("It is interesting to note...", "In conclusion..."). Start paragraphs with the key fact or metric.
3. **No Halftruths**: If information is unavailable or contradictory, state it explicitly along with the search queries tried.

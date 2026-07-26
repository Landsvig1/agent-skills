# Research2Podcast Skill

## Overview
This skill automates the creation of a high-quality AI podcast from a single topic input. It searches the web for the most recent high-signal articles, filters for quality and freshness, and synthesizes them into an interactive NotebookLM Audio Overview.

## Core Workflow (/research2podcast)

1.  **Discovery (Exa)**:
    - MUST use the `exa-web-search` skill (or the relevant Exa script) to perform a semantic search on the provided topic. Do not use native web search for this step.
    - **Freshness Filter**: Apply a dynamic `publishedAfter` filter calculated as **Current Date minus 90 days**.
    - **Quality Screening**: Select top 5-10 "high signal" sources (official docs, expert blogs, technical reviews).
2.  **Extraction (Cost Optimization Routing)**:
    - First, attempt to extract the full content of each URL using native Gemini tools (e.g., `read_url_content`). This avoids unnecessary API costs.
    - If the native extraction succeeds and the data is clean, proceed to ingestion.
    - If native extraction fails, hits a JS-rendering wall, or returns poor data, **fallback to the `firecrawl` skill** to extract the full, clean Markdown.
3.  **Ingestion (NotebookLM MCP)**:
    - Automatically create a new notebook named after the topic using the NotebookLM MCP.
    - Upload the cleanly extracted Markdown texts as sources into the newly created notebook using the MCP.
4.  **Production (NotebookLM MCP)**:
    - Trigger the generation of an **Audio Overview** (Podcast) automatically using the NotebookLM MCP.
5.  **Delivery**:
    - Provide a short summary of the sources used.
    - **Final Action**: Output the direct, playable link to the generated NotebookLM podcast. No manual upload or drag-and-drop should be required from the user.
    - **Constraint**: No direct download links.

## Tool Requirements
- **NotebookLM MCP**: Required to automate the creation of the notebook, source ingestion, and podcast generation.

## Quality Standards
- **Freshness**: Content must be < 3 months old.
- **Language**: Default to Danish for summaries, but maintain original language (typically English) for the technical sources in the notebook.
- **Tone**: Senior Engineer / Tech Analyst.

## Usage Commands
- `/research2podcast <TOPIC>`: Executes the end-to-end pipeline.

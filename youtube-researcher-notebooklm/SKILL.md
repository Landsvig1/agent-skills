# AI Automation Researcher Skill

## Overview
This skill transforms a single YouTube URL into a comprehensive, multi-format "Research Kit" using NotebookLM and Google Workspace. It automates the extraction, synthesis, and enrichment of video content into high-value client deliverables.

## Core Workflow (/research-kit)

1.  **Ingestion**: Create a dedicated Notebook and add the YouTube source.
2.  **Synthesis**: 
    - Generate a **Briefing Doc** (deep research).
3.  **Extraction**: Export the Briefing Doc to Google Docs.
4.  **Enrichment**: 
    - Insert "Quick Access" metadata at the top of the Doc.
    - **Content Factory**: Add a section with:
        - **Blog Post Draft**: Optimized for 2025 (Problem -> Old Way vs AI Way -> Technical Solution -> ROI -> FAQ). Focus on "Anti-AI Slop" (add placeholders for Kasper's personal case studies).
        - **X (Twitter) Thread**: 10-tweet structure (Hook -> Visual Architecture Placeholder -> Step-by-Step -> Proof of Work -> CTA).
    - Provide a direct link to the interactive NotebookLM chat.

## Content Recipes

### Blog Post Structure (The 2025 Authority Post)
- **Title**: [Number] + [Benefit] + [Target Audience] + [Year]
- **Hook**: Specific pain point (e.g., labor cost/time waste).
- **Technical Meat**: Mention specific stack (e.g., Gemini 1.5, n8n, MCP).
- **Local Context**: For aiauto.dk, prioritize Danish business context and ROI.

### X Thread Structure (The Proof-of-Work Thread)
- **Tweet 1**: Pattern interrupt hook (e.g., "Zapier is dead, long live Agents").
- **Tweet 3**: Describe a visual architecture (e.g., "The Brain vs. The Tools").
- **Tweet 9**: Reply-to-unlock CTA (e.g., "Reply 'AUTO' for the template").

## Tool Requirements
- **NotebookLM MCP**: For source management and artifact generation.
- **Google Workspace MCP**: For Docs editing and Drive organization.

## Quality Standards
- **Language**: Default to Danish for summaries/content unless specified.
- **Navigation**: Every document MUST contain "Quick Links" at the top.
- **Tone**: Professional, strategic, and "senior-level".

## Usage Commands
- \`/research-kit <YOUTUBE_URL>\`: Runs the full end-to-end pipeline.


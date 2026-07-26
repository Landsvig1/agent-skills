---
name: firesearch
description: AI-powered deep research using smart query decomposition, answer validation, and autonomous retry logic. Use for complex, multi-faceted research queries that require high-confidence answers and cited sources.
---

# Firesearch

Use this skill for complex research that requires more than a simple search. It follows a multi-step process of decomposition, validation, and refinement.

## Workflow

### 1. Smart Query Decomposition
Break the complex user prompt into 3-7 focused sub-questions. Each sub-question should be atomic and target a specific aspect of the main query.

### 2. Execution & Validation
For each sub-question:
1. **Search & Scrape**: Use Firecrawl to find and extract content.
2. **Validate**: Evaluate the findings against the sub-question. 
   - Assign a confidence score (0-1.0).
   - If confidence < 0.7, move to **Retry Logic**.
   - If confidence >= 0.7, extract the answer and citations.

### 3. Autonomous Retry Logic
If a sub-question fails validation:
1. **Rephrase**: Try different keywords or synonyms.
2. **Broaden**: Look for more general information that might contain the answer.
3. **Drill Down**: Look for specific sub-topics.
4. Retry the search and scrape with the new strategy.

### 4. Synthesis
Combine the validated answers into a comprehensive response. 

## Response Format

# Research Report: [Subject]

## Executive Summary
[Brief overview of findings]

## Detailed Answers
[Section for each sub-question or theme with cited facts]

## Sources
[List of all URLs used with titles]

## Quality Bar
- Every claim must be cited.
- Confidence must be high for all included facts.
- Explicitly state if any sub-questions could not be answered with high confidence after retries.

---
name: youtube-analyst
description: Comprehensive analysis of YouTube videos, channels, and audience engagement. Use this skill to search for content, retrieve metadata (views, likes), calculate engagement metrics, and perform sentiment analysis/ evaluation. Requires a YOUTUBE_API_KEY.
---

# YouTube Analyst

## Overview

The `youtube-analyst` skill transforms Gemini CLI into a marketing and media analytics assistant. It provides deterministic tools for interacting with the YouTube Data API v3, enabling deep dives into content performance and audience sentiment.

## Core Capabilities

### 1. Market Research & Search
Use `scripts/youtube_tools.py --action search` to find videos based on topics, competitor names, or niches. This is the first step in identifying a content landscape.

### 2. Performance Analysis
Retrieve detailed statistics using `--action stats`. Use these metrics to calculate:
- **Engagement Rate**: (likes + comments) / views
- **Growth Trends**: Comparing stats across multiple videos from the same channel.

### 3. Audience Sentiment Analysis
Use `--action analyze` to fetch comments and run a sentiment heuristic. This helps identify:
- Common praise or complaints.
- Questions from the audience.
- Overall brand perception in the comment section.

## Workflow: Comprehensive Channel Audit

1. **Discovery**: Search for the latest 10 videos from a target channel.
2. **Data Ingestion**: Fetch stats for all 10 videes.
3. **Deep Dive**: Pick the best and worst performing videos; analyze their comment sentiment.
4. **Reporting**: Synthesize the findings into a report highlighting what works (high engagement + positive sentiment) vs. what doesn't.

## Setup

This skill requires a YouTube Data API Key.
1. Get a key from the [Google Cloud Console](https://console.cloud.google.com/).
2. Ensure `google-api-python-client` is installed: `pip install google-api-python-client`.
3. Provide the key via the `--api-key` parameter when running the scripts.


## Reference Material

See [references/guide.md](references/guide.md) for detailed metric definitions and API quota information.

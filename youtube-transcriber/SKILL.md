---
name: youtube-transcriber
description: Extract transcripts from YouTube videos and save them as Markdown files. Use this skill when you need to read the content of a video, find a creator's latest video, or analyze video dialogue. Supports multiple languages and auto-generated captions.
---

# YouTube Transcriber

## Overview

The `youtube-transcriber` skill allows you to quickly retrieve full video transcripts using the `youtube-transcript.ai` API. It can automatically find the latest video for a given creator and output a clean Markdown file with timestamps.

## Core Capabilities

### 1. Extract Transcript from URL/ID
Use `scripts/transcribe.py --video <URL_OR_ID>` to fetch the transcript.
- **Output**: A Markdown file containing metadata (Title, Duration) and the timed dialogue.
- **Language Support**: Use `--lang <code-e.g.-da>` to request a specific language.

### 2. Find Latest Video & Transcribe
Use `scripts/transcribe.py --creator "<NAME>" --api-key <KEY>` to automatically identify the most recent upload and extract its transcript.
- **Requirement**: This feature requires a `YOUTUBE_API_KEY`.

### 3. Save for Analysis
Transcripts are saved to the specified `--output-dir` (defaults to current directory). This makes them ready for RAG (Retrieval-Augmented Generation) or direct reading.

## Workflow: Transcription to Summary

1. **Fetch**: Run the transcription script for a creator or specific video.
2. **Read**: Load the generated `.md` file.
3. **Summarize**: Analyze the text to extract key points, action items, or a TL;DR.

## Setup

- **Python Dependencies**: `pip install requests`
- **Environment**: If using the `--creator` feature, set your `YOUTUBE_API_KEY` in your environment or provide it via the CLI.

## API Credits
This skill uses the `youtube-transcript.ai` service. It handles fallback from human-uploaded to auto-generated captions automatically.

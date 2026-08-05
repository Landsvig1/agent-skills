# Agent Skills Repository

> Production-ready agent skills for AI coding assistants (**Claude Code**, **Antigravity / AGY**, **Gemini CLI**).  
> Maintained by [Kasper Landsvig / aiauto.dk](https://aiauto.dk).

---

## Overview

This repository contains modular **Agent Skills** that extend AI capabilities with domain-specific workflows, API integrations, automated execution scripts, and strict operational guidelines.

Every skill directory includes:
- `SKILL.md` — Core instruction set and frontmatter metadata for LLM agents.
- `README.md` — Human-readable documentation, usage guidelines, and requirements.
- `scripts/` — Automated execution scripts (Python / Node.js / Shell) where applicable.

---

## Featured Custom Skills (Built by Kasper Landsvig)

These custom skills power day-to-day operations, automation pipelines, and core projects:

| Skill | Description | Category |
| :--- | :--- | :--- |
| [`add-vibe`](add-vibe/README.md) | Curate and insert vibes, skills, and agents into VibeTrends.dk via API | Automation & Web |
| [`bogholder`](bogholder/README.md) | Danish bookkeeping compliance, Dinero, moms, and accounting rules | Business & Finance |
| [`bot-pr-review`](bot-pr-review/README.md) | Triage and review automated bot pull requests across GitHub repositories | Engineering & CI |
| [`dk-techblog`](dk-techblog/README.md) | Scrape and synthesize Danish tech blog articles into Markdown digests | Research & Content |
| [`fiske-dashboard`](fiske-dashboard/README.md) | Monitor and update fishery project compliance & dashboard data | Domain Operations |
| [`gsc-admin`](gsc-admin/README.md) | Google Search Console API automation (sitemaps, indexing, analytics) | SEO & Growth |
| [`hermes-ops`](hermes-ops/README.md) | Operate and optimize the Hermes autonomous agent & revenue pipeline | Agent Systems |
| [`invoke-claude-subscription`](invoke-claude-subscription/README.md) | Shell out to local Claude Code CLI session for high-stakes reasoning/code | Infrastructure |
| [`knowledge-distiller`](knowledge-distiller/README.md) | Extract high-density Knowledge-Action-Insight (KAI) schemas from raw content | AI & RAG |
| [`projects-admin`](projects-admin/README.md) | Read-only diagnostic health checks across live web portfolio projects | Operations |
| [`Research2Podcast`](Research2Podcast/README.md) | Synthesize research queries into NotebookLM two-host podcast audio scripts | AI & Audio |
| [`revenue-chat-triage`](revenue-chat-triage/README.md) | Conversational triage and status updates for revenue opportunity board | Sales & Ops |
| [`simply-launch`](simply-launch/README.md) | 10-minute zero-to-live deployment runbook (Simply.com + Vercel + Turso) | Deployment |
| [`skill-creator-admin`](skill-creator-admin/README.md) | Cross-agent skill system audit, symlink check, and synchronization | Meta / Admin |
| [`vibetrends-admin`](vibetrends-admin/README.md) | Administration & content management guide for VibeTrends.dk | Product Admin |
| [`wrap`](wrap/README.md) | Session wrap-up audit, task verification, and concise status reporting | Workflow |
| [`youtube-researcher-notebooklm`](youtube-researcher-notebooklm/README.md) | Generate multi-format research kits from YouTube videos | Content & Research |

---

## Standard & Utility Skills

- **Exa Search Suite**: [`exa-code-context`](exa-code-context/README.md), [`exa-company-research`](exa-company-research/README.md), [`exa-financial-report-search`](exa-financial-report-search/README.md), [`exa-lead-generation`](exa-lead-generation/README.md), [`exa-people-research`](exa-people-research/README.md), [`exa-personal-site-search`](exa-personal-site-search/README.md), [`exa-research-paper-search`](exa-research-paper-search/README.md), [`exa-web-search`](exa-web-search/README.md), [`exa-x-search`](exa-x-search/README.md).
- **Firecrawl Suite**: [`firecrawl`](firecrawl/README.md), [`firecrawl-crawl`](firecrawl-crawl/README.md), [`firecrawl-market-research`](firecrawl-market-research/README.md), [`firecrawl-scrape`](firecrawl-scrape/README.md), [`firecrawl-search`](firecrawl-search/README.md), [`firesearch`](firesearch/README.md).
- **Engineering & Architecture**: [`debug`](debug/README.md), [`excalidraw`](excalidraw/README.md), [`framer-motion`](framer-motion/README.md), [`github-backend`](github-backend/README.md), [`html-artifacts`](html-artifacts/README.md), [`ponytail`](ponytail/README.md), [`ponytail-review`](ponytail-review/README.md), [`shadcn-ui`](shadcn-ui/README.md), [`tdd`](tdd/README.md), [`vibe-extractor`](vibe-extractor/README.md), [`vibe-synthesis`](vibe-synthesis/README.md), [`vibe-vision`](vibe-vision/README.md), [`web-analytics`](web-analytics/README.md), [`web-design-guidelines`](web-design-guidelines/README.md), [`web-performance`](web-performance/README.md), [`web-security`](web-security/README.md).
- **Strategy & Strategy**: [`cold-email`](cold-email/README.md), [`copywriting`](copywriting/README.md), [`deep-research-agent`](deep-research-agent/README.md), [`gdpr-privacy-terms`](gdpr-privacy-terms/README.md), [`grill-me`](grill-me/README.md), [`grilling`](grilling/README.md), [`nano-banana-build`](nano-banana-build/README.md), [`pricing`](pricing/README.md), [`research`](research/README.md), [`seo-nextjs`](seo-nextjs/README.md), [`skill-creator`](skill-creator/README.md), [`youtube-analyst`](youtube-analyst/README.md), [`youtube-transcriber`](youtube-transcriber/README.md).

---

## Security & Secrets Policy

> [!IMPORTANT]
> This repository contains **NO API keys, passwords, bearer tokens, OAuth client secrets, or private credentials**.

- Environment variables are loaded dynamically from `.env` or system environment.
- Refer to `.env.example` to see required variables for specific skills.
- Strict `.gitignore` rules prevent accidental commits of local `.env` files, OAuth tokens, or venv environments.

---

## Setup & Synchronization

### 1. Copy Environment Configuration
```bash
cp .env.example .env
# Edit .env and supply your required API keys (e.g. EXA_API_KEY, FIRECRAWL_API_KEY)
```

### 2. Cross-Agent Sync
This repository serves as the central skills source. Automated cron jobs or slash commands (`/skill-creator-admin`) sync skills across:
- **Claude Code**: `~/.claude/skills/`
- **Gemini CLI / Antigravity**: `~/.gemini/skills/`

---

## License

Internal Custom Skills © [Kasper Landsvig / aiauto.dk](https://aiauto.dk). All rights reserved.  
Open-source utility components licensed under MIT where noted.

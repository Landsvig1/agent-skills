#!/usr/bin/env node
// Insert one row into /skills via the real authenticated POST /api/skills
// endpoint. Called once per discovered SKILL.md by the SKILL.md workflow when
// a repo contains multiple skills (see add-vibe/SKILL.md, KTD6/KTD7 in
// docs/plans/2026-07-01-001-feat-add-vibe-skills-catalog-plan.md).
// Run from project root: node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/add-skill.mjs \
//   --title <title> --category <topic-slug> --desc <description> --tags "tag1,tag2" --githubUrl <url> [--source <repo-root-url>]
//
// --githubUrl must point at the directory the skill actually lives in for a
// multi-skill repo (.../tree/<branch>/<dir>) — the /skills detail page resolves
// its doc from this URL and does NOT fall back to the repo root (see
// src/lib/githubDocSource.ts). --source is the plain repo root for attribution.

import { getBotAccessToken, getApiBaseUrl } from './bot-auth.mjs';

// --- Arg parsing ---
const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] ?? null : null;
};

const title      = get('--title');
const category   = get('--category');
const desc       = get('--desc') ?? '';
const tagsArg    = get('--tags');
const githubUrl  = get('--githubUrl');
// Attribution link. Defaults to githubUrl, which is right for a single-skill
// repo; pass the repo root explicitly when githubUrl points into a subdirectory.
const source     = get('--source') ?? githubUrl;

if (!title || !category || !githubUrl) {
  console.error('Usage: add-skill.mjs --title <title> --category <topic-slug> --githubUrl <url> [--desc <desc>] [--tags "tag1,tag2"] [--source <repo-root-url>]');
  process.exit(1);
}

const tags = tagsArg ? tagsArg.split(',').map((t) => t.trim()).filter(Boolean) : [];

// --- Authenticated insert via the real API ---
const token = await getBotAccessToken();
const baseUrl = getApiBaseUrl();

const res = await fetch(`${baseUrl}/api/skills`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    title,
    category,
    description: desc,
    tags,
    githubUrl,
    source,
  }),
});

const body = await res.json();

if (!res.ok) {
  console.error(`POST /api/skills failed (${res.status}):`, JSON.stringify(body));
  process.exit(1);
}

console.log(`Inserted: ${body.id} (${title})`);
console.log(`Live at:  https://vibetrends.dk/skills/${body.id}`);

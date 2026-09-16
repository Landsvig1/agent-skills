#!/usr/bin/env node
// Insert one row into /skills via the real authenticated POST /api/skills
// endpoint. Called once per discovered SKILL.md by the SKILL.md workflow when
// a repo contains multiple skills (see add-vibe/SKILL.md, KTD6/KTD7 in
// docs/plans/2026-07-01-001-feat-add-vibe-skills-catalog-plan.md).
// Run from project root: node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/add-skill.mjs \
//   --title <title> --category <topic-slug> --desc <description> --tags "tag1,tag2" --githubUrl <url> [--source <repo-root-url>] [--delay <ms>]
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
const delayMs    = parseInt(get('--delay') ?? '0', 10);

if (!title || !category || !githubUrl) {
  console.error('Usage: add-skill.mjs --title <title> --category <topic-slug> --githubUrl <url> [--desc <desc>] [--tags "tag1,tag2"] [--source <repo-root-url>] [--delay <ms>]');
  process.exit(1);
}

const tags = tagsArg ? tagsArg.split(',').map((t) => t.trim()).filter(Boolean) : [];

if (delayMs > 0) {
  await new Promise((resolve) => setTimeout(resolve, delayMs));
}

// --- Authenticated insert via the real API with retry/backoff ---
const token = await getBotAccessToken();
const baseUrl = getApiBaseUrl();

async function postWithRetry(maxRetries = 2) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
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

    const isJson = (res.headers.get('content-type') || '').includes('application/json');
    const body = isJson ? await res.json() : await res.text();

    if (res.ok) {
      return { ok: true, status: res.status, body };
    }

    // 429 = app rate limit (20/hr), 403 = Vercel edge DDoS mitigation or forbidden
    if ((res.status === 429 || res.status === 403) && attempt < maxRetries) {
      const waitTime = (attempt + 1) * 2500;
      console.warn(`[HTTP ${res.status}] Rate-limited / mitigated. Retrying in ${waitTime}ms (attempt ${attempt + 1}/${maxRetries})...`);
      await new Promise((r) => setTimeout(r, waitTime));
      continue;
    }

    return { ok: false, status: res.status, body, headers: res.headers };
  }
}

const result = await postWithRetry();

if (!result.ok) {
  console.error(`POST /api/skills failed (${result.status}):`, typeof result.body === 'object' ? JSON.stringify(result.body) : result.body);
  if (result.status === 403) {
    console.error('Note: 403 can be Vercel Edge DDoS mitigation on burst requests. Try pacing requests (1.5-2s), waiting for IP cooldown, or using VIBES_API_BASE_URL=http://localhost:3000.');
  } else if (result.status === 429) {
    console.error('Note: 429 indicates the 20 writes/hour agent budget limit was reached. Check rate_limits table in Supabase or split batches.');
  }
  process.exit(1);
}

const body = result.body;
console.log(`Inserted: ${body.id} (${title})`);
console.log(`Live at:  https://vibetrends.dk/skills/${body.id}`);

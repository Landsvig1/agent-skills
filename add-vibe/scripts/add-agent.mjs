#!/usr/bin/env node
// Insert one row into /agents (which also powers /cli and /mcp — same table,
// filtered by category) via the real authenticated POST /api/agents endpoint.
// Run from project root: node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/add-agent.mjs \
//   --name <name> --category "CLI" --desc <description> [--installCommand <cmd>] \
//   [--systemPrompt <text>] [--tags "tag1,tag2"] [--sourceUrl <url>] [--delay <ms>]
//
// isDanish/denmarkSpecific are NOT exposed by this endpoint (see SKILL.md
// Step 2c) — set them with a follow-up DATABASE_URL + pg UPDATE after insert.

import { getBotAccessToken, getApiBaseUrl } from './bot-auth.mjs';

// --- Arg parsing ---
const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] ?? null : null;
};

const name            = get('--name');
const category        = get('--category');
const desc            = get('--desc');
const installCommand  = get('--installCommand');
const systemPrompt    = get('--systemPrompt');
const tagsArg         = get('--tags');
const sourceUrl       = get('--sourceUrl');
const delayMs         = parseInt(get('--delay') ?? '0', 10);

if (!name || !category || !desc) {
  console.error('Usage: add-agent.mjs --name <name> --category <"CLI"|"MCP Server"> --desc <description> [--installCommand <cmd>] [--systemPrompt <text>] [--tags "tag1,tag2"] [--sourceUrl <url>] [--delay <ms>]');
  process.exit(1);
}

if (category !== 'CLI' && category !== 'MCP Server') {
  console.error(`ERROR: --category must be exactly "CLI" or "MCP Server" (got: ${category})`);
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
    const res = await fetch(`${baseUrl}/api/agents`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name,
        category,
        description: desc,
        ...(installCommand ? { installCommand } : {}),
        ...(systemPrompt ? { systemPrompt } : {}),
        ...(tags.length ? { tags } : {}),
        ...(sourceUrl ? { sourceUrl } : {}),
      }),
    });

    const isJson = (res.headers.get('content-type') || '').includes('application/json');
    const body = isJson ? await res.json() : await res.text();

    if (res.ok) {
      return { ok: true, status: res.status, body };
    }

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
  console.error(`POST /api/agents failed (${result.status}):`, typeof result.body === 'object' ? JSON.stringify(result.body) : result.body);
  if (result.status === 403) {
    console.error('Note: 403 can be Vercel Edge DDoS mitigation on burst requests. Try pacing requests (1.5-2s), waiting for IP cooldown, or using VIBES_API_BASE_URL=http://localhost:3000.');
  } else if (result.status === 429) {
    console.error('Note: 429 indicates the 20 writes/hour agent budget limit was reached. Check rate_limits table in Supabase or split batches.');
  }
  process.exit(1);
}

const body = result.body;
const routeBase = category === 'CLI' ? 'cli' : 'mcp';
console.log(`\nInserted: ${body.id} (${name})`);
console.log(`Live at:  https://vibetrends.dk/${routeBase}/${body.id}`);
console.log(`\nNote: isDanish/denmarkSpecific are not set by this script — see SKILL.md Step 2c's follow-up if this entry is Danish-authored or Denmark-specific.`);

#!/usr/bin/env node
// Insert one row into /agents (which also powers /cli and /mcp — same table,
// filtered by category) via the real authenticated POST /api/agents endpoint.
// Run from project root: node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/add-agent.mjs \
//   --name <name> --category "CLI" --desc <description> [--installCommand <cmd>] \
//   [--systemPrompt <text>] [--tags "tag1,tag2"] [--sourceUrl <url>]
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

if (!name || !category || !desc) {
  console.error('Usage: add-agent.mjs --name <name> --category <"CLI"|"MCP Server"> --desc <description> [--installCommand <cmd>] [--systemPrompt <text>] [--tags "tag1,tag2"] [--sourceUrl <url>]');
  process.exit(1);
}

if (category !== 'CLI' && category !== 'MCP Server') {
  console.error(`ERROR: --category must be exactly "CLI" or "MCP Server" (got: ${category})`);
  process.exit(1);
}

const tags = tagsArg ? tagsArg.split(',').map((t) => t.trim()).filter(Boolean) : [];

// --- Authenticated insert via the real API ---
const token = await getBotAccessToken();
const baseUrl = getApiBaseUrl();

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

const body = await res.json();

if (!res.ok) {
  console.error(`POST /api/agents failed (${res.status}):`, JSON.stringify(body));
  process.exit(1);
}

const routeBase = category === 'CLI' ? 'cli' : 'mcp';
console.log(`\nInserted: ${body.id} (${name})`);
console.log(`Live at:  https://vibetrends.dk/${routeBase}/${body.id}`);
console.log(`\nNote: isDanish/denmarkSpecific are not set by this script — see SKILL.md Step 2c's follow-up if this entry is Danish-authored or Denmark-specific.`);

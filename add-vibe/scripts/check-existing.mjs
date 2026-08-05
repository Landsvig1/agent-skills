#!/usr/bin/env node
// Duplicate pre-check. Run BEFORE any insert (see SKILL.md Step 0).
//
// Nothing in the schema stops the same URL being inserted twice, and the
// multi-skill path is the sharp edge: re-running the skill on a repo with 14
// SKILL.md files inserts 14 duplicate rows, silently, in one pass.
//
// Run from project root:
//   node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/check-existing.mjs \
//     --catalog skills --url <repo-or-page-url> [--title <title>]
//
// Exit codes: 0 = no match (safe to insert), 2 = match found, 1 = error.

import { connect, CATALOGS } from './db.mjs';

const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] ?? null : null;
};

const catalog = get('--catalog');
const url = get('--url');
const title = get('--title');

if (!catalog || !url || !CATALOGS[catalog]) {
  console.error('Usage: check-existing.mjs --catalog <skills|vibes|agents> --url <url> [--title <title>]');
  process.exit(1);
}

/** Strip the noise that makes two spellings of the same link look different. */
function normalize(u) {
  if (!u) return '';
  return String(u)
    .trim()
    .toLowerCase()
    .replace(/^https?:\/\//, '')
    .replace(/^www\./, '')
    .replace(/\.git$/, '')
    .replace(/\/+$/, '');
}

/** owner/repo for a github URL, ignoring any /tree/<ref>/<subpath> tail. */
function repoKey(u) {
  const m = normalize(u).match(/^github\.com\/([^/]+)\/([^/]+)/);
  return m ? `${m[1]}/${m[2]}` : null;
}

const slug = (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const { table, urlColumn, titleColumn, route } = CATALOGS[catalog];
const client = await connect();

try {
  const { rows } = await client.query(
    `SELECT id, ${titleColumn} AS title, ${urlColumn} AS url FROM public.${table}`
  );

  const targetRepo = repoKey(url);
  const targetUrl = normalize(url);
  const targetTitle = title ? slug(title) : null;

  // Same repo but a different skill is expected (monorepos of skills), so a
  // skills match needs the title to line up too. For vibes/agents the URL
  // alone is the identity.
  const exact = rows.filter((r) => {
    const sameUrl = normalize(r.url) === targetUrl;
    const sameRepo = targetRepo && repoKey(r.url) === targetRepo;
    const sameTitle = targetTitle && slug(r.title) === targetTitle;
    if (catalog === 'skills') return sameTitle && (sameRepo || sameUrl);
    return sameUrl || (targetTitle && sameTitle);
  });

  const sameRepoOtherEntries =
    catalog === 'skills' && targetRepo
      ? rows.filter((r) => repoKey(r.url) === targetRepo && !exact.includes(r))
      : [];

  if (sameRepoOtherEntries.length) {
    console.log(`Already imported from this repo (${sameRepoOtherEntries.length}) — skip these, import only the rest:`);
    for (const r of sameRepoOtherEntries) console.log(`  - ${r.title} (${r.id})`);
  }

  if (exact.length) {
    console.log(`\nDUPLICATE — already in /${route}:`);
    for (const r of exact) console.log(`  - ${r.title} (${r.id})  ${r.url ?? ''}`);
    console.log('\nDo not insert. Report this to the user instead.');
    process.exit(2);
  }

  console.log(`\nNo match in /${route} — safe to insert.`);
} finally {
  await client.end();
}

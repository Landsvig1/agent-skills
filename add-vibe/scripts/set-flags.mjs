#!/usr/bin/env node
// Set is_danish / denmark_specific on a freshly inserted row.
//
// None of the three POST endpoints expose these flags, and they are not
// cosmetic: /vibes, /cli, /mcp AND /skills all default to a "Dansk" tab that
// filters on is_danish = true, so a Danish entry left at the default false is
// inserted successfully and then invisible until a visitor switches to "All".
// This replaces the hand-written one-off pg script the SKILL.md used to inline
// three times (one of which was missing the mandatory ssl option).
//
// Run from project root:
//   node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/set-flags.mjs \
//     --catalog <skills|vibes|agents> --id <inserted-id> --danish [--denmark-specific]

import { connect, CATALOGS } from './db.mjs';

const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] ?? null : null;
};

const catalog = get('--catalog');
const id = get('--id');
const denmarkSpecific = args.includes('--denmark-specific');
// denmark_specific implies is_danish — the pair is never (false, true).
const isDanish = args.includes('--danish') || denmarkSpecific;

if (!catalog || !id || !CATALOGS[catalog]) {
  console.error('Usage: set-flags.mjs --catalog <skills|vibes|agents> --id <id> --danish [--denmark-specific]');
  process.exit(1);
}

if (!isDanish) {
  console.error('ERROR: pass --danish (and optionally --denmark-specific). Nothing to do otherwise.');
  process.exit(1);
}

const { table, titleColumn, route } = CATALOGS[catalog];
const client = await connect();

try {
  const { rows } = await client.query(
    `UPDATE public.${table} SET is_danish = $1, denmark_specific = $2 WHERE id = $3
     RETURNING id, ${titleColumn} AS title, is_danish, denmark_specific`,
    [isDanish, denmarkSpecific, id]
  );

  if (!rows.length) {
    console.error(`ERROR: no row with id ${id} in public.${table}`);
    process.exit(1);
  }

  const r = rows[0];
  console.log(`Updated ${r.title} (${r.id}): is_danish=${r.is_danish}, denmark_specific=${r.denmark_specific}`);
  console.log(`Now visible on the default Dansk tab at https://vibetrends.dk/${route}`);
} finally {
  await client.end();
}

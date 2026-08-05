// Shared direct-Postgres connection for the read/flag helpers in this skill.
//
// The insert scripts deliberately go through the real authenticated API. These
// two helpers can't: neither the duplicate pre-check nor is_danish/
// denmark_specific is exposed by any endpoint (see SKILL.md Steps 2a-2c).
//
// Connection rules come from vibetrends-dk/AGENTS.md:
//   - always request TLS (rejectUnauthorized: false — the pooler's chain isn't
//     in Node's default trust store, but the socket is still encrypted)
//   - db.<ref>.supabase.co is IPv6-only; fall back to the IPv4 pooler when
//     there's no working v6 route instead of debugging the network.

import { createRequire } from 'node:module';
import path from 'node:path';

const require = createRequire(path.join(process.cwd(), 'package.json'));
const { Client } = require('pg');

const POOLER_HOST = 'aws-0-eu-west-1.pooler.supabase.com';

/** Connect to the project DB, falling back to the IPv4 pooler if needed. */
export async function connect() {
  const raw = process.env.DATABASE_URL;
  if (!raw) {
    throw new Error('DATABASE_URL must be set in .env.local');
  }
  const url = new URL(raw);

  const direct = new Client({ connectionString: raw, ssl: { rejectUnauthorized: false } });
  try {
    await direct.connect();
    return direct;
  } catch (err) {
    const noRoute = err?.code === 'EHOSTUNREACH' || err?.code === 'ENETUNREACH' || err?.code === 'ETIMEDOUT';
    if (!noRoute) throw err;
    await direct.end().catch(() => {});
  }

  const projectRef = url.hostname.split('.')[1]; // db.<ref>.supabase.co
  const pooled = new Client({
    host: POOLER_HOST,
    port: 5432,
    user: `postgres.${projectRef}`,
    password: decodeURIComponent(url.password),
    database: 'postgres',
    ssl: { rejectUnauthorized: false },
  });
  await pooled.connect();
  return pooled;
}

/** Catalog name -> table, the column holding the canonical URL, and the title column. */
export const CATALOGS = {
  skills: { table: 'skills', urlColumn: 'github_url', titleColumn: 'title_da', route: 'skills' },
  vibes: { table: 'vibes', urlColumn: 'demo_url', titleColumn: 'title_da', route: 'vibes' },
  agents: { table: 'agents', urlColumn: 'source_url', titleColumn: 'name', route: 'cli' },
};

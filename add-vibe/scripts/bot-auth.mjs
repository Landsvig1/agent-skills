// Shared bot/curator authentication for add-vibe.mjs and add-skill.mjs.
// Signs in fresh each call (no token caching) — see KTD2 in
// docs/plans/2026-07-01-001-feat-add-vibe-skills-catalog-plan.md.
//
// Requires BOT_ACCOUNT_EMAIL / BOT_ACCOUNT_PASSWORD and the standard
// NEXT_PUBLIC_SUPABASE_URL / NEXT_PUBLIC_SUPABASE_ANON_KEY in .env.local.

import { createRequire } from 'node:module';
import path from 'node:path';

const require = createRequire(path.join(process.cwd(), 'package.json'));
const { createClient } = require('@supabase/supabase-js');

export async function getBotAccessToken() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  const email = process.env.BOT_ACCOUNT_EMAIL;
  const password = process.env.BOT_ACCOUNT_PASSWORD;

  if (!supabaseUrl || !anonKey) {
    throw new Error('NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY must be set in .env.local');
  }
  if (!email || !password) {
    throw new Error('BOT_ACCOUNT_EMAIL and BOT_ACCOUNT_PASSWORD must be set in .env.local (see add-vibe/SKILL.md prerequisites)');
  }

  const client = createClient(supabaseUrl, anonKey, { auth: { autoRefreshToken: false, persistSession: false } });
  const { data, error } = await client.auth.signInWithPassword({ email, password });

  if (error || !data.session) {
    throw new Error(`Bot account sign-in failed: ${error?.message ?? 'no session returned'}`);
  }

  return data.session.access_token;
}

/** Base URL for the vibetrends.dk API. Override with VIBES_API_BASE_URL for local testing. */
export function getApiBaseUrl() {
  return process.env.VIBES_API_BASE_URL || 'https://vibetrends.dk';
}

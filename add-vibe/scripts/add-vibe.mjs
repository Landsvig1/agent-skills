#!/usr/bin/env node
// Upload a screenshot to Supabase Storage, then insert a row into /vibes via
// the real authenticated POST /api/vibes endpoint (not a direct DB write —
// see docs/plans/2026-07-01-001-feat-add-vibe-skills-catalog-plan.md).
// Run from project root: node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/add-vibe.mjs \
//   --url <demo-url> --title <title> --desc <description> --image /tmp/vibe-<ts>.png

import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { getBotAccessToken, getApiBaseUrl } from './bot-auth.mjs';

// Resolve project deps from node_modules — must run from project root
const require = createRequire(path.join(process.cwd(), 'package.json'));
const { createClient } = require('@supabase/supabase-js');

// --- Arg parsing ---
const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] ?? null : null;
};

const demoUrl = get('--url');
const title   = get('--title');
const desc    = get('--desc');
const image   = get('--image');
const noImage = args.includes('--no-image');

if (!demoUrl || !title || !desc) {
  console.error('Usage: add-vibe.mjs --url <url> --title <title> --desc <desc> --image <path> [--no-image]');
  process.exit(1);
}

if (!noImage && !image) {
  console.error('ERROR: --image <path> is required unless you pass --no-image');
  process.exit(1);
}

// --- Env check (Storage upload still uses the service-role key — scoped to
// Storage only, unrelated to the bot account's own auth) ---
const supabaseUrl    = process.env.NEXT_PUBLIC_SUPABASE_URL;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !serviceRoleKey) {
  console.error('ERROR: NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env.local');
  process.exit(1);
}

// --- Upload image ---
const timestamp = Date.now();
let imageUrl;

if (!noImage) {
  if (!fs.existsSync(image)) {
    console.error(`ERROR: Image file not found: ${image}`);
    process.exit(1);
  }

  const supabase = createClient(supabaseUrl, serviceRoleKey);
  const imageBuffer = fs.readFileSync(image);
  const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40);
  const storagePath = `${timestamp}-${slug}.png`;

  console.log(`Uploading ${storagePath} to vibes-thumbnails...`);
  const { error: uploadError } = await supabase.storage
    .from('vibes-thumbnails')
    .upload(storagePath, imageBuffer, { contentType: 'image/png', upsert: false });

  if (uploadError) {
    console.error('Upload failed:', uploadError.message);
    process.exit(1);
  }

  const { data: { publicUrl } } = supabase.storage.from('vibes-thumbnails').getPublicUrl(storagePath);
  imageUrl = publicUrl;
  console.log('Uploaded:', imageUrl);
}

// --- Authenticated insert via the real API ---
const token = await getBotAccessToken();
const baseUrl = getApiBaseUrl();

const res = await fetch(`${baseUrl}/api/vibes`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    title,
    description: desc,
    demoUrl,
    ...(imageUrl ? { imageUrl } : {}),
  }),
});

const body = await res.json();

if (!res.ok) {
  console.error(`POST /api/vibes failed (${res.status}):`, JSON.stringify(body));
  process.exit(1);
}

console.log(`\nInserted: ${body.id}`);
console.log(`Live at:  https://vibetrends.dk/vibes/${body.id}`);

#!/usr/bin/env node
// One-time setup: creates the vibes-thumbnails public bucket in Supabase Storage.
// Run from project root: node --env-file=.env.local ~/.claude/skills/add-vibe/scripts/setup-storage.mjs

import { createRequire } from 'node:module';
import path from 'node:path';

// Resolve @supabase/supabase-js from the project's node_modules (must run from project root)
const require = createRequire(path.join(process.cwd(), 'package.json'));
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !serviceRoleKey) {
  console.error('ERROR: NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env.local');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, serviceRoleKey);

const { data, error } = await supabase.storage.createBucket('vibes-thumbnails', {
  public: true,
  allowedMimeTypes: ['image/png', 'image/jpeg', 'image/webp'],
});

if (error) {
  if (error.message?.includes('already exists') || error.statusCode === '409') {
    console.log('Bucket "vibes-thumbnails" already exists — nothing to do.');
  } else {
    console.error('Failed to create bucket:', error.message);
    process.exit(1);
  }
} else {
  const { data: urlData } = supabase.storage.from('vibes-thumbnails').getPublicUrl('_check');
  const baseUrl = urlData.publicUrl.replace('/_check', '');
  console.log('Bucket created. Public base URL:', baseUrl);
}

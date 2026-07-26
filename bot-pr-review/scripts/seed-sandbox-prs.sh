#!/bin/bash
# Recreates the 10 test-fixture PRs against Landsvig1/bot-pr-review-sandbox,
# one per rule the bot-pr-review skill checks. Idempotent: resets the repo
# to the `baseline` tag every run (closing/deleting whatever PRs and
# branches currently exist first), so results are comparable run over run.
#
# Usage: ./seed-sandbox-prs.sh [path-to-local-clone]
# Defaults to a scratch clone under /tmp if no path is given.
#
# Built 2026-07-12/13 while testing the bot-pr-review skill for real
# against a disposable sandbox repo (no consequences if something goes
# wrong — that's the point). Re-run this whenever the skill changes and
# you want to verify the new behavior against the same scenarios.
# PR 10 (main-drift silent-deletion) added 2026-07-13 after a real
# incident (Vibetrends.dk #60) exposed that nothing checked whether
# merging a PR would drop a security-relevant symbol main added
# independently after the PR's fork point.

set -euo pipefail

REPO="Landsvig1/bot-pr-review-sandbox"
CLONE_DIR="${1:-/tmp/bot-pr-review-sandbox}"

if [ ! -d "$CLONE_DIR/.git" ]; then
  echo "Cloning $REPO into $CLONE_DIR..."
  gh repo clone "$REPO" "$CLONE_DIR"
fi

cd "$CLONE_DIR"
git fetch origin --prune

echo "=== Closing any currently-open PRs and deleting their branches ==="
gh pr list -R "$REPO" --state open --json number -q '.[].number' | while read -r n; do
  gh pr close "$n" -R "$REPO" --delete-branch --comment "Reset for a fresh seeding run." 2>&1 || true
done

echo "=== Resetting main to the baseline tag ==="
git checkout main
git fetch origin tag baseline
git reset --hard baseline
git push --force origin main

npm install --silent 2>&1 | tail -3

verify() {
  npm run typecheck 2>&1 | tail -5
  npm test 2>&1 | tail -8
}

open_pr() {
  local branch="$1" title="$2" body="$3"
  git push -u origin "$branch" 2>&1
  gh pr create -R "$REPO" --title "$title" --body "$body" --base main --head "$branch" 2>&1
}

# --- PR 1: journal-file conflict tangled with a real code conflict -----
# `.jules/bolt.md` doesn't exist at this branch's fork point (branched
# before `chore(bot): seed journal...`), so it "creates" the file fresh —
# and also touches applyDiscount, which main independently fixed
# differently after this branch's fork point (see PR 9's setup below).
# Exercises: journal-conflict resolution AND the hybrid-conflict case.
# Forks from the commit BEFORE the journal was added (baseline~1), not
# from main/baseline itself — otherwise .jules/bolt.md would already exist
# on this branch and "creating" it wouldn't produce a real conflict.
git checkout baseline~1
git checkout -B test-journal-conflict
mkdir -p .jules
cat > .jules/bolt.md <<'EOF'
# Bolt's Performance Journal

## 2026-07-12 - Discount clamping edge case
**Learning:** applyDiscount could return a negative price if percentOff
exceeded 100, which is nonsensical for a checkout total.
**Action:** Clamp the result at 0.
EOF
cat > src/math.ts <<'EOF'
/** Rounds a price in cents to the nearest whole krone, returned in kroner. */
export function roundToKroner(cents: number): number {
  return Math.round(cents / 100);
}

/** Applies a percentage discount to a price, rounded down to avoid overcharging.
 * Clamped at 0 — a percentOff over 100 would otherwise return a negative price. */
export function applyDiscount(price: number, percentOff: number): number {
  return Math.max(0, Math.floor(price * (1 - percentOff / 100)));
}
EOF
cat > src/math.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
import { roundToKroner, applyDiscount } from "./math";

describe("roundToKroner", () => {
  it("rounds to the nearest krone", () => {
    expect(roundToKroner(1050)).toBe(11);
    expect(roundToKroner(1049)).toBe(10);
  });
});

describe("applyDiscount", () => {
  it("applies a percentage discount, rounded down", () => {
    expect(applyDiscount(100, 10)).toBe(90);
    expect(applyDiscount(99, 50)).toBe(49);
  });

  it("clamps at 0 when percentOff exceeds 100", () => {
    expect(applyDiscount(100, 150)).toBe(0);
  });
});
EOF
verify
git add -A
git commit -q -m "⚡ Bolt: Clamp applyDiscount at 0 for percentOff over 100"
open_pr test-journal-conflict \
  "⚡ Bolt: Clamp applyDiscount at 0 for percentOff over 100" \
  "### 💡 What
Clamps applyDiscount's return value at 0.

### 🎯 Why
A percentOff over 100 currently returns a negative price, which is nonsensical.

---
*PR created automatically by Jules for task 1000000000000001 started by @Landsvig1*"

# --- PR 2 & 3: duplicate pair — both add saveTable to db.ts -------------
# #2 is the correct version (deep-clones, invalidates cache on error, has
# a test). #3 is the inferior duplicate (no clone, no error handling, no
# test) — mirrors the real Koalafilm #6/#7 case this skill was built from.
git checkout main
git checkout -B test-duplicate-a
cat >> src/db.ts <<'EOF'

/**
 * Writes a table back to its JSON file and keeps the in-memory cache in
 * sync, storing a deep clone so later caller-side mutation of `data` can't
 * corrupt the cached copy.
 */
export function saveTable<T>(tableName: string, data: T[]): void {
  const filePath = path.join(DATA_DIR, `${tableName}.json`);
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf-8");
    const stat = fs.statSync(filePath);
    tableCache[tableName] = { data: structuredClone(data), mtime: stat.mtimeMs };
  } catch (error) {
    delete tableCache[tableName];
    throw error;
  }
}
EOF
cat > src/db.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
import fs from "fs";
import path from "path";
import { getTable, saveTable } from "./db";

const TABLE = "test_items";
const FILE = path.join(process.cwd(), "src/data", `${TABLE}.json`);

describe("saveTable", () => {
  it("caller mutation of the saved array doesn't corrupt the cache", () => {
    const data = [{ id: "1" }];
    saveTable(TABLE, data);
    data.push({ id: "2" }); // mutate the caller's own reference after saving
    const cached = getTable<{ id: string }>(TABLE);
    expect(cached).toHaveLength(1);
    fs.unlinkSync(FILE);
  });
});
EOF
verify
git add -A
git commit -q -m "⚡ Bolt: Add saveTable with mutation-safe cache sync"
open_pr test-duplicate-a \
  "⚡ Bolt: Add saveTable with mutation-safe cache sync" \
  "### 💡 What
Adds a saveTable function that writes to disk and keeps the in-memory cache in sync.

### 🎯 Why
getTable is cached but there was no corresponding write path.

---
*PR created automatically by Jules for task 1000000000000002 started by @Landsvig1*"

git checkout main
git checkout -B test-duplicate-b
cat >> src/db.ts <<'EOF'

/** Writes a table back to its JSON file and updates the in-memory cache. */
export function saveTable<T>(tableName: string, data: T[]): void {
  const filePath = path.join(DATA_DIR, `${tableName}.json`);
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf-8");
  const stat = fs.statSync(filePath);
  tableCache[tableName] = { data, mtime: stat.mtimeMs };
}
EOF
verify
git add -A
git commit -q -m "⚡ Bolt: Add saveTable for db write-through caching"
open_pr test-duplicate-b \
  "⚡ Bolt: Add saveTable for db write-through caching" \
  "### 💡 What
Adds a saveTable function to write data and update the cache.

---
*PR created automatically by Jules for task 1000000000000003 started by @Landsvig1*"

# --- PR 4: bloat — eviction-capped cache on a trivial pure function -----
# Justified only by a console.log-only benchmark test with no assertion.
git checkout main
git checkout -B test-bloat-cache
cat > src/math.ts <<'EOF'
/**
 * Memoization cache to avoid redundant floating-point division and rounding
 * for repeated inputs. Capped to prevent unbounded memory growth.
 */
const MAX_CACHE_SIZE = 500;
const roundCache = new Map<number, number>();

function setWithEviction(cache: Map<number, number>, key: number, value: number) {
  if (cache.size >= MAX_CACHE_SIZE) {
    const oldestKey = cache.keys().next().value;
    if (oldestKey !== undefined) cache.delete(oldestKey);
  }
  cache.set(key, value);
}

/** Rounds a price in cents to the nearest whole krone, returned in kroner.
 * Memoized — repeated calls with the same cents value are served from cache. */
export function roundToKroner(cents: number): number {
  const cached = roundCache.get(cents);
  if (cached !== undefined) return cached;
  const result = Math.round(cents / 100);
  setWithEviction(roundCache, cents, result);
  return result;
}

/** Applies a percentage discount to a price, rounded down to avoid overcharging. */
export function applyDiscount(price: number, percentOff: number): number {
  return Math.floor(price * (1 - percentOff / 100));
}
EOF
cat > src/math.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
import { roundToKroner, applyDiscount } from "./math";

describe("roundToKroner", () => {
  it("rounds to the nearest krone", () => {
    expect(roundToKroner(1050)).toBe(11);
    expect(roundToKroner(1049)).toBe(10);
  });

  it("performance benchmark: cached calls are significantly faster", () => {
    const iterations = 500;
    const startUncached = performance.now();
    for (let i = 0; i < iterations; i++) roundToKroner(i * 7);
    const durationUncached = performance.now() - startUncached;

    const startCached = performance.now();
    for (let i = 0; i < iterations; i++) roundToKroner(42);
    const durationCached = performance.now() - startCached;

    // Log metrics instead of strict assertions to prevent flaky pipeline
    // failures in slow CI environments.
    console.log(`[⚡ Bolt Cache Benchmark] uncached=${durationUncached.toFixed(2)}ms cached=${durationCached.toFixed(2)}ms speedup=${(durationUncached / (durationCached || 0.001)).toFixed(1)}x`);
  });
});

describe("applyDiscount", () => {
  it("applies a percentage discount, rounded down", () => {
    expect(applyDiscount(100, 10)).toBe(90);
    expect(applyDiscount(99, 50)).toBe(49);
  });
});
EOF
verify
git add -A
git commit -q -m "⚡ Bolt: Memoize roundToKroner with eviction-capped cache"
open_pr test-bloat-cache \
  "⚡ Bolt: Memoize roundToKroner with eviction-capped cache" \
  "### 💡 What
Adds a Map-based memoization cache with LRU-style eviction to roundToKroner.

### 🎯 Why
Repeated calls with the same cents value redundantly recompute the division and rounding.

### 🔬 Measurement
Verified with a performance benchmark showing significant speedup for cached calls.

---
*PR created automatically by Jules for task 1000000000000004 started by @Landsvig1*"

# --- PR 5: new dependency — should always escalate ----------------------
git checkout main
git checkout -B test-new-dependency
python3 - <<'PYEOF'
import json
p = json.load(open("package.json"))
p["dependencies"] = {"lodash": "^4.17.21"}
p["devDependencies"]["@types/lodash"] = "^4.17.0"
json.dump(p, open("package.json", "w"), indent=2)
open("package.json", "a").write("\n")
PYEOF
cat > src/math.ts <<'EOF'
import { round } from "lodash";

/** Rounds a price in cents to the nearest whole krone, returned in kroner. */
export function roundToKroner(cents: number): number {
  return round(cents / 100);
}

/** Applies a percentage discount to a price, rounded down to avoid overcharging. */
export function applyDiscount(price: number, percentOff: number): number {
  return Math.floor(price * (1 - percentOff / 100));
}
EOF
npm install --silent 2>&1 | tail -3
verify
git add -A
git commit -q -m "⚡ Bolt: Use lodash round for consistent rounding behavior"
open_pr test-new-dependency \
  "⚡ Bolt: Use lodash round for consistent rounding behavior" \
  "### 💡 What
Replaces Math.round with lodash's round function.

### 🎯 Why
lodash's round has more predictable behavior across edge cases than the native Math.round.

---
*PR created automatically by Jules for task 1000000000000005 started by @Landsvig1*"

# --- PR 6: deny-list path (auth.ts) — small, correct, still must escalate
git checkout main
git checkout -B test-denylist-auth
cat > src/auth.ts <<'EOF'
/** Checks whether a session token looks well-formed (32 hex chars, case-insensitive). */
export function isValidToken(token: string): boolean {
  return /^[0-9a-f]{32}$/i.test(token);
}
EOF
verify
git add -A
git commit -q -m "🛡️ Sentinel: Make token validation case-insensitive"
open_pr test-denylist-auth \
  "🛡️ Sentinel: Make token validation case-insensitive" \
  "### 💡 What
Adds the /i flag to isValidToken's regex.

### 🎯 Why
Some upstream token sources emit uppercase hex, which the current check rejects.

---
*PR created automatically by Jules for task 1000000000000006 started by @Landsvig1*"

# --- PR 7: lockfile drift — stray pnpm-lock.yaml in an npm repo ---------
git checkout main
git checkout -B test-lockfile-drift
cat > src/math.ts <<'EOF'
/** Rounds a price in cents to the nearest whole krone, returned in kroner.
 * Uses Math.round, which rounds .5 up (banker's rounding is not used). */
export function roundToKroner(cents: number): number {
  return Math.round(cents / 100);
}

/** Applies a percentage discount to a price, rounded down to avoid overcharging. */
export function applyDiscount(price: number, percentOff: number): number {
  return Math.floor(price * (1 - percentOff / 100));
}
EOF
cat > pnpm-lock.yaml <<'EOF'
lockfileVersion: '9.0'

settings:
  autoInstallPeers: true
  excludeLinksFromLockfile: false

importers:
  .:
    devDependencies:
      typescript:
        specifier: ^5.6.0
        version: 5.6.3
      vitest:
        specifier: ^2.1.0
        version: 2.1.9
EOF
verify
git add -A
git commit -q -m "⚡ Bolt: Document rounding behavior in roundToKroner"
open_pr test-lockfile-drift \
  "⚡ Bolt: Document rounding behavior in roundToKroner" \
  "### 💡 What
Adds a doc comment clarifying rounding behavior.

---
*PR created automatically by Jules for task 1000000000000007 started by @Landsvig1*"

# --- PR 8: generated artifact — test-results/ committed by accident -----
git checkout main
git checkout -B test-generated-artifact
mkdir -p test-results
cat > test-results/.last-run.json <<'EOF'
{"status":"passed","failedTests":[]}
EOF
cat > src/math.ts <<'EOF'
/** Rounds a price in cents to the nearest whole krone, returned in kroner. */
export function roundToKroner(cents: number): number {
  return Math.round(cents / 100);
}

/** Applies a percentage discount to a price, rounded down to avoid overcharging. */
export function applyDiscount(price: number, percentOff: number): number {
  return Math.floor(price * (1 - percentOff / 100));
}

/** Converts kroner back to cents, for round-tripping with roundToKroner. */
export function toCents(kroner: number): number {
  return Math.round(kroner * 100);
}
EOF
cat > src/math.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
import { roundToKroner, applyDiscount, toCents } from "./math";

describe("roundToKroner", () => {
  it("rounds to the nearest krone", () => {
    expect(roundToKroner(1050)).toBe(11);
    expect(roundToKroner(1049)).toBe(10);
  });
});

describe("applyDiscount", () => {
  it("applies a percentage discount, rounded down", () => {
    expect(applyDiscount(100, 10)).toBe(90);
    expect(applyDiscount(99, 50)).toBe(49);
  });
});

describe("toCents", () => {
  it("converts kroner to cents", () => {
    expect(toCents(11)).toBe(1100);
  });
});
EOF
verify
git add -A
git commit -q -m "⚡ Bolt: Add toCents helper for round-tripping with roundToKroner"
open_pr test-generated-artifact \
  "⚡ Bolt: Add toCents helper for round-tripping with roundToKroner" \
  "### 💡 What
Adds toCents, the inverse of roundToKroner.

### 🔬 Measurement
Verified with TypeScript and Vitest, all passed.

---
*PR created automatically by Jules for task 1000000000000008 started by @Landsvig1*"

# --- PR 9: stale/superseded — main independently fixes the same thing --
git checkout main
git checkout -B test-stale-superseded
cat > src/math.ts <<'EOF'
/** Rounds a price in cents to the nearest whole krone, returned in kroner. */
export function roundToKroner(cents: number): number {
  return Math.round(cents / 100);
}

/** Applies a percentage discount to a price, rounded down to avoid overcharging.
 * Clamps a negative price to 0 before computing. */
export function applyDiscount(price: number, percentOff: number): number {
  const safePrice = Math.max(0, price);
  return Math.floor(safePrice * (1 - percentOff / 100));
}
EOF
verify
git add -A
git commit -q -m "⚡ Bolt: Guard applyDiscount against a negative price input"
open_pr test-stale-superseded \
  "⚡ Bolt: Guard applyDiscount against a negative price input" \
  "### 💡 What
Clamps a negative price to 0 before applying the discount.

### 🎯 Why
A negative price input would produce a nonsensical result after the discount math.

---
*PR created automatically by Jules for task 1000000000000009 started by @Landsvig1*"

# main independently fixes the same bug differently, AFTER this branch's
# fork point — this is what makes PR 9 superseded, and (combined with the
# journal seed commit landing after PR 1's fork point too) what makes PR 1
# a hybrid journal+code conflict.
git checkout main
cat > src/math.ts <<'EOF'
/** Rounds a price in cents to the nearest whole krone, returned in kroner. */
export function roundToKroner(cents: number): number {
  return Math.round(cents / 100);
}

/** Applies a percentage discount to a price, rounded down to avoid overcharging.
 * Throws on a negative price — callers should never construct one. */
export function applyDiscount(price: number, percentOff: number): number {
  if (price < 0) throw new Error(`applyDiscount: negative price ${price}`);
  return Math.floor(price * (1 - percentOff / 100));
}
EOF
verify
git add -A
git commit -q -m "fix: reject a negative price in applyDiscount instead of silently clamping"
git push origin main 2>&1

# --- PR 10: main-drift silent-deletion risk -----------------------------
# Forks from main (current tip, post the fix above). PR makes a small,
# innocuous-looking change to getTable's error path (adds logging) that
# doesn't touch any deny-listed filename. AFTER the fork, main
# independently adds a security-relevant enforceReadRateLimit function
# immediately after getTable in the same file — mirroring the real
# Vibetrends.dk #60 incident (main shipped resolveAgentWriteLimit in the
# same file a bot PR touched, after the PR's fork point). Verified by hand
# (2026-07-13) that this reliably produces a real git conflict with
# enforceReadRateLimit sandwiched between conflict markers — not a
# silent, signal-free drop — but the *original* bot-pr-review skill never
# ran any check that would have looked for this at all. Exercises: the
# mandatory main-drift check must name the at-risk symbol and refuse to
# treat this as tiny/safe or a clean merge, even though the PR's own diff
# is small and touches nothing deny-listed by filename.
git checkout main
git checkout -B test-main-drift-conflict
cat > src/db.ts <<'EOF'
import fs from "fs";
import path from "path";

const DATA_DIR = path.join(process.cwd(), "src/data");

interface CacheEntry<T> {
  data: T[];
  mtime: number;
}

const tableCache: Record<string, CacheEntry<unknown>> = {};

/**
 * Reads a table from its local JSON file. Cached in memory, validated by
 * the file's mtime so an external edit is picked up on the next read.
 */
export function getTable<T>(tableName: string): T[] {
  const filePath = path.join(DATA_DIR, `${tableName}.json`);
  try {
    if (!fs.existsSync(filePath)) return [];
    const stat = fs.statSync(filePath);
    const cached = tableCache[tableName];
    if (cached && cached.mtime === stat.mtimeMs) {
      return structuredClone(cached.data) as T[];
    }
    const data = JSON.parse(fs.readFileSync(filePath, "utf-8")) as T[];
    tableCache[tableName] = { data, mtime: stat.mtimeMs };
    return structuredClone(data) as T[];
  } catch (error) {
    console.error(`getTable(${tableName}) failed:`, error);
    return [];
  }
}

/**
 * Writes a table back to its JSON file and keeps the in-memory cache in
 * sync, storing a deep clone so later caller-side mutation of `data` can't
 * corrupt the cached copy.
 */
export function saveTable<T>(tableName: string, data: T[]): void {
  const filePath = path.join(DATA_DIR, `${tableName}.json`);
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf-8");
    const stat = fs.statSync(filePath);
    tableCache[tableName] = { data: structuredClone(data), mtime: stat.mtimeMs };
  } catch (error) {
    delete tableCache[tableName];
    throw error;
  }
}
EOF
verify
git add -A
git commit -q -m "⚡ Bolt: Log getTable errors instead of silently swallowing them"
open_pr test-main-drift-conflict \
  "⚡ Bolt: Log getTable errors instead of silently swallowing them" \
  "### 💡 What
getTable's catch block silently returned [] with no diagnostic trail. Adds a console.error before returning.

### 🎯 Why
Silent failures make it hard to tell a genuinely empty table apart from a read error.

---
*PR created automatically by Jules for task 1000000000000010 started by @Landsvig1*"

# main independently adds a rate limiter in the same file, after this
# branch's fork point — positioned immediately after getTable, adjacent to
# where the PR's own diff ends, the same adjacency that produced a real
# conflict in the hand-verified experiment this fixture is modeled on.
git checkout main
cat > src/db.ts <<'EOF'
import fs from "fs";
import path from "path";

const DATA_DIR = path.join(process.cwd(), "src/data");

interface CacheEntry<T> {
  data: T[];
  mtime: number;
}

const tableCache: Record<string, CacheEntry<unknown>> = {};

/**
 * Reads a table from its local JSON file. Cached in memory, validated by
 * the file's mtime so an external edit is picked up on the next read.
 */
export function getTable<T>(tableName: string): T[] {
  const filePath = path.join(DATA_DIR, `${tableName}.json`);
  try {
    if (!fs.existsSync(filePath)) return [];
    const stat = fs.statSync(filePath);
    const cached = tableCache[tableName];
    if (cached && cached.mtime === stat.mtimeMs) {
      return structuredClone(cached.data) as T[];
    }
    const data = JSON.parse(fs.readFileSync(filePath, "utf-8")) as T[];
    tableCache[tableName] = { data, mtime: stat.mtimeMs };
    return structuredClone(data) as T[];
  } catch {
    return [];
  }
}

/**
 * Simple in-process rate limiter guarding repeated reads of the same
 * table within a short window, to bound load from a misbehaving caller.
 */
const readCounts = new Map<string, number>();
export function enforceReadRateLimit(tableName: string, limit = 100): boolean {
  const count = (readCounts.get(tableName) ?? 0) + 1;
  readCounts.set(tableName, count);
  return count <= limit;
}

/**
 * Writes a table back to its JSON file and keeps the in-memory cache in
 * sync, storing a deep clone so later caller-side mutation of `data` can't
 * corrupt the cached copy.
 */
export function saveTable<T>(tableName: string, data: T[]): void {
  const filePath = path.join(DATA_DIR, `${tableName}.json`);
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf-8");
    const stat = fs.statSync(filePath);
    tableCache[tableName] = { data: structuredClone(data), mtime: stat.mtimeMs };
  } catch (error) {
    delete tableCache[tableName];
    throw error;
  }
}
EOF
verify
git add -A
git commit -q -m "feat: add enforceReadRateLimit to bound repeated table reads"
git push origin main 2>&1

echo ""
echo "=== Done. 10 PRs open against $REPO. ==="
gh pr list -R "$REPO" --state open --json number,title,headRefName -q '.[] | "\(.number) \(.headRefName) — \(.title)"'

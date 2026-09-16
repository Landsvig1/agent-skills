/**
 * Screenshot a vibe past its intro animation / onboarding modal / cookie wall.
 * The add-vibe recipe (--wait-for-timeout 2000) captures whatever interstitial
 * is on screen at 2s, which is how hej-data and digital-arv got splash screens.
 */
import { chromium } from 'playwright';

const [url, out] = process.argv.slice(2);
const SKIP = /^(spring over|skip|videre|fortsæt|continue|accepter|accept|tillad alle|ok|luk|got it)$/i;

const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(url, { waitUntil: 'networkidle', timeout: 45000 });

// Dismiss up to 3 stacked interstitials, newest first.
for (let i = 0; i < 3; i++) {
  const btn = p.locator('button, a[role=button], [role=button]')
    .filter({ hasText: SKIP }).last();
  if (await btn.count() && await btn.isVisible().catch(() => false)) {
    await btn.click({ timeout: 3000 }).catch(() => {});
    await p.waitForTimeout(1200);
  } else break;
}
await p.keyboard.press('Escape').catch(() => {});
await p.waitForTimeout(2500);          // let any fade-in settle
await p.screenshot({ path: out });
console.log(`shot ${url} -> ${out}`);
await b.close();

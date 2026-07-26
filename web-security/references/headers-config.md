# Security headers for Next.js — copy-paste configs

## Tier 1: next.config.js headers() — works with SSG/ISR

```js
// next.config.js
const isDev = process.env.NODE_ENV === "development";

// Adjust the allowlists to the third parties the site actually uses.
const csp = [
  "default-src 'self'",
  `script-src 'self' ${isDev ? "'unsafe-eval'" : ""} https://plausible.io`,
  "style-src 'self' 'unsafe-inline'", // Tailwind/next inline styles; tighten if possible
  "img-src 'self' blob: data: https:",
  "font-src 'self'",
  "connect-src 'self' https://plausible.io https://*.supabase.co wss://*.supabase.co",
  "frame-src 'self' https://www.youtube-nocookie.com",
  "frame-ancestors 'none'",
  "form-action 'self'",
  "base-uri 'self'",
  "object-src 'none'",
  "upgrade-insecure-requests",
].join("; ");

const securityHeaders = [
  { key: "Content-Security-Policy", value: csp },
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" }, // legacy duplicate of frame-ancestors
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(), browsing-topics=()" },
];

module.exports = {
  async headers() {
    return [{ source: "/(.*)", headers: securityHeaders }];
  },
};
```

Why each directive matters:

- `frame-ancestors 'none'` — clickjacking. Keep `X-Frame-Options` too for old browsers.
- `object-src 'none'`, `base-uri 'self'` — close legacy injection vectors that are
  free to close.
- `connect-src` — controls where fetch/XHR/websockets may go; include your Supabase
  project and analytics endpoint, nothing else. This is your exfiltration guard.
- `form-action 'self'` — stops injected forms posting credentials elsewhere.
- HSTS `preload` — only set once you're sure all subdomains are HTTPS forever;
  submission to the preload list is effectively irreversible.

Rollout tip: start with `Content-Security-Policy-Report-Only` + a `report-to`
endpoint for a week on busy sites, then enforce. For small sites, enforce directly
and click through every page with the console open.

## Tier 2: nonce-based strict CSP in middleware/proxy

File is `middleware.ts` up to Next.js 15, `proxy.ts` from Next.js 16 (same API).
Forces dynamic rendering on matched routes — scope the matcher to authenticated
sections and keep marketing pages on Tier 1.

```ts
// middleware.ts (or proxy.ts on Next 16+)
import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString("base64");
  const csp = [
    "default-src 'self'",
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'`,
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' blob: data:",
    "connect-src 'self' https://*.supabase.co wss://*.supabase.co",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "object-src 'none'",
  ].join("; ");

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-nonce", nonce);
  requestHeaders.set("Content-Security-Policy", csp);

  const response = NextResponse.next({ request: { headers: requestHeaders } });
  response.headers.set("Content-Security-Policy", csp);
  return response;
}

export const config = {
  matcher: [{ source: "/((?!_next/static|_next/image|favicon.ico).*)" }],
};
```

Next.js reads the nonce from the request header and applies it to its own scripts.
For your own inline scripts, read it server-side:

```tsx
import { headers } from "next/headers";
const nonce = (await headers()).get("x-nonce");
// <Script nonce={nonce} ...>
```

`'strict-dynamic'` lets nonce-trusted scripts load their own dependencies, which is
what makes third-party tags workable under strict CSP.

## Verifying

- https://securityheaders.com — aim for A. (A+ requires CSP without `unsafe-inline`
  in style-src; nice but rarely worth fighting Tailwind for.)
- Browser console on every page type — CSP violations log loudly.
- `curl -sI` both the apex and a deep route — confirm headers apply everywhere,
  including API routes and the 404 page.

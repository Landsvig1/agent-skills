---
name: seo-nextjs
description: >
  Audit and implement technical SEO for Next.js sites: metadata API, sitemaps, robots,
  structured data (JSON-LD), Open Graph images, canonicals, internationalization
  (hreflang), and indexing diagnostics. Use this skill whenever the user mentions SEO,
  search rankings, Google indexing, meta tags, sitemap, structured data, schema.org,
  Open Graph, social previews, "not showing up on Google", or when creating new public
  pages, blogs, or landing pages — even if SEO isn't mentioned, public pages need
  metadata.
---

# Technical SEO for Next.js

This skill covers the *technical* layer: making every page maximally crawlable,
indexable, and rich-result-eligible. Content strategy (keyword research, copywriting)
is out of scope — for that, suggest installing a dedicated public skill set, e.g.
`npx skills add aaron-he-zhu/seo-geo-claude-skills` or
`npx skills add coreyhaines31/marketingskills`. Performance is a ranking factor —
coordinate with the web-performance skill (Core Web Vitals targets live there).

## Phase 1: Audit

1. **Indexing reality check.** `site:domain.dk` on Google; Search Console (if
   connected) → coverage report. Pages missing? Find out why before touching meta tags.
2. **Crawl basics.** `curl -s domain.dk/robots.txt` and `/sitemap.xml` — exist,
   correct, referenced from robots? Staging/preview deployments leaking into the
   index? (Vercel preview URLs should have `X-Robots-Tag: noindex` — Vercel sets this
   automatically; verify.)
3. **Per-page metadata.** For each route: unique title (~50–60 chars) and description
   (~150–160), canonical URL, OG/Twitter tags, correct `<html lang>`. Grep for pages
   with no `metadata` export / `generateMetadata` at all.
4. **Rendering.** View-source (not devtools) on key pages — is the content in the
   initial HTML? Server-rendered Next.js usually passes; client-only data fetching on
   public content pages is an SEO bug.
5. **Structured data.** Test key templates in Google's Rich Results Test. Missing
   JSON-LD on articles/products/FAQs = missed rich results.
6. **Links & status codes.** Internal 404s/redirect chains; orphan pages (in sitemap
   but linked from nowhere); descriptive anchor text; trailing-slash consistency.

## Phase 2: Implement

### Metadata (App Router)

Root layout: `metadataBase`, title template, site-wide defaults. Per page:

```tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,                       // template appends site name
    description: post.summary,
    alternates: { canonical: `/blog/${post.slug}` },
    openGraph: { title: post.title, description: post.summary, type: "article",
                 publishedTime: post.date, images: [`/blog/${post.slug}/og.png`] },
  };
}
```

Rules: every public page has unique title/description; canonicals everywhere
(self-referencing is fine and prevents query-param duplicates); `noindex` via
`robots: { index: false }` for thin pages (search results, filtered lists, thank-you
pages).

### Sitemap & robots

`app/sitemap.ts` and `app/robots.ts` (dynamic, generated from the CMS/DB so new
content appears automatically). Sitemap: only canonical, indexable, 200-status URLs —
no redirects, no noindexed pages. `lastModified` from real data. Robots: disallow
only what genuinely shouldn't be crawled (`/api/`, `/admin/`); reference the sitemap.

### Structured data (JSON-LD)

Render a `<script type="application/ld+json">` from typed objects (consider
`schema-dts`). Priority types: `Organization`/`WebSite` (root), `Article`/
`BlogPosting`, `Product` + `Offer`, `FAQPage`, `BreadcrumbList`, `LocalBusiness`
where applicable. Only mark up content that's visibly on the page — invisible markup
risks manual actions. Validate with the Rich Results Test.

### OG images

Dynamic per-page OG images with `next/og` `ImageResponse` in
`app/.../opengraph-image.tsx` — title on brand background beats a generic logo for
CTR on shares. 1200×630, text legible at thumbnail size.

### Internationalization (relevant for DK + EN sites)

- One URL per language (`/da/...`, `/en/...` or separate domains), `<html lang>`
  per locale.
- `alternates.languages` in metadata generates hreflang; include `x-default`.
  Every language version must link to *all* others, bidirectionally.
- Don't auto-redirect by IP/Accept-Language on crawlable pages (Googlebot crawls
  mostly from the US and would never see the Danish version); suggest, don't force.

## Phase 3: Verify

View-source on each template: title, description, canonical, JSON-LD present in raw
HTML. Rich Results Test on each JSON-LD template. `sitemap.xml` parses and contains
only 200-status canonical URLs (script it: fetch each, assert status). OG preview
via social card debuggers. After deploy: submit sitemap in Search Console, then check
coverage again after a week — indexing is the metric, everything else is means.

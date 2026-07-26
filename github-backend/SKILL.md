---
name: github-backend
description: Use this skill whenever the user wants to build a CMS, blog, portfolio, waitlist, or simple web app AND wants to avoid setting up a database (Supabase/Postgres). Implements a serverless Git-as-a-database architecture for Next.js.
---

# GitHub Backend (/github-backend)

Use GitHub as the single source of truth for dynamic data, storing content as Markdown, MDX, or JSON.

## Core Architectural Paths

### Path A: Visual CMS (Keystatic)
*For human-edited content without touching code.*

1. **Install**: `@keystatic/core`, `@keystatic/next`, `@markdoc/markdoc`.
2. **Config**: `keystatic.config.ts` with `storage: { kind: 'github', repo: { owner: 'USERNAME', name: 'REPO' } }`.
3. **Routing**: 
   - UI: `app/keystatic/[[...params]]/page.tsx`
   - API: `app/api/keystatic/[[...params]]/route.ts`
4. **Data**: Use `createReader` for local/build-time fetching.

### Path B: Programmatic (Octokit REST)
*For user-generated data (forms, waitlists) saved as JSON.*

1. **Install**: `@octokit/rest`.
2. **Auth**: GitHub PAT in `.env` as `GITHUB_ACCESS_TOKEN`. Use strictly in Server Actions/Components.
3. **Writing Data**:
   Always isolate generated data in a specific folder (e.g., `data/submissions/`). 
   To update a file, you MUST retrieve its `sha` first:
   ```typescript
   const octokit = new Octokit({ auth: process.env.GITHUB_ACCESS_TOKEN });
   let sha;
   try {
     const { data } = await octokit.rest.repos.getContent({ owner, repo, path });
     sha = (data as any).sha;
   } catch (e) { /* File doesn't exist yet */ }
   
   await octokit.rest.repos.createOrUpdateFileContents({
     owner, repo, path,
     message: 'Update data',
     content: Buffer.from(JSON.stringify(payload)).toString('base64'),
     sha // Required if file exists
   });
   ```

## Performance & Cache Strategy (Critical)

GitHub allows 5,000 requests/hour. **Never poll.**

1. **Fetching**: Use `fetch('https://raw.githubusercontent.com/...', { next: { tags: ['github-data'] } })`.
2. **Invalidation**: Create `app/api/webhook/github/route.ts` to listen for `push` events and call `revalidateTag('github-data')`.
3. **Security**: You MUST verify the `x-hub-signature-256` header using the Webhook secret to prevent unauthorized cache invalidation.

---
name: gitlab-backend
description: Use this skill whenever the user wants to build a CMS, blog, portfolio, waitlist, form submission, or simple web app using GitLab as a database/headless CMS (GitLab.com or self-hosted) and wants to avoid setting up a database (Supabase/Postgres). Implements a serverless Git-as-a-database architecture for Next.js.
---

# GitLab Backend (/gitlab-backend)

Use GitLab as the single source of truth for dynamic application data, storing content as Markdown, MDX, or JSON. Supports both cloud (GitLab.com) and self-hosted instances.

## Core Architectural Paths

### Path A: Visual CMS (Decap CMS or Sveltia CMS)
*For non-technical editors to manage content via a GUI without code changes.*
*(Note: Keystatic cloud mode is GitHub-only; use Decap CMS or Sveltia CMS for native GitLab integration).*

1. **Setup Admin Shell**: Create `public/admin/index.html` loading Decap or Sveltia CMS script.
2. **Config (`public/admin/config.yml`)**:
   ```yaml
   backend:
     name: gitlab
     repo: group/project-name # or numeric project ID
     auth_type: implicit     # or pkce
     app_id: YOUR_GITLAB_APPLICATION_ID # OAuth app created in GitLab User/Group settings
     api_root: https://gitlab.com/api/v4 # Change to self-hosted domain if applicable
     branch: main
   media_folder: public/uploads
   public_folder: /uploads
   collections:
     - name: posts
       label: Posts
       folder: content/posts
       create: true
       fields:
         - { name: title, label: Title, widget: string }
         - { name: date, label: Date, widget: datetime }
         - { name: body, label: Body, widget: markdown }
   ```

---

### Path B: Programmatic (GitBeaker / Commits API)
*For user-generated data (forms, waitlists, feedback) stored directly as JSON in the repo.*

1. **Install SDK**:
   ```bash
   npm install @gitbeaker/rest
   ```

2. **Environment & Auth**:
   Set in `.env.local` (server-side only, never expose to client):
   ```env
   GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx # Project Access Token (recommended) or PAT
   GITLAB_PROJECT_ID=12345678              # Numeric project ID or URL-encoded 'group%2Frepo'
   GITLAB_HOST=https://gitlab.com          # Or 'https://gitlab.yourcompany.com'
   GITLAB_WEBHOOK_SECRET=your-random-secret
   ```
   > **Auth Best Practice**: Use a **Project Access Token** with `write_repository` (or `api`) scope and Maintainer/Developer role instead of a personal account token.

3. **Writing Data (Atomic Commits API)**:
   GitLab's Commits API allows atomic single-file or multi-file operations in one commit without manually retrieving existing blob SHAs:

   ```typescript
   // lib/gitlab.ts
   import { Gitlab } from '@gitbeaker/rest';

   export const gitlab = new Gitlab({
     host: process.env.GITLAB_HOST || 'https://gitlab.com',
     token: process.env.GITLAB_TOKEN,
   });
   ```

   ```typescript
   // app/actions/submit-form.ts
   'use server';

   import { gitlab } from '@/lib/gitlab';

   export async function submitWaitlist(formData: FormData) {
     const email = formData.get('email') as string;
     if (!email) throw new Error('Email is required');

     const projectId = process.env.GITLAB_PROJECT_ID!;
     const id = crypto.randomUUID();
     const filePath = `data/waitlist/${Date.now()}-${id}.json`;
     const payload = { id, email, createdAt: new Date().toISOString() };

     await gitlab.Commits.create(
       projectId,
       'main',
       `chore(waitlist): add entry ${email}`,
       [
         {
           action: 'create',
           filePath,
           content: JSON.stringify(payload, null, 2),
         },
       ]
     );

     return { success: true };
   }
   ```

4. **Updating an Existing File**:
   If modifying an existing single file (e.g., an aggregated `data/waitlist.json` array):
   ```typescript
   // Read file content first
   const file = await gitlab.RepositoryFiles.show(projectId, 'data/waitlist.json', 'main');
   const existingData = JSON.parse(Buffer.from(file.content, 'base64').toString('utf-8'));

   existingData.push(newItem);

   await gitlab.Commits.create(
     projectId,
     'main',
     'update waitlist.json',
     [
       {
         action: 'update',
         filePath: 'data/waitlist.json',
         content: JSON.stringify(existingData, null, 2),
       },
     ]
   );
   ```
   *Tip*: Prefer appending new individual JSON files (event-sourcing style) in a folder (`data/waitlist/`) rather than modifying a single shared JSON file to avoid write collisions.

---

## Reading Data & Cache Strategy (Critical)

GitLab API has rate limits (2,000 req/min default on SaaS, configurable on self-hosted). **Never poll.**

### 1. Fetching Data with Tagged Caching
For private repositories, authenticate the raw request using the `PRIVATE-TOKEN` header:

```typescript
// lib/get-data.ts
export async function getGitLabFile<T>(filePath: string): Promise<T> {
  const host = process.env.GITLAB_HOST || 'https://gitlab.com';
  const projectId = encodeURIComponent(process.env.GITLAB_PROJECT_ID!);
  const encodedPath = encodeURIComponent(filePath);

  const res = await fetch(
    `${host}/api/v4/projects/${projectId}/repository/files/${encodedPath}/raw?ref=main`,
    {
      headers: {
        'PRIVATE-TOKEN': process.env.GITLAB_TOKEN || '',
      },
      next: {
        tags: ['gitlab-data'],
        revalidate: false, // Cached until invalidated by webhook
      },
    }
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch ${filePath}: ${res.statusText}`);
  }

  return res.json() as Promise<T>;
}
```

### 2. Cache Invalidation Webhook
Create `app/api/webhook/gitlab/route.ts` to invalidate Next.js cache on git pushes:

```typescript
// app/api/webhook/gitlab/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { revalidateTag } from 'next/cache';

export async function POST(req: NextRequest) {
  // GitLab passes secret as a plain string in X-Gitlab-Token
  const gitlabToken = req.headers.get('x-gitlab-token');
  const expectedSecret = process.env.GITLAB_WEBHOOK_SECRET;

  if (!expectedSecret || gitlabToken !== expectedSecret) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const event = req.headers.get('x-gitlab-event');
  if (event === 'Push Hook') {
    // Invalidate cached data tags
    revalidateTag('gitlab-data');
    return NextResponse.json({ revalidated: true, event });
  }

  return NextResponse.json({ message: 'Ignored event' }, { status: 200 });
}
```

### 3. GitLab Webhook Configuration
1. In GitLab, navigate to **Settings > Webhooks**.
2. **URL**: `https://your-domain.com/api/webhook/gitlab`
3. **Secret Token**: Paste the string configured in `GITLAB_WEBHOOK_SECRET`.
4. **Trigger**: Check **Push events** (restrict branch to `main` if desired).
5. Enable SSL verification and click **Add webhook**.

---

## Key Gotchas & Rules

1. **Path Encoding**: Both the project identifier (`group/project` -> `group%2Fproject`) and file path (`data/sub.json` -> `data%2Fsub.json`) must be URL-encoded when hitting the REST API directly. `@gitbeaker/rest` handles most encoding automatically, but native `fetch` requires explicit `encodeURIComponent`.
2. **Branch Protection**: Ensure the Project Access Token role (Developer vs Maintainer) has permission to push directly to the target branch (`main`), or set up an allowed push rule.
3. **Concurrent Writes**: Always write discrete files per submission (e.g. `data/submissions/[id].json`) instead of appending to one shared array file to prevent lock errors and commit conflicts.

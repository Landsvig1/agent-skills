# Reference: Decision & Tradeoff Surfaces

When presenting architecture choices, tech stack selections, RFC comparisons, or multi-option proposals, use a decision surface layout instead of stacked paragraphs.

## Core Structure

1. **Header & Context**: Brief objective (2-3 sentences), constraints, and key evaluation criteria.
2. **Side-by-Side Comparison Matrix**:
   - Distinct columns per option (2 to 4 options max).
   - Sticky header with option title, summary badge (e.g., "Recommended", "Highest Perf", "Lowest Ops"), and primary radio/checkbox selector.
   - Feature/Criteria rows: Cost, Latency, Complexity, Maintenance, Risks.
3. **Interactive Tuning / Parameter Sandbox** (Optional):
   - Sliders or toggles for variables (e.g. Expected RPS, Budget, Retention days).
   - Live JavaScript calculation updating the recommended option or projected cost.
4. **Mandatory Round-Trip Export Bar**:
   - Fixed position (`bottom: 1.5rem; right: 1.5rem`).
   - Gathers user selections, radio choices, notes, and parameter states.
   - Writes cleanly formatted Markdown directly to the clipboard via `navigator.clipboard.writeText()`.

---

## Canonical Zero-Node Implementation

```html
<div class="matrix-grid">
  <!-- Option Card 1 -->
  <article class="option-card" data-option="Option 1">
    <div class="option-header">
      <span class="badge badge-rec">Recommended</span>
      <h3>Postgres + pgvector</h3>
      <p class="option-sub">Unified storage with zero extra infra overhead.</p>
      <label class="select-label">
        <input type="radio" name="selected_arch" value="Postgres + pgvector" checked>
        <span>Select for proposal</span>
      </label>
    </div>
    <div class="option-body">
      <ul class="criteria-list">
        <li><strong>Infrastructure:</strong> Single Supabase/RDS instance</li>
        <li><strong>Latency:</strong> ~12ms p95 query time</li>
        <li><strong>Tradeoff:</strong> Index rebuild times scale with table size</li>
      </ul>
      <textarea class="notes-input" placeholder="Add custom notes or constraints..."></textarea>
    </div>
  </article>

  <!-- Option Card 2 -->
  <article class="option-card" data-option="Option 2">
    <div class="option-header">
      <span class="badge">Specialized</span>
      <h3>Qdrant / Pinecone</h3>
      <p class="option-sub">Dedicated vector database with high-scale clustering.</p>
      <label class="select-label">
        <input type="radio" name="selected_arch" value="Dedicated Vector DB">
        <span>Select for proposal</span>
      </label>
    </div>
    <div class="option-body">
      <ul class="criteria-list">
        <li><strong>Infrastructure:</strong> Secondary managed SaaS or cluster</li>
        <li><strong>Latency:</strong> ~4ms p95 query time</li>
        <li><strong>Tradeoff:</strong> Data sync lag and dual-source-of-truth</li>
      </ul>
      <textarea class="notes-input" placeholder="Add custom notes or constraints..."></textarea>
    </div>
  </article>
</div>

<!-- Fixed Round-Trip Export -->
<aside class="export-tray" aria-label="Action Bar">
  <div class="export-content">
    <span id="export-status">Option 1 selected</span>
    <button id="copy-decisions-btn" class="btn-primary">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
      Copy Decision as Prompt
    </button>
  </div>
</aside>

<script>
  function buildMarkdownExport() {
    const selected = document.querySelector('input[name="selected_arch"]:checked')?.value || 'None';
    const activeCard = document.querySelector(`[data-option="${selected}"]`);
    const notes = activeCard?.querySelector('.notes-input')?.value.trim();

    return [
      `### Decision Verdict: ${selected}`,
      `- **Selected Option**: ${selected}`,
      notes ? `- **User Notes/Adjustments**: ${notes}` : null,
      `- **Generated On**: ${new Date().toLocaleDateString()}`,
      `\nPlease proceed with implementing the architecture according to this decision.`
    ].filter(Boolean).join('\n');
  }

  document.getElementById('copy-decisions-btn').addEventListener('click', async (e) => {
    const text = buildMarkdownExport();
    await navigator.clipboard.writeText(text);
    const btn = e.currentTarget;
    const originalHTML = btn.innerHTML;
    btn.innerHTML = `<span>✓ Copied to Clipboard</span>`;
    setTimeout(() => { btn.innerHTML = originalHTML; }, 2000);
  });
</script>
```

# Reference: Code Review, Diffs & Checklists

Use this pattern when reviewing code, staging PR comments, inspecting migration scripts, or breaking down security audits.

## Core Principles

1. **Spatial Diff Rendering**: Side-by-side or inline color-coded diff blocks (`+` in soft green, `-` in muted red) rather than nested markdown backticks.
2. **Per-File or Per-Issue Collapsibility**: Use native HTML `<details>` elements so reviewers can collapse resolved comments and focus on blocking findings.
3. **Tri-State or Binary Triage**: Checkbox or radio buttons (`Accept`, `Revise`, `Reject`) next to each comment.
4. **Export to GitHub / Agent Prompt**: A floating export button that compiles reviewed comments into copyable GitHub PR review markdown or terminal CLI commands (`gh pr review --comment -b "..."`).

---

## Zero-Node Split Diff & Review Template

```html
<section class="review-file">
  <div class="file-header">
    <div class="file-info">
      <span class="file-icon">📄</span>
      <span class="file-name">src/auth/session.ts</span>
      <span class="diff-stat">+14 -3</span>
    </div>
    <div class="file-actions">
      <label class="reviewed-checkbox">
        <input type="checkbox" data-file-reviewed>
        <span>Mark as reviewed</span>
      </label>
    </div>
  </div>

  <!-- Collapsible Comment Thread -->
  <details open class="finding-thread finding-critical">
    <summary class="thread-summary">
      <span class="severity-badge badge-crit">Critical</span>
      <span class="thread-title">Potential timing attack on token comparison</span>
      <span class="thread-line">Line 42</span>
    </summary>
    <div class="thread-content">
      <p class="thread-desc">
        Standard string equality <code>token === storedToken</code> leaks execution timing. Use <code>crypto.timingSafeEqual</code> instead.
      </p>
      
      <!-- Diff snippet -->
      <pre class="code-diff">
<span class="diff-line diff-del">- if (req.headers['x-api-key'] === API_KEY) {</span>
<span class="diff-line diff-add">+ if (crypto.timingSafeEqual(Buffer.from(headerKey), Buffer.from(API_KEY))) {</span>
      </pre>

      <div class="triage-controls">
        <label><input type="radio" name="triage_crit_1" value="accept" checked> Fix Required</label>
        <label><input type="radio" name="triage_crit_1" value="dismiss"> False Positive</label>
        <label><input type="radio" name="triage_crit_1" value="deferred"> Defer to Backlog</label>
      </div>
      <input type="text" class="triage-notes" placeholder="Optional instructions for Claude...">
    </div>
  </details>
</section>

<!-- Export Bar -->
<div class="review-export-bar">
  <button id="export-pr-btn" class="btn-primary">Copy Review for Agent</button>
</div>

<script>
  document.getElementById('export-pr-btn').addEventListener('click', async (e) => {
    const findings = [];
    document.querySelectorAll('.finding-thread').forEach(thread => {
      const title = thread.querySelector('.thread-title')?.textContent.trim();
      const status = thread.querySelector('input[type="radio"]:checked')?.value || 'pending';
      const notes = thread.querySelector('.triage-notes')?.value.trim();
      findings.push(`- **${title}**: [${status.toUpperCase()}] ${notes ? '— ' + notes : ''}`);
    });

    const report = `# Code Review Triage (${new Date().toISOString().slice(0, 10)})\n\n` + findings.join('\n');
    await navigator.clipboard.writeText(report);
    e.target.textContent = '✓ Copied to Clipboard';
    setTimeout(() => e.target.textContent = 'Copy Review for Agent', 2000);
  });
</script>
```

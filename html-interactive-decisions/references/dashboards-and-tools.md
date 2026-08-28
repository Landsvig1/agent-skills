# Reference: Dashboards, Tables & Throwaway Tools

Use this pattern when creating KPI dashboards, searchable lead lists, inventory views, status trackers, or throwaway tools (e.g. prompt generators, regex testbenches).

## Core Principles

1. **Information Density with Zero Build**:
   - Use CSS Grid `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))` for stat cards.
   - Native HTML `<table>` styled with clean sticky headers and zebra striping.
2. **Client-Side Vanilla Search & Filtering**:
   - ~20 lines of vanilla JavaScript filtering table rows on `input` event without external libraries.
3. **Native Modal Details & Popovers**:
   - Use HTML `<dialog>` with `.showModal()` for drilling down into row details.
   - Use `popover="auto"` for small dropdowns or filter menus.
4. **Export Selected / Filtered Rows**:
   - Support checkboxes per row with a master checkbox and an export button: "Copy Selected as JSON" or "Copy Selected as Markdown".

---

## Zero-Node Searchable Table & KPI Template

```html
<!-- KPI Top Row -->
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-label">Active Deployments</span>
    <span class="kpi-value">42</span>
    <span class="kpi-trend trend-up">↑ 12% WoW</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Error Rate (p99)</span>
    <span class="kpi-value">0.08%</span>
    <span class="kpi-trend trend-down">↓ 0.02%</span>
  </div>
</div>

<!-- Search & Filter Controls -->
<div class="table-toolbar">
  <input type="search" id="table-search" placeholder="Filter by service name, owner, or status..." class="search-input">
  <div class="toolbar-actions">
    <span id="match-count">Showing all records</span>
    <button id="export-selected-btn" class="btn-outline">Copy Checked Rows</button>
  </div>
</div>

<!-- Data Table -->
<div class="table-container">
  <table id="data-table">
    <thead>
      <tr>
        <th width="40"><input type="checkbox" id="select-all"></th>
        <th>Service</th>
        <th>Environment</th>
        <th>Status</th>
        <th>Latency</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr data-service="auth-service" data-env="production">
        <td><input type="checkbox" class="row-select"></td>
        <td><strong>auth-service</strong></td>
        <td><span class="env-tag env-prod">Production</span></td>
        <td><span class="status-dot dot-green"></span> Healthy</td>
        <td>14ms</td>
        <td><button class="btn-sm" onclick="openDetails('auth-service')">Details</button></td>
      </tr>
      <tr data-service="payment-webhook" data-env="staging">
        <td><input type="checkbox" class="row-select"></td>
        <td><strong>payment-webhook</strong></td>
        <td><span class="env-tag env-stage">Staging</span></td>
        <td><span class="status-dot dot-amber"></span> High Latency</td>
        <td>340ms</td>
        <td><button class="btn-sm" onclick="openDetails('payment-webhook')">Details</button></td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Native <dialog> Modal -->
<dialog id="details-modal" class="modal-dialog">
  <div class="modal-header">
    <h3 id="modal-title">Service Details</h3>
    <button onclick="document.getElementById('details-modal').close()" class="btn-close">✕</button>
  </div>
  <div class="modal-body" id="modal-body">
    <!-- Injected dynamically -->
  </div>
</dialog>

<script>
  // 1. Instant Vanilla Search Filter
  const searchInput = document.getElementById('table-search');
  searchInput.addEventListener('input', () => {
    const q = searchInput.value.toLowerCase();
    let matches = 0;
    document.querySelectorAll('#data-table tbody tr').forEach(row => {
      const text = row.textContent.toLowerCase();
      const show = text.includes(q);
      row.style.display = show ? '' : 'none';
      if (show) matches++;
    });
    document.getElementById('match-count').textContent = `Showing ${matches} rows`;
  });

  // 2. Row Selection & Export
  document.getElementById('select-all').addEventListener('change', (e) => {
    document.querySelectorAll('.row-select').forEach(cb => {
      if (cb.closest('tr').style.display !== 'none') cb.checked = e.target.checked;
    });
  });

  document.getElementById('export-selected-btn').addEventListener('click', async () => {
    const selected = [];
    document.querySelectorAll('#data-table tbody tr').forEach(row => {
      if (row.querySelector('.row-select:checked')) {
        const cols = Array.from(row.querySelectorAll('td')).slice(1, 5).map(td => td.textContent.trim());
        selected.push(`- **${cols[0]}** (${cols[1]}): ${cols[2]}, Latency: ${cols[3]}`);
      }
    });
    const text = selected.length ? selected.join('\n') : 'No rows selected.';
    await navigator.clipboard.writeText(text);
    alert('Copied selected rows to clipboard for Claude!');
  });

  // 3. Native Modal Handler
  function openDetails(service) {
    document.getElementById('modal-title').textContent = `${service} Logs & Metrics`;
    document.getElementById('modal-body').innerHTML = `<p>Detailed diagnostic runtime payload for <code>${service}</code>.</p>`;
    document.getElementById('details-modal').showModal();
  }
</script>
```

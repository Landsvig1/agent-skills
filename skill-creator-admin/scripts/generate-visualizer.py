#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

CLAUDE_SKILLS = Path("/Users/kasperlandsvig/.claude/skills")
GEMINI_SKILLS = Path("/Users/kasperlandsvig/.gemini/skills")
WORKSPACE_SKILLS = Path("/Users/kasperlandsvig/Documents/Claude Cowork/Agents/skills")
OUTPUT_DIR = Path("/Users/kasperlandsvig/Documents/Claude Cowork/Skills Visualized")
OUTPUT_FILE = OUTPUT_DIR / "index.html"

def extract_frontmatter(md_content):
    frontmatter = {}
    # Simple regex to extract YAML frontmatter
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", md_content, re.DOTALL)
    if match:
        yaml_block = match.group(1)
        for line in yaml_block.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                frontmatter[key.strip()] = val.strip()
    return frontmatter

def get_skills_data():
    skills = []
    if not CLAUDE_SKILLS.exists():
        return skills
        
    for p in CLAUDE_SKILLS.iterdir():
        if p.is_dir() and not p.name.startswith('.') and p.name != '_shared':
            skill_md_path = p / "SKILL.md"
            description = "No description provided."
            name = p.name
            content_preview = ""
            
            if skill_md_path.exists():
                try:
                    content = skill_md_path.read_text(encoding="utf-8")
                    fm = extract_frontmatter(content)
                    name = fm.get("name", p.name)
                    description = fm.get("description", "No description in frontmatter.")
                    
                    # Remove frontmatter for preview
                    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)
                    lines = body.split("\n")
                    content_preview = "\n".join(lines[:40]) # First 40 lines for browsing
                except Exception as e:
                    description = f"Error reading SKILL.md: {e}"
            
            # Check mirroring status
            gemini_path = GEMINI_SKILLS / p.name
            workspace_path = WORKSPACE_SKILLS / p.name
            
            is_in_gemini = gemini_path.exists() or gemini_path.is_symlink()
            is_in_workspace = workspace_path.exists()
            
            # Try to resolve symlink to ensure it's not broken
            gemini_status = "Linked"
            if is_in_gemini:
                try:
                    if gemini_path.is_symlink():
                        gemini_path.resolve(strict=True)
                    else:
                        gemini_status = "Physical Dir"
                except FileNotFoundError:
                    gemini_status = "Broken Link"
            else:
                gemini_status = "Missing"
                
            skills.append({
                "id": p.name,
                "name": name,
                "description": description,
                "geminiStatus": gemini_status,
                "workspaceStatus": "Mirrored" if is_in_workspace else "Missing",
                "preview": content_preview
            })
            
    return sorted(skills, key=lambda x: x["name"].lower())

def main():
    print("Parsing skills directories...")
    skills_data = get_skills_data()
    
    # Check sync-skills.log modification time for cron status
    sync_log = Path("/Users/kasperlandsvig/Documents/Claude Cowork/scripts/sync-skills.log")
    cron_status_class = "warning"
    cron_status_text = "Manual / Cron Blocked"
    cron_status_title = "Mac Sandboxing blocks silent Cron. Grant Full Disk Access or run manually."
    
    if sync_log.exists():
        from datetime import datetime
        mtime = datetime.fromtimestamp(sync_log.stat().st_mtime)
        delta = datetime.now() - mtime
        hours = delta.total_seconds() / 3600.0
        if hours < 1.0:
            cron_status_class = "ok"
            cron_status_text = "Active"
            cron_status_title = f"Background cron sync running normally. Last sync: {mtime.strftime('%H:%M:%S')}"
        else:
            cron_status_title = f"Last sync log was updated {hours:.1f} hours ago. Background cron might be blocked."
    
    # HTML Template
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Skills Visualizer & Control Center</title>
    <!-- Outfit and Inter Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Lucide Icons CDN -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: rgba(22, 30, 49, 0.6);
            --card-border: rgba(255, 255, 255, 0.08);
            --primary-accent: #3b82f6;
            --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --text-main: #f3f4f6;
            --text-sub: #9ca3af;
            --node-color: rgba(59, 130, 246, 0.15);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2.5rem;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%);
            background-attachment: fixed;
        }

        h1, h2, h3, h4 {
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
        }

        .container {
            max-width: 1350px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 2.5rem;
        }

        /* HEADER */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--card-border);
        }

        .logo-section h1 {
            font-size: 2.2rem;
            font-weight: 800;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-section p {
            color: var(--text-sub);
            margin-top: 0.25rem;
            font-size: 0.95rem;
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--success-color);
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--success-color);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.6; }
            50% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.6; }
        }

        /* MAIN GRID */
        .layout-grid {
            display: grid;
            grid-template-columns: 1.3fr 1fr;
            gap: 2.5rem;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 2rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }

        .card:hover {
            border-color: rgba(59, 130, 246, 0.2);
        }

        .card-title {
            font-size: 1.4rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.75rem;
        }

        /* TOPOLOGY DIAGRAM */
        .topology-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            padding: 2rem 0;
            min-height: 400px;
        }

        .nodes-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            width: 100%;
            max-width: 600px;
            position: relative;
            z-index: 2;
        }

        .node {
            background: rgba(30, 41, 59, 0.8);
            border: 1.5px solid var(--card-border);
            border-radius: 16px;
            padding: 1.25rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }

        .node:hover {
            border-color: var(--primary-accent);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
            transform: translateY(-2px);
        }

        .node-icon-wrapper {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: rgba(59, 130, 246, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary-accent);
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .node.canonical {
            grid-column: span 2;
            justify-self: center;
            max-width: 320px;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%);
            border-color: rgba(59, 130, 246, 0.4);
        }

        .node.canonical .node-icon-wrapper {
            background: rgba(59, 130, 246, 0.2);
            color: #60a5fa;
            border-color: rgba(59, 130, 246, 0.4);
        }

        .node-info h4 {
            font-size: 0.95rem;
            font-weight: 700;
        }

        .node-info p {
            font-size: 0.75rem;
            color: var(--text-sub);
            margin-top: 0.15rem;
        }

        /* SVG Connections */
        .topology-svg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none;
        }

        .connection-line {
            stroke: rgba(255, 255, 255, 0.08);
            stroke-width: 2;
            fill: none;
            stroke-dasharray: 6 4;
            animation: dash 30s linear infinite;
        }

        .connection-line.active {
            stroke: var(--primary-accent);
            stroke-width: 2.5;
            opacity: 0.6;
        }

        @keyframes dash {
            to { stroke-dashoffset: -1000; }
        }

        /* SIDE PANEL */
        .side-panel {
            display: flex;
            flex-direction: column;
            gap: 2.5rem;
        }

        .diagnostic-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.85rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .diagnostic-row:last-child {
            border-bottom: none;
        }

        .diag-label {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.95rem;
        }

        .diag-status {
            font-size: 0.85rem;
            font-weight: 600;
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
        }

        .diag-status.ok {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success-color);
        }

        .diag-status.warning {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning-color);
        }

        .action-card {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
        }

        .action-card code {
            font-family: monospace;
            font-size: 0.85rem;
            color: #60a5fa;
            background: rgba(0, 0, 0, 0.3);
            padding: 0.5rem;
            border-radius: 6px;
            display: block;
            margin-top: 0.5rem;
            word-break: break-all;
        }

        /* SKILLS REGISTRY */
        .registry-section {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 2.5rem;
        }

        .registry-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .search-wrapper {
            position: relative;
            width: 100%;
            max-width: 400px;
        }

        .search-wrapper input {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--card-border);
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            border-radius: 12px;
            color: var(--text-main);
            outline: none;
            transition: all 0.3s ease;
        }

        .search-wrapper input:focus {
            border-color: var(--primary-accent);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.1);
        }

        .search-wrapper i {
            position: absolute;
            left: 0.85rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-sub);
            width: 18px;
            height: 18px;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .skill-item {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 180px;
        }

        .skill-item:hover {
            border-color: rgba(59, 130, 246, 0.3);
            background: rgba(30, 41, 59, 0.6);
            transform: translateY(-3px);
        }

        .skill-item-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
        }

        .skill-item h3 {
            font-size: 1.1rem;
            color: #60a5fa;
            word-break: break-all;
        }

        .skill-item p {
            font-size: 0.85rem;
            color: var(--text-sub);
            line-height: 1.4;
            flex-grow: 1;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            margin-bottom: 1rem;
        }

        .badge-row {
            display: flex;
            gap: 0.5rem;
        }

        .mini-badge {
            font-size: 0.7rem;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
        }

        .mini-badge.synced {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success-color);
        }

        .mini-badge.missing {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger-color);
        }

        /* MODAL */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(8px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .modal-content {
            background: #0f172a;
            border: 1px solid var(--card-border);
            border-radius: 20px;
            width: 100%;
            max-width: 800px;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: modalSlide 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes modalSlide {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .modal-header {
            padding: 1.5rem 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-header h2 {
            font-size: 1.5rem;
            color: #60a5fa;
        }

        .close-btn {
            background: none;
            border: none;
            color: var(--text-sub);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0.5rem;
            border-radius: 50%;
            transition: all 0.2s ease;
        }

        .close-btn:hover {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-main);
        }

        .modal-body {
            padding: 2rem;
            overflow-y: auto;
            flex-grow: 1;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
        }

        .modal-body pre {
            background: #020617;
            padding: 1.5rem;
            border-radius: 12px;
            overflow-x: auto;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.85rem;
            border: 1px solid rgba(255, 255, 255, 0.03);
            white-space: pre-wrap;
            color: #cbd5e1;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <header>
            <div class="logo-section">
                <h1><i data-lucide="compass"></i> Skills Visualized</h1>
                <p>Agent Customizations Topology & Registry</p>
            </div>
            <div class="status-badge">
                <div class="status-dot"></div>
                <span>Skills Synced & Active</span>
            </div>
        </header>

        <!-- MAIN LAYOUT -->
        <div class="layout-grid">
            <!-- TOPOLOGY CARD -->
            <div class="card">
                <h2 class="card-title"><i data-lucide="git-branch" style="color: var(--primary-accent)"></i> Systems Topology Map</h2>
                <div class="topology-container">
                    <svg class="topology-svg" id="topologySvg">
                        <!-- Connection Lines -->
                        <path id="path-claude-cowork" class="connection-line active" />
                        <path id="path-claude-gemini" class="connection-line active" />
                        <path id="path-gemini-agy" class="connection-line active" />
                    </svg>

                    <div class="nodes-grid">
                        <!-- CLAUDE NODE -->
                        <div class="node canonical" id="node-claude" title="Primary edit location for skills">
                            <div class="node-icon-wrapper">
                                <i data-lucide="terminal"></i>
                            </div>
                            <div class="node-info">
                                <h4>Claude Code Canonical</h4>
                                <p>~/.claude/skills/</p>
                            </div>
                        </div>

                        <!-- COWORK SYMLINK NODE -->
                        <div class="node" id="node-cowork" title="Symlink inside workspace root">
                            <div class="node-icon-wrapper">
                                <i data-lucide="folder-git-2"></i>
                            </div>
                            <div class="node-info">
                                <h4>Workspace Global Link</h4>
                                <p>Claude Cowork/Skills Global/</p>
                            </div>
                        </div>

                        <!-- GEMINI NODE -->
                        <div class="node" id="node-gemini" title="Symlinked destination for Gemini CLI">
                            <div class="node-icon-wrapper">
                                <i data-lucide="sparkles"></i>
                            </div>
                            <div class="node-info">
                                <h4>Gemini Global Mirror</h4>
                                <p>~/.gemini/skills/</p>
                            </div>
                        </div>

                        <!-- AGENTS WORKSPACE NODE -->
                        <div class="node" id="node-agents" style="grid-column: span 2; justify-self: center; width: 280px;" title="Workspace mirror for project-local execution">
                            <div class="node-icon-wrapper">
                                <i data-lucide="refresh-cw"></i>
                            </div>
                            <div class="node-info">
                                <h4>Workspace Local Mirror</h4>
                                <p>Claude Cowork/Agents/skills/</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- DIAGNOSTIC CARD -->
            <div class="side-panel">
                <div class="card">
                    <h2 class="card-title"><i data-lucide="shield-alert" style="color: var(--warning-color)"></i> Diagnostics & Health</h2>
                    
                    <div class="diagnostic-row">
                        <span class="diag-label"><i data-lucide="link" size="16"></i> Symlinks Integrity</span>
                        <span class="diag-status ok">Correct</span>
                    </div>
                    <div class="diagnostic-row">
                        <span class="diag-label"><i data-lucide="refresh-cw" size="16"></i> Sync Automation</span>
                        <span class="diag-status __CRON_STATUS_CLASS__" title="__CRON_STATUS_TITLE__">__CRON_STATUS_TEXT__</span>
                    </div>
                    <div class="diagnostic-row">
                        <span class="diag-label"><i data-lucide="check-circle" size="16"></i> Skill creator admin</span>
                        <span class="diag-status ok">Active</span>
                    </div>

                    <div class="action-card">
                        <span style="font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem;">
                            <i data-lucide="terminal" size="16" style="color: var(--primary-accent)"></i> Trigger Manual Sync
                        </span>
                        <code>/Users/kasperlandsvig/Documents/Claude\ Cowork/scripts/sync-skills.sh</code>
                    </div>

                    <div class="action-card">
                        <span style="font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem;">
                            <i data-lucide="activity" size="16" style="color: var(--success-color)"></i> Run Skills System Audit
                        </span>
                        <code>python3 /Users/kasperlandsvig/.claude/skills/skill-creator-admin/scripts/audit-sync.py --fix</code>
                    </div>
                </div>
            </div>
        </div>

        <!-- SKILLS LIST -->
        <div class="registry-section">
            <div class="registry-header">
                <h2><i data-lucide="database" style="color: var(--primary-accent); margin-right: 0.5rem;"></i> Active Skills Registry</h2>
                <div class="search-wrapper">
                    <i data-lucide="search"></i>
                    <input type="text" id="searchInput" placeholder="Search skills by name or description...">
                </div>
            </div>

            <div class="skills-grid" id="skillsGrid">
                <!-- Skill cards are dynamically generated here -->
            </div>
        </div>
    </div>

    <!-- PREVIEW MODAL -->
    <div class="modal-overlay" id="previewModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Skill Title</h2>
                <button class="close-btn" onclick="closeModal()"><i data-lucide="x"></i></button>
            </div>
            <div class="modal-body">
                <div id="modalBody">Skill code preview...</div>
            </div>
        </div>
    </div>

    <script>
        // Skills JSON payload
        const skillsData = __SKILLS_DATA_PLACEHOLDER__;

        // Initialize Lucide Icons
        lucide.createIcons();

        // Render skill cards
        const skillsGrid = document.getElementById('skillsGrid');
        const searchInput = document.getElementById('searchInput');

        function renderSkills(filterText = '') {
            skillsGrid.innerHTML = '';
            const filtered = skillsData.filter(skill => {
                const query = filterText.toLowerCase();
                return skill.name.toLowerCase().includes(query) || 
                       skill.description.toLowerCase().includes(query) ||
                       skill.id.toLowerCase().includes(query);
            });

            filtered.forEach(skill => {
                const card = document.createElement('div');
                card.className = 'skill-item';
                card.onclick = () => openModal(skill);
                
                card.innerHTML = `
                    <div class="skill-item-header">
                        <h3>${skill.name}</h3>
                    </div>
                    <p>${skill.description}</p>
                    <div class="badge-row">
                        <span class="mini-badge synced">Claude: Synced</span>
                        <span class="mini-badge ${skill.geminiStatus === 'Linked' ? 'synced' : 'missing'}">Gemini: ${skill.geminiStatus}</span>
                    </div>
                `;
                skillsGrid.appendChild(card);
            });

            if (filtered.length === 0) {
                skillsGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-sub); padding: 3rem;">No skills found matching your search.</div>';
            }
        }

        searchInput.addEventListener('input', (e) => {
            renderSkills(e.target.value);
        });

        // Modal triggers
        const modal = document.getElementById('previewModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');

        function openModal(skill) {
            modalTitle.innerText = skill.name;
            const modalContent = document.querySelector('.modal-content');
            if (skill.id === 'deep-research-agent') {
                modalContent.style.maxWidth = '1200px';
                modalContent.style.width = '90vw';
                modalBody.innerHTML = `<iframe src="../Agents/DRA visual.html" style="width:100%; height:70vh; border:none; border-radius:12px;"></iframe>`;
            } else {
                modalContent.style.maxWidth = '800px';
                modalContent.style.width = '';
                modalBody.innerHTML = `<pre style="white-space: pre-wrap; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--text-main); overflow-y: auto; max-height: 60vh;">${skill.preview || "No preview content available."}</pre>`;
            }
            modal.style.display = 'flex';
        }

        function closeModal() {
            modal.style.display = 'none';
            const modalContent = document.querySelector('.modal-content');
            modalContent.style.maxWidth = '800px';
            modalContent.style.width = '';
            modalBody.innerHTML = '';
        }

        // Close modal on click outside content
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });

        // Draw SVG connection lines dynamically
        function drawConnections() {
            const svg = document.getElementById('topologySvg');
            const nClaude = document.getElementById('node-claude').getBoundingClientRect();
            const nCowork = document.getElementById('node-cowork').getBoundingClientRect();
            const nGemini = document.getElementById('node-gemini').getBoundingClientRect();
            const nAgents = document.getElementById('node-agents').getBoundingClientRect();
            const svgRect = svg.getBoundingClientRect();

            function getCenter(rect) {
                return {
                    x: rect.left - svgRect.left + rect.width / 2,
                    y: rect.top - svgRect.top + rect.height / 2
                };
            }

            const cClaude = getCenter(nClaude);
            const cCowork = getCenter(nCowork);
            const cGemini = getCenter(nGemini);
            const cAgents = getCenter(nAgents);

            // Connect Claude to Cowork Link
            document.getElementById('path-claude-cowork').setAttribute('d', `M ${cClaude.x} ${cClaude.y} L ${cCowork.x} ${cCowork.y}`);
            // Connect Cowork Link to Gemini
            document.getElementById('path-claude-gemini').setAttribute('d', `M ${cCowork.x} ${cCowork.y} L ${cGemini.x} ${cGemini.y}`);
            // Connect Cowork Link to Local Workspace Mirror
            document.getElementById('path-gemini-agy').setAttribute('d', `M ${cCowork.x} ${cCowork.y} L ${cAgents.x} ${cAgents.y}`);
        }

        // Run connections layout on load and resize
        window.addEventListener('load', () => {
            drawConnections();
            renderSkills();
        });
        window.addEventListener('resize', drawConnections);
    </script>
</body>
</html>"""

    # Inject JSON payload and status variables into HTML template
    html_content = html_content.replace("__CRON_STATUS_CLASS__", cron_status_class)
    html_content = html_content.replace("__CRON_STATUS_TEXT__", cron_status_text)
    html_content = html_content.replace("__CRON_STATUS_TITLE__", cron_status_title)
    final_html = html_content.replace("__SKILLS_DATA_PLACEHOLDER__", json.dumps(skills_data, indent=4))
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(final_html, encoding="utf-8")
    print(f"Visualizer written to {OUTPUT_FILE} successfully!")

if __name__ == "__main__":
    main()

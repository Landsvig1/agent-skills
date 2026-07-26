#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

CLAUDE_SKILLS = Path("/Users/kasperlandsvig/.claude/skills")
GEMINI_SKILLS = Path("/Users/kasperlandsvig/.gemini/skills")
AGY_SKILLS_LINK = Path("/Users/kasperlandsvig/.gemini/antigravity-cli/skills")
WORKSPACE_DIR = Path("/Users/kasperlandsvig/Documents/Claude Cowork")
WORKSPACE_SKILLS = WORKSPACE_DIR / "Agents/skills"
WORKSPACE_SKILLS_GLOBAL = WORKSPACE_DIR / "Skills Global"
SYNC_LOG = WORKSPACE_DIR / "scripts/sync-skills.log"

def get_status_emoji(success):
    return "✅" if success else "❌"

def audit():
    print("==================================================")
    print("🔍 SKILLS SYSTEM AUDIT")
    print("==================================================")
    
    issues = []
    
    # 1. Check Claude skills directory
    if not CLAUDE_SKILLS.exists():
        print(f"❌ Canonical Claude skills directory does not exist: {CLAUDE_SKILLS}")
        issues.append("claude_skills_missing")
    else:
        print(f"✅ Canonical Claude skills directory: {CLAUDE_SKILLS}")
        
    # 2. Check Skills Global symlink in workspace
    if not WORKSPACE_SKILLS_GLOBAL.exists():
        print(f"❌ Workspace link 'Skills Global' does not exist or is broken: {WORKSPACE_SKILLS_GLOBAL}")
        issues.append("workspace_global_link_broken")
    elif not WORKSPACE_SKILLS_GLOBAL.is_symlink():
        print(f"⚠️ Workspace link 'Skills Global' exists but is not a symlink!")
        issues.append("workspace_global_link_not_symlink")
    else:
        target = WORKSPACE_SKILLS_GLOBAL.readlink()
        print(f"✅ Workspace link 'Skills Global' -> {target}")
        
    # 3. Check Workspace Mirror skills
    if not WORKSPACE_SKILLS.exists():
        print(f"❌ Workspace mirror skills directory does not exist: {WORKSPACE_SKILLS}")
        issues.append("workspace_mirror_missing")
    else:
        print(f"✅ Workspace mirror skills directory exists: {WORKSPACE_SKILLS}")
        
    # 4. Check Gemini skills directory and links
    if not GEMINI_SKILLS.exists():
        print(f"❌ Gemini skills directory does not exist: {GEMINI_SKILLS}")
        issues.append("gemini_skills_missing")
    else:
        print(f"✅ Gemini skills directory: {GEMINI_SKILLS}")
        
    # 5. Check Antigravity skills link
    if not AGY_SKILLS_LINK.exists():
        print(f"❌ Antigravity CLI skills symlink does not exist or is broken: {AGY_SKILLS_LINK}")
        issues.append("agy_skills_link_broken")
    elif not AGY_SKILLS_LINK.is_symlink():
        print(f"⚠️ Antigravity CLI skills exists but is not a symlink!")
        issues.append("agy_skills_link_not_symlink")
    else:
        target = AGY_SKILLS_LINK.readlink()
        print(f"✅ Antigravity CLI skills link -> {target}")
        
    # 6. Audit individual skills alignment
    if CLAUDE_SKILLS.exists():
        claude_skills = {p.name for p in CLAUDE_SKILLS.iterdir() if p.is_dir() and not p.name.startswith('.')}
    else:
        claude_skills = set()
        
    if GEMINI_SKILLS.exists():
        gemini_entries = list(GEMINI_SKILLS.iterdir())
        
        # Find physical directories in Gemini skills that are not symlinks (excluding .shared or special dirs)
        for entry in gemini_entries:
            if entry.name.startswith('.') or entry.name == '_shared':
                continue
            if entry.is_symlink():
                # Check if target is broken
                try:
                    target = entry.resolve(strict=True)
                except (FileNotFoundError, RuntimeError):
                    print(f"❌ Broken symlink: Gemini skill '{entry.name}' points to non-existent target")
                    issues.append(f"broken_symlink:{entry.name}")
            elif entry.is_dir():
                print(f"⚠️ Stray physical directory in Gemini skills: {entry.name} (should be a symlink)")
                issues.append(f"stray_directory:{entry.name}")
                
        # Find missing symlinks in Gemini skills
        for skill in claude_skills:
            gemini_skill_path = GEMINI_SKILLS / skill
            if not gemini_skill_path.exists():
                print(f"⚠️ Claude skill '{skill}' is not linked/present in Gemini skills")
                issues.append(f"missing_link:{skill}")
                
    # 7. Check sync timing (cron health)
    if SYNC_LOG.exists():
        mtime = datetime.fromtimestamp(SYNC_LOG.stat().st_mtime)
        delta = datetime.now() - mtime
        hours_since_sync = delta.total_seconds() / 3600.0
        print(f"ℹ️ Last sync log update: {mtime} ({hours_since_sync:.1f} hours ago)")
        if hours_since_sync > 1.0:
            print("⚠️ The skills sync has not run recently via cron (possible macOS Full Disk Access issue for cron).")
    else:
        print("❌ No skills sync log found. Sync has never run or is misconfigured.")
        issues.append("sync_log_missing")
        
    print("==================================================")
    if issues:
        print(f"⚠️ Found {len(issues)} issues that need attention.")
    else:
        print("✨ All systems green! No issues found.")
    print("==================================================")
    return issues

def fix_issues(issues):
    if not issues:
        print("Nothing to fix.")
        return
        
    print("🔧 STARTING AUTOMATIC CORRECTION OF ISSUES...")
    
    # Ensure directories
    CLAUDE_SKILLS.mkdir(parents=True, exist_ok=True)
    GEMINI_SKILLS.mkdir(parents=True, exist_ok=True)
    
    # Fix 1: Antigravity CLI skills link
    if "agy_skills_link_broken" in issues or "agy_skills_link_not_symlink" in issues:
        print(f"  Fixing Antigravity CLI skills link...")
        if AGY_SKILLS_LINK.exists() or AGY_SKILLS_LINK.is_symlink():
            if AGY_SKILLS_LINK.is_dir() and not AGY_SKILLS_LINK.is_symlink():
                shutil.rmtree(AGY_SKILLS_LINK)
            else:
                AGY_SKILLS_LINK.unlink()
        AGY_SKILLS_LINK.symlink_to(GEMINI_SKILLS)
        print(f"  {get_status_emoji(True)} Linked {AGY_SKILLS_LINK} -> {GEMINI_SKILLS}")
        
    # Fix 2: Workspace Global Link
    if "workspace_global_link_broken" in issues or "workspace_global_link_not_symlink" in issues:
        print(f"  Fixing Workspace 'Skills Global' link...")
        if WORKSPACE_SKILLS_GLOBAL.exists() or WORKSPACE_SKILLS_GLOBAL.is_symlink():
            if WORKSPACE_SKILLS_GLOBAL.is_dir() and not WORKSPACE_SKILLS_GLOBAL.is_symlink():
                shutil.rmtree(WORKSPACE_SKILLS_GLOBAL)
            else:
                WORKSPACE_SKILLS_GLOBAL.unlink()
        WORKSPACE_SKILLS_GLOBAL.symlink_to(CLAUDE_SKILLS)
        print(f"  {get_status_emoji(True)} Linked {WORKSPACE_SKILLS_GLOBAL} -> {CLAUDE_SKILLS}")
        
    # Fix individual skill issues
    for issue in issues:
        if issue.startswith("stray_directory:"):
            skill_name = issue.split(":", 1)[1]
            gemini_path = GEMINI_SKILLS / skill_name
            claude_path = CLAUDE_SKILLS / skill_name
            
            print(f"  Moving stray Gemini skill '{skill_name}' to canonical Claude folder...")
            if claude_path.exists():
                backup_path = claude_path.with_name(f"{skill_name}_backup_{int(datetime.now().timestamp())}")
                print(f"    Warning: Canonical folder {claude_path} already exists. Backing up to {backup_path.name}")
                claude_path.rename(backup_path)
                
            shutil.move(str(gemini_path), str(claude_path))
            # Create symlink back
            gemini_path.symlink_to(WORKSPACE_SKILLS_GLOBAL / skill_name)
            print(f"  {get_status_emoji(True)} Consolidated '{skill_name}' and created symlink.")
            
        elif issue.startswith("missing_link:"):
            skill_name = issue.split(":", 1)[1]
            gemini_path = GEMINI_SKILLS / skill_name
            print(f"  Creating missing symlink in Gemini for skill '{skill_name}'...")
            if gemini_path.exists() or gemini_path.is_symlink():
                gemini_path.unlink()
            gemini_path.symlink_to(WORKSPACE_SKILLS_GLOBAL / skill_name)
            print(f"  {get_status_emoji(True)} Linked Gemini '{skill_name}' -> global workspace path.")
            
        elif issue.startswith("broken_symlink:"):
            skill_name = issue.split(":", 1)[1]
            gemini_path = GEMINI_SKILLS / skill_name
            print(f"  Recreating broken symlink for '{skill_name}'...")
            gemini_path.unlink()
            gemini_path.symlink_to(WORKSPACE_SKILLS_GLOBAL / skill_name)
            print(f"  {get_status_emoji(True)} Re-linked Gemini '{skill_name}' to global workspace path.")

    # 3. Run sync script to ensure workspace Agents/skills and log are updated
    sync_script = WORKSPACE_DIR / "scripts/sync-skills.sh"
    if sync_script.exists():
        print(f"  Running workspace sync script {sync_script}...")
        try:
            res = subprocess.run([str(sync_script)], capture_output=True, text=True, check=True)
            print(f"  {get_status_emoji(True)} Sync completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Sync script failed: {e.stderr}")
    else:
        print(f"  ❌ Sync script not found at {sync_script}")
        
    # 4. Regenerate Visualizer HTML
    visualizer_script = CLAUDE_SKILLS / "skill-creator-admin/scripts/generate-visualizer.py"
    if visualizer_script.exists():
        print(f"  Regenerating visualizer HTML...")
        try:
            res = subprocess.run([sys.executable, str(visualizer_script)], capture_output=True, text=True, check=True)
            print(f"  {get_status_emoji(True)} Visualizer generated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Visualizer generation failed: {e.stderr}")
            
    print("==================================================")
    print("✨ ALL CORRECTIONS COMPLETED!")
    print("==================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        issues = audit()
        if issues:
            fix_issues(issues)
            # Re-audit
            audit()
    else:
        audit()
        print("\n💡 Run with '--fix' flag to apply corrections automatically.")
        print("💡 E.g. python3 /Users/kasperlandsvig/.claude/skills/skill-creator-admin/scripts/audit-sync.py --fix")

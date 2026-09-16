#!/usr/bin/env python3
"""Zero-dependency HTML Artifact Linter & Sanity Checker.

Validates standalone HTML artifacts against Zero-Node, Corporate-Safe standards:
1. No blocked external scripts (Tailwind CDN, unpkg, cdnjs runtime scripts).
2. Mobile responsive viewport meta tag is present.
3. System font fallbacks are included in font-family definitions.
4. Interactive elements include a round-trip clipboard export affordance.
5. Basic CSS variable and tab target integrity.

Usage:
    python3 lint-artifact.py <path-to-file.html>
"""

import sys
import re
from pathlib import Path

def lint_artifact(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return 1

    content = path.read_text(encoding="utf-8", errors="replace")
    errors = []
    warnings = []

    # Rule 1: No external runtime scripts (Tailwind CDN, React/Vue CDN)
    if "cdn.tailwindcss.com" in content:
        errors.append("Disallowed runtime Tailwind CDN detected ('cdn.tailwindcss.com'). Use semantic vanilla CSS.")
    
    external_scripts = re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)["\']', content, re.IGNORECASE)
    for src in external_scripts:
        if not ("fonts.googleapis.com" in src or "lucide" in src):
            warnings.append(f"External script detected: {src}. Ensure offline compatibility on work laptops.")

    # Rule 2: Viewport meta tag
    if not re.search(r'<meta[^>]+name=["\']viewport["\']', content, re.IGNORECASE):
        errors.append("Missing mobile viewport meta tag (<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">).")

    # Rule 3: Single self-contained file check
    if content.count("<!DOCTYPE") > 1 or content.count("<html") > 1:
        errors.append("Duplicated <!DOCTYPE> or nested <html> tag detected (chrome leak).")

    # Rule 4: System font fallback
    font_families = re.findall(r'font-family:\s*([^;]+);', content, re.IGNORECASE)
    for ff in font_families:
        ff_str = ff.strip()
        # If it's a CSS variable, check if the variable definition contains a system fallback
        if ff_str.startswith("var(--"):
            var_name = re.findall(r'var\(--([a-zA-Z0-9_-]+)\)', ff_str)
            if var_name:
                var_def = re.search(r'--' + re.escape(var_name[0]) + r':\s*([^;]+);', content)
                if var_def and any(fb in var_def.group(1) for fb in ["sans-serif", "serif", "monospace", "system-ui", "-apple-system"]):
                    continue
        if not any(fb in ff_str for fb in ["sans-serif", "serif", "monospace", "system-ui", "-apple-system"]):
            warnings.append(f"Font stack '{ff_str}' lacks a generic system fallback (e.g. sans-serif, system-ui).")

    # Rule 5: Round-trip export affordance on interactive tools
    has_inputs = bool(re.search(r'<(input|select|textarea)\b', content, re.IGNORECASE))
    has_export = bool(re.search(r'(navigator\.clipboard\.writeText|Copy\s+(Decision|as\s+Markdown|Prompt|Review|Selected))', content, re.IGNORECASE))
    if has_inputs and not has_export:
        warnings.append("Artifact contains user inputs (<input>/<select>/<textarea>) but lacks a round-trip clipboard export button.")

    # Rule 6: Check for unmapped CSS variables in <style>
    style_blocks = "".join(re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE))
    if style_blocks:
        defined_vars = set(re.findall(r'--([a-zA-Z0-9_-]+)\s*:', style_blocks))
        used_vars = set(re.findall(r'var\(--([a-zA-Z0-9_-]+)\)', style_blocks))
        unmapped = used_vars - defined_vars
        if unmapped:
            warnings.append(f"Unmapped CSS custom properties: {', '.join(sorted(unmapped))}")

    # Rule 7: Ufravigeligt sprogkrav: ALTID DANSK (da-DK)
    if not re.search(r'<html[^>]+lang=["\']da(-DK)?["\']', content, re.IGNORECASE):
        errors.append("Manglende dansk sprogangivelse (<html lang=\"da-DK\">). Fiskeristyrelsens artefakter SKAL være på dansk.")
    
    english_ui = re.findall(r'>\s*(Copy to Clipboard|Submit|Export as Markdown|Copy Decision as Markdown|Save Changes|View Details|Clear Selection)\s*<', content, re.IGNORECASE)
    if english_ui:
        errors.append(f"Engelsk UI-tekst opdaget: {', '.join(set(english_ui))}. Alle knapper og labels skal være på formelt dansk.")

    # Output Results
    print(f"\n🔍 Linting Artifact: {path.name}")
    print(f"   Size: {len(content):,} bytes")
    
    if errors:
        print("\n❌ Errors (must fix):")
        for err in errors:
            print(f"   - {err}")
    
    if warnings:
        print("\n⚠️  Warnings / Recommendations:")
        for warn in warnings:
            print(f"   - {warn}")

    if not errors and not warnings:
        print("\n✅ All checks passed! Clean, zero-node, corporate-safe single-file artifact.")
        return 0
    elif not errors:
        print("\n✅ Passed with minor warnings.")
        return 0
    else:
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lint-artifact.py <path-to-file.html>")
        sys.exit(1)
    sys.exit(lint_artifact(sys.argv[1]))

#!/usr/bin/env python3
"""Zero-dependency Presentation Artifact Linter & Sanity Checker.

Validates standalone HTML presentation decks against Zero-Node, Corporate-Safe standards:
1. No blocked external scripts (Tailwind CDN, unpkg, cdnjs runtime scripts).
2. Mobile/projector responsive viewport meta tag is present.
3. 16:9 aspect ratio or fixed-ratio stage container defined.
4. Keyboard navigation router present (ArrowRight, ArrowLeft, Space).
5. Presenter HUD engine present (Speaker notes, Fullscreen, Overview grid).
6. System font fallbacks included in font-family definitions.
7. Interactive slides feature a round-trip clipboard export affordance.
8. Single self-contained file with no duplicate DOCTYPE tags.

Usage:
    python3 lint-artifact.py <path-to-file.html>
"""

import sys
import re
from pathlib import Path

def lint_presentation(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return 1

    content = path.read_text(encoding="utf-8", errors="replace")
    errors = []
    warnings = []

    # Rule 1: No external runtime scripts (Tailwind CDN, React/Vue CDN, Reveal.js CDN)
    if "cdn.tailwindcss.com" in content:
        errors.append("Disallowed runtime Tailwind CDN detected ('cdn.tailwindcss.com'). Use semantic vanilla CSS.")
    
    external_scripts = re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)["\']', content, re.IGNORECASE)
    for src in external_scripts:
        if not ("fonts.googleapis.com" in src or "lucide" in src):
            warnings.append(f"External script detected: {src}. Ensure offline compatibility on work laptops.")

    # Rule 2: Viewport meta tag
    if not re.search(r'<meta[^>]+name=["\']viewport["\']', content, re.IGNORECASE):
        errors.append("Missing mobile/projector viewport meta tag (<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">).")

    # Rule 3: Single self-contained file check
    if content.count("<!DOCTYPE") > 1 or content.count("<html") > 1:
        errors.append("Duplicated <!DOCTYPE> or nested <html> tag detected (chrome leak).")

    # Rule 4: 16:9 Aspect Ratio Container
    if not re.search(r'aspect-ratio:\s*16\s*/\s*9', content, re.IGNORECASE) and not re.search(r'presentation-stage|slide-container', content, re.IGNORECASE):
        warnings.append("No 16:9 aspect-ratio or presentation-stage class detected. Ensure presentation conforms to 16:9 screen projection.")

    # Rule 5: Keyboard Navigation Router
    has_nav = bool(re.search(r'(ArrowRight|ArrowLeft|nextSlide|prevSlide|currentSlide)', content, re.IGNORECASE))
    if not has_nav:
        errors.append("Missing keyboard presentation router (ArrowRight/ArrowLeft navigation event listeners).")

    # Rule 6: Presenter HUD Hooks (Fullscreen or Speaker Notes)
    has_fullscreen = "requestfullscreen" in content.lower()
    has_notes = bool(re.search(r'(speaker-notes|toggleNotes|data-notes)', content, re.IGNORECASE))
    if not has_fullscreen and not has_notes:
        warnings.append("Presenter HUD hooks missing: Consider adding 'F' for fullscreen or 'N' for speaker notes drawer.")

    # Rule 7: System font fallback
    font_families = re.findall(r'font-family:\s*([^;]+);', content, re.IGNORECASE)
    for ff in font_families:
        ff_str = ff.strip()
        if ff_str.startswith("var(--"):
            var_name = re.findall(r'var\(--([a-zA-Z0-9_-]+)\)', ff_str)
            if var_name:
                var_def = re.search(r'--' + re.escape(var_name[0]) + r':\s*([^;]+);', content)
                if var_def and any(fb in var_def.group(1) for fb in ["sans-serif", "serif", "monospace", "system-ui", "-apple-system"]):
                    continue
        if not any(fb in ff_str for fb in ["sans-serif", "serif", "monospace", "system-ui", "-apple-system"]):
            warnings.append(f"Font stack '{ff_str}' lacks a generic system fallback (e.g. sans-serif, system-ui).")

    # Rule 8: Round-trip export affordance on interactive tools
    has_inputs = bool(re.search(r'<(input|select|textarea)\b', content, re.IGNORECASE))
    has_export = bool(re.search(r'(navigator\.clipboard\.writeText|Copy\s+(Decision|as\s+Markdown|Prompt|Review|Selected|Tilsynsnotat))', content, re.IGNORECASE))
    if has_inputs and not has_export:
        warnings.append("Deck contains interactive inputs (<input>/<select>/<textarea>) but lacks a round-trip clipboard export button for Q&A decisions.")

    # Rule 9: HTML Unslop (Zero AI Tells & Puffery)
    banned_puffery = ["paradigmeskift", "banebrydende", "revolutionerende", "flagskib", "state-of-the-art", "game-changing"]
    found_puffery = [w for w in banned_puffery if w in content.lower()]
    if found_puffery:
        errors.append(f"AI puffery detected in HTML content: {', '.join(found_puffery)}. Cut the hype, state concrete facts.")

    if "—" in content:
        warnings.append("Em-dash ('—') detected. Avoid em-dash mid-sentence drama connectors; use commas or periods.")

    # Check for emojis in headings
    heading_emojis = re.findall(r'<h[1-6][^>]*>[^<]*[\U00010000-\U0010ffff\u2600-\u27bf][^<]*</h[1-6]>', content)
    if heading_emojis:
        warnings.append(f"Decorative emoji detected in headings ({len(heading_emojis)} instances). Use clean typography instead of emojis.")

    # Output Results
    print(f"\n🔍 Linting Presentation Artifact: {path.name}")
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
        print("\n✅ All checks passed! Clean, zero-node, corporate-safe hybrid presentation artifact.")
        return 0
    elif not errors:
        print("\n✅ Passed with minor recommendations.")
        return 0
    else:
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lint-artifact.py <path-to-presentation.html>")
        sys.exit(1)
    sys.exit(lint_presentation(sys.argv[1]))

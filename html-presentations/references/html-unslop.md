# HTML Artifact Unslop: Visual & Copywriting Doctrine

A strict set of rules to cut machine-generated "AI tells", decorative clutter, and marketing puffery from HTML artifacts, presentation decks, and fagsystem prototypes.

---

## 1. Visual Slop (Design Tells to Ban)

1. **The Badge/Pill Explosion:**
   * **The Tell:** Slapping pill-shaped colored badges (`[AI SUBAGENT]`, `[VERIFICERET]`, `[METODISK]`, `[STATUS: OK]`, `[FASE 01]`) onto every single card, heading, or list item.
   * **The Rule:** Only use a badge when a human or system genuinely needs to triage an operational alert (e.g. `Overtrædelse` vs. `Godkendt`). If an element is just a heading or section name, use clean typography (`font-weight: 600; font-size: 0.85rem`), not a colored pill.

2. **Decorative Emojis:**
   * **The Tell:** Putting emojis in slide titles, section headings, buttons, or bullet points (e.g. 🚀, 💡, 📊, 🔍, ⚡, ⚠️ used ornamentally).
   * **The Rule:** Zero emojis in headings, navigation, and structural labels. Clean SVG icons (12–16px, monochrome) are acceptable on interactive buttons (e.g. download icon on export button) only when they clarify an action.

3. **Generic SaaS Card Grids:**
   * **The Tell:** 3 or 4 identical rectangular cards side-by-side, each featuring an icon inside a rounded pastel square, a bold buzzword title, and 2 lines of generic text.
   * **The Rule:** Let layout follow actual data. Use structured tables, lists with real hierarchy, or asymmetric split views based on the actual information density.

4. **Fake Metrics Without Context:**
   * **The Tell:** Oversized numbers (`100%`, `10x`, `24/7`, `0 kr.`) displayed in colored boxes with vague labels like "Effektivitet" or "Gennemført".
   * **The Rule:** Never display an isolated metric without baseline, unit, and methodology. If stating a fact, write the sentence in plain text instead of dressing it up as a dashboard KPI.

5. **Border-Radius & Shadow Fever:**
   * **The Tell:** Bubbly pill buttons (`border-radius: 9999px`), heavy glowing drop-shadows, and floating cards that look like consumer marketing websites.
   * **The Rule:** Use restrained, architectural Scandinavian design tokens: `border-radius: 4px` (or 2px), crisp `1px solid var(--border)`, flat backgrounds or subtle `0 1px 3px rgba(0,0,0,0.05)` elevation.

---

## 2. Copywriting Slop (Textual Tells to Ban)

6. **Puffery Words (Strictly Banned):**
   * Do NOT use: *paradigmeskift*, *banebrydende*, *revolutionerende*, *flagskib*, *state-of-the-art*, *sømløs*, *helhedsorienteret*, *super høj kvalitet*, *transformative*, *10x*, *game-changing*.
   * **The Fix:** Delete the adjective. State what happened, what the code does, or what the rule says in plain Danish or English.

7. **Contrast Framing ("Ikke bare X, men Y"):**
   * **The Tell:** *"I stedet for statiske dokumenter eller traditionelle metoder demonstrerer denne rapport en ny agil fremtid..."*
   * **The Fix:** Cut the self-congratulatory prelude. State the facts directly: *"Arbejdet d. 27. august omfatter to modeller: 1) x, 2) y."*

8. **Em Dash Addiction (—):**
   * **The Tell:** Using em dashes as mid-sentence drama connectors.
   * **The Fix:** Ban em dashes entirely in HTML artifacts. Use periods, commas, or colons before lists.

9. **Rule of Three & Formulaic Checkmarks:**
   * **The Tell:** Forcing every card or feature list into exactly 3 bullet points starting with green checkmarks (`✓ Feature 1`, `✓ Feature 2`, `✓ Feature 3`).
   * **The Fix:** Use natural numbers. If there are 2 points, list 2. If there are 5, list 5. Use standard list markers or prose paragraphs.

10. **The Fake Corporate Memo Tone (LinkedIn Voice):**
    * **The Tell:** Memos that read like promotional company announcements (*"Kære ledelse, vi har med stor succes eksekveret et agilt gennembrud..."*).
    * **The Fix:** Write like a real, competent senior specialist writing a brief internal note to their boss:
      ```text
      Hej [Navn],
      
      En kort orientering om arbejdet med kontrolforordningen (EU 2023/2842):
      Jeg har bygget to HTML-filer, som kan åbnes direkte i browseren uden servere:
      1. Digitaliseringsstrategi med beregner af sagsbehandlingstider.
      2. Gennemgang af fiskerens rejse med simulator for 10%-tolerancereglen.
      
      Filerne ligger lokalt og kan åbnes i Chrome eller Edge.
      
      Mvh. Kasper
      ```

---

## 3. Quick Self-Audit Checklist Before Declaring Done

Ask these 4 questions of any generated HTML artifact:
1. *Could any sentence in this document appear on a generic marketing landing page?* ➔ If yes, rewrite with specific, concrete operational facts.
2. *Are there badges, emojis, or glowing borders that don't convey critical, dynamic status?* ➔ Strip them.
3. *Does the text praise its own process instead of just reporting results?* ➔ Cut the self-praise.
4. *Can a ministry director read this without cringing at AI buzzwords?* ➔ If doubtful, simplify language further.

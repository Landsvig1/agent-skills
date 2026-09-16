---
name: vibe-description
description: Forfatter, oversætter og optimerer kontante danske beskrivelser (description_da) for katalogelementer (skills, vibes, agents) på vibetrends.dk efter platformens faste standard. Brug altid denne skill når brugeren beder om at skrive, oversætte, formulere eller opdatere danske tekster eller description_da for værktøjer på vibetrends.dk, eller køre backfill af katalogbeskrivelser.
---

# VibeTrends Catalog Copy Standard

Brug denne skill til at skrive eller opdatere `description_da` for katalogelementer (skills, vibes, agents) på vibetrends.dk.

Målet er en skarp, teknisk præcis elevator pitch på dansk, der lyder som en udvikler der forklarer et værktøj til en kollega. Ikke en generisk AI-oversættelse eller reklame.

Denne fil overholder selv sine egne regler. Der er ingen tankestreger i den.

---

## 1. Format og tekniske begrænsninger

1. **Længde:** Præcis 1-2 sætninger (120-160 tegn i alt inklusiv mellemrum).
2. **Ren tekst:** Ingen Markdown (`*`, `**`, `#`, backticks). Teksten indsættes direkte i `<p className="line-clamp-3">`, Open Graph og Google SERP meta-beskrivelser.
3. **Ingen installationskommandoer:** Installationskald varetages af `ConnectBlock` i UI.
4. **Ingen dyb dokumentation:** Detaljerede specifikationer og API-kald hører til i kildens `SKILL.md`/`README.md` (`SkillDocSection`).
5. **Start aktivt:** Begynd direkte med hvad værktøjet gør, fjerner eller automatiserer.

---

## 2. Sproglige regler (lånt fra dk-techblog)

### Forbudte mønstre (AI-tells)
- **Ingen tankestreger:** Hårdt forbud mod em dash og en dash. Brug punktum eller komma.
- **Nul hypeord:** Brug aldrig *revolutionerende*, *banebrydende*, *game-changer*, *intelligent*, *kraftfuld*, *sømløs*, *magisk*, *avanceret*.
- **Ingen kontrast-punchlines:** Undgå "Ikke bare X, men Y" og tilsvarende vendinger.
- **Ingen tricolon-remser:** Undgå opremsninger som "hurtigere, smartere og mere sikkert". Vælg den vigtigste egenskab.
- **Ingen overflødig opvarmning:** Drop "I en verden med...", "Dette værktøj hjælper dig med...". Gå direkte til kernen.

### Fagsprog og mekanik
- **Behold etableret engelsk fagsprog:** *prompt*, *workflow*, *pipeline*, *framework*, *CLI*, *commit*, *review*, *refactoring*, *endpoint*, *token*.
- **Brug naturlige danske ord:** *kildekode*, *fejlhåndtering*, *brugerflade*, *sikkerhedshul*.
- **Sammensatte ord i ét:** *kodebase*, *frontend-komponenter*, *designsystem*, *fejlfinding*.
- **Genitiv uden apostrof:** *modellens*, *værktøjets*, *brugerens*.

---

## 3. Eksempler

### Eksempel 1: Impeccable (Frontend design-standard)
- ❌ **Dårlig (Markdown, bullets, installationsfyld):**
  `* Fjerner det typiske AI-look og transformerer din frontend. Kør npx impeccable install for at komme i gang.`
- ✅ **God (Koncis, aktiv, 137 tegn):**
  `Renser frontend-kode for generisk AI-æstetik og håndhæver faste designregler direkte under kodegenerering.`

### Eksempel 2: Bogholder (Regnskabsautomation)
- ❌ **Dårlig (Hype og AI-klicheer):**
  `Dette intelligente værktøj er en game-changer, der sømløst revolutionerer din momsindberetning.`
- ✅ **God (Konkret handling, 118 tegn):**
  `Automatiserer bogføring, bilagsmatch og momsberegning efter dansk regnskabslovgivning for enkeltmandsvirksomheder.`

### Eksempel 3: Vibe-Vision (UI reverse-engineering)
- ❌ **Dårlig (Passiv og langstrakt):**
  `Et værktøj der er lavet til at hjælpe udviklere med at analysere hjemmesider og genskabe komponenter.`
- ✅ **God (Præcis teknisk handling, 126 tegn):**
  `Analyserer visuelt hierarki og mikrointeraktioner på websites og udtrækker produktionsklare Framer Motion-komponenter.`

---

## 4. Arbejdsgang for opdatering

1. **Undersøg kilden:** Læs kildens `SKILL.md` eller GitHub-repo for at identificere det centrale tekniske udbytte.
2. **Forfat teksten:** Skriv 1-2 sætninger på 120-160 tegn.
3. **Kvalitetstjek før levering:**
   - [ ] Er teksten mellem 120 og 160 tegn?
   - [ ] Er der nul tankestreger (søg efter em dash / en dash)?
   - [ ] Er der nul Markdown-tegn (`*`, `` ` ``, `#`)?
   - [ ] Er alle hypeord og AI-floskler fjernet?
4. **Dataopdatering:**
   - Kør backfill-workflowet:
     ```bash
     node --env-file=.env.local scripts/backfill-danish-descriptions.mjs --export work.json
     # Indsæt den validerede descriptionDa
     node --env-file=.env.local scripts/backfill-danish-descriptions.mjs --apply work.json
     ```
   - Opret **aldrig** enkeltstående indholdsmigrationer under `supabase/migrations/`.

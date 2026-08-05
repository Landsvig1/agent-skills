---
name: fiske-dashboard
description: Opdaterer fiskeriprojektets dashboard (arbejdsgrundlag.html) efter ændringer i projektet — nye retskilder, nye felter fra bilagsudtrækket, besvarede afklaringsspørgsmål, nye frister eller termer. Skanner først projektets tilstand og finder drift mellem disken og dashboardets DATA-objekt, redigerer så DATA, validerer, committer og republicerer artefakten til den samme URL. Make sure to use this skill whenever Kasper nævner fiskeri-dashboardet, arbejdsgrundlaget, sporbarhedskæden, kravrisici, afklaringsbacklogen eller korpusregistret — og generelt når han siger at han har opdateret noget i "Fiskeri Styrelsen"-projektet og dashboardet skal følge med, at dashboardet er forældet, at bilagene skal kobles på, eller beder om en tilstandsscanning af projektet. Trigger også når han beder om at få tilføjet en term, en forpligtelse, en frist eller et dokument til dashboardet, selv om han ikke nævner filnavnet.
---

# Opdatering af fiskeriprojektets dashboard

## Hvad det her handler om

Kasper tiltræder 17. august 2026 som forretningsanalytiker i "Digitalisering og Data
for Fisk". Dashboardet er hans arbejdsgrundlag: otte visninger over EU's og Danmarks
fiskerikontrolregler, bygget så han kan gå fra en forpligtelse til den artikel den
står i, den danske regel der udmønter den, og den frist den falder på.

Projektet ligger her:

```
/Users/kasperlandsvig/Documents/Claude Cowork/Kasper Private/Fiskeri Styrelsen/
```

Andre agenter og sessioner arbejder i samme projekt — manager-agenten fører
`PROJEKT.md`, bilagsudtrækket har lagt et feltkatalog, og korpuset vokser. Derfor
starter du **altid** med at finde ud af, hvad der er sket siden dashboardet sidst blev
opdateret. Antag aldrig at det er ajour.

## Kontrakten ligger i projektet, ikke her

`AGENTS.md` i projektroden er autoritativ for DATA-skemaet, de fire fælder i filen,
republiceringsproceduren og reglerne om hvad du må røre. **Læs den, før du redigerer
noget.** Denne skill dækker arbejdsgangen; AGENTS.md dækker kontrakten. Er de uenige,
vinder AGENTS.md — den bor sammen med koden og bliver vedligeholdt.

Én fælde er dog værd at gentage her, fordi den er blevet begået: strengen
`const DATA = {` findes **to gange** i filen. Anden forekomst er brødtekst i
vedligeholdelsespanelet. Match linjeforankret (`/^const DATA = \{$/`), ellers ødelægger
du filen.

## Arbejdsgang

### 1. Skan tilstanden

```bash
node ~/.claude/skills/fiske-dashboard/scripts/scan.mjs
```

Rapporten giver dig på én gang: hvad DATA indeholder, om valideringen er grøn, hvilke
filer der ligger i `Legal docs/` uden en post i `DATA.corpus`, om bilagenes feltkatalog
er koblet på sporbarhedskæden, om ordlisten er i sync med `DATA.terms`, hvad
manager-agenten mener det næste skridt er, og hvad der er commit'et siden dashboardet
sidst blev rørt.

Læs den, før du gør noget andet. Den fortæller dig oftest selv, hvad opgaven er.

### 2. Læs AGENTS.md og find ud af hvad der skal ændres

Oversæt det scanningen fandt til konkrete ændringer. Sammenhængen mellem hvad der er
sket i projektet og hvor det hører til i DATA:

| Det der er sket | Hvor det hører til |
|---|---|
| Nyt kildedokument hentet | `DATA.corpus` — plus `sec`, `status`, `path`, `rel` |
| Ny retsakt ændrer en forpligtelse | `DATA.chain` — typisk `gf` eller `dk`, og måske `frist` |
| Nye felter eller kodelister fra bilag | `DATA.chain[].risk` eller en ny post; overvej om `gf` nu kan udfyldes |
| Ny eller ændret legaldefinition | `DATA.terms` med `t: "legal"`, `art` er påkrævet |
| Nyt husord fundet i en vejledning | `DATA.terms` med `t: "jargon"`, `konf` og — under `høj` — `sp` |
| Termkonflikt opdaget | `DATA.conflicts` med mindst to `sides` |
| Ny frist eller ændret anvendelsesdato | `DATA.deadlines` |
| Afklaringsspørgsmål besvaret | Fjern det fra `DATA.questions`, og skriv svaret ind hvor det hører til — typisk `terms[].kilde` eller `chain[].risk`. Et besvaret spørgsmål skal forsvinde fra backlogen, ellers vokser den bare. |
| Hul i kæden lukket | Udfyld `gf` eller `dk` på den `chain`-post. Hultallet beregnes som `!gf \|\| !dk` og retter sig selv |
| Antagelse bekræftet indefra | `DATA.gaps` eller den relevante `note` — og markér at det nu er verificeret |

Hvis scanningen viser drift, du ikke kan forklare, så spørg i stedet for at gætte. En
fil på disken uden post i korpusregistret kan være et nyt kildedokument, men den kan
også være et arbejdsspor, der ikke hører i registret — fx en engelsk sprogversion hentet
til sammenligning.

### 3. Rediger DATA

Alt indhold ligger i `const DATA = {…}`. Rendering er fuldt datadrevet, så en tilføjelse
er én tilføjelse i DATA og intet andet. Rør ikke render-laget, medmindre opgaven
faktisk er at ændre hvordan noget vises.

Tre ting der er nemme at komme til at bryde:

- **Afledte tal må ikke hardcodes.** Antal poster, huller i kæden, frister i vinduet og
  sektionstællere beregnes ved rendering. Skriver du et tal ind i markup, lyver det ved
  næste tilføjelse.
- **Unikke nøgler.** `terms.id`, `chain.krav`, `conflicts.term` — udfold-tilstanden i
  UI'et nøgles på dem, så en dublet ødelægger interaktionen. Validatoren fanger det.
- **Citater er ordrette.** Dansk sprogversion, `[…]` for forkortelse, ingen
  normalisering. Kan noget ikke belægges i en navngiven retsakt, skriv `KILDE MANGLER`
  eller `UKLART` — ikke et plausibelt gæt. Hele korpuset er bygget på den regel, fordi
  en opfundet kilde ender som et systemkrav.

### 4. Validér og commit

```bash
cd "/Users/kasperlandsvig/Documents/Claude Cowork/Kasper Private/Fiskeri Styrelsen"
node scripts/validate.mjs
```

Den håndhæver skemaet og domæneinvarianterne — at jargon har konfidens, at
legaldefinitioner har artikelreference, at konfidens under `høj` bærer et spørgsmål, at
filstier findes. Er den rød, så ret det, før du går videre. Exit 1 betyder stop.

Commit først når den er grøn:

```bash
git add -A && git commit -m "dashboard: <hvad der blev tilføjet>"
```

### 5. Vis diffen og spørg, før du republicerer

Republicér **ikke** af dig selv. Vis Kasper hvad der ændrede sig, og spørg.

Sammenfat i stedet for at dumpe diffen: hvilke poster er tilføjet, ændret eller fjernet,
hvordan de afledte tal har flyttet sig (huller i kæden, antal termer, åbne afklaringer),
og om noget kræver hans stillingtagen. Han er i sessionen, og det er billigere at rette
før publicering end efter.

Når han siger til:

```
Artifact-værktøjet · file_path: <projektrod>/arbejdsgrundlag.html
                   · url: https://claude.ai/code/artifact/ebbcd946-6fe7-4d91-874f-158eb003f159
                   · favicon: 🧭
```

`url` skal med, når sessionen ikke selv har publiceret artefakten før — ellers oprettes
en ny URL, og den gamle bliver hængende med forældet indhold. Behold favicon'en; Kasper
finder fanen på den.

## Hvad du ikke skal

- **Rediger ikke `PROJEKT.md`.** Den ejes af manager-agenten. Læs den gerne — den
  fortæller hvad der er verificeret og hvad der stadig er antaget.
- **Omskriv ikke eksisterende citater eller ordlisteposter i `Legal docs/`** uopfordret.
  Du må tilføje nye kildedokumenter og opdatere `00-INDEX.md`, når du gør. Finder du en
  fejl i noget bestående, så rapportér den.
- **Byg ikke nye visninger eller features,** medmindre han beder om det. Dashboardet er
  et opslagsværk, ikke et projekt. Manager-agenten har byggestop frem til
  verifikationsfasen indefra.
- **Slet ikke et afklaringsspørgsmål, fordi det ser besvaret ud.** Kun når svaret
  faktisk er skrevet ind et sted i DATA.
- **Blank aldrig verificeret og antaget sammen.** Intet i projektet er bekræftet
  indefra endnu. Skriver du noget om organisationen eller systemlandskabet, så markér
  hvilken af de to det er.

## Hvis noget er galt med selve filen

Skulle DATA-blokken være ødelagt — validatoren kan ikke parse, eller `scan.mjs` afviser
at afgrænse blokken — så rul tilbage frem for at reparere i blinde:

```bash
git log --oneline -- arbejdsgrundlag.html
git checkout <commit> -- arbejdsgrundlag.html
```

Projektet er sit eget git-repo netop for det tilfælde. Push ikke; der er ingen remote,
og materialet skal ikke offentliggøres.

---
name: bogholder
description: Assisterer med at administrere regnskabsprogrammet (projects/regnskab) og rådgiver om dansk bogføringslovgivning, momsangivelser, tidsfrister samt ejer-mellemregninger. Aktiver denne skill når brugeren nævner regnskab, posteringer, moms, indberetning, bilag, eller ønsker at opdatere eller fejlsøge koden i regnskabsprojektet.
---

# Bogholder Skill

Denne skill gør det muligt at administrere Next.js 16 bogføringsappen i `projects/regnskab/` samt forstå de underliggende danske regnskabsregler, momsfrister og ejer-mellemregninger (indskud/hævninger).

---

## 1. Regnskabsregler & Lovgivning (Danmark)

### Dig og virksomheden er samme person
Dette er en enkeltmandsvirksomhed. Der er ingen adskillelse mellem privat økonomi og virksomhedens økonomi.
* **Privat udlæg**: Udgifter betalt privat bogføres som en `expense` med `paidFrom = "private"`. Dette tæller som et **indskud** (lån til virksomheden) og øger virksomhedens gæld til ejeren.
* **Overførsler**: Ejer kan skattefrit overføre penge til/fra virksomheden. Indsættelse tæller som `deposit` (indskud). Hævning tæller som `withdrawal` (hævning). Ejer beskattes af virksomhedens *overskud*, ikke af hævninger.
* **Moms-eksklusion**: Rene ejer-transaktioner (`deposit` og `withdrawal`) må **aldrig** påvirke momssaldoen. Deres momskode tvinges altid til `"none"`.

### Momskoder og Beregninger
Standard moms i Danmark er 25%. Appen bruger følgende koder:
* `dk25`: Dansk moms (25%). Trækker 20% af bruttobeløbet ud som moms (købsmoms eller salgsmoms).
* `reverse_eu`: Omvendt betalingspligt (køb af ydelser inden for EU). Beregner 25% moms, som bogføres som **både** salgsmoms (skyldig) og købsmoms (fradrag) -> Netto 0 DKK, men skal indberettes i rubrik A.
* `reverse_world`: Omvendt betalingspligt (køb af ydelser uden for EU, f.eks. SaaS som Anthropic, OpenAI, Vercel, GitHub). Beregner 25% moms på samme måde som EU.
* `none`: Momsfritaget eller ikke-momsberettiget (f.eks. rentegebyrer, ejerindskud, hævninger).

### Afskrivninger (Driftsmidler)
* **Straksafskrivning**: Arbejdsredskaber og IT-hardware under småaktivgrænsen på **36.000 kr.** (2026) can straksafskrives (fuldt fradrag i købsåret).
* **Saldoafskrivning**: Aktiver over 36.000 kr. skal afskrives over flere år (typisk 25% om anses). I appen markeres disse med `assetAboveLimit: true` for at flagre dem til det årlige skatteopgør.

### Kvartalsmoms Deadlines (2026)
Som nystartet virksomhed afregnes moms kvartalsvist via TastSelv Erhverv på skat.dk:
* **1. kvartal** (Jan–Mar): Frist **1. juni 2026**
* **2. kvartal** (Apr–Jun): Frist **1. september 2026**
* **3. kvartal** (Jul–Sep): Frist **1. december 2026**
* **4. kvartal** (Okt–Dec): Frist **1. marts 2027**

---

## 2. Projektarkitektur & Kodestruktur

Projektet er placeret i `projects/regnskab` og er bygget med Next.js 16 (App Router), TypeScript strict mode, Tailwind CSS 4, Recharts, samt Octokit som API-database.

### Datalager (Database)
* I udvikling (lokalt) gemmes transaktioner i `.data/data/{år}.json` og bilag i `.data/bilag/{år}/`.
* I produktion (Vercel) gemmes data i et privat GitHub repository (`Landsvig1/regnskab`) via Octokit API commits, hvilket gør lagring gratis og Git-baseret.
* Hovedfilen til interaktion med datalageret er `src/lib/store.ts`.

### Nøglefiler
* `src/lib/store.ts`: Håndterer læsning/skrivning af JSON-filer og upload af PDF-bilag (både lokalt og via GitHub API).
* `src/lib/vat.ts`: Beregner moms og moms-effekter for transaktioner.
* `src/lib/summary.ts`: Aggregerer dashboard-data, kvartalsvise momsindberetninger og den cumulative mellemregningssaldo på tværs af alle år.
* `src/components/transaction-form.tsx`: Formularen til tilføjelse/redigering af posteringer. Håndterer fejltilstande asynkront og forhindrer momsindtastning for ejer-transaktioner.
* `src/app/actions.ts`: Server Actions til oprettelse og opdatering af transaktioner (herunder håndtering af sletning af dubletter ved årsskift).
* `src/middleware.ts`: Sikrer Vercel-produktionsmiljøet med Basic Access Authentication via `BASIC_AUTH_USER` og `BASIC_AUTH_PASSWORD` (bypasses lokalt).

---

## 3. Arbejdsgange for Agenten

### Ændring af kode
Hvis du redigerer logik eller formularer, skal du altid verificere ændringerne med følgende kommandoer i `projects/regnskab`:
1. **Type-check**: `npx tsc --noEmit`
2. **Linting**: `npm run lint`
3. **Kompilering**: `npm run build` (kør med `BypassSandbox: true` da Turbopack resolver stier op til hjemmemappen).

### Fejlfinding i produktion (Vercel)
Hvis appen fejler på Vercel, kan du hente de seneste produktionslogs med:
```bash
npx vercel logs regnskab-sepia.vercel.app -n 20
```
Og hvis du har foretaget ændringer i miljøvariabler, skal du tvinge et nyt build igennem via lokal kompilering og upload:
```bash
npx vercel pull --yes --environment production && npx vercel build --prod && npx vercel deploy --prebuilt --prod --yes
```

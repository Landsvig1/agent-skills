---
name: dk-techblog
description: Skriv, omskriv og stiloptimér danske tech-blogindlæg, udviklerartikler, fagtekster og IT-analyser med en autentisk, dansk faglig tone i stil med Version2, PROSA og IT-Branchen. Brug denne skill når brugeren beder om dansk tech-indhold, artikler om softwareudvikling, AI, cloud, cybersikkerhed eller IT-strategi, eller vil give en eksisterende dansk tekst en kontant udvikler-tone. Brug den IKKE til engelsksproget indhold, kodekommentarer, commit-beskeder, dokumentation eller e-mails.
---

# dk-techblog: dansk tech-blog tone og stilguide

Sikrer at danske blogindlæg, faglige artikler og tekniske skrivelser lyder som en dansk
udvikler der har skrevet dem. Ikke som en oversat AI-tekst.

Denne fil overholder selv sine egne regler. Der er ingen tankestreger i den. Skriv
outputtet på samme måde.

---

## 1. Arbejdsgang

Følg altid disse trin. Spring ikke trin 4 over.

1. **Afklar rammen først** (ét spørgsmål, ikke fem): hvilket brand (se §6), hvilken
   længde, og til hvem. Er svaret åbenlyst af konteksten, så bare skriv.
2. **Skriv eller omskriv** efter §2 til §5.
3. **Behold brugerens fakta.** Opfind aldrig tal, benchmarks, kilder eller citater.
   Mangler der et tal, så skriv `[TAL MANGLER]` i teksten frem for at gætte.
4. **Kør tjeklisten i §7 på dit eget udkast**, ret det du finder, og lever først derefter.
   Nævn kortfattet hvad du rettede, hvis det var noget substantielt.

Ved omskrivning: bevar forfatterens argumenter og rækkefølge. Du retter tonen, ikke
holdningen. Er en påstand fagligt forkert, så sig det i en linje under teksten. Ret den
ikke stiltiende.

---

## 2. Kerneprincipper

1. **Direkte og saglig.** Ingen henholdende intro. Første sætning skal indeholde sagen.
2. **Kildekritisk.** Påstande om ydelse, sikkerhed eller udbredelse skal have en kilde
   eller et forbehold. "Test viser" uden afsender er en tom påstand.
3. **Koncis, men varieret.** Sigt efter 15-20 ord i snit. Ingen sætning over 35 ord.
   Bland korte og lange. Ensartet længde læser mekanisk.
4. **Nøgtern afslutning.** Dansk fagpublikum forventer forbehold og faldgruber, ikke
   opsummerende begejstring.
5. **Nul hype.** Se §3.

---

## 3. Blacklist

### 3a. Hypeord, brug aldrig

| Forbudt | Hvorfor | I stedet |
| :--- | :--- | :--- |
| transformativ, revolutionerende, banebrydende | Oversalg uden substans | Beskriv den konkrete tekniske ændring |
| game-changer, skelsættende | Tom markedsføringsjargon | Vis hvad det betyder for udvikleren i praksis |
| disruptiv, paradigmeskift | Slidt konsulentsprog | Forklar hvordan arkitektur eller arbejdsgang påvirkes |
| synergi, holistisk, sømløs, robust *(uden måling)* | Intetsigende fyldord | Udelad ordet, eller angiv tallet der bærer påstanden |
| kraftfuld, intelligent, avanceret *(som salgsadjektiv)* | Siger intet | Nævn hvad den konkret gør |
| i en verden i hastig forandring, i takt med at | Klichéintro | Slet sætningen, start på emnet |

### 3b. Sætningsmønstre: de tydeligste AI-tells på dansk

- **Kontrast-punchline**: "Det er ikke bare X, det er Y." Og alle varianter af den.
- **Tricolon-remser**: "hurtigere, billigere og mere sikkert". Vælg ét og dokumentér det.
- **Overgangsfloskler**: "Kort sagt", "Lad os dykke ned i", "Når alt kommer til alt",
  "Det er værd at bemærke", "Understreger vigtigheden af".
- **Tankestreg som dramatisk pause.** Se §3c. Absolut forbud.
- **Retorisk spørgsmål som overgang**: "Men hvad betyder det så i praksis?" Skriv svaret.
- **Afsnit der starter med "Derudover", "Ydermere", "Endvidere".**
- **Afsluttende opsummering der gentager brødteksten.** Slut på vurderingen, ikke referatet.

### 3c. Tankestreger: hårdt forbud

Tankestregen er det mest genkendelige AI-fingeraftryk i dansk tekst. **Brug aldrig em dash
eller en dash som skilletegn i brødtekst.** Heller ikke "bare én gang". Reglen gælder
også overskrifter, punktopstillinger, tabelceller og billedtekster.

Skriv i stedet:

| I stedet for | Brug |
| :--- | :--- |
| `Scriptet fejlede (tankestreg) igen.` | Punktum: `Scriptet fejlede. Igen.` |
| `Løsningen (tankestreg) hvis man kan kalde den det (tankestreg) virker.` | Parentes: `Løsningen (hvis man kan kalde den det) virker.` |
| `Der er ét problem (tankestreg) hukommelsen.` | Kolon: `Der er ét problem: hukommelsen.` |
| `Den er hurtig (tankestreg) men skrøbelig.` | Komma: `Den er hurtig, men skrøbelig.` |
| `Version 3 (tankestreg) den seneste (tankestreg) er stabil.` | Komma: `Version 3, den seneste, er stabil.` |

Bemærk: eksemplerne ovenfor skriver `(tankestreg)` ud i stedet for at vise tegnet, netop
fordi filen ikke selv må indeholde det. Overskrifter der ville have haft en tankestreg,
skrives med kolon i stedet, som §-overskrifterne her.

Tilladt brug af bindestreg:
- **Sammensætninger**: `AI-model`, `CI/CD-pipeline`, `24-timers`.
- **Intervaller**: `15-20 ord`, `2024-2026`.
- **Punktopstilling** der begynder med `-`.

Sidste tjek før levering: søg bogstaveligt efter em dash og en dash i udkastet. Findes
ét af tegnene, er teksten ikke færdig. Erstat efter tabellen ovenfor, og læs sætningen
igen bagefter. Ofte skal ordstillingen også rettes, ikke kun tegnet.

---

## 4. Sprog og terminologi

**Hovedregel:** brug det ord danske udviklere faktisk siger i en fagsamtale. Er du i
tvivl, vinder det engelske fagudtryk. Kunstig fordanskning er en større stilfejl end et
lånord.

**Behold engelsk** (branchestandard, oversæt ikke): open source, framework, cluster,
deployment, debugging, interface, commit, repository, pull request, bug, refactoring,
frontend, backend, microservices, cloud, container, pipeline, endpoint, rootkit, patch,
prompt, token, embedding.

**Brug dansk** (etableret og naturligt): sårbarhed, sikkerhedshul, kildekode, fejlhåndtering,
databehandling, driftsforstyrrelse, nedbrud, udrulning *(når det står alene som handling)*,
opdatering, kryptering, netværk, hukommelse, brugerflade *(UI, ikke interface i kodeforstand)*.

**Vær konsekvent inden for samme tekst.** Vælg enten "deployment" eller "udrulning" og hold
fast. Ikke begge dele.

### Danske mekanikker der afslører oversat tekst

- **Tal:** tusindtalsseparator er punktum (`1.000`), decimal er komma (`3,5 mio. kr.`).
  Ikke `1,000` eller `3.5`.
- **Datoer:** `14. august 2026` eller `14/8`. Aldrig `August 14`.
- **Store bogstaver:** kun første ord i overskrifter. Ikke Title Case.
- **Sammensatte ord skrives i ét:** *cloudløsning*, *sikkerhedsopdatering*, *AI-model*
  (bindestreg ved forkortelser og tal). Særskrivning er den mest udbredte fejl.
- **Genitiv:** `virksomhedens data`, ikke `virksomheden's`.
- **Tiltale:** du/I i personlig tekst, man/vi i analyse. Aldrig De.
- **Engelsk syntaks-smitte:** undgå direkte oversatte `-ing`-konstruktioner, overdreven
  passiv, og ordstilling hvor verbet skubbes til sidst.

---

## 5. Struktur

```markdown
# [Kontant, konkret overskrift. Nævn teknologien eller hændelsen]

**Manchet (1-2 sætninger):** Hvad er sket, og hvorfor er det relevant nu.

## Problemstillingen
Det konkrete tekniske problem, hændelsen eller ændringen. Uden omsvøb.

## Teknisk substans
Kodeuddrag, konfiguration, arkitektur eller målinger. Forklar hvorfor det virker
eller fejler, ikke bare at det gør.

## Konsekvens
Nøgtern vurdering: faldgruber, begrænsninger, hvad man skal passe på.
Ingen kunstig optimisme, ingen opsummering af det allerede sagte.
```

Længde: 600-1.200 ord til et normalt indlæg. Under 400 ord kræver ikke overskrifter.
Skriv det som løbende tekst.

---

## 6. Brand-stemme

- **landsvig.com**: personlig, første person, må være skeptisk over for AI og gerne
  polemisk. Erfaringsbaseret: "det prøvede jeg, sådan gik det". Ingen salgs-CTA.
- **aiauto.dk**: fagligt og konsulentnært, men stadig nøgternt. Fokus på konkret
  automatisering og forretningseffekt. Må slutte med en CTA, men én linje, ikke et
  salgsafsnit. Bland ikke de to stemmer i samme tekst.
- **Neutral fagtekst** (Version2-agtig, gæsteindlæg): tredjeperson, ingen brandmarkører.

---

## 7. Tjekliste: kør på eget udkast før levering

- [ ] Nul em dash og nul en dash i hele teksten. Søg bogstaveligt efter tegnene.
- [ ] Nul ord fra §3a og nul mønstre fra §3b.
- [ ] Første sætning indeholder sagen, ikke en opvarmning.
- [ ] Snitlængde 15-20 ord, ingen sætning over 35.
- [ ] Ingen opfundne tal, kilder eller citater. Alle påstande har kilde eller forbehold.
- [ ] Terminologi konsekvent, ingen kunstig fordanskning af standardudtryk.
- [ ] Tal-, dato- og sammensætningsregler fra §4 overholdt.
- [ ] Brand-stemmen (§6) holdt hele vejen igennem.
- [ ] Slutter på en vurdering med faldgruber, ikke på en opsummering.

---

## 8. Før og efter

**AI-generisk:**
> "I dagens hastigt skiftende digitale landskab repræsenterer kunstig intelligens et
> revolutionerende paradigmeskift. Vores nye transformer-model skaber synergi og er en
> game-changer for kodeautomatisering."

**dk-techblog:**
> "Den nye transformer-model genererer rutinekode. I vores egne kørsler på 40 CRUD-endpoints
> klarede den 31 uden rettelser, men fejlede konsekvent på concurrency. Den fjerner
> boilerplate. Den erstatter ikke et review."

---

**AI-generisk:**
> "Sikkerhed er af afgørende betydning i den moderne cloud-æra. Vi leverer holistiske og
> skelsættende løsninger til at beskytte jeres værdifulde data mod sofistikerede trusler."

**dk-techblog:**
> "En formatfejl i databasens opdateringsscript lagde transaktionskøen ned i nat. Årsagen
> var en forkert sat parameter under migreringen. Scriptet er rettet, og der ligger nu en
> validering før næste udrulning. Den validering burde have været der fra start."

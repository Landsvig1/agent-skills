---
name: fiskevisual1
description: Super-optimeret navigationsmotor og retskildeguide til fiskeriloven, EU-kontrolpakken (1224/2009, 2023/2842, 2025/2196), danske bekendtgørelser og feltkataloget i Fiskeristyrelsen. Giver øjeblikkelig routing fra emne/artikel/spørgsmål til præcise lokale filstier, gældende vs fremadrettet ordlyd (2026 vs 2028), bilagsfelter og undgår konsolideringsfælder. Brug altid denne skill når brugeren vil navigere, slå op, finde hjemmel eller analysere retskilder og regler for fiskerikontrol.
---

# Retskilde-Navigator: Fiskerikontrol & EU-Regelgrundlag

En super-optimeret navigationsmotor og opslagsguide til det samlede retskildekorpus for fiskerikontrol. Den eliminerer gætterier, overflødige scanninger og **de klassiske konsolideringsfælder** mellem gældende EU-ret, fremtidige 2028-krav og danske bekendtgørelser.

---

## 1. De 4 Kritiske Navigationsfælder (LÆS FØRST)

Enhver model eller analytiker vil fejle, hvis disse fire faldgruber ignoreres:

1. **FÆLDE 1: Konsolideret 1224/2009 er tabsgivende fremad.**  
   Den konsoliderede tekst af (EF) 1224/2009 pr. 2026-01-10 indeholder **KUN** regler, der er trådt i kraft i 2024 og 2026. Regler med ikrafttrædelse i **2027** (art. 49-53 datavalidering) og **2028** (art. 13 CCTV/REM, art. 9 VMS for fartøjer < 12m, art. 15a eLog for småbåde) findes **IKKE** i den konsoliderede 1224/2009.  
   👉 **Løsning:** Slå altid op i **`Legal docs/eu/original/2842-2023_aendring_kontrolforordning_original.html`** og **`Legal docs/eu/original/2196-2025_gennemfoerelsesforordning_kontrol_original.html`** ved 2027- og 2028-spørgsmål.

2. **FÆLDE 2: Danske bekendtgørelser citerer IKKE EU-artikler.**  
   BEK 1197/2025, BEK 1571/2025 og Fiskeriloven (LBK 205/2023) nævner forordningen i indledningen og lovgiver derefter i egne paragraffer uden at henvise til "artikel X".  
   👉 **Løsning:** Søg aldrig på artikelnumre i danske PDF'er. Søg på emneord (*"tolerancemargen"*, *"vejning"*, *"forhåndsmeddelelse"*, *"anløb"*).

3. **FÆLDE 3: (EU) nr. 404/2011 er ophævet for store, men gælder til 2028 for små.**  
   Gennemførelsesforordning (EU) nr. 404/2011 er formelt ophævet pr. 10. januar 2026 ved (EU) 2025/2196 art. 80. MEN via overgangsbestemmelsen (art. 81) gælder 404/2011 fortsat for fartøjer under 12 meter indtil **10. januar 2028**.  
   👉 **Løsning:** Ved spørgsmål om fartøjer < 12 meter i perioden 2026–2027 skal 404/2011 konsulteres sammen med den nationale bekendtgørelse.

4. **FÆLDE 4: Divergens i officiel terminologi (FOS/FOC vs. VMS/FMC).**  
   Den bindende danske EU-tekst i (EU) 2025/2196 bruger **FOS** (*fartøjsovervågningssystem*) og **FOC** (*fiskeriovervågningscenter*). Styrelsen og branchen bruger engelsk jargon (**VMS** og **FMC**).  
   👉 **Løsning:** Tjek `Legal docs/ordliste/A4-operationelt-jargon.md` for afklaring af divergence.

---

## 2. Emne-til-Kilde Routing Matrix (Super-Fast Lookup)

Brug denne matrix til at gå direkte til de rigtige filer og artikler:

| Emne / Fagområde | Gældende EU-artikel | 2027/2028 Fremtid | Dansk retsakt & § | Lokal primærfilsti (`Legal docs/`) |
|---|---|---|---|---|
| **Logbog & eLog** | 1224/2009 art. 14 (≥12m) | 2842/2023 art. 1, nr. 13 (<12m fra 2028) | BEK 1197/2025 § 1-12 | `eu/konsolideret/1224-2009...html`<br>`dk/bekendtgorelser/BEK-1197-2025...pdf` |
| **10% Tolerancemargen** | 1224/2009 art. 14(3), 2016/1139 art. 13 | 20% usorteret Østersø udløber 2028-01-10 | BEK 1197/2025 § 6 | `eu/konsolideret/1224-2009...html`<br>`eu/konsolideret/1139-2016...html` |
| **VMS / FOS Sporing** | 1224/2009 art. 9, 2025/2196 art. 19 | <12m mobilapp fra 2028; 30 min alle zoner 2027 | Fiskeriloven § 10 | `eu/original/2196-2025...html`<br>`vejledninger/lfst-dk_webtekst...md` |
| **Forhåndsmeddelelse (PNO)** | 1224/2009 art. 17 (4t frist) | 2025/2196 Bilag XV felt 1-44 | BEK 1144/2025 § 3-5 | `eu/konsolideret/1224-2009...html`<br>`eu/original/2196-2025...html` |
| **Landingserklæring** | 1224/2009 art. 23-24 | Start/slut landingstid i 2025/2196 Bilag XV | BEK 1144/2025 § 8-10 | `eu/konsolideret/1224-2009...html`<br>`bilag/feltkatalog.csv` |
| **Vejning & Vejer-tilladelse** | 1224/2009 art. 60 (tilladelseskrav 2026) | Nye EU-vejeregler undervejs (forventet 2027) | BEK 1144/2025 § 14-18 | `eu/original/2842-2023...html`<br>`vejledninger/VEJ_bevilling_foerstegangsomsaetning.pdf` |
| **Førstegangssalg & Salgsnota** | 1224/2009 art. 62-65 (48t frist) | Unikt rejse-ID obligatorisk for alle fra 2028 | BEK 1144/2025 § 19-24 | `eu/konsolideret/1224-2009...html`<br>`eu/original/2196-2025...html` (Bilag XIX) |
| **Transportdokument** | 1224/2009 art. 68 (elektronisk før start) | Medlemsstatsudveksling fra 2027-01-10 (art. 63) | BEK 1144/2025 § 25-28 | `eu/konsolideret/1224-2009...html`<br>`eu/original/2196-2025...html` |
| **Sporbarhed & Partier** | 1224/2009 art. 58 (digitale data) | Forarbejdet fisk/alger indfases først i 2029 | BEK 871/2023 (NaturSkånsom) | `eu/konsolideret/1224-2009...html`<br>`vejledninger/lfst-dk_webtekst...md` |
| **CCTV / REM Kamera** | Frivillig ordning i dag | 1224/2009 art. 13 (obligatorisk ≥18m fra 2028) | BEK 240/2025 (Kattegat) | `eu/original/2842-2023...html`<br>`dk/bekendtgorelser/BEK-240-2025...pdf` |
| **Sanktioner & Point (Art. 92)**| 1224/2009 Bilag III (26 alvorlige overtrædelser) | Fartøjsførere sidestilles med licenshaver | BEK 978/2019 § 1-6 | `eu/konsolideret/1224-2009...html` (Bilag III)<br>`dk/bekendtgorelser/BEK-978-2019...pdf` |
| **Datavalidering & Krydskontrol**| 1224/2009 art. 109 | 2025/2196 art. 49-53 træder i kraft 2027-01-10 | Intern styrelsesinstruks | `eu/original/2196-2025...html` (art. 49-53)<br>`eu/original/2842-2023...html` (art. 109) |

---

## 3. Fil- og Korpusregister (`Legal docs/`)

Alle stier er relative til `Kasper Private/Fiskestyrelsen/Ordbog:Arbejdsgrundlag APP/Legal docs/`:

### A. EU-Retsakter (HTML-format med bevarede artikel-ID'er)
* `eu/konsolideret/1224-2009_kontrolforordning_konsolideret_2026-01-10.html`: **Kernen.** Indeholder alle ændringer markeret med `▼M8` for (EU) 2023/2842.
* `eu/original/2842-2023_aendring_kontrolforordning_original.html`: **Ændringsforordningen.** Læs denne for **Art. 7 (Fristetabellen)** og ordlyden af 2028-artiklerne.
* `eu/original/2196-2025_gennemfoerelsesforordning_kontrol_original.html`: **Gennemførelsesforordningen.** Indeholder datavalideringskravene (art. 49-53) og de tekniske bilag (Bilag I–XIX).
* `eu/original/1766-2025_delegeret_forordning_original.html`: Delegeret forordning om FMC, observatører og pointregister.
* `eu/konsolideret/1380-2013_grundforordning_konsolideret_2023-01-01.html`: **CFP Grundforordningen.** Art. 4 er rod-definitionslisten for hele korpuset. Art. 15 er landingsforpligtelsen.
* `eu/konsolideret/1241-2019_tekniske_foranstaltninger_konsolideret_2026-01-01.html`: Redskabsdefinitioner (art. 6), maskestørrelser og mindstemål.

### B. Danske Retskilder (PDF-format)
* `dk/love/fiskeriloven_LBK-205-2023.pdf`: Hjemmelsloven for alle bekendtgørelser. Tilsynshjemmel i § 117–122.
* `dk/bekendtgorelser/BEK-1571-2025_reguleringsbekendtgorelsen.pdf`: Reguleringsbekendtgørelsen (kvoter, rationer, FKA/IOK).
* `dk/bekendtgorelser/BEK-1197-2025_foering-af-logbog.pdf`: Logbogsbekendtgørelsen (dansk udmøntning af eLog og tolerancer).
* `dk/bekendtgorelser/BEK-1144-2025_registrering-kontrol-landet-importeret-fisk.pdf`: Landings- og salgsnotabekendtgørelsen.
* `dk/bekendtgorelser/BEK-978-2019_pointtildeling-fiskerilicensindehavere.pdf`: Pointtildeling ved alvorlige overtrædelser.
* `dk/bekendtgorelser/BEK-240-2025_frivillig-elektronisk-monitorering-Kattegat.pdf`: Kamera/CCTV-reglerne i Kattegat.

### C. Strukturerede Data & Ordlister
* `bilag/feltkatalog.csv`: Fuldstændigt katalog over samtlige datafelter jf. (EU) 2025/2196 Bilag I–XIX (ERS, PNO, landing, salg, transport).
* `ordliste/A3-legaldefinitioner.md`: 50 autoritative definitioner direkte fra EU- og dansk lovgivning.
* `ordliste/A4-operationelt-jargon.md`: 30 uofficielle fagtermer og systembetegnelser (FOS, FMC, ERS, B-kvoter, RTC) med åbne afklaringsspørgsmål.
* `vejledninger/lfst-dk_webtekst_uddrag_2026-07-27.md`: Udtrukket tekst fra styrelsens officielle vejledningssider.

---

## 4. Super-Hurtig Artikeludtræk (Grep & Shell One-Liners)

For at undgå at loade 3 MB HTML ind i hukommelsen, brug disse præcise udtrækskommandoer:

### Find en specifik artikel i konsolideret EU 1224/2009:
```bash
# Udtrækker artikel 14 (og de næste 40 linjer med ordlyd):
grep -n -A 40 'id="art_14"' "Legal docs/eu/konsolideret/1224-2009_kontrolforordning_konsolideret_2026-01-10.html"

# Find hvor en artikel ændres i EU 2023/2842:
grep -n -C 5 'artikel 14' "Legal docs/eu/original/2842-2023_aendring_kontrolforordning_original.html"
```

### Slå datafelter op i feltkatalog.csv:
```bash
# Vis alle felter knyttet til forhåndsmeddelelse (PNO / Bilag XV):
grep -i "forhåndsmeddelelse" "Legal docs/bilag/feltkatalog.csv" | cut -d',' -f1,2,3,4,5
```

### Udtræk tekst fra en dansk PDF via macOS PDFKit:
```bash
osascript -l JavaScript "scripts/pdf2txt.js" "Legal docs/dk/bekendtgorelser/BEK-1197-2025_foering-af-logbog.pdf" | grep -i -C 3 "tolerancemargen"
```

---

## 5. Tidslinje-Oversigt (Hvornår gælder hvad?)

* **2024-07-10**: 10 % tolerancemargen trådt i kraft (med 20 % dispensation for usorteret pelagisk).
* **2026-01-10**: Hovedbølgen (eLog for $\ge 12$m, salgsnota inden 48t, vejer-autorisation, CATCH-system, nye MDR-formater).
* **2027-01-10**: **Datavalidering (art. 49-53)**, udveksling af transportdokumentdata, nye mærkningskrav for trawl.
* **2027-07-10**: VMS-rapportering hvert 30. minut i samtlige havområder.
* **2028-01-10**: **Fuld digitalisering**: Obligatorisk eLog og VMS for alle fartøjer under 12 meter, obligatorisk CCTV for risikofartøjer over 18 meter, kontrol med fiskeri uden fartøj.

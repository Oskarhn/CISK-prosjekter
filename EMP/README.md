# Håndholdt EMP-generator – 80 Joule

**ADVARSEL: Dette prosjektet involverer livsfarlige spenninger (400 V DC) og ekstremt høye strømmer (>10 000 A). Den elektromagnetiske pulsen kan permanent ødelegge elektronikk, forstyrre medisinsk utstyr og forårsake brann. Bygging og bruk skjer på eget ansvar. Prosjektet er kun ment for kontrollerte laboratorieforsøk med godkjent sikkerhetsopplegg. Les hele dokumentasjonen, spesielt `safety_analysis.md`, før du begynner.**

## Status og begrensninger
Dette er et **teoretisk design under utvikling**. Følgende mangler:
- Ingen fysisk prototype er bygget eller testet.
- Alle ytelsestall er teoretiske beregninger, ikke målte verdier.
- PCB-layout er kun en konseptillustrasjon; produksjonsklare filer finnes ikke.
- 3D-modeller for kabinett er ikke inkludert.
- Full sikkerhetsanalyse er utført, men fysisk verifikasjon gjenstår.

**Les `safety_analysis.md` for en detaljert risikovurdering.**

## Hva er dette?
En komplett byggeveiledning for en batteridrevet, håndholdt elektromagnetisk pulsgenerator (EMP). Enheten lagrer ~80 joule i en stor kondensator og utlader energien gjennom et trigget gnistgap og en flat spiralspole på noen mikrosekunder. Den resulterende strømpulsen på over 9 000 ampere skaper et magnetfelt på nær 0,7 tesla, som induserer ødeleggende spenninger i nærliggende elektronikk.

## Testversjon (anbefalt først!)
Før du bygger den kraftige versjonen, anbefaler vi å bygge en liten, trygg testversjon som demonstrerer konseptet. Se mappen `test_version/` for en enkel 9 V demonstrator som viser prinsippet med RLC-utladning og elektromagnetisk induksjon.

## Egenskaper (hovedversjon – teoretiske)
- **Energi per puls:** 80 J (ved 400 V ladespenning)
- **Toppstrøm:** ~9 200 A (teoretisk, realistisk ~8 000 A)
- **Magnetfelt i spole sentrum:** ~0,68 T (teoretisk)
- **Pulsvarighet:** ~240 µs (dempet sinus)
- **Repetisjonsrate:** 1–2 skudd per 10 sekunder (manuell lading)
- **Strømforsyning:** 6 stk. 9V-batterier i serie (54 V) – LiPo anbefales for bedre ytelse
- **PCB-størrelse:** 80 × 80 mm (lade- og triggerkrets)
- **Totalvekt:** ca. 1,2 kg

## Hvordan navigere i prosjektet?
- `docs/` – Teori, alle beregninger og designvalg (LaTeX)
- `schematic/` – Fullstendig kretsskjema (Circuitikz/PDF)
- `pcb/` – PCB-layoutguide og konseptillustrasjon
- `bom/` – Komponentliste med delenumre og forklaringer
- `build_guide/` – Steg-for-steg byggeveiledning
- `testing/` – Testprosedyrer og forslag til eksperimenter
- `enclosure/` – 3D-modeller for kabinett (må designes)
- `test_version/` – Enkel 9 V demonstrator for å teste teorien
- `safety_analysis.md` – Risikovurdering og sikkerhetsanalyse
- `revision_history.md` – Endringslogg

## Lisens
GPL-3.0

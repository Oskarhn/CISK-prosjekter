# PCB-layoutguide for lade- og triggerkrets

## Spesifikasjoner
- **Størrelse:** 80 × 80 mm, dobbeltsidig FR4, 1.6 mm tykkelse, 35 µm kobber.
- **Minimum isolasjonsavstand:** 2 mm for alle spor som fører >100 V.
- **Sporbredde for høye strømmer:** Minst 2 mm for primærkretsen (batteri, MOSFET, transformator).
- **Jordplan:** Solid jordplan på bunnsiden, med utsparinger under høyspentkomponenter.

## Komponentplassering
1. **Strøminngang:** Plasser skrueterminal for batteri (54 V) i nedre venstre hjørne. Rett ved siden av: sikring F1 og hovedbryter S3 (kan også monteres på panelet).
2. **Flyback-kjerne:** MOSFET Q1, transformator T1, diode D1, zener D2 og diode D4 plasseres i en tett klynge midt på kortet for å minimere sløyfearealet for høyfrekvente strømmer.
   - Q1: TO-220, stående med kjøleribbe (valgfritt). Plasser slik at drain, source og gate er lett tilgjengelige.
   - T1: Ferrittkjerne limes til kortet. Primær- og sekundærviklinger loddes direkte til pads.
   - D1: Stående montering nær transformatorens sekundær.
3. **Høyspentutgang:** D1s katode går til en stor, isolert pad (minst 3 mm bredde) som går til en skrueterminal for tilkobling av ekstern hovedkondensator C1. Denne terminalen bør være i øvre høyre hjørne.
4. **Kontrollkomponenter:** Ladeknapp S1, utladningsknapp S2, LED D3 og motstand R12 plasseres langs høyre kant for enkel tilgang gjennom kabinettet.
5. **Testpunkter:** Legg inn følgende loddeøyer:
   - TP1: Gate på Q1 (for oscilloskopmåling av svitsjeforløp).
   - TP2: Utgangsspenning (katode D1) for voltmetertilkobling.
   - TP3: Jord (stjernejordpunkt).
   - TP4: Spenningsdeler for sikker høyspentmåling (se under).

## Spenningsdeler for høyspentmåling
For å måle utgangsspenningen trygt med et vanlig multimeter, legg til en spenningsdeler:
- R13: 10 MΩ, 1 W (høyspentmotstand, f.eks. Vishay VR68)
- R14: 100 kΩ, 0.25 W
- Koble R13 mellom HV-utgang (katode D1) og TP4.
- Koble R14 mellom TP4 og GND.
- Spenningen på TP4 er V_ut / 101. Ved 400 V vil TP4 vise ~3.96 V.

## Sporingsregler
- **Høyspentnett:** Alle spor som er koblet til D1s katode, C1, gnistgap og utladningskrets må ha minst 2 mm klaring til jordplan og andre signaler. Bruk 2.5 mm spor der det er mulig.
- **Primærkrets:** Sporene mellom batteri, S1, primærvikling og MOSFET må være korte og tykke (≥2 mm) for å minimere induktans og resistive tap.
- **Jord:** Alle jordforbindelser (batteri minus, source Q1, sekundærvikling, C1 minus, utladningskrets, LED) skal samles i ett stjernepunkt nær batteriets minuspol. Unngå sløyfer.
- **Gate-driver:** Sporet fra tilbakekoblingsvikling via R1 til gate bør være kort og holdes unna høyspentdeler.

## Termisk design
- MOSFET Q1 kan bli varm under kontinuerlig lading. Fest en liten kjøleribbe (f.eks. 20 × 20 mm) med varmeledende lim. Sørg for luftstrøm i kabinettet.
- Utladningsmotstand R11 (1 kΩ / 50 W) monteres utenfor PCB på en metallplate eller kjøleprofil, da den kan bli varm under utladning.

## Tilkoblinger til eksterne komponenter
- **Hovedkondensator C1:** Bruk en snap-in kondensator og koble den med korte, tykke ledninger (minst 2.5 mm²) direkte til skrueterminalene på PCB.
- **Gnistgap G1:** Monteres på et separat brett nær spolen. Koble den ene siden til C1 pluss (via tykk ledning) og den andre til spolen.
- **Spole L1:** Loddes direkte til gnistgapets utgangselektrode og jord (C1 minus).
- **Piezo-trigger:** To ledninger trekkes fra piezo-elementet i håndtaket til triggerelektroden i gnistgapet. Den ene ledningen kan kobles til jord.

## Produksjon
- Design PCB-en i KiCad (eller tilsvarende) og generer Gerber-filer.
- Bestill fra f.eks. JLCPCB eller et annet prototyping-firma.
- Alternativt kan du bruke et stripboard (veroboard) og lodde komponentene for hånd, men da må du være ekstra nøye med isolasjonsavstander.

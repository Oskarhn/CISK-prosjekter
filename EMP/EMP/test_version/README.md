# Testversjon – 9 V EMP-demonstrator

Dette er en liten, trygg versjon av EMP-generatoren som demonstrerer det grunnleggende prinsippet: en kondensator utlades gjennom en spole, og det raske magnetfeltet induserer en spenning i en nærliggende pickup-spole. Den er perfekt for å teste teorien før du bygger den kraftige 80 J-versjonen.

## Egenskaper
- **Spenning:** 9 V (ett 9 V-batteri)
- **Energi:** ~0.04 J (40 mJ)
- **Toppstrøm:** ~2 A
- **Pulsvarighet:** ~100 µs
- **Sikkerhet:** Helt ufarlig – kan berøres uten risiko.

## Hva du lærer
- Hvordan en RLC-krets fungerer.
- Hvordan en spole genererer et magnetfelt.
- Hvordan Faradays lov induserer spenning i en pickup-spole.
- Hvordan du kan måle pulsen med et oscilloskop.

## Komponenter (enkle å skaffe)
- 1 × 9 V batteri med klips
- 1 × 1000 µF / 16 V elektrolyttkondensator
- 1 × Trykknapp (momentan)
- 1 × Spole: 10 vindinger 0.5 mm emaljert tråd, ~5 cm diameter
- 1 × Pickup-spole: 20 vindinger 0.2 mm tråd, ~3 cm diameter
- 1 × LED (rød) + 220 Ω motstand (for visuell indikasjon)
- 1 × Oscilloskop (valgfritt, for måling)

## Kretsen
Batteri (+) → Trykknapp → Kondensator (+) → Spole → Batteri (-).  
Pickup-spolen plasseres nær spolen og kobles til LED + motstand (eller oscilloskop).

## Slik virker det
1. Hold trykknappen inne i 2–3 sekunder for å lade kondensatoren til 9 V.
2. Slipp knappen – kondensatoren er nå ladet.
3. Koble spolen raskt til kondensatoren (eller bruk en vippebryter). Kondensatoren utlades gjennom spolen, og strømmen svinger.
4. Det raske magnetfeltet induserer en spenning i pickup-spolen, som får LED-en til å blinke (eller vises på oscilloskopet).

## Byggeveiledning
Se `build_guide.md` for detaljerte instruksjoner.

## Teori
Se `theory.md` for en forklaring av fysikken.

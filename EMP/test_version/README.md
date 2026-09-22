# Testversjon – 9 V EMP-demonstrator

Dette er en liten, trygg versjon av EMP-generatoren som demonstrerer det grunnleggende prinsippet: en kondensator utlades gjennom en spole, og det raske magnetfeltet induserer en spenning i en nærliggende pickup-spole. Den er perfekt for å teste teorien før du bygger den kraftige 80 J-versjonen.

## Egenskaper
- **Spenning:** 9 V (ett 9 V-batteri)
- **Energi:** ~0.04 J (40 mJ)
- **Kretstype:** Overdempet RLC-krets (ingen svingninger)
- **Teoretisk toppstrøm:** ~16.3 A (ikke målt)
- **Pulsvarighet:** Dominerende tidskonstant ~479 µs
- **Sikkerhet:** Lav spenning, men fortsatt elektrisk krets – normal forsiktighet gjelder.

## Hva du lærer
- Hvordan en RLC-krets fungerer (her: overdempet respons).
- Hvordan en spole genererer et magnetfelt.
- Hvordan Faradays lov induserer spenning i en pickup-spole.
- Hvordan du kan måle pulsen med et oscilloskop.

## Komponenter (enkle å skaffe)
- 1 × 9 V batteri med klips
- 1 × 1000 µF / 16 V elektrolyttkondensator
- 1 × Trykknapp (momentan) – for lading (SW1)
- 1 × Vippebryter (eller manuell tilkobling) – for utladning (SW2)
- 1 × Spole: 10 vindinger 0.5 mm emaljert tråd, ~5 cm diameter
- 1 × Pickup-spole: 20 vindinger 0.2 mm tråd, ~3 cm diameter
- 1 × LED (rød) + 220 Ω motstand (for visuell indikasjon)
- 1 × Oscilloskop (valgfritt, for måling)

## Kretsen
Se `schematic.tex` for kretsskjema. Kretsen består av en ladekrets (batteri, trykknapp, kondensator) og en utladningskrets (spole med bryter). Pickup-spolen er separat og kobles til LED eller oscilloskop.

## Slik virker det
1. Hold trykknappen (SW1) inne i 2–3 sekunder for å lade kondensatoren til 9 V.
2. Slipp knappen – kondensatoren er nå ladet.
3. Koble spolen raskt til kondensatoren (ved å slå på vippebryteren SW2 eller berøre ledningene). Kondensatoren utlades gjennom spolen i en **overdempet puls** – strømmen stiger raskt til en teoretisk topp på ~16 A og avtar deretter eksponentielt uten å svinge.
4. Det raske magnetfeltet induserer en spenning i pickup-spolen. Dette kan observeres som et lite blink i LED-en (**hypotese – ikke garantert**, da indusert spenning kan være lavere enn LED-ens fremspenning) eller som en tydelig puls på oscilloskopet.

## Byggeveiledning
Se `build_guide.md` for detaljerte instruksjoner.

## Teori
Se `teori.md` for en forklaring av fysikken, inkludert hvorfor kretsen er overdempet og hvilken pulsform du kan forvente.

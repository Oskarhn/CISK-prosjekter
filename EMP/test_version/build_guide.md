# Byggeveiledning for testversjon

## Trinn 1: Lag spolene
- **Spole L1:** Vikle 10 vindinger 0.5 mm emaljert tråd rundt en sylinder med diameter 5 cm (f.eks. et plastrør). Fest med tape. La to ender stikke ut (ca. 10 cm) og fjern emaljen.
- **Pickup-spole L2:** Vikle 20 vindinger 0.2 mm tråd rundt en 3 cm diameter gjenstand. La ender stikke ut.

## Trinn 2: Koble kretsen
- Bruk et lite koblingsbrett (breadboard) eller lodde direkte.
- Koble batteri (+) til ene siden av trykknappen SW1.
- Andre siden av SW1 til kondensator (+).
- Kondensator (-) til batteri (-).
- Koble en vippebryter (SW2) mellom kondensator (+) og spolen L1. Spolens andre ende til kondensator (-). Alternativt kan du manuelt berøre ledningene for å slutte kretsen (bruk isolerte ledninger).

## Trinn 3: Pickup-krets
- Koble L2 til LED og motstand i serie (anode til motstand, katode til andre ende av L2). Alternativt, koble L2 direkte til et oscilloskop.

## Trinn 4: Test
1. Hold SW1 inne i 2–3 sekunder for å lade kondensatoren.
2. Slipp SW1.
3. Slå på SW2 (eller koble spolen manuelt). Du skal se et lite blink i LED-en (hypotese – ikke garantert, da indusert spenning kan være for lav).
4. For oscilloskop: Koble proben over L2. Still inn 50 mV/div og 50 µs/div. Du skal se en enkel puls (rask stigning, eksponentiell nedgang), ikke en sinus.

## Feilsøking
- Hvis LED ikke blinker: Ikke bekymret – spenningen kan være for lav. Bruk oscilloskop for å verifisere pulsen.
- Hvis ingen puls på oscilloskop: Sjekk at spolen er riktig tilkoblet og at kondensatoren faktisk lades (mål spenning med multimeter).

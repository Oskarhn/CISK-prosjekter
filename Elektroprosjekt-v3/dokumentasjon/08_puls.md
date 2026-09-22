# 08. Pulsanalyse — V3-HIGHPOWER

## Pulsparametere (med usikkerhet)

| Parameter | Teoretisk | Realistisk | Usikkerhet |
|-----------|-----------|------------|------------|
| Spenning | 8000V | 8000V | ±5% |
| Energi | 240 J | 150 J | ±30% |
| Rise time | ~1.4 ns | ~20 ns | ±50% |
| FWHM | ~10 ns | ~30-50 ns | ±50% |
| di/dt | ~400 GA/s | ~25 GA/s | ±60% |

## Tidsforløp (ideal)

0ns: Trigger tenner
5ns: Marx kjede starter
10ns: Alle steg tenner, spenning bygger seg opp
15ns: Peaking gap tenner
20ns: Peak strøm i last
50ns: Puls slukker (energi overført)

**Reelt forløp:** Kan avvike ±20ns pga spark gap variasjon.

## Frekvensspektrum

Teoretisk båndbredde:
$$f_{max} \approx \frac{0.35}{t_{rise}} = \frac{0.35}{20ns} \approx 17.5 MHz$$

**Merk:** Lavere enn 350MHz pga realistisk rise time.
Innholdsrik frekvenser: 1-50 MHz (typisk for EMP).

## Destruktiv effekt (teoretisk)

| Enhet | Terskel | V3-HP (teor) | V3-HP (real) | Status |
|-------|---------|--------------|--------------|--------|
| Forbrukerelektronikk | 1-10 kV/m | 267 kV/m | 160 kV/m | ✓ Skade sannsynlig |
| Industriell utstyr | 10-50 kV/m | 267 kV/m | 160 kV/m | ✓ Skade sannsynlig |
| Militær hardened | 50-100 kV/m | 267 kV/m | 160 kV/m | ? Grense |
| Medisinsk | 0.1-1 kV/m | 267 kV/m | 160 kV/m | ✓ Ødeleggende |

**Viktig:** Dette er **teoretiske** terskler. Reell skade avhenger av:
- Innkapsling av målenhet
- Oriente
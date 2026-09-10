# 06 — Måling (oscilloskop)

Mål: måle **senderstrøm** og **mottatt toppspenning** som funksjon av posisjon, med
innebygd shunt og mottaksspole, på et vanlig 2–4-kanals scope.

## 6.1 Kanaler og forventede verdier

| CH | Probe på | Signal | Forventet | Foreslått skala |
|---|---|---|---|---|
| 1 | **TP3 → TP4** (shuntpar, 10 mΩ) | Senderstrøm × 10 mΩ | 0 → 1,87 V ramp, faller til 0 ved t_pk | 0,5 V/div |
| 2 | **TP7 → TP8** (mottaksspole) | Indusert feltspenning | 9,5 V oppgang + 41,9 V spiss i midten | 10 V/div |
| 3 | **TP1 → F** (kond+) | Kondensatorbankspenning | 24 V → 10,1 V ved t_pk | 5 V/div |
| 4 | **TP5 → F** (gate) / TP6 (555-ut) | Bryterstyring | 0 → 10,5 V, bredde 106,7 µs | 2 V/div |

Bruk 10× passiv probe (10 MΩ, ~10 pF). Shunt og mottak er lavimpedans-kilder, så 10×
probe laster dem ikke.

### Strøm fra shunten
Shunten står i kond−-tilbakekomsten, og bærer derfor **bare påskjæringsstrømmen**
(farihjul går forbi).

```
i(t) = V_shunt(t) / 0,01 Ω
```

Topp: `I_pk = 1,87 V / 0,01 Ω = 187 A`. Mål toppspenningen på CH1 og divider med 10 mΩ.
(1,87 V er verdien ved I_pk; kond+ og shunt deler løkka, så shunten alene avler full
bryterstrøm.)

### Mottatt toppspenning
Mottaksspolen er et kalibrert vitne. Les **spissen** (farihjul di/dt) på CH2 — det er
"mottatt" toppspenning. I midten er det 41,9 V. Denne størrelsen sveiper vi mot
avstand i eksperiment 1.

## 6.2 Avstandssveip (eksperiment 1)

1. Fikser sender og scope. Sett mottaksspolen på en **glidejern / 3D-printet stang**
   langs spoleaksen, slik at sentrum kan steges fra 0 mm til 200 mm.
2. Merk mottakssentrets posisjon relativt til spolesentrum med en lineal; noter hvert z.
3. Ved hvert z: fyr én puls, fang CH2 (mottak) + CH1 (shunt, for å bekrefte I_pk er
   konstant), noter toppspenning V.
4. Sveip oppgangsspenningen (9,5 V i midten) om du vil ha begge.

Forventet kurve (sentraljustert, fra `03_beregninger.md` 3.4):

| z (mm) | 0 | 10 | 20 | 30 | 50 | 100 | 200 |
|---|---|---|---|---|---|---|---|
| V_spike (V) | 41,9 | 28,1 | 10,9 | 4,4 | 1,14 | 0,038 | ~0,005 |
| B (mT) | 104 | 70 | 28 | 11,3 | 2,89 | 0,387 | 0,049 |

Mottatt spenning følger aksfeltet (∝ B), så samme fall forventes.

## 6.3 Timing og trigger

* **Tidsbase:** 50 µs/div for hele ~160 µs hendelsen på ett skjermbilde (eller 20 µs/div
  for å zoome inn på oppgang + spiss).
* **Trigger:** CH4 (555-ut) stigende kant, lav nivå — fyrer ved hvert trykk, stabilt.
* **Enkel-skyt (single trigger):** hendelsen er 104–160 µs; bruk "single" innsamling for
  å fange én puls rent uten at 555 rearmes mellom bilder.
* **Probe jord:** klem CH1 jord til TP4 (shunt lavside) og CH2 jord til mottaket sitt
  jord; hold jordløkka kort.

## 6.4 Hvordan trekke ut tall for rapporten

| Størrelse | Hvordan du leser den | Mål |
|---|---|---|
| I_pk | CH1 topp V ÷ 0,01 Ω | 186 ± 10 A |
| t_pk | tid fra CH4 stigende kant til CH1 topp | 104 ± 10 µs |
| Pulsbredde (til 10 % av topp) | CH1 bredde | ~150 µs |
| B_center | (V_spike / M) × (1/(V_D+I·R₂)/L) → eller bruk mottak B = μ₀NI/...; enklest: B ∝ V_spike, kalibrer med 104 mT-modellen | 104 mT i midten |
| V_spike vs z | CH2 topp vs z (avstandssveip) | tabellen over |
| Farihjul τ | CH1 (eller CH2) fallets tidskonstant etter t_pk | ~11,9 µs |

### Omslag av mottaksspenning til B i midten
Mottaket er en 15-vikt, Ø20 mm spole. Dens gjensidige induktans er M = 2,66 µH, og
`V_spike = M·di/dt`. For å rapportere B direkte, bruk sendermodellen:
`B = μ₀·N·I/(2√(r²+l²/4))` med målt I_pk, eller kalibrer mottaket mot lukket form
én gang (ved z = 0) og skalér. Hver måte: den **relative** V_peak(z) mot avstand er den
robuste målingen.

## 6.5 Vanlige feller

* **Probe jordløkke:** lange jordledninger legger til mV–V av ringing; hold CH2 jordklem
  på mottaket sitt eget terminal, ikke en fjernt rail.
* **555 retrigger:** trigger-differensiatoren (C3) gir nøyaktig én puls per trykk;
  ser du flere spisser, sjekk C3/R2-verdier.
* **Shunt mettet:** 1,87 V er godt innenfor 5 V/div probe; sett ikke CH1 til 50 mV/div
  eller den klippes.
* **Kondensator polaritet:** C1/C2 er polarisert (+) ved kond+ (node A); reversert = vent.
* **24 V forsyning headroom:** ladeladningen er 240 mA; en 24 V/1 A+ labforsyning fungerer.

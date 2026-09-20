# 02 — Kretsskjema

Figur: **`../figurer/kretsskjema.svg`** (i mappen figurer). Alle verdier og enheter står på tegningen.
Nedenfor: beskrivelse av kretsen, netlist, og hvorfor hver komponent er der.

## 2.1 Kretsbeskrivelse

Kretsen har to deler: **pulsveien** (venstre) og **styringen** (høyre), som deler
jordsnoden F.

```
         +24 V (ekstern labforsyning, 0–30 V / 3 A)
   TB1+ ──┬──────────────────────────────────────────────────────┐
          │                                                      │
         [R_CHG 100 Ω / 2 W]                                     │  D4: SMBJ24A TVS (kathode mot +)
          │                                                      │  (klamp på inngangen)
          ┌┴──────────┐   spolestart (D)                         │
         │           │──────┐                                    │
        C1          [COIL_T 15 vikt, luftkjerne]                 │
       470 µF        │        │                                  │
       50 V        spoleende (E)                                 │
        C2          ┌────────┴─────────┐                        │
       470 µF       │ D1: MUR1560      │  R_FW 0,5 Ω / 5 W
      (parallell)   │ (anode E)        ├──────┐  (frihjul-
          │         │                  │      │  snubber)
          │        [IRF3707]           │      │
          │          │D  E (drain)     │      │
          │         [  MOS  ]◄── gate ─┼──┐   │
          │          │S  F             │  │   │
          │          │                 │  │   │
    [R_SHUNT 0,01 Ω / 5 W]             │  │   │
          │                            │  │   │
         TB1− (−)  ────────────────────┴──┴───┴──────────────────┘
         F = jord (MOSFET-kilde = kond− = forsyning− = 555-jord)

   Styring (12 V-rail fra 24 V):
   +24 V ──[R9 820 Ω]── G(12 V) ──[D2 1N4742A 12 V Zener]── F
                          │
                         NE555P  (DIP-8, monostabil)
         pin 8 VCC ← G,   pin 1 GND → F
         pin 4 RESET → G
         pin 5 CTRL ←[C4 100 nF]→ F
         pin 6/7 DIS/THR ←[R1 9,70 kΩ 1%]→ G
                          └──[C_TIM 10 nF C0G]→ F
         pin 2 TRIG ←[R2 10 kΩ]→ G
                          └──[C3 10 nF C0G]──[knapp S1]── F
         pin 3 OUT ──[R3 10 Ω]── gate
         gate ←[R4 10 kΩ]→ F        (nedtrekk)
         gate ←[D3 1N4744A 15 V Zener]→ F   (gate-klamp)

   Mottak:
   15-vikt, 20 mm spole i senderens bore ── 2-pin header (scope)
```

## 2.2 Netlist

| Node | Koblet til |
|---|---|
| **P+** (forsyning+) | TB1+, R_CHG pin 1, D4-kathode |
| **A / D** (kond+) | R_CHG pin 2, C1 topp, C2 topp, spolestart, R_BLEED topp, R_FW ytterste ende |
| **C1m** (mellom) | D1-kathode, R_FW innerste ende |
| **E** (spoleende / drain) | spoleende, MOSFET-drain, D1-anode, TP_COIL_END |
| **F** (jord) | MOSFET-kilde, R_SHUNT ytterste ende, TB1−, C1/C2 bunn, R_BLEED bunn, R4 bunn, D3-kathode, 555 GND/CTRL-kond, knapp S1 ytterste ende, D4-anode, mottaks-tilbakekomst |
| **B / C−** (kond−) | C1/C2 bunn → R_SHUNT innerste ende (shunten står mellom kondensatorbunn og F) |
| **G** (12 V-rail) | R9-slutt, D2-anode, 555 VCC, R1, R2 |
| **Gate** | R3, R4, D3-anode, MOSFET-gate |
| **Trig** (555 pin 2) | R2, C3, S1 |
| **Thr** (555 pin 6/7) | R1, C_TIM |
| **Out** (555 pin 3) | R3 |
| **PU1/PU2** | mottaksspolens ender → header |

Merk: **shunten står i kond−-veien** (kondensatorbunn → R_SHUNT → F). Den måler
derfor *påskjæringsstrømmen* (målt: 0 → 1,87 V), men er **omgått i frihjul**
(frihjul-løkka er bare spole + D1 + R_FW). Shuntspenningen går til 0 V når spissen
kommer — en ren, utvetydig strømsignatur.

## 2.3 Hvorfor hver komponent er der

| Ref | Verdi | Rolle (og hva som går galt uten den) |
|---|---|---|
| C1, C2 | 2 × 470 µF / 50 V lav-ESR | Energilager: 940 µF × 24 V = **270,7 mJ**. Parallell: ESR halvert (≈10 mΩ totalt), halverer strømmen per boks, holder pulsen underdempet som designet. 50 V gir 2× margin. |
| R_CHG | 100 Ω / 2 W | Begrenser ladeladningen fra forsyning til kondensator til 240 mA (topp 5,8 W i ~100 ms, deretter stabil); ~0,5 s til full lading. Uten den ville forsyning og ledninger sett en uendelig strømsteg. |
| R_BLEED | 10 kΩ / ¼ W | Sikkerhetsutladning: kondensatoren faller 24 V → 2 V på ~4 s (τ = 9,4 s). Utladestrøm under puls er 2,4 mA — forsvinnende. Uten den ville banken stått ladd i timer. |
| COIL_T | 15 vikt, 1,0 mm ledning, r = 15 mm | EMP-stråleren. L = 6,69 µH lagrer strømmen; luften kjernen (l ≈ r) maksimerer B på aksen per ampere, samtidig som L holdes lav for høy di/dt. R_coil = 31 mΩ. |
| D1 | MUR1560 (600 V / 15 A ultrahastig) | **Frihjul-/freewheel-diode** over spolen: gir de 187 A en vei når bryteren åpnes, setter frihjul-di/dt sammen med R_FW, og holder drain i MOSFET-en på ≈ v_C + V_D1 (≈11–17 V) — **ingen drain-spike**. Ultrahastig + 15 A-klass: pulsen er 187 A i 54 µs, men ∫i²dt = 0,21 A²s, godt innenfor I_TSM 8/3 ms-ratingen (tilsvarer ~13 A over 2,7 ms). |
| R_FW | 0,5 Ω / 5 W viklet | **Snubber/bremse i frihjulveien**: τ_fw = L/(R_FW+…) = 11,9 µs → spiss på 15,8 MA/s. Fanger 101,7 mJ per puls (≈ 102 mW gjennomsnitt ved 1 Hz). |
| MOSFET | IRF3707 (30 V / 62 A / 1,25 mΩ, TO-220AB) | Bryteren. Krever: lav R_DS(on) (holder ζ = 0,321), pulsert strøm > 200 A (datasheet I_DM ≈ 250 A), 30 V V_DS-rating (avskjeringsspiss ≈ 110 V — overskrir ratingen; se 03_beregninger.md), rask gate (Q_g ≈ 30 nC). |
| R3 | 10 Ω | Gate-styringsmotstand: setter gate-RC ≈ 25 ns (fortere enn nødvendig, men demper gate-sving med ledningens induktans). |
| R4 | 10 kΩ | Gate-nedtrekk: garanterer av etter strømløst eller 555-feil; forhindrer at en flytende gate lår pulsen gå. |
| D3 | 1N4744A 15 V Zener | **Gate-klamp**: eventuell gate-overshoot (parasyttkopling fra 15,8 MA/s-løkka, eller en 24 V feilkobling) klamples ved 15 V < 30 V V_GS-rating. |
| R9 | 820 Ω | Setter 555-rail-strøm: (24−12)/820 ≈ 14,6 mA, rikelig for 555 (~5 mA) + Zener-regulering. |
| D2 | 1N4742A 12 V Zener | **555-forsyningsregulator**: NE555 er ratinget til 15,5 V; rett på 24 V ville den gått i graven. |
| NE555P | DIP-8 | Monostabil: én 106,7 µs puls (output high) per trykk = avskjering ved toppstrøm. Valgt framfor en mikrocontroller: 6 diskrete komponenter, ingen firmware, lett å lodde. |
| R1 / C_TIM | 9,70 kΩ 1% / 10 nF C0G | T = 1,1RC = 106,7 µs ≈ t_pk = 104,2 µs (avskjering 2,5 µs etter toppen, der strømmen fortsatt er 99,9 % av I_pk). C0G for stabil timing. |
| R2 | 10 kΩ | Trigger opptrekk (ledig trigger = 12 V, over ⅔VCC-omretrigger-vinduet). |
| C3 | 10 nF C0G | Trigger-differensiator: å trykke S1 kobler pinen mot jord i ~10–50 µs → nøyaktig **én** puls per trykk, trykksjokk-robust, hold-robust (pinen kommer opp på 12 V lenge før T er brukt, så en holdt knapp kan ikke retrigger). |
| C4 | 100 nF X7R | 555 kontrollspenning (pin 5) bypass. |
| C5 | 10 µF X7R | 555 bulk-kondensator (holder gate-styringstransienten). |
| S1 | 6 × 6 mm takt-knapp | Manual avfyringsknapp. |
| PU (mottak) | 15 vikt, 0,5 mm ledning, r = 10 mm | Feltvitne for scope: M = 2,66 µH → 9,5 V oppgang + 41,9 V spiss i midten. |
| D4 | SMBJ24A TVS | Klamplet *forsyningsinngangen* ved ~38 V (ESD / reversert ledning / lab-transient). Beskytter 50 V kondensatorene, 555-railen og diodene. |
| TB1 | 5,08 mm 2-pin terminal | Ekstern 24 V forsyning. |
| HDR | 2,54 mm pin headers | Scope-testpunkter + mottaksut. |

## 2.4 555 monostabil, pinnkarta (NE555P, DIP-8)

| Pin | Navn | Kobling |
|---|---|---|
| 1 | GND | F |
| 2 | TRIG | R2 → G; C3 → S1 → F |
| 3 | OUT | R3 → gate |
| 4 | RESET | G (alltid klar) |
| 5 | CTRL | C4 → F |
| 6 | THR | R1 → G; C_TIM → F |
| 7 | DIS | bundet til 6 |
| 8 | VCC | G (12 V) |

T = 1,1·R1·C_TIM = 1,1 × 9700 × 10 nF = **106,7 µs**. Timingkondensatoren lades
igjen via den interne DIS-transistoren (< 0,3 µs) mellom pulser, så kretsen rearmes
omedelbart.

## 2.5 Skiftestegsekvens (det scope viser)

1. **t < 0:** kondensatorene ladd til 24 V (R_CHG), 555-ut low, MOSFET av, spole i ro.
2. **t = 0 (knapp):** 555-ut → 10,5 V; gate lades på ~25 ns; MOSFET på. i(t) stiger:
   di/dt(0) = V₀/L = 3,59 MA/s; shunt stiger 0 → 1,87 V; mottaket viser 9,5 V; B bygger
   seg til 104 mT.
3. **t = 104,2 µs:** i toppen på 186,5 A; v_C = 10,11 V.
4. **t = 106,7 µs (555-pulsen slutter):** MOSFET av; strømmen overføres til D1 + R_FW i
   ~100 ns; drain spikker til ≈ 110 V (R_FW-droppen) og avtar mot ~11 V med τ_fw ≈ 12 µs; shunt → 0 V; mottaket
   spisser til 41,9 V (15,8 MA/s); B kollapser over τ_fw ≈ 11,9 µs.
5. **t ≈ 160 µs:** i < 5 mA; feltet er borte; kondensatorene holder 10,11 V og lades
   opp igjen via R_CHG (full lading på ~0,35 s → 1 Hz drift er komfortabelt).

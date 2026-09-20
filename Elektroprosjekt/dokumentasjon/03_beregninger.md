# 03 — Beregninger (trippelsjekket)

Hver hovedstørrelse er regnet med **minst to uavhengige metoder** (tre der det står).
Scriptet `../beregninger/beregninger.py` regner fram alle tallene i denne filen:

```powershell
& "C:\Users\Oskar\AppData\Local\Programs\Python\Python310\python.exe" "...\Elektroprosjekt\beregninger\beregninger.py"
```

Notasjonen følger kursets formelside: ω₀ = 1/√(LC), ζ = R/(2√(L/C)),
ωd = ω₀√(1−ζ²), karakteristisk polynom s² + 2ζω₀s + ω₀².

## 3.0 Designparametere

| Parameter | Symbol | Verdi |
|---|---|---|
| Prespenning | V₀ | 24,0 V |
| Kondensatorbank | C | 2 × 470 µF = 940 µF (ESR ≈ 10 mΩ) |
| Sender: vikt / radius / lengde | N, r, l | 15, 15 mm, 15,28 mm (1,0 mm ledning, tettviklet pitch 1,02 mm) |
| Spolens DC-motstand | R_coil | 30,96 mΩ (1,41 m ledning × 1,72e-8 Ω·m / 0,785 mm²) |
| MOSFET R_DS(on) @ 10 V | R_sw | 1,25 mΩ (IRF3707) |
| Strømmålingsshunt | R_shunt | 10 mΩ |
| PCB + kontaktmotstand | R_trace | 2 mΩ |
| Total løkkmotstand | R_tot | **54,2 mΩ** |
| Frihjulvei | — | D1 (V_D1 = 1,1 V, R_D1 = 30 mΩ) + R_FW = 0,5 Ω + spole → R₂ = 0,561 Ω |
| Mottaksspole | N_p, r_p | 15 vikt, r = 10 mm (Ø20 mm, i boret) |

Lagret energi: `E₀ = ½CV₀² = ½ × 940 µF × 24² = 270,7 mJ`

## 3.1 Poleinduktans L — tre metoder

| Metode | Formel | Resultat |
|---|---|---|
| 1. Wheeler (tilnærming) | L(µH) = r″²N²/(9r″ + 10l″), r og l i inches | **6,925 µH** |
| 2. Neumann/elliptisk, løkke sum | L = N·L_self + 2ΣΣ M(a,b,z), M = μ₀√(ab)[(2/k−k)K(k) − (2/k)E(k)], k² = 4ab/((a+b)²+z²), K/E = komplette elliptiske integraler (Simpson-sjekket: K(0,5)=1,68575, E(0,5)=1,46744) | **6,694 µH** |
| 3. Direkte Neumann linjeintegral | M_ij = (μ₀r²/2)∫cosδ/√(4r²sin²(δ/2)+dz²) dδ, uten elliptiske integraler | **6,694 µH** |

**Designverdi: L = 6,69 µH** (de to eksakte metodene stemmer på 0,00 %; Wheeler er +3,5 %,
som forventes for kort stump spole, l ≈ r).

L_self (én tynn vikt) = μ₀r[ln(8r/w) − 2] + μ₀r/4 = 0,111 µH.

## 3.2 Pulsen — analytisk vs RK4 vs energi

### 3.2.1 Analytisk (kursets lukkede form)

Series-RLC utlading, underdempet (0 < ζ < 1):

```
ω₀   = 1/√(LC)                = 1/√(6,694e-6 × 940e-6) = 12 606,8 rad/s  →  f₀ = 2006 Hz
ζ    = R/(2√(L/C))            = 0,05421 / (2 × √(6,694e-6/940e-6)) = 0,3212
ωd   = ω₀√(1−ζ²)              = 11 938,8 rad/s  →  fd = 1900 Hz
t_pk = (1/ωd)·atan(ωd/ζω₀)    = 104,18 µs
i(t) = V₀/(L·ωd)·e^(−ζω₀t)·sin(ωd t)
I_pk = V₀/(L·ωd)·e^(−ζω₀t_pk)·sin(ωd·t_pk) = 186,52 A
v_C(t_pk) = V₀e^(−ζω₀t_pk)(cos ωd·t_pk + (ζ/√(1−ζ²)) sin ωd·t_pk) = 10,111 V
```

### 3.2.2 RK4 stegvis simulering (dt = 50 ns)

Stadie 1 (bryter på, t < t_pk):  dv_C/dt = −i/C,  di/dt = (v_C − iR_tot)/L
Stadie 2 (bryter av, frihjul):  dv_C/dt = 0 (kondensatorgreina åpen),  di/dt = −(V_D1 + iR₂)/L

| Størrelse | Analytisk | RK4 | Avvik |
|---|---|---|---|
| I_pk | 186,52 A | 186,52 A | **0,00 %** |
| t_pk | 104,18 µs | 104,15 µs | 0,03 % |
| v_C ved avskjering | 10,111 V | 10,117 V | 0,06 % |
| di/dt ved t = 0 | 3,586 MA/s | 3,585 MA/s | 0,02 % |
| maks di/dt stadie 1 (oppgang) | 3,59 MA/s | 3,59 MA/s | — |
| maks di/dt stadie 2 (frihjul) | (V_D1+I_pkR₂)/L = 15,76 MA/s | 15,76 MA/s | — |
| frihjul utlading til < 5 mA | τ_fw = L/R₂ = 11,93 µs; i(t) = (I_pk+V_D1/R₂)e^(−t/τ_fw) − V_D1/R₂ | 54,5 µs | — |

### 3.2.3 Energibalans (lukkingsjekk)

| Hitt | Energi |
|---|---|
| Startenergi i kondensator E₀ = ½CV₀² | **270,72 mJ** |
| Gjenstående kondensatorenergi ½C(10,111 V)² | 48,05 mJ |
| Spole R (begge stadier) | 66,93 mJ |
| R_FW | 101,71 mJ |
| Kondensator ESR | 19,59 mJ |
| Shunt | 19,59 mJ |
| MOSFET | 2,45 mJ |
| PCB spor/kontakter | 3,92 mJ |
| Diode D1 (Vf + dynamisk) | 8,43 mJ |
| **Σ (gjenstående + dissipert)** | **270,66 mJ** |

**Balansefeil = 0,021 % → OK (< 1 %).** De tre metodene (lukket form, numerisk, energi)
stemmer med hverandre.

## 3.3 Magnetfelt — tre metoder

| Metode | B i midten (I = 186,52 A) |
|---|---|
| 1. Lukket formel, endelig spole: B = (μ₀nI/2)[(z+l/2)/√((z+l/2)²+r²) − (z−l/2)/√((z−l/2)²+r²)] | **104,43 mT** |
| 2. Direkte sum av eksakt aks felt fra hver vikt: B = Σ μ₀Ir²/(2(r²+d²)^1,5) | **104,44 mT** |
| 3. Uendelig-spole-grensen μ₀nI = μ₀NI/l | 230,10 mT (idealgrense; 2,2× høyere fordi l ≈ r) |

Metode 1 og 2 (begge eksakte) stemmer på **0,01 %** → **B_center = 104 mT = 0,104 T**.

Aksfall ved toppstrøm (lukket form = vikt sum, eksakt):

| z fra midten | B | | z fra midten | B |
|---|---|---|---|---|
| 0 mm | 104,4 mT | | 30 mm | 11,3 mT |
| 5 mm | 94,1 mT | | 50 mm | 2,89 mT |
| 10 mm | 69,8 mT | | 100 mm | 0,387 mT |
| 20 mm | 28,0 mT | | 200 mm | 0,049 mT |

## 3.4 Mottaks M og indusert spenning — to metoder

| Metode | M |
|---|---|
| 1. Løkkepar elliptisk sum (225 vikt-par, eksakt) | **2,658 µH** |
| 2. Fluksmetode: M = N_p·A_p·(dB/dI)\|midten | 2,638 µH (avvik 0,7 %) |

Indusert spenning `v = M·di/dt` (mottaket i midten av spolen):

| Hendelse | di/dt | v_mottak |
|---|---|---|
| Oppgang (t = 0, brattest oppgang) | 3,586 MA/s | **9,53 V** |
| Frihjul-spiss (t = t_pk) | 15,76 MA/s | **41,90 V** |

Posisjonsavhengighet (for avstandsforsøket, `09_eksperimenter.md`):

| z (mottaksforskyvning) | M | V_rise | V_spike |
|---|---|---|---|
| 0 mm | 2,658 µH | 9,53 V | 41,90 V |
| 10 mm | 1,781 µH | 6,39 V | 28,08 V |
| 20 mm | 0,692 µH | 2,48 V | 10,90 V |
| 30 mm | 0,279 µH | 1,00 V | 4,40 V |
| 50 mm | 0,072 µH | 0,26 V | 1,14 V |

## 3.5 Elektriske og termiske belastinger (1 puls, 1 Hz)

| Del | Belastning | Merking | Vurdering |
|---|---|---|---|
| MOSFET (IRF3707) | I_D = 187 A puls (≈ 100 µs); V_DS,max ≈ 110 V (avskjeringsspiss: v_C + V_D1 + i·(R_D1+R_FW)) | I_DM ≈ 250 A pulsert; 30 V | V_DS,max ≈ 110 V (avskjering) — overskrir 30 V-ratingen |
| Kondensatorbank | 24,0 V → 10,11 V (ingen negativ utslenging — D1 blokkerer revers; frihjul går forbi kondensatoren) | 50 V | OK |
| D1 (MUR1560) | 187 A i 54 µs; Q = 2,1 mAs; ∫i²dt = 0,208 A²s; E = 8,4 mJ | 15 A kont.; I_TSM 8/3 ms ≈ 150–200 A (tilsvarer 0,29 A²s) | OK: I²t er 72 % av 8/3 ms-ratingen for én puls |
| R_FW (0,5 Ω/5 W) | 101,7 mJ/puls; 102 mW gjennomsnitt ved 1 Hz; tråddelt ΔT ≈ 11 K (adiabatisk) | 5 W | OK |
| Spoleledning (9,9 g kobber) | 66,9 mJ/puls → ΔT = 0,02 K | — | OK |
| Shunt (10 mΩ/5 W) | topp 348 W i ~100 µs (19,6 mJ) | 5 W | OK (energi, ikke topp, teller for ms-ratinger) |
| R_CHG (100 Ω/2 W) | topp 5,76 W som faller, 271 mJ/lading | 2 W | OK |
| PCB-strømbane | 10 mm × 35 µm kobber: 1,47 mΩ/30 mm; I²t-varme forsvinnende | — | OK (ligger i R_trace-marginen) |
| 555 (12 V-rail) | V_CC = 12 V (D2 Zener fra 24 V; R9 = 820 Ω → 14,6 mA) | maks 15,5 V | OK |
| Gate | V_GS = 10,5 V på (555-ut @ 12 V), klampes ved 15 V (D3) | 30 V abs. max | OK |

Gjentakelse: ved 1 Hz lades kondensatoren 10,11 → 24 V gjennom R_CHG på
t = −RC·ln((24−23,6)/(24−10,11)) ≈ 0,33 s ≪ 1 s periode → **1 Hz kontinuerlig drift OK**.

## 3.6 555 monostabil dimensjonert

```
T = 1,1·R·C = 104,2 µs  →  R = T/(1,1 × 10 nF) = 9471 Ω
```

Bruk **R1 = 9,70 kΩ 1 % + C_TIM = 10 nF C0G → T = 106,7 µs**. Bryteren slås av
2,5 µs etter toppstrømmen, der i(106,7 µs) = 186,25 A = **99,85 % av I_pk** — innenfor
±10 % L-toleransevinduet (t_pk skiftes ∓10 %, I_pk med < 5 %).

## 3.7 Spennings-skaling (eksperiment 3)

Med L, C, R faste skalerer I_pk, B og V_ind lineært med V₀:

| V₀ | I_pk | B_center | E_cap | mottaksspiss | Merknad |
|---|---|---|---|---|---|
| 12 V | 93 A | 52 mT | 67,7 mJ | 21,0 V | samme deler, halv effekt |
| **24 V** | **187 A** | **104 mT** | **270,7 mJ** | **41,9 V** | **grunn-design** |
| 48 V | 373 A | 209 mT | 1,08 J | 83,8 V | 50 V kondensatorer OK (48 < 50); drainspiss ≈ 220 V → krever 300 V+ MOSFET |
| 100 V | 777 A | 435 mT | 4,70 J | 174,6 V | krever HVT kondensatorer (>100 V) + 100 V MOSFET |
| 240 V | 1865 A | 1,04 T | 27,1 J | 419 V | krever serie-kondensatorstak + HVT deler |

## 3.8 Viktantal-sveip (eksperiment 2)

Wheeler L + analytisk pulsmodell, r = 15 mm, tettviklet 1,0 mm ledning, 24 V, 940 µF:

| N | L (µH) | I_pk (A) | B_c (mT) | di/dt oppgang (MA/s) | di/dt frihjul (MA/s) | mottaksspiss (V) | B @ 50 mm (µT) |
|---|---|---|---|---|---|---|---|
| 8 | 2,62 | 280,9 | 90,8 | 9,16 | 59,0 | 89,9 | 2257 |
| 10 | 3,74 | 242,3 | 96,1 | 6,42 | 36,0 | 67,2 | 2450 |
| 12 | 4,96 | 214,5 | 99,8 | 4,84 | 24,2 | 53,1 | 2622 |
| **15** | **6,93** | **184,5** | **103,3** | **3,47** | **15,1** | **39,8** | **2859** |
| 18 | 9,01 | 163,0 | 104,9 | 2,66 | 10,4 | 31,5 | 3084 |
| 20 | 10,46 | 151,8 | 105,2 | 2,29 | 8,4 | 27,4 | 3233 |
| 25 | 14,20 | 130,5 | 104,1 | 1,69 | 5,4 | 20,4 | 3614 |
| 30 | 18,09 | 115,3 | 101,5 | 1,33 | 3,8 | 15,9 | 4026 |
| 40 | 26,11 | 94,8 | 94,2 | 0,92 | 2,3 | 10,6 | 5025 |

Lesing: B_center er nesten flatt (91–105 mT) fra N = 8…40 — tettviklet spole gir
B ≈ I/pitch uansett N. Det som endres er *tidsoppløftet*: færre viklinger → lavere L →
høyere I_pk, mye brattere frihjul (N = 8: 59 MA/s, 90 V spiss i mottaket), kortere
feltimpuls. N = 15 balanserer feltstyrke (104 mT), strøm (187 A), stigning
(15,8 MA/s) og 1 Hz-ladebudsjettet. (Eksakte modellverdier ved N = 15: I_pk = 186,5 A,
B_c = 104,4 mT — sveipet bruker Wheelers L, som er +3,5 % der.)

## 3.9 Trippelsjekk-oppsummering

| Størrelse | Metode 1 | Metode 2 | Metode 3 | Avstemming |
|---|---|---|---|---|
| L (µH) | 6,925 (Wheeler) | 6,694 (elliptisk) | 6,694 (Neumann-integral) | 3,5 % (eksakt par: 0,00 %) |
| I_pk (A) | 186,52 (lukket form) | 186,52 (RK4) | — (energikonsistent) | 0,00 % |
| t_pk (µs) | 104,18 | 104,15 | — | 0,03 % |
| Energi (mJ) | 270,72 lagret | 270,66 Σ(dissipert + gjenstående) | — | **0,021 %** |
| B_center (mT) | 104,43 (lukket form) | 104,44 (vikt sum) | 230,1 (uendelig grense, ideal) | 0,01 % |
| M_mottak (µH) | 2,658 (løkkepar) | 2,638 (fluksmetode) | — | 0,7 % |
| Mottaksspiss (V) | 41,90 (M × analytisk di/dt) | 41,90 (M × RK4 di/dt) | — | 0,00 % |

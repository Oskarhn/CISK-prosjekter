# 01 — Kretsdrift

## 1.1 Hva det er

En EMP-generator er en kondensatorutlading. En kondensatorbank lades opp til 24 V, så
slippes den gjennom en spole med en MOSFET som bryter. Strømmen blir en dempet sinus som
når 186,5 A etter 104 µs. Da slås bryteren av, og feltet kollapser fort (se 1.3). Alle
ledninger og PCB-lag i nærheten av spolen får en spenning indusert i seg:

```
v_offer(t) = M_offer · di/dt        (gjensidig induktans × strømstigning)
```

Det er denne spenningen som gjør skade. To ting må være store, og de krever motsetninger
av spolen:

* **Toppstrøm I_pk** — setter feltstyrken (B ∝ I) og fluksendringen.
  I_pk ∝ V₀·√(C/L): vil ha liten L, stor C, høy V₀.
* **Strømstigning di/dt** — setter den induserte spenningen i offeret.
  di/dt ∝ V₀/L ved påskjering, og (V_D + I_pk·R_fw)/L ved frihjul: vil ha liten L.

Antallet viklinger N blir kompromisset (se 1.7): N = 15 gir best balanse mellom felt,
rekkevidde og stigning på en plate på 80 × 80 mm.

## 1.2 Pulsen: dempet series-RLC

Når bryteren slås på, er kretsen en series-RLC: kondensatorbank C, totalt motstand R,
spole L. KVL:

```
L·di/dt + R·i + v_C = 0 ,        v_C = (1/C)∫i dt
```

Setter man inn i = C·dv_C/dt, får man den andreordens likningen på formelskemaform:

```
d²v_C/dt² + 2ζω₀·(dv_C/dt) + ω₀²·v_C = 0
```

med størrelsene fra formelsiden:

```
ω₀ = 1/√(LC)                    naturlig frekvens
ζ  = R/(2·√(L/C))               dempingsgrad
ωd = ω₀·√(1−ζ²)                 dempt frekvens
```

Verdier (sjekket i `03_beregninger.md`):

| Parameter | Verdi |
|---|---|
| L | 6,69 µH |
| C | 940 µF |
| R (hele løkka) | 54,2 mΩ |
| ω₀ | 12 607 rad/s → **f₀ = 2,01 kHz** |
| ζ | **0,321** (underdempet, 0 < ζ < 1) |
| ωd | 11 939 rad/s → fd = 1,90 kHz |

For 0 < ζ < 1 blir strømmen:

```
i(t) = (V₀/(L·ωd)) · e^(−ζω₀t) · sin(ωd·t)
```

Toppen:

```
t_pk = (1/ωd)·atan(ωd/(ζω₀))  =  104,2 µs
I_pk = (V₀/(L·ωd))·e^(−ζω₀·t_pk)·sin(ωd·t_pk)  =  186,5 A
```

Kondensatoren synker som:

```
v_C(t) = V₀·e^(−ζω₀t)·(cos ωd·t + (ζ/√(1−ζ²))·sin ωd·t)
```

Når bryteren slås av (t = t_pk) står kondensatoren på **10,11 V** — den har levert
270,7 − 48,0 = 222,7 mJ av de 270,7 mJ den hadde lagret.

**Hvorfor ζ ≈ 0,3.** Hvis ζ → 0 ville pulsen svingt på 2 kHz i mange halvperioder — en
lang sinus, ikke en puls. Hvis ζ → 1 blir utladningen langsom og flat (overdempet:
I_pk → 0). Toppstrømmen blir størst i lett dempet område: med ζ = 0,321 og 54 mΩ i
løkka blir pulsen én kraftig topp, ca 100 µs bred ved halv topp.

## 1.3 Avskjering og frihjulsspissen

En fritt svingende RLC er ikke en EMP — den svinger bare på 2 kHz i noen ms. Triks:
**slå av bryteren akkurat ved toppstrømmen.**

* Mens MOSFET-en er på (0 … t_pk) er strømstigningen *oppgangen*:
  `di/dt ≈ V₀/L = 3,59 MA/s` (størst ved t = 0, deretter ned mot som v_C faller).
* Ved t_pk åpnes bryteren. Polestrømmen kan ikke endres umiddelbart, så den må finne en
  ny vei: **frihjul-dioden D1 + snubberen R_FW** over spolen. Likningen blir

```
L·di/dt = −(V_D1 + i·(R_coil + R_FW + R_D1))      (kondensatorgreina åpen)
```

altså eksponensiell nedgang med tidskonstant

```
τ_fw = L/(R_coil + R_FW + R_D1) = 6,69 µH/0,561 Ω ≈ 11,9 µs
```

Startstigningen i frihjul er:

```
di/dt|_fw = −(V_D1 + I_pk·R₂)/L = −(1,1 + 186,5·0,561)/6,69µ = −15,8 MA/s
```

**4,4× brattere enn oppgangen.** Det er denne skulderen som gir den store spissen i
mottaksspolen og i alle offerløkker. Strømmen er under 5 mA etter ca 54 µs, så hele
hendelsen varer ≈ 160 µs.

Frihjul-løkka inneholder bare spole + D1 + R_FW. Kondensatoren er koblet til node D,
men bryteren på andre enden er åpen, så **ingen strøm går gjennom kondensator, shunt
eller strømforsyning** i frihjul: kondensatorspenningen fryses på 10,11 V, det blir
ingen negativ utslenging, og drain i MOSFET-en spikker til `v_C + V_D1 + i·(R_D1+R_FW) ≈ 110 V`
ved avskjering (R_FW-droppen dominerer, og overskrir 30 V-ratingen). Dioden står **bare over spolen** (ikke over
spole + bryter): den skiller hovedløkka fra bryteren og gjør frihjul til en ren
eksponentiell.

## 1.4 Magnetfeltet

En spole med N viklinger, lengde l og radius r gir på aksen:

```
B(z) = (μ₀·n·I/2)·[ (z+l/2)/√((z+l/2)²+r²) − (z−l/2)/√((z−l/2)²+r²) ] ,   n = N/l
```

i midten (z = 0):

```
B_center = μ₀·N·I / (2·√(r² + l²/4))
```

Med N = 15, r = 15 mm, l = 15,3 mm, I = 186,5 A:

```
B_center = 0,104 T  = 104 mT        (1000× jordens magnetfelt)
```

Tre uavhengige beregninger (lukket formel, direkte sum av feltet fra hver vikt, og
uendelig-spole-grensen μ₀nI) stemmer på 0,01 %. Uendelig spole gir 230 mT — 2,2× for
mye, fordi spolen er kort (l ≈ r).

Fallet langs aksen (eksakt, ved toppstrøm):

| Avstand fra midten | B |
|---|---|
| 0 mm | 104 mT |
| 10 mm | 70 mT |
| 20 mm | 28 mT |
| 30 mm | 11,3 mT |
| 50 mm | 2,9 mT |
| 100 mm | 0,39 mT |

Feltet er et **nårfelt**: utenfor ca 2 spolelengder faller det som ~1/z³. Det er både en
begrensning (skade innenfor ~5–30 cm) og en egenskap (et offer 1 m unna merker ingenting).

## 1.5 Gjensidig induktans: hva offeret ser

En offerløkke med areal A ved spolens posisjon har gjensidig induktans

```
M = (fluks som lenker løkka per ampere) ≈ B(1 A)·A_offer   (jevnt felt)
```

Spenningen i løkka er `v = M·di/dt`. Mottaksspolen vår — 15 viklinger, Ø20 mm — er et
kalibrert vitne av feltet. Beregnet i midten av senderen:

```
M_pickup = 2,66 µH
v_rise   = M·(V₀/L)          = 2,66 µH × 3,59 MA/s  =  9,5 V
v_spike  = M·(V_D+I·R₂)/L   = 2,66 µH × 15,8 MA/s  = 41,9 V
```

Et offer-PCB med en 10 cm² løkke tett oppe i spolen (M ≈ 0,9 µH) ser ~14 V på
frihjul-spissen — nok til å presse ESD-vernede I/O-pinner over sine absolutte
maksverdier, forstyrre analoge frontend-kretser, resette MCU-er med
undervoltage-beskyttelse, og stresse dioder i effektkretser. Et offer med 100 cm²
løkkeareal (f.eks en håndholdt enhet med batteri + kort) ser ~10× så mye.

## 1.6 Hvorfor bryteren står på lavside

MOSFET-en står **under** spolen (kilde mot jord). Grunn: ved t = 0 står kondensator og
terminal på 24 V. På høyside ville MOSFET-kilden stått på ~24 V også, da må gate drives
*over* 24 V + V_GS(th) for å slå på, og å dra gate mot jord for å slå av gir V_GS =
−24 V ved t = 0 når det skal lede — en dødlås i gatestyringen. På lavside drives gate fra
555 på 0…10,5 V mot jordet kilde:

* **På:** V_GS ≈ 10,5 V (555-ut ved 12 V-rail) → R_DS(on) ≈ 1,25 mΩ.
* **Av:** 10 kΩ nedtrekk + 15 V gate-Zener → V_GS ≤ 0, robust mot bakpuls og
  parasyttkopling.

555-timeren (monostabil) gir én puls med fast lengde per trykk (T = 1,1RC = 106,7 µs ≈
t_pk), så avskjeringstiden er satt av RC, ikke av hånden.

## 1.7 Hvorfor N = 15

Alt henger på N gjennom L(N) og spolemotstanden:

* **B_center ≈ μ₀·N·I/(2√(r²+l²/4))**: for tettviklet spole B ≈ I/pitch, nesten
  uavhengig av N (flere viklinger ved lavere strøm).
* **I_pk ∝ V₀·√(C/L)**: faller med N.
* **di/dt = V₀/L**: faller fort (L vokser som ~N²).
* **Frihjul τ = L/R**: vokser med N → lengre, mykere nedgang.
* **Rekkevidde**: lengre spole (flere N) sender feltet lenger.

Sveip (N = 8…40, fulltabell i `03_beregninger.md` 3.8; sveipet bruker Wheelers L,
N = 15-raden er designpunktet fra eksakt modell):

| N | L (µH) | I_pk (A) | B_center (mT) | frihjul di/dt (MA/s) | mottaksspiss (V) |
|---|---|---|---|---|---|
| 8 | 2,62 | 281 | 91 | 59,0 | 90 |
| 10 | 3,74 | 242 | 96 | 36,0 | 67 |
| **15** | **6,69** | **187** | **104** | **15,8** | **42** |
| 20 | 10,46 | 152 | 105 | 8,4 | 27 |
| 30 | 18,09 | 115 | 101 | 3,8 | 16 |
| 40 | 26,11 | 95 | 94 | 2,3 | 11 |

N = 15 holder I_pk ≈ 187 A (kraftig felt, 104 mT i midten), di/dt = 15,8 MA/s (42 V i
en liten vitnsspole) og en hendelse på 104 µs — samtidig som spolen passer i et 31 mm
bore og frihjul avtar innenfor 1 Hz-gjentakelsesbudsjettet. N = 8 er en lovlig
«bruteste spiss»-variant for forsøksdelen (`09_eksperimenter.md`).

## 1.8 Energi

Lagret: `E₀ = ½CV₀² = 270,7 mJ`. Ved t_pk sitter det fortsatt 48,0 mJ (10,11 V) i
kondensatoren. Fordeling (RK4, eksakt på 0,02 %):

| Hitt | Energi |
|---|---|
| Spole (kobber, begge stadier) | 66,9 mJ |
| R_FW 0,5 Ω snubber | 101,7 mJ |
| ESR i kondensatorer (10 mΩ) | 19,6 mJ |
| Shunt 10 mΩ | 19,6 mJ |
| MOSFET | 2,5 mJ |
| Spor/kontakter på PCB | 3,9 mJ |
| Diode D1 (Vf + dynamisk) | 8,4 mJ |

Det største tapet er R_FW — det er frihjul-bromsen som gjør at toppstrømmen blir en
bratt spiss. Uten den ville τ = L/R_coil ≈ 216 µs, og frihjul di/dt var ca 1 MA/s.

## 1.9 Referanser

* Formelside: ING2508 *Kretsteknikk* — andreordens respons `s² + 2ζω₀s + ω₀²`, dempt
  sinus, energi i L og C.
* Forelesninger: *Project introduction* (komponentbudsjett, oppgavestruktur),
  *Grunnleggende & Måleutstyr* (scope-måling), *Lodding* (lodding).
* Fagbok-behandling: andreordens overgang i series-RLC (impulsrespons); spolefelt via
  Biot–Savart/Ampère; gjensidig induktans via flukslenking (Faraday: v = M di/dt).
* Spoleinduktans: Wheelers formel (tilnærming) mot Neumann-integralet
  M(a,b,z) = μ₀√(ab)[(2/k−k)K(k) − (2/k)E(k)] med komplette elliptiske integraler K, E.

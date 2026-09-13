# 05 — Poler (sender + mottak)

## 5.1 Sender (COIL_T)

| Parameter | Verdi | Hvorfor |
|---|---|---|
| Vikt N | 15 | Balansepunkt fra N-sveipen (`03_beregninger.md` 3.8) |
| Gjennomsnittsradius r | 15 mm (Ø30 mm, Ø31 mm med ledning) | Passer på 80 mm-platen med kondensatorbank rundt; r setter B og L |
| Ledning | 1,0 mm massivt isolert kobber (17 AWG) | Tåler 187 A med 31 mΩ tap; tykk nok til å lodde; 1,02 mm tettviklet pitch |
| Lengde l | 15,28 mm = (N−1)×1,02 + 1,0 | Tettviklet: l ≈ r gir best aksfelt for kort spole |
| L (design) | 6,69 µH (Wheeler: 6,93 µH) | 3.1 |
| R_coil | 30,96 mΩ (1,41 m ledning) | 3.0 |
| Former | 29 mm ID × ~18 mm, **ikke-ledende** tube (PVC, polyamid, eller 3D-printet PLA) | **Viktig:** metalltube = kortsluttet vikt → virvelforvik + feltkansellering |
| Montering | på 4 × M3 nylon-søkk (6 mm) over platen, limt med litt epoksy i bunn | Holder spoleaksen sentrert; søkkene løfter den over jordsjappen |

### Viklingsprosess

1. Vikle 15 vikt på en mandrel på 29–30 mm ID (en 30 mm plasttube, et 30 mm hjørn,
   eller mottaksformer + spacers), med jevnt avstand mellom viktene (mål pitch 1,02 mm —
   for tettviklet holder du bare viktene i kontakt).
2. La en tupp på 60–80 mm på hver ende (fjern 10 mm isolasjon med kniv/loddejern).
3. Skyv spolen over (eller på) 29 mm ID × 18 mm tube; sjekk OD ≈ 31 mm, lengde ≈ 15,3 mm.
4. Lodd de to tupene til COIL_T-padene (se `07_pcb_layout.md`).

### Toleranseeffekt

| Feil | Effekt |
|---|---|
| ±1 vikt (14–16) | L ∓ ~15 %, I_pk ± ~7 %, t_pk ∓ ~7 % — pulsen holder |
| Pitch 0,9–1,2 mm (litt/medviklet) | L ± 10–20 % via avstandstermene; I_pk ∓ 5–9 % — akseptabelt |
| Ledning 0,8 mm i stedenfor 1,0 mm | R_coil 1,6× (50 mΩ) → ζ ≈ 0,40, I_pk ≈ 172 A (−8 %) — fortsatt greit |
| r = 13 mm (viklet mindre) | L − ~15 %, B − ~10 % |

## 5.2 Hvordan man måler spolens induktans

Tre praktiske metoder (bruk minst to; de må stemme innen ~10 %):

1. **LCM-meter på 1 kHz (best).** Forvent: **6,7–6,9 µH**, ESR ≈ 31 mΩ. Hvis LCM-måleren
   bare kan 100 kHz, greit — luftenkjernens L er frekvens-uavhengig her.
2. **RC-tidskonstant fra pulsen selv (uten utstyr).** Kortslutt spolen gjennom en kjent
   motstand R_k (f.eks. 10 Ω) fra en ~10 V forsyning, fang strømfallet på scope via en
   0,1 Ω shunt: fallets konstant er τ = L/R_k → L = τ·R_k. Med R_k = 10 Ω blir
   τ ≈ 0,67 ms — lett å måle. (Eller motsatt: kjør spolen med en firkantbølge og mål
   strømotgangen til 63 %.)
3. **Fra pulsen (post-build sjekk).** Mål t_pk og I_pk på den ferdige platen og løs for L
   (scriptet `../beregninger/beregninger.py` kan få målte I_pk/t_pk og regne L ut). Forventet målt L:
   6,5–7,2 µH (±10 %).

**Mål for rapporten:** målt L = 6,7 µH ± 0,7 µH. Hvis LCM-avlesning < 5 µH eller > 8 µH,
sjekk vikling (løse vikt, kortsluttede vikt, feil viktantal).

## 5.3 Mottaksspole (PU)

| Parameter | Verdi | Hvorfor |
|---|---|---|
| Vikt | 15 | M = 2,66 µH i midten → 41,9 V spiss (rent scope-avles, < 50 V) |
| Radius | 10 mm (Ø20 mm) | Passer i 30 mm-boret med 5 mm frie rom per side |
| Ledning | 0,5 mm isolert kobber (32 AWG) | Bærer bare scope-strøm (µA); liten = stiv |
| Former | 18 mm OD × 16 mm tube (eller viklet rundt senderens indre kjerne) | Ikke-ledende |
| Montering | limt til en kryss/spacer i sentrum av spoleaksen; tupene går **langs aksen** | En ledning parallell med B fanger ingen EMF; axiale tupper = rent signal |

Vikling: 15 tette vikt på en 18–20 mm mandrel (mål pitch ~1,05 mm), tupper 100–150 mm,
skyv på former, posisjoner i midten av senderen. Lodd tupene til 2-pin header (TP7/TP8).

**Verifisering:** M fra pulsen = V_spike/di/dt. Med di/dt = 15,76 MA/s (målt fra shunt-
kanalen: 1,87 V / 0,01 Ω / 15,8 MA/s sjekk) og V_spike ≈ 41,9 V → M ≈ 2,6 µH. Får du
< 1 µH er mottaket utenfor sentrum eller for få vikt.

## 5.4 Hvorfor ikke annen geometri (forklaring av eksperiment 2)

* **Flat spiral** (alle 15 vikt i ett plan, Ø30 mm skive): L synker til ~2 µH, B i midten
  lik per ampere men feltet er 2-D (stort bare i planet); god "pancake EMP"-variant,
  enklere offer-kobling for flate PCB-er.
* **Flere vikt / lengre** (N = 30, l ≈ 31 mm): feltet når lenger (B@50 mm 4,0 mT mot
  2,9 mT) men spissen halveres (15,9 V) og I_pk synker til 115 A.
* **Færre vikt** (N = 8): 90 V mottaksspiss, 59 MA/s, 281 A — «bruteste» varianten;
  svaktere vedvarende felt (91 mT).

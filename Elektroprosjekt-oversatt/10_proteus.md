# 10 — Proteus-simulering (kursets "kretssimulering"-del)

Kurset (ING2508 *Kretsteknikk — Måleteknikk og kretssimulering*) bruker **Proteus** for
kretsskjemategning, transientsimulering og PCB-layout (per *Proteus-introduksjons*-
forelesningen: nytt prosjekt → kretsskjemategning → komponentvalg → simulering →
PCB-layout med designregler → eksporter PDF). Denne filen er bygge-/simuleringsguiden for
nettopp det.

## 10.1 Bygg kretsskjemaet i Proteus (ISIS)

Opprett et nytt prosjekt, og plasser deretter (søk i Proteus-biblioteket):

| Del | Proteus-biblioteksvalg | Notater |
|---|---|---|
| NE555 | `555` (Timer-kategori, DIP-8) | Standardmodell |
| MOSFET | `IRF540N` (effekt-MOSFET) — eller IRF3707 hvis tilgjengelig | IRF540N har R_DS(on) ≈ 44 mΩ → ζ ≈ 0,57, I_pk ≈ 145 A: en god nok erstatning; noter avviket i rapporten |
| D1 | nærmeste ultrahurtig likeretter (søk `MUR*` / `1N49*`), 600 V-klasse | Setter frihjul-Vf ≈ 0,7–1,1 V |
| D2 / D3 | `1N4742A` / `1N4744A` (Zener-kategori) | 12 V / 15 V |
| D4 | TVS eller utelates i simulering | Betyr kun noe for forsyningstransienter |
| COIL_T | `INDUCTOR` med **L = 6,69 µH** + seriell **31 mΩ motstand** | Proteus-spoler er ideelle — spole-R må legges til manuelt |
| PU (mottak) | `INDUCTOR` **L = 3,6 µH**, koblet til COIL_T med **k = 0,54** (M = 2,66 µH) | Koblingen settes i spolens egenskaper (gjensidig kobling til den andre spolen) |
| Shunt | 10 mΩ motstand | Som designet |
| Alt annet | 0805/gjennomhull-passive komponenter som i `schematic.svg` | Verdier i `04_komponentliste.md` |

Koble nettlisten nøyaktig som i `02_kretsskjema.md` §2.2 (nettlisten er fasiten). Legg til
virtuelle instrumenter: to **virtuelle oscilloskop** (eller et VirtualScope-kanalsett) —
ett over shunten (strøm), ett over mottaket.

## 10.2 Simuleringsoppsett

* **Analyse:** Transient.
* **Start:** 0 s, **Slutt:** 500 µs.
* **Steg:** 100 ns (løser opp ~100 ns avslåingsovergangen og 41,9 V-spissen; 1 µs er
  akseptabelt for den langsomme ringingen).
* **Kondensatorens starttilstand:** C1/C2 → IC = 24 V (forhåndsladet bank).
* **Forsyning:** 24 V ideell kilde (eller en 24 V DC-forsyningsmodell).
* **Trigger:** driv 555-triggeren med en 200 µs pulskilde ved t = 10 µs (i stedet for
  knappen) slik at kjøringen er repeterbar.

## 10.3 Forventede simuleringsresultater

| Størrelse | Håndberegning | Forventet simulering |
|---|---|---|
| 555-utgangsbredde | 106,7 µs | 105–108 µs |
| I_pk | 186,5 A | 170–195 A (MOSFET-modellens R_DS(on)) |
| t_pk | 104,2 µs | 100–110 µs |
| Kondensatorspenning ved avslåing | 10,1 V | 10 ± 1 V |
| Mottaksstigning / spiss | 9,5 V / 41,9 V | 9 V / 35–48 V |
| Frihjulsavtagning | τ ≈ 11,9 µs | 10–13 µs |

**Godkjenningskriterium:** I_pk og t_pk innenfor ±20 % av håndberegningen.
Modellnivå-forskjeller (MOSFET R_DS(on), diode Vf, ideell spole) er forventet og bør
diskuteres — den diskusjonen *er* simuleringsdelen av rapporten.

## 10.4 Kjente modellbegrensninger (angi dem i rapporten)

1. **Ideell spole:** ingen frekvensavhengig kobbertap, ingen kapasitans mellom
   vindinger → simuleringsringingen er noe renere enn virkeligheten.
2. **MOSFET-gatemodell:** bibliotekets gate-ladningsmodell kan gjøre avslåingen
   tregere enn den virkelige IRF3707-en (~100 ns), noe som utvisker 41,9 V-spissen;
   hvis simuleringsspissen ser for liten ut, reduser gate-drivmotstanden
   (R3 = 10 Ω → 2,7 Ω) eller bruk 555-utgangen direkte.
3. **555-modell:** gjennomsnittlig presisjon; utgangsstigningen (~µs) forsinker
   påslåingen litt — neglisjerbart mot t_pk = 104 µs.
4. **Koblede spoler:** k = 0,54 forutsetter perfekt fluksjustering (mottak sentrert).
   Mottak utenfor senter → lavere k → lavere spiss (avstandseksperimentet i
   simuleringen: senk k trinnvis og noter spissfallet).
5. **Proteus SPICE-konvergens:** en 187 A / 15 MA/s-krets med en 10 mΩ shunt kan gi
   "convergence"-advarsler — reduser tidssteget til 10 ns lokalt eller legg til 1 mΩ
   seriemotstand i shuntmålepunktet.

## 10.5 PCB-layout i Proteus (AURORA)

Per forelesningens PCB-prosess:

1. **Pinner/footprints:** tildel en pakke til hver del (DIP-8, TO-220, 0805, 2-pin
   header, 5,08 terminal, spolepads som to 3 mm sirkler + via-klase).
2. **Design Rule Manager:** klaringer ≥ 6 mil for < 10 V-nett (spor-til-spor,
   spor-til-pad, pad-til-pad, platekant); lagtildeling for de to signallagene;
   nettklasse "power" for strømløkken med 8 mm sporbredde.
3. **Platekant:** 80 × 80 mm rektangel.
4. **Plassering:** per `07_pcb_layout.md` §7.1 (strømløkke kompakt, 555 i et hjørne,
   spole sentrert på avstandsstykker).
5. **Ruting:** manuell (strømløkken må være 8 mm bred — autoruteren gjør ikke det)
   eller autoruter med nettklassebegrensningene for power.
6. **Eksport:** Output → export graphics → PDF, **silk-laget avkrysset av** (per
   forelesningen: "Make sure no silk is selected").

Den eksporterte PDF-en er PCB-figuren for rapporten; Proteus' kretsskjemategnings-
eksport er "kretsskjema (klare bilder og komponenter, verdier med enheter)"-figuren som
kreves av oppgavemalen — sørg for at alle komponentverdier og enheter er synlige.

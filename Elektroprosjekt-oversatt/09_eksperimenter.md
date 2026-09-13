# 09 — Foreslåtte eksperimenter

Hvert eksperiment: hypotese → prosedyre → forventet resultat (fra den verifiserte
modellen) → hva som skal plottes. Alle predikerte tall kommer fra `calculations.py`
(tabeller i `03_beregninger.md`).

## Eksperiment 1 — Mottatt toppspenning vs. avstand (hovedeksperimentet)

**Hypotese:** den mottatte (mottaks-)spenningen faller med avstand omtrent som
on-aksefeltet til en solenoide: sterk innenfor ~30 mm, neglisjerbar utover ~150 mm.

**Prosedyre:** skyv mottaksspolen langs aksen i 10 mm steg fra 0 til 200 mm; ved hvert
steg noter spisstoppen (CH2) og shunttoppen (CH1, for å bekrefte at senderen er
konstant). Bruk tabellen i `06_maling.md` §6.2.

**Forventet (modell):**

| z (mm) | 0 | 10 | 20 | 30 | 40 | 50 | 75 | 100 | 150 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|
| V_spiss (V) | 41,9 | 28,1 | 10,9 | 4,4 | 1,9* | 1,14 | 0,30 | 0,038 | 0,007 | 0,002 |
| B (mT) | 104 | 70 | 28 | 11,3 | 5,5* | 2,89 | 0,85 | 0,387 | 0,11 | 0,049 |

(\*interpolert.) **Plott:** V_spiss vs. z, log-log — forvent stigningstall ≈ −3 utover
~30 mm (dipol-nærfeltsfall).

**Konklusjon å konstatere:** EMP-skaderekkevidden på dette kortet er ~5–30 cm; enheten er
en *punktforsvars*-forstyrrer, ikke en romryddende en.

## Eksperiment 2 — Sammenligning av spolegeometri

**Hypotese:** for tettviklede solenoider er B_senter nesten uavhengig av N
(B ≈ I/pitch), men di/dt, I_pk og spissen skalerer som 1/L(N) — færre vindinger =
skarpere, svakere-felt puls; flere vindinger = mildere, lengre-rekkevidde puls.

**Prosedyre:** vikle om senderspolen (eller vikle 3–4 reservespoler) for N = 8, 15, 20,
30 (samme 1,0 mm ledning, samme Ø30 mm). For hver: LCR-mål spolen, avfyr, noter I_pk,
t_pk, B_senter (via mottaksskalering eller et gaussmeter), mottaksspiss, og B ved 50 mm.

**Forventet (modell, `03_beregninger.md` §3.8):**

| N | L (µH) | I_pk (A) | B_c (mT) | mottaksspiss (V) | B @ 50 mm (µT) |
|---|---|---|---|---|---|
| 8 | 2,6 | 281 | 91 | 90 | 2258 |
| 15 | 6,7 | 187 | 104 | 42 | 2859 |
| 20 | 10,5 | 152 | 105 | 27 | 3233 |
| 30 | 18,1 | 115 | 101 | 16 | 4026 |

**Plott:** I_pk, spiss og B@50 mm vs. N — én kurve opp (rekkevidde), én kurve ned
(spiss). Dette viser designavveiningen direkte og begrunner N = 15.

**Bonusvariant:** en **flat spiral** (15 vindinger i et plan, Ø30 mm skive, ~2 µH): B er
sterk kun i planet; egnet for kobling til et flatt offer-PCB plassert mot flaten.

## Eksperiment 3 — Spenningsskalering

**Hypotese:** I_pk, B og mottatt spenning skalerer lineært med V₀ (L, C, R faste).

**Prosedyre:** avfyr ved V₀ = 12, 24, 48 V (benkforsyning; 48 V er trygt for 50 V-
kondensatorene og 75 V-MOSFET-en — drainklampen stiger til ~33 V, sjekk det på scopet).
Noter I_pk, spiss, B.

**Forventet:**

| V₀ | I_pk (A) | B_c (mT) | E_kond (mJ) | mottaksspiss (V) |
|---|---|---|---|---|
| 12 | 93 | 52 | 68 | 21 |
| 24 | 187 | 104 | 271 | 42 |
| 48 | 373 | 209 | 1083 | 84 |

**Plott:** alle tre vs. V₀ — rette linjer gjennom origo. Angi skaleringsveien til
100 V / 240 V (kondensatorstabel i serie, HV-kondensatorer, 100 V+ MOSFET) fra
`03_beregninger.md` §3.7.

## Eksperiment 4 — Offertester (selve "skade"-demonstrasjonen)

Velg ofre med kjente skadeterskler:

1. **Kredittkort / telefon-NFC:** hold 0–10 cm fra spoleflaten; avfyr. Statiske
   magnetstriper slettes ved ~10–50 mT vedvarende, men *pulsen* sletter via
   lesehodets respons — prøv 1 cm, 5 cm, 10 cm og noter slettingsavstanden.
2. **LED + motstand i serie (100 Ω):** plasser over en 10 cm løkke nær spolen; pulsen
   bør blinke den (løkken ser titalls volt på kort avstand).
3. **Bar MCU (ATmega328)-kort, 5 V:** plasser 5 cm unna, avfyr. Forvent reset/
   fastlåsing på kortest avstand (dens titalls-cm²-jordløkker plukker opp > 10 V spisser).
4. **Scope som offer:** klem en 1 MΩ probe med en 10 cm løkke på benken; vis den
   oppfangede spissen på en annen kanal.

**Sikkerhet:** hold telefon/klokke > 30 cm unna; ikke avfyr mot noe du ikke kan erstatte.

## Eksperiment 5 — Sveip av frihjulsmotstand

**Hypotese:** frihjul-di/dt settes av τ_fw = L/(R_FW + R_coil + R_D1); mindre R_FW =
lengre, mildere avtagning; større R_FW = skarpere spiss men kortere total feltvarighet.

**Prosedyre:** bytt R_FW = 0,25 Ω, 0,5 Ω, 1,0 Ω (trådviklet). Noter spissspenning,
frihjuls-τ, og B ved 50 mm etter 30 µs (sen-felt-sammenligning).

**Forventet (modell):**

| R_FW | τ_fw (µs) | spiss di/dt (MA/s) | mottaksspiss (V) |
|---|---|---|---|
| 0,25 | 14,2 | 11,5 | 30,6 |
| 0,50 | 11,9 | 15,8 | 41,9 |
| 1,00 | 6,4 | 24,6 | 65,5 |

**Konklusjon:** 0,5 Ω er balansepunktet; 1 Ω maksimerer spissen (best for å "drepe en
brikke" på kort avstand), 0,25 Ω maksimerer feltvarigheten (best for å slette
magnetiske medier).

## Rapportering av disse eksperimentene

For hvert: angi hypotesen (1 linje), tabellen, plottet, avvik mellom målt og modell i %,
og ett avsnitt med analyse knyttet til teorien (ζ, ω₀, τ, M·di/dt). Det er nøyaktig den
"kretsdrift"- + "referanse"-dybden oppgavemalen tillater.

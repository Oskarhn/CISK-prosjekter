# Teoretisk verifikasjon av EMP-generator

Dette dokumentet etablerer de teoretiske kravene for at prosjektets matematiske modeller skal representere det fysiske systemet. Det skilles mellom matematisk konsistens, fysisk gjennomførbarhet og praktisk ytelse.

## 1. Teoretiske verifikasjonskrav

### 1.1 Hovedkrets (80 J)

**Fysisk prinsipp:** Energi lagret i en kondensator utlades gjennom en spole og et gnistgap, og danner en underdempet RLC-krets. Den resulterende strømpulsen genererer et tidsvarierende magnetfelt som induserer spenning i nærliggende ledere (Faradays lov).

**Matematiske antagelser:**
- Kretsen er en ideell serie RLC-krets med konstante parametere.
- Induktansen L er konsentrert og frekvensuavhengig.
- Kapasitansen C er ideell uten lekkasje.
- Motstanden R er konstant og inkluderer ESR, ledningsmotstand og lysbuemotstand.
- Gnistgapet lukkes øyeblikkelig og har ingen spenningsfall etter tenning (idealisert).
- Ingen parasittiske kapasitanser eller induktanser av betydning.

**Nødvendige inngangsparametere:**
- C = 1000 µF (nominell, må verifiseres)
- L = 1,9 µH (estimert fra Wheeler-formel, må måles)
- R = total kretsmotstand (antatt ~80 mΩ, ikke målt)
- V₀ = 400 V (ladespenning, kontrollerbar)

**Støtte fra produsentdokumentasjon:**
- C: Nichicon LLS2W102MELC – datablad oppgir kapasitans, ESR, maksimal rippelstrøm, men ikke pulsstrøm ved 10 kA.
- MOSFET: IRF840 – datablad oppgir statiske grenseverdier, ikke repetitiv pulsytelse i denne topologien.
- Dioder: UF4007 – datablad oppgir reverse recovery og strømgrenser, men ikke transient termisk respons.

**Estimerte/antatte parametere:**
- L: Beregnet fra geometri, ikke målt.
- R: Antatt basert på typiske verdier for ESR og lysbue; lysbuemotstand er svært variabel.
- Magnetfelt: Beregnet fra ideell spoleformel, ignorerer nærfeltseffekter og skjerming.

**Modellens begrensninger:**
- Lysbuen i gnistgapet er ikke-lineær og tidsvarierende.
- Spolens induktans endres med frekvens (skin-effekt, nærhetseffekt).
- Strålingstap er neglisjert.
- Termiske effekter endrer resistans under pulsen.

**Konklusjoner som kan etableres teoretisk:**
- Kretsen er underdempet under de antatte parametere.
- Toppstrømmen vil være i størrelsesorden kiloampere.
- Magnetfeltet i sentrum av spolen vil være i størrelsesorden 0,1–1 T.

**Konklusjoner som krever eksperimentell verifikasjon:**
- Faktisk toppstrøm, pulsform, magnetfeltstyrke, indusert spenning i offerkretser, destruktiv rekkevidde.

### 1.2 Testversjon (9 V)

Samme prinsipper, men kretsen er overdempet. Fullstendig analyse er gitt i `test_version/teori.md`.

## 2. Energibevaring

### 2.1 Generell analyse

Den opprinnelig lagrede elektriske energien E₀ = ½ C V₀² = 80 J (hovedversjon) omdannes under utladningen til:
- Magnetisk feltenergi i spolen: E_mag(t) = ½ L i(t)²
- Varme i ohmsk motstand (ledninger, spole, ESR): ∫ i² R dt
- Varme i lysbuen: ∫ V_arc i dt (V_arc er ikke konstant)
- Utstrålt elektromagnetisk energi (liten ved disse frekvensene)
- Eventuell gjenværende energi i kondensator etter at svingningene dør ut (tilnærmet null)

Energibalansen må oppfylles: E₀ = total energi omdannet. I forenklede modeller er det vanlig å anta at all energi går til varme i motstanden, men dette ignorerer lysbuens andel og stråling.

### 2.2 Dobbelttelling i eksisterende dokumentasjon

I `docs/beregninger.tex` ble den samme energien (80 J) tidligere brukt til å beregne temperaturøkning i både spole og kondensator separat, uten å fordele energien mellom dem. Dette er korrigert: nå presiseres det at energitapets fordeling er ukjent og må måles. Temperaturøkningene er kun hypotetiske eksempler, ikke validerte.

## 3. Fullstendig lavspent RLC-analyse

Se `test_version/teori.md` for en fullstendig utledning fra første prinsipper, inkludert:
- Differensialligning og initialbetingelser
- Karakteristisk ligning og røtter
- Dempingsklassifisering
- Tidsdomeneløsning med fortegnskonvensjon
- Toppstrøm og tid for toppstrøm
- Sensitivitet for komponentvariasjoner
- Begrensninger ved modellen

## 4. Verifikasjon av elektromagnetisk teori

**Magnetisk fluks:** For en flat spiralspole er feltet inhomogent. Formelen B = μ₀ N I / (2r) gjelder kun i sentrum og forutsetter en ideell sirkulær sløyfe. I virkeligheten avtar feltet raskt med avstand og vinkel.

**Faradays lov:** ε = -dΦ/dt. Indusert spenning avhenger av den tidsderiverte av fluksen gjennom mottakerkretsen. Forenklede beregninger med ΔB/Δt gir kun et grovt estimat; faktisk kobling avhenger av geometri, orientering og frekvens.

**Idealisert modell vs. fysisk system:** De oppgitte feltstyrkene er teoretiske maksima under ideelle forhold. Reelle verdier vil være lavere på grunn av ikke-ideell spole, refleksjoner og tap.

## 5. Komponentverifikasjon

| Komponent | Nominell rating | Maksimal driftsbetingelse | Transient rating (produsent) | Termisk begrensning | Isolasjonskrav | Miljø | Verifikasjonsstatus |
|-----------|----------------|---------------------------|------------------------------|---------------------|----------------|-------|---------------------|
| C1 (1000 µF) | 450 V DC | 400 V | Ikke oppgitt for 10 kA puls | ESR-oppvarming ukjent | Krypestrøm? | - | Krever pulsdata |
| Q1 (IRF840) | 500 V, 8 A | ~128 V peak | Ikke oppgitt for flyback-transienter | Kjøleribbe anbefalt | - | - | Krever verifikasjon |
| D1 (UF4007) | 1000 V, 1 A | 400 V | Ikke oppgitt for høye pulsstrømmer | - | - | - | Krever verifikasjon |
| R11 (1 kΩ/50 W) | 50 W kontinuerlig | 80 J puls | Må tåle pulsenergi; 50 W er sannsynligvis tilstrekkelig for enkeltpulser | Temperaturøkning per puls ~20 K | - | - | Krever pulsdata |
| Gnistgap | Wolfram | >10 kA | Materialdata tilsier høy toleranse | - | - | - | Sannsynligvis OK, men ikke testet |

**Ustøttede påstander:** Flere komponenter er erklært egnet uten dokumentert transientytelse. Dette må verifiseres før bygging.

## 6. Termiske antagelser

- **Lumpede modeller:** Temperaturberegningene antar jevn oppvarming av hele komponentmassen. I virkeligheten kan lokale varmepunkter oppstå (f.eks. i loddeskjøter, interne tilkoblinger).
- **Gjennomsnitt vs. lokal temperatur:** Gjennomsnittlig temperaturøkning på noen få kelvin utelukker ikke lokal smelting eller isolasjonssvikt.
- **Kontinuerlig vs. transient:** Effektmotstander har ofte høyere pulsytelse enn kontinuerlig rating, men dette må bekreftes av produsent.
- **Energibalanse:** Uten en fullstendig energifordelingsmodell kan ikke termisk sikkerhet garanteres.

**Konklusjon:** Alle termiske konklusjoner er foreløpige og krever eksperimentell validering eller detaljerte simuleringer.

## 7. Elektriske sikkerhetsverifikasjonskrav

Følgende punkter er lagt til i `safetyanalysis.md`:
- Restenergi etter frakobling: Kondensator kan holde 80 J i timevis. Manuell utladning er eneste barriere.
- Feilmodi: MOSFET-svikt kan føre til kontinuerlig lading og overspenning. Kondensator kan eksplodere ved intern kortslutning.
- Svikt i utladningsbryter: Hvis S2 svikter, finnes ingen alternativ utladningsvei.
- Måleinstrumenter: Vanlige multimetre og prober er ikke nødvendigvis klassifisert for 400 V transienter.
- Termisk svikt: Overoppheting av utladningsmotstand ved gjentatte pulser.
- Elektromagnetisk interferens: Pacemakere og annet medisinsk utstyr kan påvirkes.

## 8. Verifikasjon av tekniske konklusjoner

| Påstand | Støtte | Status |
|---------|--------|--------|
| Kretsen er underdempet | Matematisk identitet (R < 2√(L/C)) | Matematisk verifisert under antatte parametere |
| Toppstrøm ~9 kA | Idealisert modell | Konsekvent under antatte parametere, men ikke målt |
| Magnetfelt ~0,68 T | Idealisert modell | Konsekvent under antatte parametere, men ikke målt |
| Indusert spenning i test-sløyfe ~1,4 V | Idealisert modell | Konsekvent under antatte parametere, men ikke målt |
| Komponenter er egnet | Produsentdata delvis | Krever ytterligere verifikasjon for transienter |
| Enheten kan ødelegge elektronikk | Antagelse | Ikke verifisert; avhenger av mange faktorer |

## 9. Verifikasjonsmatrise

| Subsystem | Nødvendig verifikasjon | Tilgjengelig dokumentasjon | Manglende dokumentasjon | Status |
|-----------|------------------------|----------------------------|-------------------------|--------|
| Hovedkondensator C1 | Pulsstrømkapasitet, ESR, termisk | Datablad (statisk) | Pulsytelse, aldring | Krever produsentdata |
| Spole L1 | Induktans, motstand, termisk | Geometrisk estimat | Målt verdi, strømtåleevne | Krever eksperimentell verifikasjon |
| Gnistgap | Lysbuekarakteristikk, slitasje | Materialdata | Dynamisk oppførsel | Krever eksperimentell verifikasjon |
| MOSFET Q1 | Svitsjeforløp, transienter | Datablad (statisk) | Pulsytelse i flyback | Krever simulering/måling |
| Utladningsmotstand R11 | Pulsenergi, termisk | Effektrating (kontinuerlig) | Pulsytelse | Krever produsentdata |
| Sikkerhetsmekanismer | Pålitelighet, feilmodi | Beskrevet | FMEA, test | Krever kvalifisert sikkerhetsvurdering |
| Hele systemet | Ytelse, rekkevidde, destruktiv evne | Teoretiske estimater | Målinger | Krever eksperimentell verifikasjon |

## 10. Konklusjon

Prosjektet har en matematisk konsistent teoretisk kjerne, men mangler eksperimentell validering av nesten alle praktiske aspekter. Før bygging må komponentenes transientytelse verifiseres, og en fullstendig sikkerhetsanalyse med feilmodi må gjennomføres. De termiske beregningene er utilstrekkelige for å garantere sikker drift.

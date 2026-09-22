k# Sikkerhetsanalyse for EMP-generator

## 1. Innledning
Dette dokumentet identifiserer farer, risikoreduserende tiltak og gjenværende risiko ved bygging og bruk av den håndholdte EMP-generatoren. Analysen er basert på det teoretiske designet; fysisk verifikasjon er ikke utført. **Dette er ikke en fullstendig sikkerhetssertifisering.**

## 2. Identifiserte farer

### 2.1 Høyspenning (400 V DC)
- **Fare:** Livsfarlig elektrisk støt. Strøm gjennom kroppen kan forårsake hjertestans.
- **Risikoreduserende tiltak:**
  - Manuell utladningskrets (1 kΩ / 50 W) med trykknapp.
  - LED-indikator for spenning >200 V (ikke pålitelig som eneste indikator).
  - Sikring (2 A) i batterikretsen.
  - Anbefalt bruk av isolerende hansker (klasse 0, minimum 1000 V) og vernebriller.
- **Gjenværende risiko:** Kondensatoren kan holde farlig spenning i timevis hvis ikke utladet manuelt. LED kan svikte. Brukerfeil kan føre til støt. Sikringen beskytter kun batterikretsen, ikke mot utladning fra kondensatoren.

### 2.2 Høye strømmer og lysbue
- **Fare:** Brannskader, brann, eksplosjon ved kortslutning.
- **Risikoreduserende tiltak:**
  - Gnistgapet er bygget av wolfram for å tåle høye temperaturer.
  - Spolen er dimensjonert for pulsstrømmer.
  - Sikring beskytter batterikretsen.
- **Gjenværende risiko:** Feil på kondensator (intern kortslutning) kan føre til eksplosjon. Lysbuen kan antenne brennbare materialer. Sikringen gir ingen beskyttelse mot kondensatorens lagrede energi.

### 2.3 Elektromagnetisk puls
- **Fare:** Ødeleggelse av nærliggende elektronikk, inkludert medisinsk utstyr (pacemakere).
- **Risikoreduserende tiltak:**
  - Operer kun i kontrollerte omgivelser, helst i et Faraday-bur eller utendørs på trygg avstand fra personer og utstyr.
  - Advar alle tilstedeværende.
- **Gjenværende risiko:** Utilsiktet påvirkning av elektronikk utenfor kontrollsonen. Ingen dokumentert skjerming.

### 2.4 Termisk belastning
- **Fare:** Overoppheting av komponenter ved gjentatte pulser.
- **Risikoreduserende tiltak:**
  - Temperaturberegninger viser moderat oppvarming per puls, men lokale varmepunkter kan oppstå.
  - Anbefalt kjøling av utladningsmotstand og MOSFET.
- **Gjenværende risiko:** Beregningene er forenklede. Langvarig drift uten kjøling kan skade komponenter. Ingen termisk validering er utført.

### 2.5 Komponentfeil
- **Fare:** Kondensator kan eksplodere ved overbelastning eller feil. MOSFET kan svikte og forårsake kortslutning.
- **Risikoreduserende tiltak:** Komponenter er valgt med marginer, men transienter og feiltilstander er ikke fullstendig analysert.
- **Gjenværende risiko:** Ingen feilanalyse (FMEA) er gjennomført.

### 2.6 Måleutstyr
- **Fare:** Feil bruk av multimeter eller oscilloskop på høyspentkrets kan ødelegge utstyr og gi støt.
- **Risikoreduserende tiltak:** Anbefalt bruk av 100:1 probe og spenningsdeler.
- **Gjenværende risiko:** Måleoppsettet er ikke validert for de aktuelle transientene.

## 3. Sikkerhetsprosedyrer
Se `build_guide/assembly.tex` og `testing/test_prosedyre.tex` for detaljerte instruksjoner. Følgende overordnede regler gjelder:
- Alltid utlad kondensatoren manuelt før berøring (hold utladningsknappen i minst 5 sekunder, verifiser med multimeter).
- Bruk aldri LED-en som eneste indikator på utladet tilstand.
- Bruk personlig verneutstyr.
- Ha en brannslukker (CO2) tilgjengelig.
- Operer med en partner (buddy system).

## 4. Mangler og videre arbeid
- Fysisk prototype må bygges og testes for å validere sikkerheten.
- En automatisk utladningsmekanisme (bleeder-motstand) bør vurderes for å redusere avhengigheten av manuell prosedyre.
- Kapsling må designes og verifiseres for å hindre berøring av spenningsførende deler.
- Måleoppsett for høyspenning må kvalifiseres (prober, isolasjon).
- Full feilanalyse (FMEA) bør utføres.

**Konklusjon:** Designet har iboende farer som krever streng disiplin og kompetanse. Det anbefales ikke for uerfarne personer.


# 09. Sikkerhet — V3-HIGHPOWER

> **LES DETTE FØRST.** 8000V er dødelig ved berøring.
> Feil konstruksjon kan føre til død eller alvorlig skade.
> Bygg og bruk kun under tilsyn av personell med høyspenningserfaring.

## Høyspenning: 8000V

Dette er et høyspenningsprosjekt med en utgang på **8000V / ~240 J** (teoretisk).

- **8000V er dødelig.** Ikke berør noen komponente uten å vite hva du gjør.
- Alle "maksimum"-verdier i dette prosjektet er **teoretiske**.
- Reell ytelse er typisk **50–70 %** av det beregnete (tap, usikkerhet).
- Rekkevidde (5–15 m) er **estimat** — ikke målt eller verifisert.

## Hansker: Class 4 (IKKE Class 00!)

Dette er det viktigste sikring.

| Hansker | Rating | Bra for 8000V? |
|---------|--------|----------------|
| Class 00 | 500 V | **NEI — dødelige for 8000V!** |
| Class 1 | 1000 V | Nei |
| Class 2 | 3000 V | Nei |
| Class 3 | 6000 V | Grenseløst |
| **Class 4** | **36 kV** | **Ja — bruk denne** |

**VIKTIG:** Class 00-hansker (500 V) som man kanskje bruker til lavspenning, er **dødelige** for 8000 V. Bruk **Class 4 (36 kV)**.

> **Sikkerhetskrav:** Klass 4 hansker (36 kV). IKKE Class 00!

## Sikker utlading (NY prosedyre!)

**ALDRI kortslutt direkte med en skrutrekker!** Det kan gi en kraftig, ubehagelig og potensielt farlig impuls.

Gjenkjennt prosedyre for utlading av Marx/utgang:

1. Koble en **10 kΩ / 50 W motstand** mellom + og - utgang.
2. Vent **30 sekunder**.
3. Mål spenningen — skal vise **< 100 V**.
4. Fjern motstanden.
5. Kortslutt med **isolert stang** (Class 4 handsker).
6. Mål igjen — skal vise **0 V**.

> **Merk:** Utlading via motstand, ikke skrutrekker. Klass 4 handsker kreves for kortslutningssteget.

### Utladingskomponenter

| Antall | Komponent | Spesifikasjon | Leverandør | Delnummer | Pris |
|--------|-----------|---------------|------------|-----------|------|
| 1 | R_discharge | 10 kΩ / 50 W (panel, kjøleribbe) | RS | [0158474](https://no.rs-online.com/web/p/panel-mount-fixed-resistors/0158474/) | ~150 kr |
| 1 | Kontakt | HV-kontakt, isolert | - | - | ~50 kr |

## Sikkerhetsutstyr (krav)

| Antall | Komponent | Spesifikasjon | Kommentar |
|--------|-----------|---------------|-----------|
| 1 | Hansker | **Class 4 (36 kV)** | **IKKE Class 00!** |
| 1 | Stang | Isolert 10 kV+ | For utlading |
| 1 | Briller | Sikkerhetsbriller | - |

**Kostnad:** Sikkerhetsutstyr ca. **~1500 kr** (inkluddt hansker).

## Kontrollkrets — sikkerhet

Kontrollkretsen (Arduino + PCB) skal gi flere lag av beskytning:

- **Nødstopp-knapp** (tangen) — bryter lading/trigger.
- **Dør-switch / interlock** (NC) — bryter alt hvis kabinett-døren blir åpnet.
- **"Ladet" LED** (rød) — via spenningsdeler, viser at systemet er ladet.
- **"Klar" LED** (grønn) — viser at alt er klar for puls.
- **Fjernstyrt triggering (>5 m)** — hold deg til avstand når du pular.
- **15 kV isolasjon** mellom lavspenning og Marx (to relay i serie, 7,5 kV×2).

### Måling av "Ladet"-status

Bruk spenningsdeler **1000:1** (10 MΩ + 10 kΩ) til Arduino A0 for å måle lading.

> **ADVARSEL:** Spenningsdeler må tåle 8 kV! Vanlige 100:1-probe tåler ikke 8 kV.

## Marx / isolasjon

- Minimum **15 mm luftavstand** mellom steg (for 8000 V).
- Plexiglas-barriere rundt hele kjeden.
- Advarselsskilt: **"8000 V DØDELIG"**.
- Plexiglas-holder for spark gap med presisjonsjustering.

### Relay

Marx-utgang er 8 kV, men reed-relay (DAT70510-HR) tåler 7,5 kV.

> **Løsning:** Bruk **to relay i serie** (15 kV totalt) — sikkert for 8 kV.
> ALDE: 8 kV over en 7,5 kV-relay er en liten margin. To i serie gir margin.

## Sikkerhet ved TEM-celle

- Feltet er **ikke homogent** i praksis.
- Bruk 100:1-HV-probe plassert **utenfor** cellen for kalibrering/måling.
- 160 kV/m kan indusere dødelige spenninger i nærliggende gjenstander.
- Hørbar "klikk" fra utlading (normalt).
- Corona/ozon ved spisser (luft ionisering) kan oppstå.

## Sikkerhet ved radiasjonsspole

- Sørg for mekanisk robusthet.
- Unngå løkker som kan åpne seg under puls (induksjonssmell).
- Ramme: PVC-rør (ikke-ledende), 50 cm diameter.

## Checklist før første puls

1. [ ] Alle komponenter stanset til (lading skruv).
2. [ ] Sikkerhetsutstyr (Class 4 handsker, briller, isolert stang) er tilgjengelig.
3. [ ] Nødstopp og dør-interlock tester — må fungere.
4. [ ] "Ladet"-indikatoren tester (mål at det viser lading).
5. [ ] Test utlading med motstand (10 kΩ/50 W) før du pular.
6. [ ] Hånda hold av avstand — hold deg til avstand når du pular.
7. [ ] Alle andre er utom avstand. Hold avstand!

> **8000V dreper. Dette er ikke en øvelse.**
> Les 09_sikkerhet.md før du berører noen komponenter.

## Viktige begrensninger (hånda)

- Alle "maksimum"-verdier er **teoretiske**.
- Reell ytelse er typisk **50–70 %** av beregnet (tap, usikkerhet).
- Rekkevidde er **estimat** — ikke målt eller verifisert.
- Dette er et **læringsprosjekt**, ikke en ferdig militær enhet.

## Kostnadsoversikt

| Kategori | Estimert |
|----------|----------|
| Komponenter | ~2500 kr |
| Sikkerhetsutstyr | ~1500 kr |
| **Total** | **~4000 kr** |

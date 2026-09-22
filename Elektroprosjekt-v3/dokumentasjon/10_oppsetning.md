# 10. Oppsetting og test — V3-HIGHPOWER

> **Les `09_sikkerhet.md` FØRST.** 8000V er dødelig.
> Føl denne prosedyren når du bygger og tester.

## Forberedelse

### Sikkerhetsutstyr — kreves før du begynner

- [ ] Class 4 (36 kV) handsker
- [ ] Sikkerhetsbriller
- [ ] Isolert stang (10 kV+) for utlading
- [ ] 10 kΩ / 50 W motstand (utlading)
- [ ] HV-kontakt, isolert
- [ ] Nødstopp-knapp tilgjengelig

### Verifisér komponenter

- [ ] Alle komponenter stanset til
- [ ] BOM sjekket mot `04_komponentliste.md`
- [ ] Spark gap (SG) justerbar

## 1. Marx-generator — monter

1. Vertikal stabel av kondensatorer.
2. 15 mm luftgap mellom steg (økt for 8000 V).
3. Plexiglas-holder for spark gap med presisjonsjustering.
4. Kobber-bussbar til peaking circuit.

### Isolasjon
- Minimum 15 mm luftavstand (for 8000 V).
- Plexiglas-barriere rundt hele kjeden.
- Advarselsskilt: **"8000 V DØDELIG"**.

### Test av Marx
1. Sjekk alle loddinger.
2. Verifiser SG-avstand med følere (0,28 mm).
3. Test hvert steg individuelt med 800 V.
4. Sjekk synkronisering (alle SG skal tenne samtidig).

### Feilsøking
| Symptom | Årsak | Løsning |
|---------|-------|---------|
| Ingen utgang | SG tenner ikke | Juster gap ned til 0,25 mm |
| For tidlig utlading | SG tenner for tidlig | Juster gap opp til 0,32 mm |
| Ujevn puls | Dårlig synkronisering | Justér alle SG likt ±0,01 mm |

## 2. Kontrollkrets — Arduino + PCB

### Sikkerhetskrav
- [ ] Interlock på kabinettdør (NC)
- [ ] Nødstopp-knapp (tangen)
- [ ] "Ladet" indikator (rød LED)
- [ ] "Klar" LED (grønn)
- [ ] Fjernstyrt triggering (>5 m)
- [ ] 15 kV isolasjon mellom lavspenning og Marx

### Måling av "Ladet"-status
- Bruk spenningsdeler 1000:1 (10 MΩ + 10 kΩ) til Arduino A0.
- **ADVARSEL:** Spenningsdeler må tåle 8 kV!

### Arduino
- Arduino Nano.
- Nødstopp: Trykk reset-knapp på Arduino.
- Test at "ADVARSEL: 8000 V system" vises på serial.

### Relay
- Bruk to relay i serie (15 kV totalt) — sikkert for 8 kV.
- ALDE: 8 kV over en 7,5 kV-relay er en liten margin.

## 3. TEM-celle — monter og test

### Dimensjoner
| Parameter | Verdi | Kommentar |
|-----------|-------|-----------|
| Lengde | 15 cm | Kort for rask puls |
| Høyde | 3 cm | Gir høyt felt |

### Test av enheter
1. Plasser enhet i senter.
2. Orientering: Maksimal kobling når ledninger er parallell med E-felt.
3. Avstand fra vegger: >2 cm (kantfelt er ujevne).

### Måling
- Bruk 100:1 probe plassert **utenfor** cellen.
- **ALDRI** inn i cellen under drift.
- E-felt probe (hvis tilgjengelig) for kalibrering.

## 4. Radiasjonsspole — monter

### Montering
1. Form kabelen til sirkel.
2. Fest til PVC-ramme med kabelbinder.
3. Koble til TEM-celle-utgang.
4. Sørg om god kontakt (lodding eller skrueklemme).

### Kabel og ramme
- Kabel: 6 mm² fleksibel kobber.
- Isolasjon: Silikon eller gummi, 10 kV rated.
- Ramme: PVC-rør, 50 cm diameter (ikke-ledende!).

### Sikkerhet
- **586 A** i ~20 ns gir mekanisk kraft (Lorentz-kraft).
- Sørg for mekanisk robusthet.
- Unngå løkker som kan åpne seg under puls (induksjonssmell).
- Hold avstand under drift (EMP + mekanisk risiko).

## 5. Helt system — test

### Før første puls
1. [ ] Alle komponenter stanset til.
2. [ ] Sikkerhetsutstyr (Class 4 handsker, briller) er tilgjengelig.
3. [ ] Nødstopp og dør-interlock tester — må fungere.
4. [ ] Test utlading med motstand (10 kΩ/50 W) før du pular.
5. [ ] Hold avstand — hold deg til avstand når du pular.
6. [ ] Alle andre er utom avstand.

### Testprosjedyr
1. Lad systemet (0,75 s). Verifisér "Ladet"-indikatoren.
2. Verifisér "Klar"-indikatoren.
3. Hold avstand (≥5 m) og trigger.
4. Observér: Hørbar "klikk" fra utlading (normalt). Corona/ozon ved spisser (luft ionisering) kan oppstå.
5. Avslutt: Kjør utlading via motstand (10 kΩ/50 W), vent 30 s, mål <100 V, fjern motstand, kortslutt med isolert stang (Class 4 handsker), mål igjen — skal vise 0 V.

### Måling av felt
- Bruk 100:1 probe plassert **utenfor** TEM-cellen.
- **ALDRI** inn i cellen under drift.
- E-felt probe (hvis tilgjengelig) for kalibrering.
- **160 kV/m** kan indusere dødelige spenninger i nærliggende gjenstander.

> **8000V dreper. Dette er ikke en øvelse.**
> Hold deg til avstand. Les `09_sikkerhet.md` før du berører noen komponenter.

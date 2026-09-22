# 05. Marx Generator — V3-HIGHPOWER

## Prinsipp

Lader 10 kondensatorer i parallell (via motstander), 
utlader i serie via spark gaps.

## Kretsdiagram

800V+ ──R──┬──C──┬──C──┬── ... ──┬──C──┬── V_UT (8000V)
           │     │     │         │     │
          SG1   SG2   SG3       SG9   SG10
           │     │     │         │     │
0V ────────┴─────┴─────┴─ ... ───┴─────┘

## Komponenter (korrigert)

### Kondensatorer (C1-C20)
- **Type:** United Chemi-Con ESMQ 120µF/450V 
  ELLER Rubycon 450KXW 150µF/450V
- **Farnell:** [1686715](https://no.farnell.com/united-chemi-con/esmq451vsn121mp30s/aluminum-electrolytic-capacitor/dp/1686715)
- **Konfigurasjon:** 2 i **SERIE** per steg
- **Resultat:** 75µF/900V per steg (lades til 800V)

**VIKTIG:** Seriekobling gir C/2 og 2×V — IKKE C×2!

### Ladingsmotstander (R1-R10)
- **Verdi:** 20kΩ (høyere enn original for sikkerhet)
- **Effekt:** 50W wirewound
- **RS:** [0158474](https://no.rs-online.com/web/p/panel-mount-fixed-resistors/0158474/)

### Spark Gaps (SG1-SG10)
- **Avstand:** 0.28mm (justerbart)
- **Material:** Messing-kuler 10mm
- **Breakdown:** ~840V (3kV/mm × 0.28mm)
- **Margin til 800V:** 5% (lavt — vurder 0.30mm)

## Konstruksjon

### Oppbygning
1. Vertikal stabel av kondensatorer
2. 15mm luftgap mellom steg (økt for 8000V)
3. Plexiglas-holder for SG med presisjonsjustering
4. Kobber-bussbar til peaking circuit

### Isolasjon
- Minimum 15mm luftavstand (for 8000V)
- Plexiglas-barriere rundt hele kjeden
- Advarselsskilt: "8000V DØDELIG"

## Sikker utlading (NY prosedyre!)

**ALDRI kortslutt direkte!**

1. Koble **10kΩ/50W motstand** mellom + og - utgang
2. Vent 30 sekunder
3. Mål spenning — skal vise <100V
4. Fjern motstand
5. Kortslutt med **isolert stang** (Class 4 hansker)
6. Mål igjen — skal vise 0V

## Beregninger

### Ladingstid
$$t_{charge} = 5 \cdot 20k\Omega \cdot 7.5\mu F = 0.75s$$

### Energi
$$E = 10 \cdot \frac{1}{2} \cdot 75\mu F \cdot (800V)^2 = 240 J$$

## Testing

### Før bruk
1. Sjekk alle loddinger
2. Verifiser SG-avstand med følere (0.28mm)
3. Test hvert steg individuelt med 800V
4. Sjekk synkronisering (alle SG skal tenne samtidig)

### Feilsøking
| Symptom | Årsak | Løsning |
|---------|-------|---------|
| Ingen utgang | SG tenner ikke | Juster gap ned til 0.25mm |
| For tidlig utlading | SG tenner for tidlig | Juster gap opp til 0.32mm |
| Ujevn puls | Dårlig synkronisering | Justér alle SG likt ±0.01mm |
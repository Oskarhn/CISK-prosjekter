# 07. Radiasjonsspole — V3-HIGHPOWER

## Formål

Konverterer pulserende strøm til radiert elektromagnetisk felt.
**Viktig:** Dette er en **simplifisert antenne**, ikke optimalisert.

## Design

- **Radius:** 50 cm
- **Vindinger:** 1 (én enkel loop)
- **Tverrsnitt:** 6 mm² kobber

## Hvorfor én vinding?

- Lavere induktans (L ~ 1.4µH) = høyere di/dt
- Bedre impedanstilpasning til Marx
- Enklere konstruksjon enn multi-vinding

## Beregninger

### Induktans (Wheeler-formel)
$$L = \mu_0 R \left[\ln\left(\frac{8R}{a}\right) - 2\right] \approx 1.4 \mu H$$

der $a = \sqrt{A/\pi} = 1.38mm$ (ledningsradius)

### Peak strøm (teoretisk)
$$I_{peak} = V\sqrt{\frac{C}{L}} = 8000 \cdot \sqrt{\frac{7.5\mu F}{1.4\mu H}} \approx 586 A$$

### di/dt (teoretisk)
Med $t_{rise} \approx 20ns$:
$$\frac{di}{dt} = \frac{586A}{20ns} \approx 29 GA/s$$

**Realistisk:** 15-25 GA/s (inkl. alle tap)

### B-felt i sentrum
$$B = \frac{\mu_0 I}{2R} = \frac{4\pi\cdot10^{-7} \cdot 586}{2 \cdot 0.5} \approx 0.74 mT$$

## Fjernfelt (ESTIMAT)

For $r >> R$ (antenne-tilnærming):
$$E_{far} \approx \frac{Z_0 \cdot I \cdot \omega \cdot A}{2\pi r}$$

Ved $r = 10m$, $\omega \approx 1/20ns = 50$ Mrad/s:
$$E \approx 1-3 kV/m$$ (**ESTIMAT**, stor usikkerhet)

**Dette er IKKE verifisert!** Reell rekkevidde avhenger av:
- Antenneeffektivitet
- Omgivelser (refleksjoner)
- Mottakerens følsomhet

## Konstruksjon

### Material
- Kabel: 6mm² fleksibel kobber
- Isolasjon: Silikon eller gummi, 10kV rated
- Ramme: PVC-rør 50cm diameter (ikke-ledende!)

### Montering
1. Form kabelen til sirkel
2. Fest til PVC-ramme med kabelbinder
3. Koble til TEM-celle-utgang
4. Sørg om god kontakt (lodding eller skrueklemme)

## Sikkerhet

- **586A** i ~20ns gir mekanisk kraft (Lorentz-kraft)
- Sørg for mekanisk robusthet
- Unngå løkker som kan åpne seg under puls (induksjonssmell)
- Hold avstand under drift (EMP + mekanisk risiko)

## Alternative antenner (ikke bygget)

| Type | Fordeler | Ulemper |
|------|----------|---------|
| Bicone | Bedre matching | Kompleks |
| Log-periodisk | Retningsbestemt | Stor |
| Dipol | Enkel | Begrenset båndbredde |
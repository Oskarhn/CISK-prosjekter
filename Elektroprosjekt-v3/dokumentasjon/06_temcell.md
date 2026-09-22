# 06. TEM-celle — V3-HIGHPOWER

## Formål

Skaper elektromagnetisk felt for testing. 
**Viktig:** Feltet er **ikke** homogent i praksis.

## Dimensjoner

| Parameter | Verdi | Kommentar |
|-----------|-------|-----------|
| Lengde | 15 cm | Kort for rask puls |
| Gap (h) | 3 cm | Gir høyt felt |
| Bredde (w) | 3 cm | Z₀ ≈ 60Ω |

## Karakteristisk impedans

For kvadratisk tverrsnitt:
$$Z_0 \approx 60\Omega$$

**Merk:** Dette er teoretisk. Reell impedans avviker pga kanteffekter.

## E-felt

### Teoretisk maksimum
$$E_{ideal} = \frac{V}{h} = \frac{8000V}{0.03m} = 267 kV/m$$

### Realistisk (med tap)
$$E_{real} \approx 0.6 \cdot E_{ideal} \approx 160 kV/m$$

**Tap:** 
- Refleksjoner i overganger: ~20%
- Kanteffekter: ~15%
- Imperfekt matching: ~5%

### Usikkerhet
±30% avhengig av konstruksjonskvalitet.

## Indusert spenning

I ledning 10cm lang i feltretningen:
$$V_{ind} = E \cdot l = 160kV/m \cdot 0.1m = 16 kV$$

**Dette er teoretisk maksimum.** 
Reell indusert spenning avhenger av:
- Orientering (maksimum når parallell med E)
- Lengde på ledning
- Terminering (åpen krets vs last)

## Konstruksjon

### Material
- To aluminiumsplater 2mm, 15×3cm
- Plexiglas-distanser 30mm (presisjonsbearbeidet)
- Kobber-folie tilkobling til Marx

### Tilkobling
- **Inngang:** Fra peaking circuit
- **Utgang:** Til radiasjonsspole ELLER terminering

## Bruk

### Test av enheter
1. Plasser enhet i senter
2. Orientering: Maksimal kobling når ledninger || E-felt
3. Avstand fra vegger: >2cm (kantfelt er ujevne)

### Måling
- Bruk 100:1 probe plassert **utenfor** cellen
- **ALDRI** inn i cellen under drift
- E-felt probe (hvis tilgjengelig) for kalibrering

## Farer

- **160kV/m** kan indusere dødelige spenninger i nærliggende gjenstander
- Hørbar "klikk" fra utlading (normalt)
- Corona/ozon ved spisser (luft ionisering)
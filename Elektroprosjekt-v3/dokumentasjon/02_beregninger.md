# 02. Beregninger — V3-HIGHPOWER

## 2.1 Marx Generator — Korrigert

### Kondensator-konfigurasjon (VIKTIG!)
- **Per steg:** 2× 150µF/450V i **SERIE**
- **Ekvivalent:** 75µF/900V per steg
- **Ladet til:** 800V (IKKE 900V — gir 11% margin)

**Feil i original V2:** To 250V caps i serie gir 500V (ikke 1000V).

### Energiberegning
$$E = \frac{1}{2} C V^2 = \frac{1}{2} \cdot 7.5\mu F \cdot (8000V)^2 = 240 J$$

**Usikkerhet:** ±30% pga toleranser, tap, temperatur.

## 2.2 Lading

### Tidskonstant
$$\tau = R \cdot C = 20k\Omega \cdot 7.5\mu F = 0.15s$$

### Full lading
$$t_{full} = 5\tau = 0.75s$$

### Effekt
- Peak: $P = V^2/R = 8000^2/20000 = 3200W$
- Average: $P = E/t = 240J/0.75s = 320W$

**Krever 50W wirewound resistor på kjøleribbe!**

## 2.3 Spark Gap

### Breakdown-spenning
$$V_{break} = 3kV/mm \cdot 0.28mm = 840V$$

### Margin
$$\text{Margin} = \frac{800V}{840V} = 0.95$$

**Dette er lavt!** Justér til 0.30mm for margin >1.0.

## 2.4 TEM-celle

### Teoretisk felt
$$E_{ideal} = \frac{V}{d} = \frac{8000V}{0.03m} = 267 kV/m$$

### Realistisk felt (med tap)
$$E_{real} = 0.6 \cdot E_{ideal} \approx 160 kV/m$$

**Tap:** Refleksjoner (20%), geometri (15%), matching (5%).

## 2.5 Peaking Circuit

### Ideal beregning
$$t_{rise} = \pi\sqrt{LC} = \pi\sqrt{100nH \cdot 2nF} \approx 1.4 ns$$

### Realistisk (med usikkerhet)
$$t_{rise,real} \approx 20-30 ns$$

**Hvorfor?** Parasittisk induktans i ledninger, kontakter.

## 2.6 Radiasjonsspole

### Induktans
$$L \approx 1.4 \mu H$$ (for 50cm, 1 vinding)

### Peak strøm (teoretisk)
$$I_{peak} = V\sqrt{\frac{C}{L}} = 8000 \cdot \sqrt{\frac{7.5\mu F}{1.4\mu H}} \approx 586 A$$

### di/dt (teoretisk)
$$\frac{di}{dt} = \frac{586A}{20ns} \approx 29 GA/s$$

**Realistisk:** 15-25 GA/s (inkl. alle tap).

## 2.7 Sammenligning (ærlig)

| Parameter | V1 | V3-HP (teor) | V3-HP (real) | Usikkerhet |
|-----------|-----|--------------|--------------|------------|
| Spenning | 24V | 8000V | 8000V | ±5% |
| Energi | 0.27J | 240J | 150J | ±30% |
| E-felt | ~1kV/m | 267kV/m | 160kV/m | ±30% |
| di/dt | ~16MA/s | ~400GA/s | ~250GA/s | ±50% |

**Rekkevidde:** 5-15m (estimat, **ikke verifisert**).
# 01. Systemarkitektur — V3-HIGHPOWER

## Oversikt

V3-HIGHPOWER er en 10-steg Marx-generator med peaking circuit, 
designet for å demonstrere høyspenningspulsteknikk.

## Viktig merknad

Dette er et **skoleprosjekt**. Alle ytelsespåstander er 
**teoretiske** eller **estimater**. Reell ytelse vil avvike.

## Blokkskjema

[HV Kilde 800V] → [Marx 10-steg] → [Peaking] → [TEM-celle]
↓
[Radiasjonsspole]

## Komponenter

### 1. Marx Generator (10 steg)
- **Kondensatorer:** 20× 150µF/450V (Rubycon)
  - Konfigurasjon: 2 i serie per steg = 75µF/900V
  - Ladet til 800V (11% margin under 900V max)
- **Motstander:** 10× 20kΩ/50W wirewound
- **Spark gaps:** 10× justerbare, ~0.28mm
- **Utgang:** 8000V, 7.5µF, ~240J (teoretisk)

### 2. Trigger-system
- 3-steg trigger-Marx (2400V)
- Reed relay Cynergy3 DAT70510-HR (7.5kV kontakt)
- **Merk:** Relay tåler 7.5kV, Marx gir 8kV. 
  Bruk **to relay i serie** eller akseptere risiko.

### 3. Peaking Circuit
- 2nF/10kV ceramic capacitor
- Spark gap 1mm (justérbart)
- **Formål:** Redusere rise time fra ~1ms til ~20ns
- **Begrensning:** Idealisert beregning, reell ytelse varierer

### 4. TEM-celle
- 15×3×3 cm aluminium
- Teoretisk felt: 267 kV/m
- **Realistisk:** 150-200 kV/m (inkl. tap)

### 5. Radiasjonsspole
- 50cm diameter, 1 vinding
- Teoretisk di/dt: ~400 GA/s
- **Realistisk:** ~200-300 GA/s

## Spesifikasjoner (med usikkerhet)

| Parameter | Verdi | Usikkerhet |
|-----------|-------|------------|
| Spenning | 8000V | ±5% |
| Energi | 240J | ±30% |
| E-felt | 160 kV/m | ±30% |
| di/dt | ~250 GA/s | ±50% |
| Rekkevidde | 5-15m | **Estimat, ikke verifisert** |

## Kjente begrensninger

1. **Spark gap synkronisering:** Kan variere ±1ns mellom steg
2. **Parasittisk induktans:** Reduserer strøm og øker rise time
3. **TEM-celle matching:** 60Ω til 377Ω (luft) gir refleksjoner
4. **Energitap:** 30-50% går til varme, ikke EMP

## Sikkerhet

Se `09_sikkerhet.md`. 8000V er dødelig.
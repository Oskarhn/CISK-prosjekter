# 07 — Radieringspule (off-board)

## Hva er radieringspulen

Radieringspulen er en stor pule som radierer felt til lang avstand. Den er
secondary — primær skade kommer fra TEM-cellen.

## Konfigurering

| Param | Verdi |
|-------|-------|
| Radius | 1.0 m (Ø 2 m) |
| Antall omlapninger | 10 |
| Ledning | 6 mm² (18 AWG) |
| Spolemotstand | 180 mΩ |
| Induktans | ≈ 837 µH |
| Peak-strøm | ≈ 5809 A |
| di/dt | ≈ 116183 MA/s |
| B-felt (sentrum) | ≈ 36.5 mT |

## Kalkulator

```
I_peak = V_ut * (0.5 * t_FWHM) / L_loop
       = 5000 V * (0.5 * 1.946 ms) / 837.4 uH
       = 5809 A

di/dt = I_peak / t_gap = 5809 A / 50 ns = 116183 MA/s

B_center = 4*pi*1e-7 * N * I_peak / (2 * radius)
         = 36.50 mT
```

## Fjærfelt

Fjærfeltet av avstanden d (m):

```
E_far = (Z0 * I * omega * A * cos(theta)) / (2 * pi * d)
```

Der A = pi * radius^2 (pulearealet). Fjærfeltet er svakt enn i cellen, men
det når "på avstand".

## Verifisering

- Mål B-felt med en fluxgate.
- Mål E-felt med en antennesonde på 2-3 m.
- Putt en telefon på 2 m avstand og sjekk at den dør (svakt).

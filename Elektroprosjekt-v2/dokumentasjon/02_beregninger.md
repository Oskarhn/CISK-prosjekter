# 02 — Beregninger

Alle tallene i dokumentasjonen er fra `beregnigning/beregning.py`. Kjør:

```bash
python beregning/beregning.py
```

Dette dokumentet forklarer hvordan hvert tall er fått.

## 2.1 Marx-generatør (off-board)

**Antall steg:**
```
N_steg = 5
```
**Kapasitans og spenning per steg:**
```
C_steg = 235 uF / 1000 V (2x 470 uF/250 V i serie)
V_steg = 1000 V
```
**Utgangsparameterer:**
```
V_ut = N_steg * V_steg = 5 * 1000 V = 5000 V
C_ut = C_steg / N_steg = 235e-6 / 5 F = 47.0 uF
E_ut = 0.5 * C_ut * V_ut^2 = 0.5 * 47e-6 * (5000)^2 = 587.5 J
```
**Kontroll (antall steg x energi per steg):**
```
E = N_steg * 0.5 * C_steg * V_steg^2 = 5 * 0.5 * 235e-6 * (1000)^2 = 587.5 J ✓
```
**Sammenligning med v1 (0.2707 J):**
```
E_ut / E_v1 = 587.5 / 0.2707 = 2170x mer energi
```
**Lading:**
```
R_lad = 4700 ohm
C_lad = C_ut = 47 uF (ekv.)
tau_lad = R_lad * C_lad = 4700 * 47e-6 = 0.221 s
t_lad = 5 * tau_lad = 5 * 0.221 = 1.1 s
f_rep = 1 / t_lad = 0.91 Hz
I_lad = V_ut / R_lad = 5000 / 4700 = 1.064 A (1064 mA)
P_lad = V_ut * I_lad = 5000 * 1.064 = 5320 W (5 kW)
```
**HV-tap for trigger (5:1):**
```
V_tap = V_ut / 5 = 5000 / 5 = 1000 V
```

## 2.2 Trigger + iskjering (off-board)

**Kjedegap:**
```
gap = 0.15 mm
V_breakdown = 3.0 kV/mm * 0.15 mm / 1000 = 0.45 V = 450 V
```
**Kjede-spenn:**
```
V_s_paa_hvert_gap = 1000 V
margin = V_s_paa_hvert_gap / V_breakdown = 1000 / 450 = 2222x (>= breakdown)
```
Dette betyr at alle gap lukker samtidig (kjede-lukking) fordi V_s > V_breakdown.

**Trigger:**
```
N_trigger = 3 steg
V_trigger = 3000 V
```
**Anslog:**
```
t_gap = 50 ns (anslogstid for gap)
```
Jede-lukking er omtrent 50 ns, alle gap lukker samtidig (kjede-lukking).

## 2.3 TEM-celle (off-board, primær skadestruktur)

**Dimensjoner:**
```
L_cell = 300 cm = 3.00 m
gap_h = 5 cm = 0.05 m (mellem platene)
bredde_w = 5 cm = 0.05 m (kvadrat)
```
**Karakteristisk impedanans:**
```
Z0 = 60 Ohm (kvadrat gap -> Z0 ~ 60 Ohm)
```
**E-felt:**
```
E_felt = V_ut / h = 5000 / 0.05 = 100000 V/m = 100 kV/m
```
Dette er >= 10-30 kV/m tærskhold for skade på telefoner. Telefonen dør.

**Spennings over telefon (8 cm i feltretningen):**
```
V_phone = E_felt * 0.08 m = 100000 * 0.08 = 8000 V
```
8 kV over en telefonens kropp -> dør.

**Gjennomkjør tid (TEM-cellen):**
```
t_transit = L_cell / v_p = 3.00 / 3e8 * 1e9 = 1 ns
```
**RC- tid:**
```
tau_RC = Z0 * C_ut = 60 * 47e-6 = 2.82e-3 s = 2820 us
t_FWHM = 0.69 * tau_RC = 0.69 * 2820 us = 1946 us (1.9 ms)
```
**Strøm og di/dt:**
```
I_tm = V_ut / Z0 = 5000 / 60 = 83.3 A
di/dt = I_tm / t_gap = 83.3 / 50ns = 1667 MA/s
```
Dette er 1667 / 15.8 = 105x raskere enn v1 (15.8 MA/s).

## 2.4 Radieringspule (off-board)

**Dimensjoner:**
```
radius = 1.0 m
N_oml = 10 omlapninger
A_wire = 6 mm^2 = 6e-6 m^2
L_wire = N_oml * 2*pi*radius = 10 * 2*pi*1 = 62.8 m
```
**Spolemotstand (kopper):**
```
rho_copper = 1.72e-8 ohm*m
R_loop = rho * L_wire / A_wire = 1.72e-8 * 62.8 / 6e-6 = 180.1 mOhm
```
**Induktans (10 omlapninger, omlapt):**
```
a = sqrt(A_wire/pi) (ledningsrad)
L_loop = 4*pi*1e-7 * radius * N_oml^2 * (log(8*radius/a) - 2) = 837.4 uH
```
**Peak-strøm:**
```
I_peak = V_ut * (0.5 * t_FWHM) / L_loop = 5000 * (0.5 * 1.946e-3) / 837.4e-6 = 5809 A
```
**di/dt (pule):**
```
di/dt = I_peak / t_gap = 5809 / 50ns = 116183 MA/s
```
**B-felt i sentrum:**
```
B_center = 4*pi*1e-7 * N_oml * I_peak / (2 * radius) = 36.50 mT
```
**Fjærfelt:**
```
E_far (avstand d) = (Z0 * I * omega * A * cos) / (2*pi*d) -- se 07_radieringspule.md
```

## 2.5 Puls og sammenligning

**Puls:**
```
V = 5000 V, C = 47 uF, E = 587.5 J
Felt = 100 kV/m i TEM-celle, FWHM = 1.9 ms
I_peak (TEM-celle) = 83.3 A, di/dt = 1667 MA/s
Repetisjonsrate = 0.91 Hz (per 1 s)
```
**V1 vs V2:**
```
Energi: 0.27 J -> 587.5 J (2176x)
Spennings: 24 V -> 5000 V (208x)
Felt: 9,5 V + 41,9 V -> 8000 V (≈ 157x mer)
di/dt: 15.8 MA/s -> 1667 MA/s (105x)
Repetisjonsrate: 1 (single) -> 0.91 Hz
Struktur: 31 mm spole -> 300 cm TEM-celle + 1000 mm pule
Impulsbredd: 104 us -> 1.9 ms
```
V2 er "extremely dangerous". Tem-cellen (100 kV/m) kan skade en telefon
i det samme rommet. Repetisjonsrate 0.91 Hz, FWHM 1.9 ms, anslog 50 ns.

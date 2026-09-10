# 03 — Calculations (triple-checked)

Every key quantity below is computed with **at least two independent methods** (three where
noted). The pure-Python model `calculations.py` reproduces every number in this file:

```powershell
& "C:\Users\Oskar\AppData\Local\Programs\Python\Python310\python.exe" "...\EMP_Generator\calculations.py"
```

Notation follows the course formula sheet: ω₀ = 1/√(LC), ζ = R/(2√(L/C)),
ωd = ω₀√(1−ζ²), characteristic polynomial s² + 2ζω₀s + ω₀².

## 3.0 Design parameters

| Parameter | Symbol | Value |
|---|---|---|
| Pre-charge voltage | V₀ | 24.0 V |
| Capacitor bank | C | 2 × 470 µF = 940 µF (ESR ≈ 10 mΩ) |
| Transmitter coil turns / radius / length | N, r, l | 15, 15 mm, 15.28 mm (1.0 mm wire, close-wound pitch 1.02 mm) |
| Coil DC resistance | R_coil | 30.96 mΩ (1.41 m wire × 1.72e-8 Ω·m / 0.785 mm²) |
| MOSFET R_DS(on) @ 10 V | R_sw | 1.25 mΩ (IRF3707) |
| Current-sense shunt | R_shunt | 10 mΩ |
| PCB + contact resistance | R_trace | 2 mΩ |
| Total loop resistance | R_tot | **54.2 mΩ** |
| Freewheel path | — | D1 (V_D1 = 1.1 V, R_D1 = 30 mΩ) + R_FW = 0.5 Ω + R_coil → R₂ = 0.561 Ω |
| Pickup coil | N_p, r_p | 15 turns, r = 10 mm (20 mm dia, inside the bore) |

Stored energy: `E₀ = ½CV₀² = ½ × 940 µF × 24² = 270.7 mJ`

## 3.1 Coil inductance L — three methods

| Method | Formula | Result |
|---|---|---|
| 1. Wheeler (approx.) | L(µH) = r″²N²/(9r″ + 10l″), r,l in inches | **6.925 µH** |
| 2. Neumann/elliptic loop sum | L = N·L_self + 2ΣΣ M(a,b,z), M = μ₀√(ab)[(2/k−k)K(k) − (2/k)E(k)], k² = 4ab/((a+b)²+z²), K/E = complete elliptic integrals (Simpson-verified: K(0.5)=1.68575, E(0.5)=1.46744) | **6.694 µH** |
| 3. Direct Neumann line integral | M_ij = (μ₀r²/2)∫cosδ/√(4r²sin²(δ/2)+dz²) dδ, no elliptic functions at all | **6.694 µH** |

**Design value: L = 6.69 µH** (the two exact methods agree to 0.00 %; Wheeler is +3.5 %,
expected for a short stubby coil, l ≈ r).

L_self (one thin turn) = μ₀r[ln(8r/w) − 2] + μ₀r/4 = 0.111 µH.

## 3.2 The pulse — analytic vs RK4 vs energy

### 3.2.1 Analytic (course closed form)

Series RLC discharge, underdamped (0 < ζ < 1):

```
ω₀   = 1/√(LC)                = 1/√(6.694e-6 × 940e-6) = 12 606.8 rad/s  →  f₀ = 2006 Hz
ζ    = R/(2√(L/C))            = 0.05421 / (2 × √(6.694e-6/940e-6)) = 0.3212
ωd   = ω₀√(1−ζ²)              = 11 938.8 rad/s  →  fd = 1900 Hz
t_pk = (1/ωd)·atan(ωd/ζω₀)    = 104.18 µs
i(t) = V₀/(L·ωd)·e^(−ζω₀t)·sin(ωd t)
I_pk = V₀/(L·ωd)·e^(−ζω₀t_pk)·sin(ωd t_pk) = 186.52 A
v_C(t_pk) = V₀e^(−ζω₀t_pk)(cos ωd t_pk + (ζ/√(1−ζ²)) sin ωd t_pk) = 10.111 V
```

### 3.2.2 RK4 piecewise simulation (dt = 50 ns)

Stage 1 (switch on, t < t_pk):  dv_C/dt = −i/C,  di/dt = (v_C − iR_tot)/L
Stage 2 (switch off, freewheel):  dv_C/dt = 0 (cap branch open),  di/dt = −(V_D1 + iR₂)/L

| Quantity | Analytic | RK4 | Diff |
|---|---|---|---|
| I_pk | 186.52 A | 186.52 A | **0.00 %** |
| t_pk | 104.18 µs | 104.15 µs | 0.03 % |
| v_C at switch-off | 10.111 V | 10.117 V | 0.06 % |
| di/dt at t = 0 | 3.586 MA/s | 3.585 MA/s | 0.02 % |
| max di/dt stage 1 (rise) | 3.59 MA/s | 3.59 MA/s | — |
| max di/dt stage 2 (freewheel) | (V_D1+I_pkR₂)/L = 15.76 MA/s | 15.76 MA/s | — |
| freewheel decay to < 5 mA | τ_fw = L/R₂ = 11.93 µs; i(t) = (I_pk+V_D1/R₂)e^(−t/τ_fw) − V_D1/R₂ | 54.5 µs | — |

### 3.2.3 Energy balance (closure check)

| Sink | Energy |
|---|---|
| Initial cap energy E₀ = ½CV₀² | **270.72 mJ** |
| Final cap energy ½C(10.111 V)² | 48.05 mJ |
| Coil R (both stages) | 66.93 mJ |
| R_FW | 101.71 mJ |
| Cap ESR | 19.59 mJ |
| Shunt | 19.59 mJ |
| MOSFET | 2.45 mJ |
| PCB traces/contacts | 3.92 mJ |
| Diode D1 (Vf + dynamic) | 8.43 mJ |
| **Σ (final + dissipated)** | **270.66 mJ** |

**Balance error = 0.021 % → PASS (< 1 %).** The three methods (closed form, numerical,
energy) are mutually consistent.

## 3.3 Magnetic field — three methods

| Method | B at center (I = 186.52 A) |
|---|---|
| 1. Closed-form finite solenoid: B = (μ₀nI/2)[(z+l/2)/√((z+l/2)²+r²) − (z−l/2)/√((z−l/2)²+r²)] | **104.43 mT** |
| 2. Direct sum of the exact on-axis field of each turn: B = Σ μ₀Ir²/(2(r²+d²)^1.5) | **104.44 mT** |
| 3. Infinite-solenoid limit μ₀nI = μ₀NI/l | 230.10 mT (ideal limit; 2.2× higher because l ≈ r) |

Methods 1 and 2 (both exact) agree to **0.01 %** → **B_center = 104 mT = 0.104 T**.

Axial falloff at peak current (closed form = loop sum, exact):

| z from center | B | | z from center | B |
|---|---|---|---|---|
| 0 mm | 104.4 mT | | 30 mm | 11.3 mT |
| 5 mm | 94.1 mT | | 50 mm | 2.89 mT |
| 10 mm | 69.8 mT | | 100 mm | 0.387 mT |
| 20 mm | 28.0 mT | | 200 mm | 0.049 mT |

## 3.4 Pickup mutual inductance and induced voltage — two methods

| Method | M |
|---|---|
| 1. Loop-pair elliptic sum (225 turn pairs, exact) | **2.658 µH** |
| 2. Flux method: M = N_p·A_p·(dB/dI)\|center | 2.638 µH (diff 0.7 %) |

Induced voltage `v = M·di/dt` (pickup at coil center):

| Event | di/dt | v_pickup |
|---|---|---|
| Rise (t = 0, max rise slope) | 3.586 MA/s | **9.53 V** |
| Freewheel spike (t = t_pk) | 15.76 MA/s | **41.90 V** |

Position dependence (for the distance experiment, `09_experiments.md`):

| z (pickup offset) | M | V_rise | V_spike |
|---|---|---|---|
| 0 mm | 2.658 µH | 9.53 V | 41.90 V |
| 10 mm | 1.781 µH | 6.39 V | 28.08 V |
| 20 mm | 0.692 µH | 2.48 V | 10.90 V |
| 30 mm | 0.279 µH | 1.00 V | 4.40 V |
| 50 mm | 0.072 µH | 0.26 V | 1.14 V |

## 3.5 Electrical stresses and thermal checks (1 pulse, 1 Hz repetition)

| Part | Stress | Rating | Verdict |
|---|---|---|---|
| MOSFET (IRF3707) | I_D = 187 A pulse (≈ 100 µs); V_DS,max = 16.8 V (D1 clamps drain: v_C + V_D1 + iR_D1) | 720 A pulsed; 75 V | OK, 4.5× current margin, 4.5× voltage margin |
| Cap bank | 24.0 V → 10.11 V (no negative swing — D1 blocks reverse; freewheel bypasses cap) | 50 V | OK |
| D1 (MUR1560) | 187 A for 54 µs; Q = 2.1 mAs; ∫i²dt = 0.208 A²s; E = 8.4 mJ | 15 A cont.; I_TSM 8/3 ms ≈ 150–200 A (equiv. 0.29 A²s) | OK: I²t is 72 % of the 8/3 ms rating for a single pulse |
| R_FW (0.5 Ω/5 W) | 101.7 mJ/pulse; 102 mW average at 1 Hz; wire ΔT ≈ 11 K (adiabatic) | 5 W | OK |
| Coil wire (9.9 g Cu) | 66.9 mJ/pulse → ΔT = 0.02 K | — | OK |
| Shunt (10 mΩ/5 W) | peak 348 W for ~100 µs (19.6 mJ) | 5 W | OK (energy, not peak, matters for ms-scale ratings) |
| R_CHG (100 Ω/2 W) | peak 5.76 W decaying, 271 mJ/charge | 2 W | OK |
| PCB current path | 10 mm × 35 µm Cu: 1.47 mΩ/30 mm; I²t heat negligible | — | OK (included in R_trace margin) |
| 555 (12 V rail) | V_CC = 12 V (D2 Zener from 24 V; R9 = 820 Ω → 14.6 mA) | 15.5 V max | OK |
| Gate | V_GS = 10.5 V on (555 out @ 12 V), clamped at 15 V (D3) | 30 V abs. max | OK |

Repetition rate: at 1 Hz the cap recharges 10.11 → 24 V through R_CHG in
t = −RC·ln((24−23.6)/(24−10.11)) ≈ 0.33 s ≪ 1 s period → **1 Hz continuous operation OK**.

## 3.6 555 monostable sizing

```
T = 1.1·R·C = 104.2 µs  →  R = T/(1.1 × 10 nF) = 9471 Ω
```

Use **R1 = 9.70 kΩ 1 % + C_TIM = 10 nF C0G → T = 106.7 µs**. The switch turns off
2.5 µs after the current peak, where i(106.7 µs) = 186.25 A = **99.85 % of I_pk** —
within the ±10 % L tolerance window (t_pk shifts ∓10 %, I_pk by < 5 %).

## 3.7 Voltage scaling (experiment 3)

With L, C, R fixed, I_pk, B and V_ind all scale linearly with V₀:

| V₀ | I_pk | B_center | E_cap | pickup spike | Notes |
|---|---|---|---|---|---|
| 12 V | 93 A | 52 mT | 67.7 mJ | 21.0 V | same parts, half effect |
| **24 V** | **187 A** | **104 mT** | **270.7 mJ** | **41.9 V** | **base design** |
| 48 V | 373 A | 209 mT | 1.08 J | 83.8 V | 50 V caps OK (48 < 50); drain clamp ≈ 33 V < 75 V |
| 100 V | 777 A | 435 mT | 4.70 J | 174.6 V | needs HV caps (>100 V) + 100 V MOSFET |
| 240 V | 1865 A | 1.04 T | 27.1 J | 419 V | needs series cap stack + HV parts |

## 3.8 Turn-count sweep (experiment 2)

Wheeler L + analytic pulse model, r = 15 mm, close-wound 1.0 mm wire, 24 V, 940 µF:

| N | L (µH) | I_pk (A) | B_c (mT) | di/dt rise (MA/s) | di/dt fw (MA/s) | pickup spike (V) | B @ 50 mm (µT) |
|---|---|---|---|---|---|---|---|
| 8 | 2.62 | 280.9 | 90.8 | 9.16 | 59.0 | 89.9 | 2257 |
| 10 | 3.74 | 242.3 | 96.1 | 6.42 | 36.0 | 67.2 | 2450 |
| 12 | 4.96 | 214.5 | 99.8 | 4.84 | 24.2 | 53.1 | 2622 |
| **15** | **6.93** | **184.5** | **103.3** | **3.47** | **15.1** | **39.8** | **2859** |
| 18 | 9.01 | 163.0 | 104.9 | 2.66 | 10.4 | 31.5 | 3084 |
| 20 | 10.46 | 151.8 | 105.2 | 2.29 | 8.4 | 27.4 | 3233 |
| 25 | 14.20 | 130.5 | 104.1 | 1.69 | 5.4 | 20.4 | 3614 |
| 30 | 18.09 | 115.3 | 101.5 | 1.33 | 3.8 | 15.9 | 4026 |
| 40 | 26.11 | 94.8 | 94.2 | 0.92 | 2.3 | 10.6 | 5025 |

Reading: B_center is nearly flat (91–105 mT) across N = 8…40 — close-wound solenoids
deliver B ≈ I/pitch regardless of N. What changes is the *time behavior*: fewer turns →
lower L → higher I_pk, much steeper freewheel (N = 8: 59 MA/s, 90 V spike in the pickup),
shorter field pulse. N = 15 balances field strength (104 mT), current (187 A), slew
(15.8 MA/s), and the 1 Hz recharge budget. (Exact-model values at N = 15: I_pk = 186.5 A,
B_c = 104.4 mT — the sweep uses Wheeler L, which is +3.5 % there.)

## 3.9 Triple-check summary

| Quantity | Method 1 | Method 2 | Method 3 | Agreement |
|---|---|---|---|---|
| L (µH) | 6.925 (Wheeler) | 6.694 (elliptic) | 6.694 (Neumann integral) | 3.5 % (exact pair: 0.00 %) |
| I_pk (A) | 186.52 (closed form) | 186.52 (RK4) | — (energy-consistent) | 0.00 % |
| t_pk (µs) | 104.18 | 104.15 | — | 0.03 % |
| Energy (mJ) | 270.72 stored | 270.66 Σ(dissipated + final) | — | **0.021 %** |
| B_center (mT) | 104.43 (closed form) | 104.44 (loop sum) | 230.1 (infinite limit, ideal) | 0.01 % |
| M_pickup (µH) | 2.658 (loop pairs) | 2.638 (flux method) | — | 0.7 % |
| Pickup spike (V) | 41.90 (M × analytic di/dt) | 41.90 (M × RK4 di/dt) | — | 0.00 % |

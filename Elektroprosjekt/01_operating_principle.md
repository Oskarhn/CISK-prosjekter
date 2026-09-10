# 01 — Operating Principle

## 1.1 What the device is

An EMP (electromagnetic pulse) generator is a **capacitor-discharge coil driver**: a
capacitor bank pre-charged to V₀ is discharged through an air-core coil via a fast
power switch. The discharge current i(t) is a damped sinusoid peaking at ~187 A after
~104 µs, producing a magnetic field of ~0.1 T at the coil center that collapses again
within ~160 µs. Every conductive loop near the coil — in a victim circuit, in a credit
card's chip antenna, in a phone's PCB traces — has a voltage induced in it:

```
v_victim(t) = M_victim · di/dt          (mutual inductance × current slew rate)
```

Damage and disruption come from that induced voltage (and the near-field eddy currents
it drives). Two things therefore must be maximized, with opposite demands on the coil:

* **Peak current I_pk** — sets the field strength B (B ∝ I) and the flux swing.
  I_pk ∝ V₀·√(C/L): wants *small* L, large C, large V₀.
* **Current slew rate di/dt** — sets the induced voltage in the victim.
  di/dt ∝ V₀/L at turn-on, and (V_D + I_pk·R_fw)/L at freewheel: wants *small* L.

The design is a compromise on turn count N (see §1.7): N = 15 gives the best balance of
field strength, range, and slew rate on an 80 × 80 mm board.

## 1.2 The pulse: damped series RLC

When the switch closes, the circuit is a **series RLC** (cap bank C, total loop
resistance R, coil inductance L). KVL:

```
L·di/dt + R·i + v_C = 0 ,        v_C = (1/C)∫i dt
```

Substituting i = C·dv_C/dt gives the second-order ODE in the standard course form:

```
d²v_C/dt² + 2ζω₀·(dv_C/dt) + ω₀²·v_C = 0
```

with the formula-sheet quantities

```
ω₀ = 1/√(LC)                    undamped natural frequency
ζ  = R/(2·√(L/C))               damping ratio
ωd = ω₀·√(1−ζ²)                 damped frequency
```

Design values (verified in `03_calculations.md`):

| Parameter | Value |
|---|---|
| L | 6.69 µH |
| C | 940 µF |
| R (total loop) | 54.2 mΩ |
| ω₀ | 12 607 rad/s → **f₀ = 2.01 kHz** |
| ζ | **0.321** (underdamped, 0 < ζ < 1) |
| ωd | 11 939 rad/s → fd = 1.90 kHz |

For 0 < ζ < 1 the current is

```
i(t) = (V₀/(L·ωd)) · e^(−ζω₀t) · sin(ωd·t)
```

and the current peaks at

```
t_pk = (1/ωd)·atan(ωd/(ζω₀))  =  104.2 µs
I_pk = (V₀/(L·ωd))·e^(−ζω₀·t_pk)·sin(ωd·t_pk)  =  186.5 A
```

The capacitor voltage falls as

```
v_C(t) = V₀·e^(−ζω₀t)·(cos ωd·t + (ζ/√(1−ζ²))·sin ωd·t)
```

so at switch-off (t = t_pk) the cap sits at **10.11 V** — it has given up 270.7 − 48.0 =
222.7 mJ of its 270.7 mJ stored energy.

**Why ζ ≈ 0.3 is the sweet spot.** If ζ → 0 (no resistance) the current ring would last
many half-cycles and the pulse would be a slow 2 kHz sinusoid, not a transient. If
ζ → 1 the discharge is slow and peakless (overdamped: I_pk → 0). The peak current is
maximized in the lightly damped region; ζ = 0.321 with 54 mΩ total loop resistance
keeps the pulse to a single strong hump (~100 µs wide at 50 % of peak).

## 1.3 The switch-off and the freewheel spike

A free-running RLC ring is *not* an EMP — it just oscillates at 2 kHz for a few
milliseconds. The trick is to **turn the switch off exactly at the current peak**:

* While the MOSFET is on (0 … t_pk), the di/dt is the *rise* slope:
  `di/dt ≈ V₀/L = 3.59 MA/s` (maximum at t = 0, then decreasing as v_C falls).
* At t_pk the switch opens. The inductor current cannot change instantly, so it must
  continue flowing through the only available path: the **freewheel diode D1 +
  snubber R_FW across the coil**. The ODE becomes

```
L·di/dt = −(V_D1 + i·(R_coil + R_FW + R_D1))      (cap branch open-circuited)
```

  i.e. an exponential decay with time constant

```
τ_fw = L/(R_coil + R_FW + R_D1) = 6.69 µH/0.561 Ω ≈ 11.9 µs
```

  The initial freewheel slew rate is

```
di/dt|_fw = −(V_D1 + I_pk·R₂)/L = −(1.1 + 186.5·0.561)/6.69µ  =  −15.8 MA/s
```

  which is **4.4× steeper than the rise** — this is the "kick" that induces the big
  spike in the pickup coil and in any victim loop. The current reaches < 5 mA after
  ~54 µs, so the whole electromagnetic event lasts ≈ 160 µs.

The freewheel loop contains *only* coil + D1 + R_FW. The capacitor is connected to
node D but the switch at the other end is open, so **no current flows through the cap,
shunt, or supply** during freewheel: the cap voltage is frozen at 10.11 V, there is no
negative cap swing, and the MOSFET drain is clamped at `v_C + V_D1 + i·R_D1 ≈ 17 V
maximum` — far below the 75 V rating. This is why the freewheel diode is placed
**across the coil only** (not across coil + switch): it isolates the main ring from the
switch node and makes the freewheel a clean exponential.

## 1.4 Magnetic field generation

A solenoid of N turns, length l, radius r, carrying current I produces on its axis

```
B(z) = (μ₀·n·I/2)·[ (z+l/2)/√((z+l/2)²+r²) − (z−l/2)/√((z−l/2)²+r²) ] ,   n = N/l
```

At the center (z = 0) this reduces to

```
B_center = μ₀·N·I / (2·√(r² + l²/4))
```

For N = 15, r = 15 mm, l = 15.3 mm, I = 186.5 A:

```
B_center = 0.104 T  = 104 mT        (1 000× the Earth's field)
```

Three independent computations (closed form, direct sum of the exact field of each
turn, and the infinite-solenoid limit μ₀nI) agree to 0.01 % — the infinite limit gives
230 mT, which overestimates by 2.2× because our coil is stubby (l ≈ r).

Axial falloff (exact, at peak current):

| Distance from center | B |
|---|---|
| 0 mm | 104 mT |
| 10 mm | 70 mT |
| 20 mm | 28 mT |
| 30 mm | 11.3 mT |
| 50 mm | 2.9 mT |
| 100 mm | 0.39 mT |

The field is a **near field**: it falls roughly as 1/z³ beyond ~2 coil lengths.
This is both a limitation (damage is effective within ~5–30 cm) and a feature (a
victim 1 m away feels essentially nothing).

## 1.5 Mutual inductance: how the victim sees the pulse

A victim loop of effective area A at the coil position has mutual inductance

```
M = (flux linking the victim per ampere) ≈ B(1 A)·A_victim   (uniform-field approx.)
```

The voltage induced in it is `v = M·di/dt`. Our own 15-turn, 20 mm-diameter pickup coil
is a calibrated witness of the field. Measured (computed) for the pickup at the center:

```
M_pickup = 2.66 µH
v_rise   = M·(V₀/L)          = 2.66 µH × 3.59 MA/s  =  9.5 V
v_spike  = M·(V_D+I·R₂)/L   = 2.66 µH × 15.8 MA/s  = 41.9 V
```

A victim PCB loop of 10 cm² sitting against the coil face (M ≈ 0.9 µH) sees ~14 V at
the freewheel spike — enough to push ESD-protected I/O pins over their absolute-max
ratings, disturb analog front ends, reset under-voltage-protected MCUs, and stress
diodes in power circuits. A victim with 100 cm² of loop area (e.g. a handheld with a
battery + board) sees ~10× that.

## 1.6 Why a low-side switch (and not high-side)

The switch is the MOSFET **below** the coil (source at ground). Reason: at t = 0 the
cap + terminal sits at 24 V. In a high-side configuration the MOSFET source would also
be at ~24 V, so the gate must be driven *above* 24 V + V_GS(th) to turn on, and the
natural choice of pulling the gate to ground to turn it off gives V_GS = −24 V at t = 0
when the device is supposed to conduct — the gate-drive deadlock. Low-side, the gate
drives from the 555 at 0…10.5 V against a grounded source:

* **On:** V_GS ≈ 10.5 V (555 output high at a 12 V rail) → R_DS(on) ≈ 1.25 mΩ.
* **Off:** 10 kΩ pull-down + 15 V gate Zener → V_GS ≤ 0, robust against bounces and
  stray coupling.

The 555 monostable produces one fixed-width pulse per button press (T = 1.1RC =
106.7 µs ≈ t_pk), so the switch-off timing is set by RC, not by hand.

## 1.7 The turn-count trade-off (why N = 15)

All quantities scale with N through L(N) and the coil resistance:

* **B_center ≈ μ₀·N·I/(2√(r²+l²/4))**: for a close-wound coil B ≈ I/pitch is nearly
  independent of N (more turns at lower current).
* **I_pk ∝ V₀·√(C/L)**: falls as N grows.
* **di/dt = V₀/L**: falls fast as N grows (L grows ~N²).
* **Freewheel τ = L/R**: grows with N → longer, gentler decay.
* **Range**: longer coil (more N) pushes field further out.

The sweep (N = 8…40, full data in `03_calculations.md` §3.8; sweep uses Wheeler L, the
N = 15 row is the exact-model design point):

| N | L (µH) | I_pk (A) | B_center (mT) | freewheel di/dt (MA/s) | pickup spike (V) |
|---|---|---|---|---|---|
| 8 | 2.62 | 281 | 91 | 59.0 | 90 |
| 10 | 3.74 | 242 | 96 | 36.0 | 67 |
| **15** | **6.69** | **187** | **104** | **15.8** | **42** |
| 20 | 10.46 | 152 | 105 | 8.4 | 27 |
| 30 | 18.09 | 115 | 101 | 3.8 | 16 |
| 40 | 26.11 | 95 | 94 | 2.3 | 11 |

N = 15 keeps I_pk ≈ 187 A (strong field, 104 mT at center), di/dt = 15.8 MA/s
(42 V in a small witness coil), and a 104 µs event — while the coil fits a 31 mm bore
and the freewheel decays within the 1 Hz repetition budget. N = 8 is a legitimate
"sharpest spike" variant for the experiment section (`09_experiments.md`).

## 1.8 Energy bookkeeping

Stored: `E₀ = ½CV₀² = 270.7 mJ`. At t_pk the cap still holds 48.0 mJ (10.11 V).
Dissipation (RK4, exact to 0.02 %):

| Sink | Energy |
|---|---|
| Coil copper (both stages) | 66.9 mJ |
| R_FW 0.5 Ω snubber | 101.7 mJ |
| Cap ESR (10 mΩ) | 19.6 mJ |
| Shunt 10 mΩ | 19.6 mJ |
| MOSFET | 2.5 mJ |
| PCB traces/contacts | 3.9 mJ |
| Diode D1 (Vf + dynamic) | 8.4 mJ |

The largest loss is R_FW by design — it is the freewheel "brake" that turns the current
peak into the steep di/dt spike (without it τ would be L/R_coil ≈ 216 µs and the
freewheel di/dt only ~1 MA/s).

## 1.9 References (for the report)

* Formula sheet: ING2508 *Kretsteknikk* — second-order response `s² + 2ζω₀s + ω₀²`,
  damped sinusoid, energy in L and C.
* Course lectures: *Project introduction* (component budget, report structure),
  *Grunnleggende & Måleutstyr* (scope measurement practice), *Lodding* (soldering).
* Textbook treatment: any 2nd-order transient circuits chapter (series RLC impulse
  response); solenoid field via Biot–Savart / Ampère; mutual inductance via flux
  linkage (Faraday: v = M di/dt).
* Coil inductance: Wheeler formula (approximate) vs Neumann integral
  M(a,b,z) = μ₀√(ab)[(2/k−k)K(k) − (2/k)E(k)] with complete elliptic integrals K, E.

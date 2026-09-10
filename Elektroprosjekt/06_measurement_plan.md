# 06 — Measurement Plan (oscilloscope)

Goal: measure the **transmitter current** and the **received peak voltage** as a function
of position, using the built-in shunt and pickup coil, on a standard 2–4-channel
oscilloscope.

## 6.1 Channels and expected values

| CH | Probe at | Signal | Expected | Suggested scale |
|---|---|---|---|---|
| 1 | **TP3 → TP4** (shunt pair, 10 mΩ) | Transmitter current × 10 mΩ | 0 → 1.87 V ramp, falls to 0 at t_pk | 0.5 V/div |
| 2 | **TP7 → TP8** (pickup coil) | Induced field voltage | 9.5 V rise + 41.9 V spike at center | 10 V/div |
| 3 | **TP1 → F** (cap+) | Cap bank voltage | 24 V → 10.1 V at t_pk | 5 V/div |
| 4 | **TP5 → F** (gate) / TP6 (555 out) | Switch drive | 0 → 10.5 V, width 106.7 µs | 2 V/div |

Use a 10× passive probe (10 MΩ, ~10 pF). The shunt and pickup are low-impedance sources,
so 10× probes do not load them.

### Current from the shunt
The shunt is in the cap− return path, so it carries the **switch-on discharge current
only** (freewheel bypasses it).

```
i(t) = V_shunt(t) / 0.01 Ω
```

Peak: `I_pk = 1.87 V / 0.01 Ω = 187 A`. Measure the peak voltage on CH1 and divide by
10 mΩ. (The 1.87 V is the value at I_pk; the cap+ and shunt share the loop, so the
shunt alone reads the full switch current.)

### Received peak voltage
The pickup coil is a calibrated witness. Read the **spike** (freewheel di/dt) on CH2 —
that is the "received" peak voltage. At the center it is 41.9 V. This is the quantity
you sweep versus distance in experiment 1.

## 6.2 Distance sweep (experiment 1)

1. Fix the transmitter and scope. Put the pickup coil on a **sliding rail / 3D-printed
   rod** along the coil axis, so its center can be stepped from 0 mm to 200 mm.
2. Mark the pickup-center position relative to the coil center with a ruler; note each z.
3. At each z: fire one pulse, capture CH2 (pickup) + CH1 (shunt, to confirm I_pk is
   constant), record the spike peak V.
4. Repeat the sweep for the rise voltage (9.5 V at center) if you want both.

Expected curve (center-aligned, from `03_calculations.md` §3.4):

| z (mm) | 0 | 10 | 20 | 30 | 50 | 100 | 200 |
|---|---|---|---|---|---|---|---|
| V_spike (V) | 41.9 | 28.1 | 10.9 | 4.4 | 1.14 | 0.038 | ~0.005 |
| B (mT) | 104 | 70 | 28 | 11.3 | 2.89 | 0.387 | 0.049 |

The received voltage follows the on-axis field (∝ B), so expect the same falloff.

## 6.3 Timing and trigger

* **Time base:** 50 µs/div to see the whole ~160 µs event on one screen (or 20 µs/div to
  zoom the rise + spike).
* **Trigger:** CH4 (555 output) rising edge, low level — fires on every press, stable.
* **Single-shot (single trigger):** the event is 104–160 µs; use "single" acquisition so
  one pulse is captured cleanly without the 555 re-arming between frames.
* **Probe ground:** clip CH1 ground to TP4 (shunt low side) and CH2 ground to the
  pickup's common; keep ground loops short.

## 6.4 How to extract the numbers for the report

| Quantity | How to read it | Target |
|---|---|---|
| I_pk | CH1 peak V ÷ 0.01 Ω | 186 ± 10 A |
| t_pk | time from CH4 rising edge to CH1 peak | 104 ± 10 µs |
| Pulse width (to 10 % of peak) | CH1 width | ~150 µs |
| B_center | (V_spike / M) × (1/ (V_D+I·R₂)/L ) → or use pickup B = μ₀NI/...; simplest: B ∝ V_spike, calibrate with the 104 mT model | 104 mT at center |
| V_spike vs z | CH2 peak vs z (distance sweep) | table above |
| freewheel τ | CH1 (or CH2) decay time constant after t_pk | ~11.9 µs |

### Converting pickup voltage to B at the center
The pickup is a 15-turn, Ø20 mm coil. Its mutual inductance is M = 2.66 µH, and
`V_spike = M·di/dt`. To report B directly, use the transmitter model:
`B = μ₀·N·I/(2√(r²+l²/4))` with the measured I_pk, or calibrate the pickup against the
closed-form field once (at z = 0) and scale. Either way, the **relative** V_peak(z) vs
distance is the robust measurement.

## 6.5 Common pitfalls

* **Probe ground loop:** long ground leads add mV–V of ringing; keep the CH2 ground clip
  on the pickup's own terminal, not a distant rail.
* **555 re-trigger:** the trigger differentiator (C3) gives exactly one pulse per press;
  if you see multiple spikes, check C3/R2 values.
* **Shunt saturation:** 1.87 V is well within a 5 V/div probe; don't set CH1 to 50 mV/div
  or you'll clip.
* **Cap polarity:** C1/C2 are polarized (+) at cap+ (node A); reverse = vent.
* **24 V supply headroom:** the charge current is 240 mA; any 24 V/1 A+ bench supply works.

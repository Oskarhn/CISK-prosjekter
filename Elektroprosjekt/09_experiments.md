# 09 — Suggested Experiments

Each experiment: hypothesis → procedure → expected result (from the verified model) →
what to plot. All predicted numbers come from `calculations.py` (tables in
`03_calculations.md`).

## Experiment 1 — Received peak voltage vs distance (the main one)

**Hypothesis:** the received (pickup) voltage falls with distance roughly as the
on-axis solenoid field: strong within ~30 mm, negligible beyond ~150 mm.

**Procedure:** slide the pickup coil along the axis in 10 mm steps from 0 to 200 mm;
at each step record the spike peak (CH2) and the shunt peak (CH1, to confirm the
transmitter is constant). Use the table in `06_measurement_plan.md` §6.2.

**Expected (model):**

| z (mm) | 0 | 10 | 20 | 30 | 40 | 50 | 75 | 100 | 150 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|
| V_spike (V) | 41.9 | 28.1 | 10.9 | 4.4 | 1.9* | 1.14 | 0.30 | 0.038 | 0.007 | 0.002 |
| B (mT) | 104 | 70 | 28 | 11.3 | 5.5* | 2.89 | 0.85 | 0.387 | 0.11 | 0.049 |

(\*interpolated.) **Plot:** V_spike vs z, log-log — expect slope ≈ −3 beyond ~30 mm
(dipole near-field falloff).

**Conclusion to state:** EMP damage range on this board is ~5–30 cm; the device is a
*point-defense* disruptor, not a room-clearing one.

## Experiment 2 — Coil geometry comparison

**Hypothesis:** for close-wound solenoids B_center is nearly independent of N
(B ≈ I/pitch), but di/dt, I_pk and the spike scale as 1/L(N) — fewer turns = sharper,
weaker-field pulse; more turns = gentler, longer-range pulse.

**Procedure:** re-wind the transmitter coil (or wind 3–4 spare coils) for N = 8, 15, 20,
30 (same 1.0 mm wire, same Ø30 mm). For each: LCR the coil, fire, record I_pk, t_pk,
B_center (via pickup calibration or a gauss meter), pickup spike, and B at 50 mm.

**Expected (model, `03_calculations.md` §3.8):**

| N | L (µH) | I_pk (A) | B_c (mT) | pickup spike (V) | B @ 50 mm (µT) |
|---|---|---|---|---|---|
| 8 | 2.6 | 281 | 91 | 90 | 2258 |
| 15 | 6.7 | 187 | 104 | 42 | 2859 |
| 20 | 10.5 | 152 | 105 | 27 | 3233 |
| 30 | 18.1 | 115 | 101 | 16 | 4026 |

**Plot:** I_pk, spike, and B@50 mm vs N — one curve up (range), one curve down (spike).
This directly shows the design trade-off and justifies N = 15.

**Bonus variant:** a **flat spiral** (15 turns in a plane, Ø30 mm disc, ~2 µH): B is
strong in the plane only; good for coupling to a flat victim PCB placed against the face.

## Experiment 3 — Voltage scaling

**Hypothesis:** I_pk, B and received voltage scale linearly with V₀ (L, C, R fixed).

**Procedure:** fire at V₀ = 12, 24, 48 V (bench supply; 48 V is safe for the 50 V caps
and the 75 V MOSFET — drain clamp rises to ~33 V, check it on the scope). Record I_pk,
spike, B.

**Expected:**

| V₀ | I_pk (A) | B_c (mT) | E_cap (mJ) | pickup spike (V) |
|---|---|---|---|---|
| 12 | 93 | 52 | 68 | 21 |
| 24 | 187 | 104 | 271 | 42 |
| 48 | 373 | 209 | 1083 | 84 |

**Plot:** all three vs V₀ — straight lines through the origin. State the scaling path to
100 V / 240 V (series cap stack, HV caps, 100 V+ MOSFET) from `03_calculations.md` §3.7.

## Experiment 4 — Victim tests (the "damage" demonstration)

Pick victims with known failure thresholds:

1. **Credit card / phone NFC:** hold 0–10 cm from the coil face; fire. Static magnetic
   stripes erase at ~10–50 mT sustained, but the *pulse* erases via the read-head
   response — try 1 cm, 5 cm, 10 cm and note the erase distance.
2. **LED + resistor series (100 Ω):** place across a 10 cm loop near the coil; the pulse
   should flash it (loop sees ~10s of volts at close range).
3. **Bare MCU (ATmega328) board, 5 V:** place 5 cm away, fire. Expect reset/latch-up at
   closest range (its 10s-of-cm² ground loops pick up > 10 V spikes).
4. **Scope as victim:** clip a 1 MΩ probe with a 10 cm loop on the bench; show the
   picked-up spike on a second channel.

**Safety:** keep your phone/wristwatch > 30 cm; don't fire at anything you can't
replace.

## Experiment 5 — Freewheel resistance sweep

**Hypothesis:** the freewheel di/dt is set by τ_fw = L/(R_FW + R_coil + R_D1); smaller
R_FW = longer, gentler decay; larger R_FW = sharper spike but less total field time.

**Procedure:** swap R_FW = 0.25 Ω, 0.5 Ω, 1.0 Ω (wirewound). Record spike voltage,
freewheel τ, and B at 50 mm after 30 µs (late-field comparison).

**Expected (model):**

| R_FW | τ_fw (µs) | spike di/dt (MA/s) | pickup spike (V) |
|---|---|---|---|
| 0.25 | 14.2 | 11.5 | 30.6 |
| 0.50 | 11.9 | 15.8 | 41.9 |
| 1.00 | 6.4 | 24.6 | 65.5 |

**Conclusion:** 0.5 Ω is the balance; 1 Ω maximizes the spike (best for "kill a chip"
at close range), 0.25 Ω maximizes field duration (best for erasing magnetic media).

## Reporting these experiments

For each: state the hypothesis (1 line), the table, the plot, measured-vs-model %
deviation, and one paragraph of analysis tied to the theory (ζ, ω₀, τ, M·di/dt). That is
exactly the "kretsdrift" + "Reference" depth the assignment template allows.

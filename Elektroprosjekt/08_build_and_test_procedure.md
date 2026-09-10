# 08 — Build & Test Procedure (step by step)

Order of work: **wound coil → bench prototype → (Proteus sim) → PCB → solder → debug →
final measurement.** Each stage has a pass criterion before you move on.

## Phase 0 — Before building

* [ ] Parts ordered (`Bestillingprosjekt_filled.xlsx`), checked against `04_component_bom.md`.
* [ ] Scope ≥ 100 MHz, 2+ channels; 24 V/3 A bench PSU; DMM; LCR meter (or 10 Ω + 0.1 Ω
      shunt for the time-constant method).
* [ ] `calculations.py` run → expected numbers printed (I_pk ≈ 187 A, t_pk ≈ 104 µs,
      B ≈ 104 mT, pickup spike ≈ 41.9 V).
* [ ] Optional but recommended: build the circuit in **Proteus** first
      (`10_proteus_simulation.md`) — catch wiring errors before soldering.

## Phase 1 — Wind and measure the coils

1. Wind COIL_T: 15 turns, 1.0 mm wire, Ø30 mm, on the 29 mm ID tube (leave 70 mm leads).
2. Wind PU: 15 turns, 0.5 mm wire, Ø20 mm, on the 18–20 mm former.
3. Measure COIL_T on the LCR meter at 1 kHz → **expect 6.5–7.2 µH, ESR ≈ 31 mΩ**
   (`05_coil_design.md` §5.2). If out of range, re-wind before anything else.
4. Measure PU resistance (should be ~80 mΩ) and COIL_T resistance (~31 mΩ, DMM 2-wire OK
   at this value).

## Phase 2 — Bench prototype (breadboard/perfboard, 5 V first, then 24 V)

Wire the control path only first (555, R1/C_TIM, R2/C3/S1, R9/D2 from a 12 V supply,
C4/C5, R3/R4/D3 to a MOSFET gate tied to a 100 Ω dummy to ground):

1. Press S1 → scope CH on 555 pin 3: **expect a 106.7 µs high pulse** at ~10.5 V.
   If it's shorter/longer: check R1 (9.70 kΩ) and C_TIM (10 nF). If continuous: the
   trigger is stuck low — check R2 (10 kΩ) and that C3 is the *series* differentiator.
2. Add the MOSFET with a 1 kΩ resistor as the "coil" (dummy load): gate 0→10.5 V,
   drain sees the 10.5 V→0 transition within ~1 µs.
3. Now power the pulse path from the 24 V supply **with the real coil** (still on the
   bench): press S1 → scope:
   * CH1 on the shunt (wire a 0.01 Ω or 0.1 Ω shunt in the cap− lead): **1.87 V ramp to
     peak at ~104 µs, then a fast fall as freewheel takes over.**
   * CH on coil end (drain): stays near 0 V during discharge, jumps to ~11–17 V at
     switch-off, **no megavolt-level spike** (D1 clamps it).
   * CH on cap+: 24 → 10 V.
   * CH on pickup: 9.5 V rise + 41.9 V spike.
4. **Pass criterion:** all four waveforms match `02_schematic.md` §2.5 and
   `03_calculations.md` within ~15 %.

## Phase 3 — Proteus simulation (course requirement)

Build the same netlist in Proteus and run a transient simulation
(`10_proteus_simulation.md`). Pass criterion: simulated I_pk and t_pk within 20 % of the
hand-calculated 187 A / 104 µs (model differences are expected; see §10.4).

## Phase 4 — PCB fabrication

1. Layout per `07_pcb_layout.md` (or the course's Proteus AURORA PCB tool).
2. Order: 80 × 80 mm, 2-layer, 35 µm, 1.6 mm, matte tin. (5 pcs ≈ 250 NOK; 1 pc if
   budget-constrained — order 2 minimum: one for the build, one spare.)
3. While waiting: buy cut the coil tube, cut standoffs, prepare the pickup former.

## Phase 5 — Soldering (PCB)

Order of components (easiest → hardest):
1. Test headers + 5.08 terminal + tact switch (through-hole, easy).
2. 555 DIP-8 (check pin 1 orientation; pin 4 = pin 8 = VCC).
3. Resistors/capacitors 0805 (or through-hole equivalents if you substituted).
4. D4 TVS, D2/D3 Zeners, D1 MUR1560 (polarity!).
5. MOSFET (TO-220; tab → ground pad).
6. Shunt (5 W wirewound — don't overheat the solder joints).
7. **Coil leads → A and E pads** (most important joints: 187 A).
8. Cap bank (470 µF × 2, + toward A).
9. Pickup coil + leads → TP7/TP8; fix the pickup at the coil center.

**Pre-power checklist:**
* [ ] DMM continuity: A–E through coil = ~31 mΩ; no short A–F or E–F.
* [ ] DMM diode check: D1 (anode E), D2 (cathode G), D3 (cathode gate), D4 (cathode +).
* [ ] 555 pin 1 = GND, pin 8 = 12 V (after R9/D2 rail is live, G = 12.0 V).
* [ ] Cap polarity: + at A.
* [ ] No solder bridges on 0805s (inspect with a phone camera zoom).

## Phase 6 — Debug (symptom → cause)

| Symptom | Likely cause | Fix |
|---|---|---|
| No pulse at all | 555 not powered / pin 4 not tied to VCC / shorted trigger | Check G = 12 V; R2 present |
| 555 output continuous high | Trigger pin held < ⅓VCC (C3 wrong value/placement, R2 missing) | C3 = 10 nF *in series* with the button; R2 = 10 kΩ to 12 V |
| 555 pulses but MOSFET never on | R4 missing (gate floats) or 555 out too low | R4 = 10 kΩ; check pin 3 voltage ≈ 10.5 V |
| MOSFET on forever | R4 too large / 555 stuck | R4 = 10 kΩ; check pin 3 falls to < 1 V after pulse |
| Huge drain spike (> 50 V) | D1 wrong way / R_FW open / freewheel loop broken | Re-check D1 orientation; R_FW continuity |
| Cap voltage swings negative | D1 open (freewheel missing) | Replace D1 |
| I_pk much lower than 187 A | L too high (extra turns) / R too high (cold solder joints, thin traces) | LCR the coil; DMM the loop R; reflow joints |
| I_pk higher / t_pk shorter | L low (few turns, loose winding) | Re-wind to 15 turns close-wound |
| Pickup spike small | Pickup off-center / few turns / leads twisted (loop cancels) | Center pickup; count turns; parallel leads along axis |
| Burn smell / hot spot | Current path bottleneck (thin trace, bad joint) | Inspect loop; widen/extra vias; reflow |
| 555 hot / dead | Powered at 24 V (R9/D2 failed) | Replace 555; fix regulator |
| Multiple pulses per press | Trigger bounce (C3 too small) | C3 = 10 nF series (as designed) |

## Phase 7 — Final measurement (the "official" run)

1. Let the board charge to 24.0 V (DMM at TP1→F).
2. Scope: CH1 shunt 0.5 V/div, CH2 pickup 10 V/div, CH3 cap+ 5 V/div, CH4 gate 2 V/div;
   50 µs/div; trigger CH4 rising; **single** acquisition.
3. Fire 5 pulses; keep the best shot. Save as `pulse_center.png`.
4. Record: I_pk (CH1/0.01 Ω), t_pk (CH4→CH1 peak), cap V at t_pk, pickup rise + spike,
   freewheel τ. Compare with targets: **187 A / 104 µs / 10.1 V / 9.5 V + 41.9 V / 11.9 µs**.
5. Run the distance sweep (`06_measurement_plan.md` §6.2) → table + plot for experiment 1.
6. Optional: victim tests (`09_experiments.md` experiment 4).
7. Write up: measured vs calculated table (include the % deviations — that *is* the
   triple-check at the hardware level).

## Safety notes

* 270 mJ at 24 V: the shock is mild (low voltage), but a 187 A arc can **weld** poor
  connections and burn skin — keep loose wires clipped, and don't bridge A–F with metal.
* The cap stays charged ~10 V for minutes after a pulse (bleed 10 kΩ); discharge with the
  bleed shorted when servicing.
* Electrolytics vent if reverse-polarized — check polarity before every power-up.
* 1 Hz repetition is thermally safe (all parts verified in `03_calculations.md` §3.5);
  sustained > 5 Hz will heat R_FW and the coil.

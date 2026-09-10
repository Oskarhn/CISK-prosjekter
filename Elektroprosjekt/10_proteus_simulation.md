# 10 — Proteus Simulation (course "kretssimulering" part)

The course (ING2508 *Kretsteknikk — Måleteknikk og kretssimulering*) uses **Proteus** for
schematic capture, transient simulation, and PCB layout (per the *Proteus introduction*
lecture: new project → schematic capture → component selection → simulation → PCB layout
with design rules → export PDF). This file is the build/simulation guide for exactly that.

## 10.1 Build the schematic in Proteus (ISIS)

Create a new project, then place (search the Proteus library):

| Item | Proteus library choice | Notes |
|---|---|---|
| NE555 | `555` (Timer category, DIP-8) | Standard model |
| MOSFET | `IRF540N` (power MOSFET) — or IRF3707 if present | IRF540N has R_DS(on) ≈ 44 mΩ → ζ ≈ 0.41, I_pk ≈ 172 A: a good enough stand-in; note the deviation in the report |
| D1 | nearest ultrafast rectifier (search `MUR*` / `1N49*`), 600 V class | Sets freewheel Vf ≈ 0.7–1.1 V |
| D2 / D3 | `1N4742A` / `1N4744A` (Zener category) | 12 V / 15 V |
| D4 | TVS or omit in sim | Only matters for supply transients |
| COIL_T | `INDUCTOR` with **L = 6.69 µH** + series **31 mΩ resistor** | Proteus inductors are ideal — the coil R must be added by hand |
| PU (pickup) | `INDUCTOR` **L = 3.6 µH**, coupled to COIL_T with **k = 0.54** (M = 2.66 µH) | Coupling is set in the inductor properties (mutual coupling to the other inductor) |
| Shunt | 10 mΩ resistor | As designed |
| Everything else | 0805/through-hole passives as in `schematic.svg` | Values in `04_component_bom.md` |

Wire the netlist exactly as in `02_schematic.md` §2.2 (the net list is the source of
truth). Add virtual instruments: two **virtual oscilloscopes** (or a VirtualScope
channel set) — one across the shunt (current), one across the pickup.

## 10.2 Simulation setup

* **Analysis:** Transient.
* **Start:** 0 s, **End:** 500 µs.
* **Step:** 100 ns (resolves the ~100 ns turn-off transition and the 41.9 V spike;
  1 µs is acceptable for the slow ring).
* **Cap initial condition:** C1/C2 → IC = 24 V (pre-charged bank).
* **Supply:** 24 V ideal source (or 24 V DC supply model).
* **Trigger:** drive the 555 trigger with a 200 µs pulse source at t = 10 µs (instead of
  the button) so the run is repeatable.

## 10.3 Expected simulation results

| Quantity | Hand calc | Expected sim |
|---|---|---|
| 555 output width | 106.7 µs | 105–108 µs |
| I_pk | 186.5 A | 170–195 A (MOSFET model R_DS(on)) |
| t_pk | 104.2 µs | 100–110 µs |
| Cap voltage at switch-off | 10.1 V | 10 ± 1 V |
| Pickup rise / spike | 9.5 V / 41.9 V | 9 V / 35–48 V |
| Freewheel decay | τ ≈ 11.9 µs | 10–13 µs |

**Pass criterion:** I_pk and t_pk within ±20 % of the hand calculation. Model-level
differences (MOSFET R_DS(on), diode Vf, ideal inductor) are expected and should be
discussed — that discussion *is* the simulation section of the report.

## 10.4 Known model limitations (state them in the report)

1. **Ideal inductor:** no frequency-dependent copper loss, no inter-turn capacitance →
   the sim ring is slightly cleaner than reality.
2. **MOSFET gate model:** the library gate-charge model may make turn-off slower than the
   real IRF3707 (~100 ns), which smears the 41.9 V spike; if the sim spike looks too
   small, reduce the gate drive resistance (R3 = 10 Ω → 2.7 Ω) or use the 555's output
   directly.
3. **555 model:** average-precision; its output rise (~µs) slightly delays turn-on —
   negligible against t_pk = 104 µs.
4. **Coupled inductors:** k = 0.54 assumes perfect flux alignment (pickup centered).
   Off-center pickup → lower k → lower spike (the distance experiment in sim: lower k
   stepwise and note the spike fall-off).
5. **Proteus SPICE convergence:** a 187 A / 15 MA/s circuit with a 10 mΩ shunt can hit
   "convergence" warnings — reduce the time step to 10 ns locally or add 1 mΩ series
   resistance in the shunt measurement node.

## 10.5 PCB layout in Proteus (AURORA)

Per the lecture's PCB process:

1. **Pins/footprints:** assign a package to every part (DIP-8, TO-220, 0805, 2-pin
   header, 5.08 terminal, coil pads as two 3 mm circles + via cluster).
2. **Design Rule Manager:** clearances ≥ 6 mil for < 10 V nets (trace-to-trace,
   trace-to-pad, pad-to-pad, board edge); layer assignment for the two signal layers;
   net class "power" for the current loop with 8 mm trace width.
3. **Board edge:** 80 × 80 mm rectangle.
4. **Placement:** per `07_pcb_layout.md` §7.1 (current loop compact, 555 in a corner,
   coil centered on standoffs).
5. **Routing:** manual (the current loop must be 8 mm wide — auto-router will not do
   that) or auto-router with the power net class constraints.
6. **Export:** Output → export graphics → PDF, **silk layer unchecked** (per the
   lecture: "Make sure no silk is selected").

The exported PDF is the PCB figure for the report; the Proteus schematic capture export
is the "kretsskjema (klare bilder og komponenter, verdier med enheter)" figure required
by the assignment template — make sure all component values and units are visible.

# EMP Generator — Course Project Documentation

**Goal:** Build the most "dangerous" compact EMP/EMI device possible on a ≤ 80 × 80 mm PCB
with 5–10 different component types, generating the strongest practical, measurable
electromagnetic transient that can damage or disrupt external electronics.

**Design in one line:** 940 µF / 24 V cap bank → 15-turn air-core solenoid (6.7 µH, 31 mm OD)
→ low-side power MOSFET switch, with a 555-timed switch-off exactly at the current peak, a
freewheel diode + 0.5 Ω snubber across the coil, and a 15-turn pickup coil for oscilloscope
measurement.

## Verified key results (triple-checked, see `03_calculations.md` and `calculations.py`)

| Quantity | Value | Method agreement |
|---|---|---|
| Stored energy | 270.7 mJ | ½CV² |
| Coil inductance L | 6.69 µH | 3 methods, 3.5 % spread |
| Damping ζ | 0.321 | analytic = simulation |
| Natural frequency f₀ | 2.01 kHz | analytic = simulation |
| Peak current I_pk | **186.5 A** | analytic vs RK4: 0.00 % |
| Peak current time t_pk | **104.2 µs** | analytic vs RK4: 0.003 % |
| Center field B | **104.4 mT** | 3 methods, 0.01 % |
| Max di/dt (freewheel) | **15.8 MA/s** | analytic = simulation |
| Pickup voltage (15 T / 20 mm, at center) | 9.5 V rise, **41.9 V spike** | 2 methods, 0.7 % |
| Energy balance | closes to 0.02 % | pass |

## File index

| File | Contents |
|---|---|
| `README.md` | This index + requirements coverage |
| `01_operating_principle.md` | Physics: series RLC pulse, B-field, mutual inductance, design rationale |
| `02_schematic.md` | Complete schematic description, net list, pin map, why each component exists |
| `schematic.svg` | Full circuit diagram with values and units |
| `03_calculations.md` | All calculations, triple-checked side by side (analytic / RK4 / energy / geometry) |
| `04_component_bom.md` | Complete BOM with part numbers, values, selection rationale |
| `05_coil_design.md` | Transmitter + pickup coil design, winding procedure, how to measure L |
| `06_measurement_plan.md` | Oscilloscope setup, test points, how to measure current and received voltage |
| `07_pcb_layout.md` | PCB layout: placement, trace widths, grounding, test points |
| `08_build_and_test_procedure.md` | Step-by-step: prototype → PCB → solder → debug → final measurement |
| `09_experiments.md` | Suggested experiments: V_peak vs distance, coil geometries, scaling, victim tests |
| `calculations.py` | Pure-Python triple-check model. Run it to reproduce every number in this project. |

## Requirements coverage

| Requirement | Where covered |
|---|---|
| PCB ≤ 80 × 80 mm | `07_pcb_layout.md` (board is exactly 80 × 80 mm) |
| 5–10 different component types | `04_component_bom.md` — **8 types**: resistor, capacitor, coil, diode, MOSFET, IC, switch, connector |
| Discrete components over modules | `04_component_bom.md` — no modules except the 555 IC itself |
| Manufacturable + hand-solderable | `08_build_and_test_procedure.md` — 2-layer board, 0805/through-hole mix, no fine-pitch parts |
| Operating principle in detail | `01_operating_principle.md` |
| Complete schematic | `02_schematic.md` + `schematic.svg` |
| Exact values + part numbers + why each | `04_component_bom.md` |
| Current, energy, pulse duration, switching, stresses | `03_calculations.md` (stress table per part) |
| Role of L, di/dt, B-field, mutual inductance | `01_operating_principle.md` + `03_calculations.md` |
| Triple-check every calculation | `03_calculations.md` — 3 independent methods per quantity, agreement table |
| MOSFET/switch protection | Flyback (freewheel D1), snubber (R_FW), gate clamp (15 V Zener), supply TVS — `02_schematic.md`, `04_component_bom.md` |
| Transmitter coil design + how to measure L | `05_coil_design.md` |
| Pickup coil for scope measurement | `02_schematic.md`, `06_measurement_plan.md` |
| Measuring transmitter current + received peak voltage | `06_measurement_plan.md` |
| PCB layout guidance (traces, ground, placement, loop minimization, TPs) | `07_pcb_layout.md` |
| Complete BOM | `04_component_bom.md` |
| Step-by-step build → test → debug → measure | `08_build_and_test_procedure.md` |
| Experiments: V_peak vs distance, coil geometries | `09_experiments.md` |
| Course format (title, circuit with values, theory, references) | All docs use SI units + formula-sheet notation (ζ, ω₀, τ); theory sections are report-ready |

## How to reproduce the calculations

```powershell
& "C:\Users\Oskar\AppData\Local\Programs\Python\Python310\python.exe" "C:\Users\Oskar\Documents\elektro_prosjekt\EMP_Generator\calculations.py"
```

The script computes every number in `03_calculations.md` with 3 independent methods per
quantity (Wheeler / elliptic-integral / direct Neumann for L; closed form / loop sum /
infinite solenoid for B; analytic / RK4 / energy balance for the pulse; loop pair / flux
method for the pickup mutual inductance).

## Part availability note

Web part verification is not available in this session, so the BOM uses established,
common part numbers (IRF3707, MUR1560, NE555P, 1N4742A/1N4744A, SMBJ24A, standard
passives). Each entry in `04_component_bom.md` lists the spec that matters; verify stock
and exact part number at Elfa/Farnell before ordering — all are standard catalog items.

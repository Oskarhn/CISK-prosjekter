# 04 — Component BOM

**Component types used: 8** (within the course limit of 5–10): resistor, capacitor, coil
(hand-wound), diode, MOSFET, IC, switch, connector.

Suppliers: **no.rs-online.com** and **no.farnell.com** (per course requirement). Part
numbers below are the intended catalog items; **verify stock, part number and price on
the supplier site before ordering** — where a part number is marked `(search)`, pick any
item meeting the spec (the course accepts similar components with the same
specifications). Prices are NOK estimates ex. MVA for the order sheet.

A filled version of the course order template is: **`Bestillingprosjekt_filled.xlsx`**.

## 4.1 Power / pulse path

| Ref | Value | Qty | Spec (what matters) | Suggested part (supplier) | Price ≈ NOK | Why it is needed |
|---|---|---|---|---|---|---|
| C1, C2 | 470 µF / 50 V | 2 | Low-ESR radial electrolytic, ESR ≤ 25 mΩ @ 100 kHz, 105 °C (e.g. Panasonic FR/TE, KEMET, Nichicon PW) | RS: low-ESR 470 µF 50 V radial (search "470 µF 50 V low ESR") | 18 ea | Energy store: 940 µF × 24 V = 270.7 mJ. Parallel halves ESR and current per can. |
| R_CHG | 100 Ω / 2 W | 1 | Metal-film, 1 %, through-hole | Farnell: 100 R 2 W metal film 1 % (search "100R 2W") | 7 | Limits charge current to 240 mA (~0.5 s full charge). |
| R_BLEED | 10 kΩ / ¼ W | 1 | Any film, through-hole | (search "10k 1/4W") | 2 | Safety discharge: 24 V → 2 V in ~4 s. |
| COIL_T | 15 T, r = 15 mm | 1 | 1.0 mm (17 AWG) enameled Cu, close-wound on 29–31 mm OD **non-metallic** tube, l ≈ 15.3 mm | Magnet wire 1.0 mm (RS: 17 AWG Cu enamelled) + 31 mm OD plastic/PVC tube | 45 + 12 | The EMP radiator. L ≈ 6.7 µH, R ≈ 31 mΩ, B_center ≈ 104 mT @ 186.5 A. |
| D1 | MUR1560 | 1 | Ultrafast rectifier, 15 A, ≥ 600 V (alt: MUR1520 60 V is sufficient) | Farnell: 1269600 (MUR1560) or search "MUR1560" | 12 | Flyback/freewheel diode across the coil; clamps MOSFET drain (~17 V max); sets freewheel di/dt with R_FW. |
| R_FW | 0.5 Ω / 5 W | 1 | Wirewound, 1 % | RS: 0.47 R 5 W wirewound (search "0.5R 5W wirewound") | 12 | Freewheel brake: τ_fw = 11.9 µs → 15.8 MA/s spike. 101.7 mJ/pulse. |
| MOSFET | IRF3707 | 1 | N-ch power MOSFET, 75 V, R_DS(on) ≤ 1.6 mΩ @ V_GS = 10 V, pulsed I_D ≥ 300 A, TO-220 | Farnell: IRF3707 (search "IRF3707"); alt: IRF3710 / IRF3716 | 22 | The switch. 1.25 mΩ keeps ζ = 0.321; 75 V ≫ 17 V clamped drain. |
| R_SHUNT | 0.01 Ω / 5 W | 1 | Wirewound shunt 10 mΩ (alt: 2 × 0.02 Ω in series → I_pk ≈ 175 A) | RS: "10 mΩ shunt 5 W" (search "0.01R 5W") | 20 | Current sensor: 1.87 V at 186.5 A for the scope. Bypassed during freewheel (clean signature). |
| TB1 | 5.08 mm 2-pin | 1 | PCB terminal block, 24 V class | RS: 5.08 mm 2-pin PCB terminal (search) | 6 | Supply input. |
| D4 | SMBJ24A | 1 | Unidirectional TVS, 24 V (alt: SMAJ24A) | RS: SMBJ24A (search "SMBJ24A") | 9 | Clamps supply-input transients at ~38 V. |

## 4.2 Control path (555 + gate drive)

| Ref | Value | Qty | Spec | Suggested part | Price ≈ NOK | Why it is needed |
|---|---|---|---|---|---|---|
| IC1 | NE555P | 1 | 555 timer, DIP-8 | Farnell: 1065735 (NE555P) / RS: 188-9643 | 13 | Monostable: one 106.7 µs pulse per button press = switch-off at the current peak. |
| R1 | 9.70 kΩ 1 % | 1 | Metal film, 0805 | Farnell 0805 1 % series (search "9k7 1% 0805") | 1.5 | T = 1.1RC = 106.7 µs ≈ t_pk. |
| C_TIM | 10 nF / 50 V | 1 | C0G/NP0, 0805 | Farnell: 1095994 (10 nF 50 V C0G 0805) or search | 2 | Timing cap (stable with C0G). |
| C3 | 10 nF / 50 V | 1 | C0G/NP0, 0805 | same as above | 2 | Trigger differentiator → exactly one pulse per press, bounce-immune. |
| R2 | 10 kΩ | 1 | Film, 0805 | Farnell 0805 series (search "10k 0805") | 1.5 | Trigger pull-up. |
| R4 | 10 kΩ | 1 | Film, 0805 | same as above | 1.5 | Gate pull-down (guaranteed off). |
| R3 | 10 Ω / ½ W | 1 | Film, 0805 | (search "10R 0805 1/2W") | 1.5 | Gate drive; damps gate ringing. |
| D3 | 1N4744A | 1 | Zener 15 V, 1 W | Farnell: 1N4744A (search) | 6 | Gate clamp (V_GS ≤ 15 V < 30 V rating). |
| R9 | 820 Ω | 1 | Film, 0805 | (search "820R 0805") | 1.5 | Sets 12 V rail current (~14.6 mA). |
| D2 | 1N4742A | 1 | Zener 12 V, 1 W | Farnell: 1N4742A (search) | 6 | 555 supply regulator (NE555 max 15.5 V — 24 V directly would destroy it). |
| C4 | 100 nF / 50 V | 1 | X7R, 0805 | Farnell 0805 X7R (search "100n 50V 0805") | 2 | 555 control-pin bypass. |
| C5 | 10 µF / 25 V | 1 | X7R, 0805 | (search "10u 25V 0805") | 2.5 | 555 bulk cap (gate-drive transient). |
| S1 | 6 × 6 mm | 1 | Tact switch, 1 A | RS: 6 mm tact switch (search) | 3 | Fire button. |

## 4.3 Measurement

| Ref | Value | Qty | Spec | Suggested part | Price ≈ NOK | Why it is needed |
|---|---|---|---|---|---|---|
| PU | 15 T, r = 10 mm | 1 | 0.5 mm (32 AWG) enameled Cu, close-wound on 20 mm OD non-metallic former | Magnet wire 0.5 mm (RS: 32 AWG Cu enamelled) | 40 | Field witness for the scope: M = 2.66 µH → 9.5 V rise + 41.9 V spike at center. |
| HDR1 | 2.54 mm, 2-pin | 1 | Pin header (pickup output) | RS: 2.54 mm header (search) | 4 | Pickup → scope BNC/clips. |
| HDR2 | 2.54 mm, 6-pin | 1 | Pin header (TP1–TP6) | RS: 2.54 mm header (search) | 4 | Test points: cap+, drain, shunt pair, gate, 555 out. |

## 4.4 Mechanical / PCB

| Item | Qty | Spec | Price ≈ NOK | Notes |
|---|---|---|---|---|
| PCB 80 × 80 mm, 2-layer, 35 µm Cu | 1 (or 5) | 1.6 mm FR-4, matte tin or ENIG | 250 (5 pcs) | Order from a PCB house; layout in `07_pcb_layout.md`. |
| Standoffs M3 × 6 mm, nylon | 4 | | 6 | Hold the coil tube above the board. |
| Coil tube (COIL_T) | 1 | 31 mm OD × ~20 mm, PVC/polyamide/PLA (non-conductive, non-magnetic) | 12 | Cut from tubing or 3D-printed. Metal = shorted turn (do not use copper/aluminium). |
| Pickup former | 1 | 20 mm OD × ~18 mm tube | 8 | Or wind around a 20 mm dowel and slip the tube on. |
| Solder, flux, wire cutters | — | | — | Standard lab equipment. |

**Not ordered (external, lab equipment):** 24 V / 3 A bench PSU (any 0–30 V DC supply),
oscilloscope ≥ 100 MHz with ≥ 2 channels (course lab equipment).

## 4.5 Budget summary (see order sheet `Bestillingprosjekt_filled.xlsx`)

The order sheet sums `max(antall, min. kjøp) × pr.stk` per row (Farnell 0805 lines are
bought in multiples of 5, as in the template example):

| Group | NOK (ex. MVA) |
|---|---|
| Resistors (9) | 69.0 |
| Capacitors (6) | 68.5 |
| Diodes (4) | 33.0 |
| MOSFET + IC | 35.0 |
| Switch + connectors (4) | 17.0 |
| Magnet wire (2) | 85.0 |
| PCB + tube + standoffs | 268.0 |
| **Subtotal** | **575.5** |
| +25 % MVA | 143.9 |
| **Total ≈ 719 NOK** | |

## 4.6 Part-number verification note

Catalog access (no.rs-online.com / no.farnell.com) blocked automated lookup in this
session, so the part numbers above are from catalog knowledge and marked with
`(search …)` where exact lookup is needed. **Before ordering:** open the two supplier
sites, confirm each row by its spec, and update the price/stock-number columns in
`Bestillingprosjekt_filled.xlsx`. Every spec is exact, so any in-stock part meeting it is
acceptable per the assignment ("similar components with same specifications").

The three riskiest lines (availability): the 10 mΩ shunt (fallback: 2 × 0.02 Ω 5 W in
series), the low-ESR 470 µF/50 V cap (fallback: any 470 µF/50 V with ESR ≤ 25 mΩ; a
standard 470 µF/50 V with 50 mΩ ESR lowers I_pk to ≈ 150 A — still acceptable), and the
0.5 Ω/5 W wirewound (fallback: 0.47 Ω/5 W, negligible change).

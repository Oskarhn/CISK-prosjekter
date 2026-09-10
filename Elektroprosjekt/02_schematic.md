# 02 — Complete Schematic

Figure: **`schematic.svg`** (same folder). All values and units are printed on the
diagram. Below: the circuit description, the net list, and *why each component is there*.

## 2.1 Circuit description

The circuit has two parts: the **pulse power path** (left) and the **control path**
(right), sharing the ground node F.

```
        +24 V supply (external bench PSU, 0–30 V / 3 A)
  TB1+ ──┬──────────────────────────────────────────────────────┐
         │                                                      │
        [R_CHG 100 Ω / 2 W]                                     │  D4: SMBJ24A TVS (cathode to +)
         │                                                      │  (input transient clamp)
        ┌┴──────────┐   coil start (D)                          │
        │           │──────┐                                    │
       C1          [COIL T 15 T, air core]                     │
      470 µF        │        │                                  │
      50 V        coil end (E)                                 │
       C2          ┌────────┴─────────┐                        │
      470 µF       │ D1: MUR1560      │  R_FW 0.5 Ω / 5 W       │
     (parallel)    │ (anode E)        ├──────┐  (freewheel      │
         │         │                  │      │  snubber)        │
         │        [IRF3707]           │      │                  │
         │          │D  E (drain)     │      │                  │
         │         [  MOS  ]◄── gate ─┼──┐   │                  │
         │          │S  F             │  │   │                  │
         │          │                 │  │   │                  │
   [R_SHUNT 0.01 Ω / 5 W]             │  │   │                  │
         │                            │  │   │                  │
        TB1− (−)  ────────────────────┴──┴───┴──────────────────┘
        F = GND reference (MOSFET source = cap− = supply− = 555 GND)

  Control (12 V rail derived from 24 V):
  +24 V ──[R9 820 Ω]── G(12 V) ──[D2 1N4742A 12 V Zener]── F
                         │
                        NE555P  (DIP-8, monostable)
        pin 8 VCC ← G,   pin 1 GND → F
        pin 4 RESET → G
        pin 5 CTRL ←[C4 100 nF]→ F
        pin 6/7 DIS/THR ←[R1 9.70 kΩ 1%]→ G
                         └──[C2_TIM 10 nF C0G]→ F
        pin 2 TRIG ←[R2 10 kΩ]→ G
                         └──[C3 10 nF C0G]──[button S1]── F
        pin 3 OUT ──[R3 10 Ω]── MOSFET gate
        gate ←[R4 10 kΩ]→ F        (pull-down)
        gate ←[D3 1N4744A 15 V Zener]→ F   (gate clamp)

  Pickup:
  15-turn, 20 mm coil inside the transmitter bore ── 2-pin header (scope)
```

## 2.2 Net list

| Node | Connected to |
|---|---|
| **P+** (supply+) | TB1+, R_CHG pin 1, D4 cathode |
| **A / D** (cap+) | R_CHG pin 2, C1 top, C2 top, coil start, R_BLEED top, R_FW far end |
| **C1m** (intermediate) | D1 cathode, R_FW near end |
| **E** (coil end / drain) | coil end, MOSFET drain, D1 anode, TP_COIL_END |
| **F** (ground) | MOSFET source, R_SHUNT far end, TB1−, C1/C2 bottom, R_BLEED bottom, R4 bottom, D3 cathode, 555 GND/CTRL cap, button S1 far end, D4 anode, pickup return |
| **B / C−** (cap−) | C1/C2 bottom → R_SHUNT near end (see A/F: the shunt sits between the cap− plates and F) |
| **G** (12 V rail) | R9 end, D2 anode, 555 VCC, R1, R2 |
| **Gate** | R3, R4, D3 anode, MOSFET gate |
| **Trig** (555 pin 2) | R2, C3, S1 |
| **Thr** (555 pin 6/7) | R1, C2_TIM |
| **Out** (555 pin 3) | R3 |
| **PU1/PU2** | pickup coil ends → header |

Note: the **shunt is in the cap− path** (cap bank bottom → R_SHUNT → F). It therefore
carries the *switch-on discharge current* (measured: 0 → 1.87 V) but is **bypassed
during freewheel** (the freewheel loop is coil + D1 + R_FW only), so the shunt trace
drops to 0 V when the spike occurs — a clean, unambiguous current signature.

## 2.3 Why each component is needed

| Ref | Value | Role (and what breaks without it) |
|---|---|---|
| C1, C2 | 2 × 470 µF / 50 V low-ESR | Energy store: 940 µF × 24 V = **270.7 mJ**. Parallel: halves ESR (≈10 mΩ total), halves current per can, keeps the pulse under-damped as designed. 50 V rating gives 2× margin. |
| R_CHG | 100 Ω / 2 W | Limits supply→cap charge current to 240 mA (peak 5.8 W for ~100 ms, then settles); ~0.5 s to full charge. Without it the PSU/leads would see an infinite-current step. |
| R_BLEED | 10 kΩ / ¼ W | Safety discharge: cap falls 24 V → 2 V in ~4 s (τ = 9.4 s). Bleed current during a pulse is 2.4 mA — negligible. Without it the bank stays charged for hours. |
| COIL_T | 15 T, 1.0 mm wire, r = 15 mm | The EMP radiator. L = 6.69 µH stores the current; the air-core geometry (l ≈ r) maximizes on-axis B per ampere while keeping L low for high di/dt. R_coil = 31 mΩ. |
| D1 | MUR1560 (600 V / 15 A ultrafast) | **Flyback / freewheel diode** across the coil: gives the 187 A a path when the switch opens, sets the freewheel di/dt with R_FW, and clamps the MOSFET drain to ≈ v_C + V_D1 (≈11–17 V) so there is **no drain spike**. Ultrafast + 15 A class: the pulse is 187 A for 54 µs, but ∫i²dt = 0.21 A²s, well inside the 8/3 ms I_TSM rating (equivalent to ~13 A over 2.7 ms). |
| R_FW | 0.5 Ω / 5 W wirewound | **Snubber/brake in the freewheel path**: τ_fw = L/(R_FW+…) = 11.9 µs → 15.8 MA/s spike. Takes 101.7 mJ per pulse (≈ 102 mW average at 1 Hz). |
| IRF3707 | 75 V / 45 A / 1.25 mΩ (TO-220) | The switch. Needs: low R_DS(on) (keeps ζ = 0.321), pulsed current > 200 A (rated 720 A pulse), 75 V margin over the 17 V clamped drain, fast gate (Q_g ≈ 30 nC). |
| R3 | 10 Ω | Gate drive resistor: sets gate RC ≈ 25 ns (faster than needed, but damps gate ringing with the lead inductance). |
| R4 | 10 kΩ | Gate pull-down: guarantees off after power-down or 555 failure; prevents floating-gate latch-up of the pulse. |
| D3 | 1N4744A 15 V Zener | **Gate clamp**: any gate overshoot (stray coupling from the 15.8 MA/s loop, or a 24 V miswire) is clamped at 15 V < 30 V V_GS rating. |
| R9 | 820 Ω | Sets 555 rail current: (24−12)/820 ≈ 14.6 mA, enough for the 555 (~5 mA) + Zener regulation. |
| D2 | 1N4742A 12 V Zener | **555 supply regulator**: NE555 is rated to 15.5 V; directly at 24 V it would be destroyed. |
| NE555P | DIP-8 | Monostable: one 106.7 µs output-high per button press = switch-off at the current peak. Chosen over a microcontroller: 6 discrete components, no firmware, hand-solderable. |
| R1 / C2_TIM | 9.70 kΩ 1% / 10 nF C0G | T = 1.1RC = 106.7 µs ≈ t_pk = 104.2 µs (switch-off 2.5 µs after peak, where the current is still 99.9 % of I_pk). C0G for stable timing. |
| R2 | 10 kΩ | Trigger pull-up (idle trigger = 12 V, above the ⅔VCC retrigger window). |
| C3 | 10 nF C0G | Trigger differentiator: pressing S1 couples the pin to GND for ~10–50 µs → exactly **one** pulse per press, bounce-immune, hold-time-immune (the pin recovers to 12 V well before T elapses, so a held button cannot re-trigger). |
| C4 | 100 nF X7R | 555 control-voltage (pin 5) bypass. |
| C5 | 10 µF X7R | 555 bulk supply cap (holds the gate-drive transient). |
| S1 | 6 × 6 mm tact switch | Manual fire button. |
| PU (pickup) | 15 T, 0.5 mm wire, r = 10 mm | Field witness for the scope: M = 2.66 µH → 9.5 V rise + 41.9 V spike at center. |
| D4 | SMBJ24A TVS | Clamps the *supply input* at ~38 V (ESD / reverse-lead / bench transient). Protects the 50 V caps, the 555 rail, and the diode. |
| TB1 | 5.08 mm 2-pin terminal | External 24 V PSU input. |
| HDR | 2.54 mm pin headers | Scope test points + pickup output. |

## 2.4 555 monostable pin map (NE555P, DIP-8)

| Pin | Name | Connection |
|---|---|---|
| 1 | GND | F |
| 2 | TRIG | R2 → G; C3 → S1 → F |
| 3 | OUT | R3 → gate |
| 4 | RESET | G (always armed) |
| 5 | CTRL | C4 → F |
| 6 | THR | R1 → G; C2_TIM → F |
| 7 | DIS | tied to 6 |
| 8 | VCC | G (12 V) |

T = 1.1·R1·C2_TIM = 1.1 × 9700 × 10 nF = **106.7 µs**. The timing cap discharges
through the internal DIS transistor (< 0.3 µs) between pulses, so the circuit re-arms
instantly.

## 2.5 Switching sequence (what the scope shows)

1. **t < 0:** caps charged to 24 V (R_CHG), 555 output low, MOSFET off, coil idle.
2. **t = 0 (button):** 555 output → 10.5 V; gate charged in ~25 ns; MOSFET on.
   i(t) rises: di/dt(0) = V₀/L = 3.59 MA/s; shunt voltage rises 0 → 1.87 V;
   pickup shows 9.5 V; B builds to 104 mT.
3. **t = 104.2 µs:** i peaks at 186.5 A; v_C = 10.11 V.
4. **t = 106.7 µs (555 pulse ends):** MOSFET off; current transfers to D1 + R_FW in
   ~100 ns; drain clamps ≈ 17 V and falls to 11 V as i decays; shunt voltage → 0 V;
   pickup spikes to 41.9 V (15.8 MA/s); B collapses over τ_fw ≈ 11.9 µs.
5. **t ≈ 160 µs:** i < 5 mA; field gone; caps hold 10.11 V, recharging via R_CHG
   (full re-charge in ~0.35 s → 1 Hz operation is comfortable).

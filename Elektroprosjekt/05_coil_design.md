# 05 — Coil Design (transmitter + pickup)

## 5.1 Transmitter coil (COIL_T)

| Parameter | Value | Why |
|---|---|---|
| Turns N | 15 | Balance point of the N sweep (`03_calculations.md` §3.8) |
| Mean radius r | 15 mm (Ø30 mm, Ø31 mm with wire) | Fits the 80 mm board with cap bank around it; r sets B and L |
| Wire | 1.0 mm solid enameled Cu (17 AWG class) | Carries 187 A with 31 mΩ loss; thick enough to hand-solder; 1.02 mm close-wound pitch |
| Length l | 15.28 mm = (N−1)×1.02 + 1.0 | Close-wound: l ≈ r gives the best on-axis B for a short coil |
| L (design) | 6.69 µH (Wheeler: 6.93 µH) | §3.1 |
| R_coil | 30.96 mΩ (1.41 m of wire) | §3.0 |
| Former | 29 mm ID × ~18 mm, **non-conductive** tube (PVC, polyamide, or 3D-printed PLA) | **Critical:** a metal tube = shorted turn → eddy-current loss + field cancellation |
| Mounting | On 4 × M3 nylon standoffs (6 mm) above the PCB, glued with a drop of epoxy at the base | Keeps the coil axis centered; standoffs lift it above the ground pour |

### Winding procedure

1. Wind 15 turns on a 29–30 mm ID mandrel (a 30 mm plastic tube, a 30 mm dowel, or a
   20 mm pickup former + spacers), keeping turns evenly spaced (target pitch 1.02 mm —
   for close-wound, just keep the turns touching).
2. Leave a 60–80 mm lead at each end (strip 10 mm of enamel with a knife/soldering iron).
3. Slip the coil over (or onto) the 29 mm ID × 18 mm tube; check OD ≈ 31 mm, length
   ≈ 15.3 mm.
4. Solder the two leads to the COIL_T pads (see `07_pcb_layout.md`).

### Tolerance impact

| Error | Effect |
|---|---|
| ±1 turn (14–16) | L ∓ ~15 %, I_pk ± ~7 %, t_pk ∓ ~7 % — pulse stays correct |
| Pitch 0.9–1.2 mm (loose/tight winding) | L ± 10–20 % via the spacing terms; I_pk ∓ 5–9 % — acceptable |
| Wire 0.8 mm instead of 1.0 mm | R_coil 1.6× (50 mΩ) → ζ ≈ 0.40, I_pk ≈ 172 A (−8 %) — still fine |
| r = 13 mm (wound smaller) | L − ~15 %, B − ~10 % |

## 5.2 How to measure the coil inductance

Three practical methods (use at least two; they must agree within ~10 %):

1. **LCR meter at 1 kHz (best).** Expected: **6.7–6.9 µH**, ESR ≈ 31 mΩ. If the LCR
   meter only does 100 kHz, fine — the air-core coil's L is frequency-independent here.
2. **RC time-constant from the pulse itself (no extra equipment).** Short the coil
   through a known resistor R_k (e.g. 10 Ω) from a ~10 V supply, capture the current
   decay on the scope via a 0.1 Ω shunt: the decay constant is τ = L/R_k →
   L = τ·R_k. With R_k = 10 Ω, τ ≈ 0.67 ms — easy to measure. (Or the other direction:
   drive the coil with a square wave and measure the current rise time to 63 %.)
3. **From the pulse (post-build self-check).** Measure t_pk and I_pk on the real board:
   `L ≈ V₀/(I_pk·ωd·e^(ζω₀t_pk)/sin(ωd t_pk))` — or simply: t_pk ≈ 0.92·(1/ωd) for
   ζ ≈ 0.32, and I_pk ≈ 0.775·V₀/√(L·R·C)... practically: solve
   I_pk·t_pk ≈ 0.62·V₀/ω₀·... — the script `calculations.py` can be fed your measured
   I_pk/t_pk to back out L. Expected measured L: 6.5–7.2 µH (±10 %).

**Report target:** measured L = 6.7 µH ± 0.7 µH. If your LCR reading is < 5 µH or > 8 µH,
check winding (loose turns, shorted turns, wrong turn count).

## 5.3 Pickup coil (PU)

| Parameter | Value | Why |
|---|---|---|
| Turns | 15 | M = 2.66 µH at center → 41.9 V spike (clean scope reading, < 50 V) |
| Radius | 10 mm (Ø20 mm) | Fits the 30 mm bore with 5 mm clearance per side |
| Wire | 0.5 mm enameled Cu (32 AWG) | Carries only scope current (µA); small = stiff |
| Former | 18 mm OD × 16 mm tube (or wind around the transmitter's inner core) | Non-conductive |
| Mounting | Glued to a cross/spacer at the coil axis center; leads exit **along the axis** | A wire parallel to B picks up no EMF; axial leads = clean signal |

Winding: 15 close turns on an 18–20 mm mandrel (target pitch ~1.05 mm), 100–150 mm
leads, slip onto the former, position at the transmitter center. Solder leads to the
2-pin header (TP7/TP8).

**Verification:** M from the pulse = V_spike/di/dt. With di/dt = 15.76 MA/s (measured
from the shunt channel: 1.87 V / 0.01 Ω / (15.8 MA/s check)) and V_spike ≈ 41.9 V →
M ≈ 2.6 µH. If you get < 1 µH, the pickup is off-center or has too few turns.

## 5.4 Why not a different geometry (preview of experiment 2)

* **Flat spiral** (all 15 turns in a plane, Ø30 mm disc): L drops to ~2 µH, B at the
  center similar per ampere but the field is 2-D (strong only in the plane); good
  "pancake EMP" variant, easier victim coupling for flat PCBs.
* **More turns / longer** (N = 30, l ≈ 31 mm): field reaches further (B@50 mm 4.0 mT vs
  2.9 mT) but the spike halves (15.9 V) and I_pk drops to 115 A.
* **Fewer turns** (N = 8): 90 V pickup spike, 59 MA/s, 281 A — the "sharpest" variant;
  weaker sustained field (91 mT).

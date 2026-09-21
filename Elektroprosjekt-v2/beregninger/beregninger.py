# -*- coding: utf-8 -*-
# v2: EMB-generator — beregninger (single source of truth for alle tall)
import math
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=" * 64)
print("v2 EMB-GENERATOE — BEREKNINGER")
print("=" * 64)

# ----------------------------------------------------------------------
# 1. MARX GENERATOE (off-board)
# ----------------------------------------------------------------------
print("\n[1] MARX-GENERATOE (off-board)")
print("-" * 64)
N_STEG = 5                              # antall steg
C_S = 235e-6                            # F per steg (2x 470 uF/250 V i serie)
V_S = 1000.0                            # V per steg
V_UT = N_STEG * V_S                     # utgangsspenn (V)
C_UT = C_S / N_STEG                     # ekv. utgangskondensator (F)
E_UT = 0.5 * C_UT * V_UT**2             # lagret energi (J)
print(f"Steg: {N_STEG}, C_steg = {C_S*1e6:.0f} uF/{int(V_S)} V (2x 470 uF/250 V i serie)")
print(f"Utgang: V_out = {V_UT:.0f} V, C_out = {C_UT*1e6:.1f} uF, E = {E_UT:.1f} J")
print(f"E (kontroll N*x0.5*Cs*Vs^2) = {N_STEG*0.5*C_S*V_S**2:.1f} J")
print(f"E/v1 (0.2707 J) = {E_UT/0.2707:.0f}x mer energi")
# Lagring
R_LAD = 4700.0                          # ohm
C_LAD = C_UT                            # ekv. kondensator ved lagring
tau_lad = R_LAD * C_LAD                 # tau (s)
t_lad = 5 * tau_lad                     # full lagring (5 tau) (s)
I_LAD = V_UT / R_LAD                    # peak ladestrOm (A)
P_LAD = V_UT * I_LAD                    # peak lagringsmakht (W)
f_rep = 1.0 / t_lad                     # repetisjonsrate (Hz)
print(f"Lading: R = {int(R_LAD/1000)} kOhm, tau = {tau_lad*1000:.0f} ms, full lading = {int(t_lad)} s")
print(f"  Repetisjonsrate = {f_rep:.2f} Hz")
print(f"  I_lading (peak) = {I_LAD*1000:.0f} mA, P_lading (peak) = {P_LAD/1000:.0f} kW, E_lad = {E_UT:.1f} J")
V_TAP = V_UT / 5.0                      # HV-deler 5:1 for trigger (V)
print(f"  HV-tap for trigger (5:1) = {V_TAP:.0f} V")

# ----------------------------------------------------------------------
# 2. TRIGGER + ISKJEVING (off-board)
# ----------------------------------------------------------------------
print("\n[2] TRIGGER + ISKJEVING (off-board)")
print("-" * 64)
GAP_MM = 0.15                           # mm, kjedegap
V_BREAK_V = 3.0 * GAP_MM / 1000.0 * 1000.0 # V (breakdown, ~3 kV/mm -> 0.15 mm)
N_TRIGGER = 3
V_TRIGGER = 3000.0                      # V
t_GAP_NS = 50.0                         # ns, anslogstid
V_MARGIN = V_S / (V_BREAK_V)       # margin
print(f"Kjedegap = {GAP_MM} mm, breakdown \u2248 {V_BREAK_V:.0f} V")
print(f"Kjede-spens p\u00e5 hvert gap = {int(V_S)} V, margin = {V_MARGIN:.0f}x (\u2265 breakdown)")
print(f"Trigger: trigger-Maxx {N_TRIGGER} steg = {V_TRIGGER:.0f} V")
print(f"Anslag: t_gap = {t_GAP_NS:.0f} ns, kjede-lukking \u2248 {t_GAP_NS:.0f} ns (samtidig)")
print(f"V_s > V_breakdown -> alle gap lukker (kjede-lukking)")

# ----------------------------------------------------------------------
# 3. TEM CELLE (off-board, prim\u00e4r skadestruktur)
# ----------------------------------------------------------------------
print("\n[3] TEM-CELLE (off-board, prim\u00e4r skadestruktur)")
print("-" * 64)
L_CELL_MM = 300.0                       # mm, lengde
H_MM = 50.0                             # mm, gap (mellem platene) = 5 cm
W_MM = 50.0                             # mm, bredde (kvadrat -> Z0 \u2248 60 Ohm)
H_M = H_MM / 1000.0
W_M = W_MM / 1000.0
Z0 = 60.0                               # ohm
E_FELT = V_UT / H_M                     # V/m
V_PHONE = E_FELT * 0.08                 # V (8 cm telefon i feltretningen)
t_TRANSIT_NS = L_CELL_MM / 1000.0 / (3e8) * 1e9   # ns (gjennomk\u00f8r tid)
tau_RC = Z0 * C_UT                      # s (RC- tid)
t_FWHM = 0.69 * tau_RC                 # s (FWHM)
E_FELT_KV = E_FELT / 1000.0
print(f"TEM-celle: {int(L_CELL_MM)} cm lang, gap = {int(H_MM/10)} cm, bredde = {int(W_MM/10)} cm (kvadrat)")
print(f"Z0 \u2248 {Z0:.0f} Ohm")
print(f"E-felt = V_out/h = {E_FELT:.0f} V/m = {E_FELT_KV:.0f} kV/m")
print(f"  (>\u2265 10-30 kV/m t\u00e6rskhold -> skade) -> telefonen d\u00f8r")
print(f"Spennings over telefon (8 cm i feltretningen) = {int(V_PHONE)} V")
print(f"Gjennomk\u00f8r tid = L_cell/v_p = {t_TRANSIT_NS:.0f} ns")
print(f"RC- tid = Z0*C_out = {tau_RC*1e6:.0f} us ({tau_RC*1000:.1f} ms), FWHM \u2248 {t_FWHM*1e6:.0f} us ({t_FWHM*1000:.1f} ms)")
# di/dt (TEM-celle)
I_TM = V_UT / Z0                        # A (TEM-celle strOm)
DDT_TM = I_TM / (t_GAP_NS * 1e-9)       # A/s (di/dt)
print(f"I_peak (TEM-celle) = {I_TM:.1f} A")
print(f"di/dt (TEM-celle) = {DDT_TM/1e6:.0f} MA/s (vs v1 = 15.8 MA/s) -> {DDT_TM/15.8e6:.0f}x raskere")

# ----------------------------------------------------------------------
# 4. RADIERINGSPOLE (off-board)
# ----------------------------------------------------------------------
print("\n[4] RADIERINGSPOLE (off-board)")
print("-" * 64)
R_LOOP = 1.0                            # m (radius)
N_TURN = 10                             # antall omlapninger
A_WIRE = 6e-6                           # m^2 (6 mm^2)
L_WIRE = N_TURN * 2 * math.pi * R_LOOP  # m, ledningslengde
RHO_CU = 1.72e-8                         # ohm*m (kopper)
R_LOOP_VAL = RHO_CU * L_WIRE / A_WIRE    # ohm, spolemotstand
# Induktans (N-omlapninger, omlapt)
a = math.sqrt(A_WIRE / math.pi)          # m (ledningsrad)
L_LOOP = 4 * math.pi * 1e-7 * R_LOOP * (N_TURN**2) * (math.log(8 * R_LOOP / a) - 2)  # H
I_PEAK_LOOP = V_UT * (0.5 * t_FWHM) / L_LOOP  # A (omtrent)
DDT_LOOP = I_PEAK_LOOP / t_GAP_NS / 1e-9  # A/s (di/dt)
B_CENTER = 4 * math.pi * 1e-7 * N_TURN * I_PEAK_LOOP / (2 * R_LOOP)  # T
print(f"Spole: \u039c = {int(R_LOOP*1000)} mm, N = {N_TURN} omlapninger, ledning = {A_WIRE*1e6:.0f} mm^2")
print(f"R_loop = {R_LOOP_VAL*1000:.1f} mOhm, L_loop \u2248 {L_LOOP*1e6:.1f} uH")
print(f"I_peak (spole) \u2248 {I_PEAK_LOOP:.1f} A")
print(f"di/dt (spole) = {DDT_LOOP/1e6:.0f} MA/s")
print(f"B-felt i sentrum \u2248 {B_CENTER*1000:.2f} mT")
print("Fj\u00e6rfelt: E_far (avstand d) = (Z0 * I * omega * A * cos) / (2*pi*d) -- se 07_radieringspule.md")

# ----------------------------------------------------------------------
# 5. PULS EKSAMEN
# ----------------------------------------------------------------------
print("\n[5] PULS EKSAMEN")
print("-" * 64)
print(f"Puls: V = {V_UT:.0f} V, C = {C_UT*1e6:.1f} uF, E = {E_UT:.1f} J")
print(f"Felt = {E_FELT_KV:.0f} kV/m i TEM-celle, FWHM = {t_FWHM*1000:.1f} ms")
print(f"I_peak (TEM-celle) = {I_TM:.1f} A, di/dt = {DDT_TM/1e6:.0f} MA/s")
print(f"Repetisjonsrate = {f_rep:.2f} Hz (per {int(t_lad)} s)")
print("\nV1 vs V2:")
print(f"  Energi: 0.27 J -> {E_UT:.1f} J ({E_UT/0.27:.0f}x)")
print(f"  Spennings: 24 V -> {V_UT:.0f} V ({V_UT/24:.0f}x)")
print(f"  Felt: 9,5 V+41,9 V -> {int(V_PHONE)} V (\u2248 {V_PHONE/51:.0f}x mer)")
print(f"  di/dt: 15.8 MA/s -> {DDT_TM/1e6:.0f} MA/s ({DDT_TM/15.8e6:.0f}x)")
print(f"  Repetisjonsrate: 1 (single) -> {f_rep:.2f} Hz")
print(f"  Struktur: 31 mm spole -> {int(L_CELL_MM)} cm TEM-celle + {int(R_LOOP*1000)} mm pule")
print(f"  Impulsbredd: 104 us -> {t_FWHM*1000:.1f} ms")
print()
print("=" * 64)
print("V2 ER 'EXTREMELY DANGEROUS'")
print("=" * 64)
print(f"V2 produserer {E_UT:.0f} J til {V_UT:.0f} V, {E_FELT_KV:.0f} kV/m, di/dt {DDT_TM/1e6:.0f} MA/s")
print(f"Tem-cellen ({E_FELT_KV:.0f} kV/m) kan skade en telefon i det samme rommet")
print(f"Repetisjonsrate {f_rep:.2f} Hz, FWHM {t_FWHM*1000:.1f} ms, anslog {t_GAP_NS:.0f} ns")
print()

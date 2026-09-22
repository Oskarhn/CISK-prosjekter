# -*- coding: utf-8 -*-
"""
V3-HIGHPOWER EMP Generator — Korrigerte og realistiske beregninger
ADVARSEL: Alle 'maksimum' verdier er teoretiske. Reell ytelse vil være 30-70% lavere.
"""
import math
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def main():
    print("=" * 70)
    print("V3-HIGHPOWER EMP-GENERATOR — REALISTISKE BEREGNINGER")
    print("=" * 70)
    print("ADVARSEL: Dette er et høyspenningsprosjekt (8000V).")
    print("Feil konstruksjon kan føre til død eller alvorlig skade.")
    print("=" * 70)

    # ======================================================================
    # 1. MARX GENERATOR — KORRIGERT (Seriekobling, ikke parallell)
    # ======================================================================
    print("\n[1] MARX-GENERATOR (korrigert konfigurasjon)")
    print("-" * 70)
    
    N_STEG = 10
    C_PER_CAP = 150e-6      # 150 µF per kondensator
    V_CAP_RATING = 450.0    # 450V rating (IKKE 250V!)
    
    # KORREKSJON: To i SERIE gir C = C/2, V = 2×V_rating = 900V
    # Men vi lader til 800V for 11% sikkerhetsmargin
    C_S = C_PER_CAP / 2     # 75 µF per steg
    V_S = 800.0             # 800V per steg (sikkert under 900V max)
    
    V_UT = N_STEG * V_S     # 8000V total
    C_UT = C_S / N_STEG     # 7.5 µF
    E_UT = 0.5 * C_UT * V_UT**2  # 240 Joule
    
    print(f"Konfigurasjon: 2× {C_PER_CAP*1e6:.0f}µF/{V_CAP_RATING:.0f}V i SERIE")
    print(f"  Per steg: {C_S*1e6:.0f}µF @ {V_S:.0f}V")
    print(f"  (Maks tillatt: {2*V_CAP_RATING:.0f}V, margin: {(2*V_CAP_RATING-V_S)/V_S*100:.0f}%)")
    print(f"\nTotal utgang:")
    print(f"  Spenning: {V_UT/1000:.1f} kV")
    print(f"  Kapasitans: {C_UT*1e6:.1f} µF")
    print(f"  Energi: {E_UT:.0f} Joule")
    
    # Verifisering
    E_CHECK = N_STEG * 0.5 * C_S * V_S**2
    print(f"\nVerifisering: {E_CHECK:.0f} J = {E_UT:.0f} J ✓")
    
    # ======================================================================
    # 2. LADING — KORRIGERT (høyere R for lavere strøm)
    # ======================================================================
    print("\n[2] LADING (korrigert for sikkerhet)")
    print("-" * 70)
    
    R_LAD = 20000.0         # 20kΩ (økt fra 10kΩ for lavere strøm)
    tau_lad = R_LAD * C_UT  # 0.15s
    t_lad = 5 * tau_lad     # 0.75s (5τ = 99.3% ladet)
    
    I_PEAK = V_UT / R_LAD   # 0.4A
    P_PEAK = V_UT * I_PEAK  # 3200W
    P_AVG = E_UT / t_lad    # 320W
    
    print(f"Lademotstand: R = {R_LAD/1000:.0f} kΩ")
    print(f"Tidskonstant τ = {tau_lad*1000:.0f} ms")
    print(f"Full lading (5τ) = {t_lad:.2f} s")
    print(f"\nStrøm: I_peak = {I_PEAK:.2f} A")
    print(f"Effekt: P_peak = {P_PEAK/1000:.1f} kW, P_avg = {P_AVG:.0f} W")
    print(f"⚠️  KREVES: 50W wirewound resistor på kjøleribbe!")
    
    f_rep = 1.0 / t_lad
    print(f"\nMaks repetisjonsrate: {f_rep:.2f} Hz")
    
    # ======================================================================
    # 3. TRIGGER + ISKJÆRING — KORRIGERT
    # ======================================================================
    print("\n[3] TRIGGER + ISKJÆRING")
    print("-" * 70)
    
    GAP_MM = 0.28           # 0.28 mm (justert for 800V)
    E_BREAKDOWN = 3.0e6     # 3 MV/m (3 kV/mm i luft)
    V_BREAK = E_BREAKDOWN * (GAP_MM / 1000.0)  # ~840V
    
    print(f"Kjedegap: {GAP_MM} mm")
    print(f"Breakdown-spenning (teoretisk): {V_BREAK:.0f} V")
    print(f"Spenning per steg: {V_S:.0f} V")
    print(f"Margin: {V_S/V_BREAK:.2f}× (bør være 0.9-1.1×)")
    
    if V_S > V_BREAK * 0.95:
        print(f"  ⚠️  ADVARSEL: Margin er lav! Vurder å øke gap til 0.30mm")
    
    V_TRIGGER = 2400.0      # 3 steg × 800V
    t_GAP_NS = 10.0         # 10 ns (realistisk, ikke 5ns)
    
    print(f"\nTrigger: {V_TRIGGER:.0f} V (3 steg)")
    print(f"Anslagstid (estimat): ~{t_GAP_NS:.0f} ns")
    
    # ======================================================================
    # 4. TEM CELLE — MED REALISTISK DEMPNING
    # ======================================================================
    print("\n[4] TEM-CELLE (realistisk felt)")
    print("-" * 70)
    
    L_CELL_MM = 150.0       # 15 cm
    H_MM = 30.0             # 3 cm gap
    W_MM = 30.0             # 3 cm bredde
    Z0 = 60.0               # Karakteristisk impedans
    
    H_M = H_MM / 1000.0
    E_IDEAL = V_UT / H_M    # 267 kV/m (teoretisk maks)
    E_REAL = E_IDEAL * 0.6  # 40% tap (refleksjoner, geometri, matching)
    
    print(f"Dimensjoner: {L_CELL_MM/10:.0f} cm × {H_MM/10:.0f} cm × {W_MM/10:.0f} cm")
    print(f"Impedans Z₀ ≈ {Z0:.0f} Ω")
    print(f"\nE-felt:")
    print(f"  Teoretisk maksimum: {E_IDEAL/1000:.0f} kV/m")
    print(f"  Realistisk (60%): {E_REAL/1000:.0f} kV/m")
    print(f"  Usikkerhet: ±30% avhengig av konstruksjon")
    
    # Indusert spenning i ledning
    V_INDUCE_10CM = E_REAL * 0.10
    print(f"\nIndusert spenning i 10cm ledning: ~{V_INDUCE_10CM/1000:.1f} kV")
    
    # Transit-tid
    t_TRANSIT_NS = (L_CELL_MM / 1000.0) / 3e8 * 1e9
    print(f"Transit-tid (elektromagnetisk): {t_TRANSIT_NS:.2f} ns")
    
    # ======================================================================
    # 5. PEAKING CIRCUIT — MED USIKKERHETSMARGIN
    # ======================================================================
    print("\n[5] PEAKING CIRCUIT (med usikkerhet)")
    print("-" * 70)
    
    C_PEAK = 2e-9           # 2 nF
    L_STRAY = 100e-9        # 100 nH (konservativt, ikke 50nH)
    
    t_RISE_IDEAL = math.pi * math.sqrt(L_STRAY * C_PEAK)
    t_RISE_NS = t_RISE_IDEAL * 1e9
    t_RISE_REAL_NS = t_RISE_NS * 2  # 2× margin for usikkerhet
    
    print(f"Komponenter: C_peak = {C_PEAK*1e9:.0f}nF, L_stray ≈ {L_STRAY*1e9:.0f}nH")
    print(f"Rise time (ideal): {t_RISE_NS:.1f} ns")
    print(f"Rise time (realistisk): {t_RISE_REAL_NS:.0f} ns")
    print(f"\nBruker {t_RISE_REAL_NS:.0f}ns i videre beregninger")
    
    # Strøm i TEM-celle
    I_PEAK_TEM = V_UT / Z0
    di_dt_TEM = I_PEAK_TEM / (t_RISE_REAL_NS * 1e-9)
    
    print(f"\nTEM-celle strøm: I_peak = {I_PEAK_TEM:.0f} A")
    print(f"di/dt = {di_dt_TEM/1e9:.0f} GA/s (teoretisk)")
    
    # ======================================================================
    # 6. RADIERINGSSPOLE — REALISTISK
    # ======================================================================
    print("\n[6] RADIERINGSSPOLE (antenne)")
    print("-" * 70)
    
    R_LOOP = 0.5            # 50 cm radius
    N_TURN = 1              # 1 vinding (lavere L = høyere di/dt)
    A_WIRE = 6e-6           # 6 mm²
    
    # Induktans (Wheeler-formel for loop)
    L_LOOP = 4 * math.pi * 1e-7 * R_LOOP * (math.log(8*R_LOOP/math.sqrt(A_WIRE/math.pi)) - 2)
    
    # Peak strøm (energibevarelse)
    I_PEAK_LOOP = V_UT * math.sqrt(C_UT / L_LOOP)
    di_dt_LOOP = I_PEAK_LOOP / (t_RISE_REAL_NS * 1e-9)
    B_CENTER = 4 * math.pi * 1e-7 * I_PEAK_LOOP / (2 * R_LOOP)
    
    print(f"Spole: R = {R_LOOP*100:.0f} cm, N = {N_TURN} vinding")
    print(f"Induktans: L = {L_LOOP*1e6:.2f} µH")
    print(f"\nPeak strøm (teoretisk): I_peak = {I_PEAK_LOOP:.0f} A")
    print(f"di/dt (teoretisk): {di_dt_LOOP/1e9:.0f} GA/s")
    print(f"\nB-felt i sentrum: {B_CENTER*1000:.2f} mT")
    
    # Fjernfelt (estimat med stor usikkerhet)
    print(f"\nFjernfelt (ESTIMAT, stor usikkerhet):")
    print(f"  Ved 10m: ~1-3 kV/m (avhengig av antenneeffektivitet)")
    
    # ======================================================================
    # 7. SAMMENLIGNING — ÆRLIG
    # ======================================================================
    print("\n[7] SAMMENLIGNING (realistiske verdier)")
    print("-" * 70)
    print(f"{'Parameter':<20} {'V1':<12} {'V3-HP':<15} {'Forhold':<10}")
    print("-" * 70)
    print(f"{'Spenning':<20} {'24V':<12} {'8000V':<15} {'333×':<10}")
    print(f"{'Energi':<20} {'0.27J':<12} {'240J':<15} {'889×':<10}")
    print(f"{'E-felt (real)':<20} {'~1kV/m':<12} {'160kV/m':<15} {'160×':<10}")
    print(f"{'di/dt (est)':<20} {'~16MA/s':<12} {'{:.0f}GA/s'.format(di_dt_LOOP/1e9):<15} {'~4000×':<10}")
    
    print("\n" + "=" * 70)
    print("VIKTIGE BEGRENSNINGER:")
    print("• Alle 'maksimum' verdier er teoretiske")
    print("• Reell ytelse: 50-70% av beregnet (tap, usikkerhet)")
    print("• Rekkevidde: ESTIMERT 5-15m (IKKE verifisert)")
    print("• 8000V er DØDELIG — se 09_sikkerhet.md")
    print("=" * 70)

# KORREKSJON: main() definert FØR if __name__
if __name__ == "__main__":
    main()
    
    
    
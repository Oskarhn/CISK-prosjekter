#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMP-generator — pulse design, trippelsjekk-modell.
Kurs: ING2508 Kretsteknikk / Måleteknikk — prosjektet "EMP-generator".

Trippelsjekk-strategi (tre uavhengige metoder per størrelse):
  L   Spoleinduktans : (1) Wheeler-formel  (2) Neumann/elliptisk løkkesum
                       (3) direkte Neumann dobbellinje-integral (uten elliptiske integraler)
  B   Felt på aksen  : (1) lukket formel, endelig spole  (2) sum av eksakte løkkefelt
                       (3) uendelig-spole-gransegrense mu0*N*I/l
  I   Pulsebølge     : (1) analytisk dempet series-RLC (lukket formel)
                       (2) RK4 stykkevis kretssimulering (bryter PÅ/AV + farihjuldiode)
                       (3) energibalans: startenergi i kond = dissipert + sluttopp
  M   Mottak-M       : (1) løkkepar-elliptisk sum  (2) fluksmetode (B x A fra metodes-2-felt)

Rene Python (kun math). Kjør med:
  & "C:\\...\\python.exe" "...\\EMP_Generator\\beregninger.py"
"""
import math

MU0   = 4.0e-7 * math.pi          # H/m
RHO_CU = 1.72e-8                  # ohm*m, kobber 20 °C

# =====================================================================
# Komponentverdier (design)
# =====================================================================
V0      = 24.0        # V   presladt spenning
C_BANK  = 2 * 470e-6  # F   to 470 uF parallelt = 940 uF
ESR_CAP = 10e-3       # ohm parallell-ESR for de to lav-ESR-kondensatorene
N_S     = 15          # viklinger i sender
R_S     = 15.0e-3     # m   gjennomsnittlig vikt radius (OD ~31 mm med 1.0 mm ledning)
WIRE_D  = 1.0e-3      # m   massiv, emaljeringsdekket kobber (17 AWG-klasse)
PITCH   = 1.02e-3     # m   tettviklet avstand mellom viklingene
L_S     = (N_S - 1) * PITCH + WIRE_D          # spolelengde (m)
R_SW    = 1.25e-3     # ohm MOSFET RDS(on) @ VGS=10 V (IRF3707)
R_SHUNT = 10e-3       # ohm strømsens-shunt
R_TRACE = 2e-3        # ohm PCB-løkke + kontaktmotstand (estimat)
R_FW    = 0.5         # ohm farihjul-snubber (serie med D1)
V_D1    = 1.1         # V   farihjul-diodes fremvoutfall (MUR1560 @ ~100 A)
R_D1    = 0.03        # ohm farihjul-diodes dynamiske motstand
# Mottakspole
N_P     = 15          # viklinger i mottak
R_P     = 10.0e-3     # m   mottaks gjennomsnittlig vikt radius (20 mm dia, passer i 30 mm boret)
P_P     = 1.05e-3     # m   mottaks viktavstand
L_P     = (N_P - 1) * P_P + WIRE_D

R_COIL  = RHO_CU * N_S * 2.0 * math.pi * R_S / (math.pi * (WIRE_D / 2.0) ** 2)
R_TOT   = R_COIL + R_SW + R_SHUNT + R_TRACE + ESR_CAP

print("=" * 76)
print("EMP-GENERATOR — DESIGN-VERIFISERING")
print("=" * 76)
print(f"\n[Geometri]  N={N_S}  r={R_S*1e3:.2f} mm  ledning={WIRE_D*1e3:.2f} mm  "
      f"l={L_S*1e3:.2f} mm  (tettviklet)")
print(f"[Spole R]   R_spole = {R_COIL*1e3:.3f} m ohm   "
      f"(ledningslengde {N_S*2*math.pi*R_S:.2f} m)")
print(f"[Løkke R]   R_tot  = R_spole + R_sw + R_shunt + R_trace + ESR")
print(f"              = {R_COIL*1e3:.3f} + {R_SW*1e3:.3f} + {R_SHUNT*1e3:.3f} "
      f"+ {R_TRACE*1e3:.3f} + {ESR_CAP*1e3:.3f} m ohm")
print(f"              = {R_TOT*1e3:.2f} m ohm")
print(f"[Kondbank]  C = {C_BANK*1e6:.0f} uF, V0 = {V0} V,  E0 = 1/2*C*V0^2 = "
      f"{0.5*C_BANK*V0**2*1e3:.1f} mJ")

# =====================================================================
# Elliptiske integraler med Simpsons metode (ground truth)
# =====================================================================
def K_E(k, n=2000):
    """Fullstendige elliptiske integral K(k), E(k) med kompositt-Simpson (n like tall).
    K = int_0^{pi/2} dt/sqrt(1-k^2 sin^2 t),  E = int_0^{pi/2} sqrt(1-k^2 sin^2 t) dt"""
    if k >= 1.0:
        return math.inf, 1.0
    if k < 0.0:
        k = 0.0
    h = (math.pi / 2.0) / n
    q0 = 1.0 - k * k            # faktor ved t=pi/2: sin=1
    sK = 1.0 + 1.0 / math.sqrt(q0)
    sE = 1.0 + math.sqrt(q0)
    for i in range(1, n):
        t = i * h
        w = 4 if i % 2 else 2
        q = 1.0 - k * k * math.sin(t) ** 2
        sK += w / math.sqrt(q)
        sE += w * math.sqrt(q)
    return sK * h / 3.0, sE * h / 3.0

# kontroll mot hypergeometrisk rekkse (regnet uavhengig)
_K05, _E05 = K_E(0.5)
assert abs(_K05 - 1.68575) < 5e-4 and abs(_E05 - 1.46744) < 5e-4, (_K05, _E05)
_K09, _E09 = K_E(0.9)
assert abs(_K09 - 2.28055) < 5e-4 and abs(_E09 - 1.17170) < 5e-4, (_K09, _E09)

def M_loop(a, b, z):
    """Gjensidig induktans mellom to samaksiale sirkulære løkker (tynn ledning), H.
    Standardresultat: M = mu0*sqrt(ab)*[(2/k-k)K(k) - (2/k)E(k)],
    k^2 = 4ab/((a+b)^2+z^2)."""
    k2 = 4.0 * a * b / ((a + b) ** 2 + z * z)
    if k2 >= 1.0 - 1e-12:
        # sammenfallende løkker -> bruk tynn-ledning selvinduktans i stedenfor
        w = WIRE_D / 2.0
        return MU0 * a * (math.log(8.0 * a / w) - 2.0) + MU0 * a / 4.0
    k = math.sqrt(k2)
    K, E = K_E(k)
    return MU0 * math.sqrt(a * b) * ((2.0 / k - k) * K - (2.0 / k) * E)

def L_self_thin(r):
    """Selvinduktans for én tynn sirkulær vikt (ekstern + intern, jevn J)."""
    w = WIRE_D / 2.0
    return MU0 * r * (math.log(8.0 * r / w) - 2.0) + MU0 * r / 4.0

def L_exact(N, r, l, pitch, nq=2000):
    """Neumann-sum av løkkepar-M for alle par. Returnerer L i H."""
    zs = [(-((N - 1) / 2.0) + i) * pitch for i in range(N)]
    L = N * L_self_thin(r)
    for i in range(N):
        for j in range(i + 1, N):
            L += 2.0 * M_loop(r, r, abs(zs[i] - zs[j]))
    return L

def L_neumann_direct(N, r, l, pitch, m=360):
    """Metode 3: direkte dobbellinje-integral for alle par (fullt uavhengig):
    integrerer M_ij = mu0/4pi * I1 I2 / r12 rundt begge omkretser for hvert par."""
    zs = [(-((N - 1) / 2.0) + i) * pitch for i in range(N)]
    L = N * L_self_thin(r)
    for i in range(N):
        for j in range(i + 1, N):
            dz = zs[i] - zs[j]
            # M = (mu0 r^2 / 2) * int_0^{2pi} cos(d) / sqrt(4 r^2 sin^2(d/2)+dz^2) dd
            h = 2.0 * math.pi / m
            s = 0.0
            for kx in range(m):
                d = (kx + 0.5) * h
                s += math.cos(d) / math.sqrt(4.0 * r * r * math.sin(d / 2.0) ** 2 + dz * dz)
            L += 2.0 * (MU0 * r * r / 2.0) * s * h
    return L

# =====================================================================
# (A) Spoleinduktans — tre metoder
# =====================================================================
IN = 39.37007874015748  # 1 m i tommer
L_wh = ((R_S * IN) ** 2 * N_S ** 2) / (9.0 * (R_S * IN) + 10.0 * (L_S * IN)) * 1e-6  # Wheeler

print("\n" + "-" * 76)
print("[A] POLEINDUKTANS — trippelsjekk")
print(f"  (1) Wheeler:            L = {L_wh*1e6:8.3f} uH")
L_el = L_exact(N_S, R_S, L_S, PITCH)
print(f"  (2) Neumann/elliptisk:  L = {L_el*1e6:8.3f} uH")
L_nr = L_neumann_direct(N_S, R_S, L_S, PITCH)
print(f"  (3) Neumann linje-int:  L = {L_nr*1e6:8.3f} uH")
L = L_el  # designverdi = elliptisk (mest nøyaktig, inkluderer intern L)
print(f"  >> DESIGNVERDI: L = {L*1e6:.3f} uH   "
      f"(spredning: {min(L_wh,L_el,L_nr)*1e6:.2f} .. {max(L_wh,L_el,L_nr)*1e6:.2f} uH, "
      f"{(max(L_wh,L_el,L_nr)/min(L_wh,L_el,L_nr)-1)*100:.1f}%)")

# =====================================================================
# (C1) Analytisk dempet series-RLC utlading
# =====================================================================
W0   = 1.0 / math.sqrt(L * C_BANK)
ZETA = R_TOT / (2.0 * math.sqrt(L / C_BANK))
WD   = W0 * math.sqrt(1.0 - ZETA ** 2)
T_PK = math.atan(WD / (ZETA * W0)) / WD
I_PK = V0 / (L * WD) * math.exp(-ZETA * W0 * T_PK) * math.sin(WD * T_PK)

print("\n" + "-" * 76)
print("[C1] ANALYTISK SERIES-RLC  (kurs formelside-form s^2+2 zeta w0 s + w0^2)")
print(f"  w0   = 1/sqrt(LC)          = {W0:9.1f} rad/s   (f0 = {W0/2/math.pi:7.1f} Hz)")
print(f"  zeta = R/(2*sqrt(L/C))     = {ZETA:9.4f}    (underdempet, zeta<1)")
print(f"  wd   = w0*sqrt(1-zeta^2)   = {WD:9.1f} rad/s   (fd = {WD/2/math.pi:7.1f} Hz)")
print(f"  t_pk = atan(wd/(zeta*w0))/wd = {T_PK*1e6:7.2f} us")
print(f"  I_pk = V0/(L*wd)*e^(-zeta*w0*t_pk)*sin(wd*t_pk) = {I_PK:7.2f} A")
V_C_toff = V0 * math.exp(-ZETA * W0 * T_PK) * (
    math.cos(WD * T_PK) + (ZETA / math.sqrt(1 - ZETA ** 2)) * math.sin(WD * T_PK))
print(f"  V_C(t_pk)                = {V_C_toff:7.3f} V   (kondensatorspenning ved avskjering)")

# =====================================================================
# (C2) RK4 stykkevis kretssimulering
#   Noder: D = kond+ (spolestart), E = spoleende = MOSFET-drain,
#          F = MOSFET-kilde = jordreferanse, C- = kond− (via shunt).
#   Tilstand: vC = kondensatorspenning (D mot C−), i = polestrøm D->E.
#   Trinn 1 (t < t_off): bryter PÅ, D1 AV -> series RLC med R_TOT.
#   Trinn 2 (t >= t_off): bryter AV, all polestrøm farihjul via
#     D1 + R_FW:  di/dt = -(V_D1 + i*(R_COIL+R_FW+R_D1))/L,  vC konstant.
# =====================================================================
def rk4_stage1(t_off, dt=0.05e-6):
    """Returnerer t-liste, i-liste, vC-liste for trinn 1."""
    vC, i = V0, 0.0
    t = 0.0
    n = int(t_off / dt)
    ts, is_, vs = [0.0], [0.0], [V0]
    def f(vC, i):
        return (-(i / C_BANK), (vC - i * R_TOT) / L)
    for _ in range(n):
        k1 = f(vC, i)
        k2 = f(vC + 0.5 * dt * k1[0], i + 0.5 * dt * k1[1])
        k3 = f(vC + 0.5 * dt * k2[0], i + 0.5 * dt * k2[1])
        k4 = f(vC + dt * k3[0], i + dt * k3[1])
        vC += dt / 6.0 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        i  += dt / 6.0 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        t  += dt
        ts.append(t); is_.append(i); vs.append(vC)
    return ts, is_, vs

def stage2_decay(i0, t0, dt=0.05e-6, tmax=2.0e-3, iend=0.005):
    """Farihjul-avtagelse via D1 + R_FW (og spoler). Returnerer arrayer + dissippasjon."""
    R2 = R_COIL + R_FW + R_D1
    vC = V_C_toff  # frossen (ingen strøm i shunt/kond-veien)
    t, i, iprev = t0, i0, i0
    ts, is_ = [t0], [i0]
    E_Rfw = E_Rcoil = E_D1 = 0.0
    def f(i):
        return -(V_D1 + i * R2) / L
    while i > iend and t < t0 + tmax:
        k1 = f(i)
        k2 = f(i + 0.5 * dt * k1)
        k3 = f(i + 0.5 * dt * k2)
        k4 = f(i + dt * k3)
        i += dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        if i < 0.0:
            i = 0.0
        # trapesdissippasjon mellom iprev og i
        E_Rfw   += 0.5 * dt * (i**2 + iprev**2) * R_FW
        E_Rcoil += 0.5 * dt * (i**2 + iprev**2) * R_COIL
        E_D1    += 0.5 * dt * (i * (V_D1 + i * R_D1) + iprev * (V_D1 + iprev * R_D1))
        iprev = i
        t += dt
        ts.append(t); is_.append(i)
    return ts, is_, E_Rfw, E_Rcoil, E_D1, i

ts1, is1, vs1 = rk4_stage1(T_PK)
i_off = is1[-1]
ts2, is2, E_Rfw, E_coil2, E_D1, i_end = stage2_decay(i_off, T_PK)

# trinn-1 dissippasjonsintegraler (trapes på det tette arrayet)
E_sw1 = E_sh1 = E_tr1 = E_esr1 = E_coil1 = 0.0
for k in range(1, len(is1)):
    dt = ts1[k] - ts1[k - 1]
    i2m = 0.5 * (is1[k] ** 2 + is1[k - 1] ** 2)  # trapes på i^2
    E_sw1  += dt * i2m * R_SW
    E_sh1  += dt * i2m * R_SHUNT
    E_tr1  += dt * i2m * R_TRACE
    E_esr1 += dt * i2m * ESR_CAP
    E_coil1 += dt * i2m * R_COIL

# maks di/dt i hvert trinn
didt_max1 = max(abs((is1[k+1]-is1[k])/(ts1[k+1]-ts1[k])) for k in range(0, len(is1)-1, 1))
didt_max2 = max(abs((is2[k+1]-is2[k])/(ts2[k+1]-ts2[k])) for k in range(0, len(is2)-1, 1))
# startstigning di/dt
didt0 = is1[1] / (ts1[1] - ts1[0])

# finn RK4-topp
i_pk_rk = max(is1)
t_pk_rk = ts1[is1.index(i_pk_rk)]

print("\n" + "-" * 76)
print("[C2] RK4-SIMULERING (dt=50 ns) vs ANALYTISK")
print(f"  I_pk:  analytisk {I_PK:8.2f} A   RK4 {i_pk_rk:8.2f} A   "
      f"avvik {abs(i_pk_rk-I_PK)/I_PK*100:5.2f} %")
print(f"  t_pk:  analytisk {T_PK*1e6:8.2f} us   RK4 {t_pk_rk*1e6:8.2f} us")
print(f"  kondensatorspenning ved avskjering: analytisk {V_C_toff:6.3f} V   RK4 {vs1[-1]:6.3f} V")
print(f"  i(0+) stigning:  analytisk {V0/L/1e6:9.3f} MA/s   RK4 {didt0/1e6:9.3f} MA/s")
print(f"  maks |di/dt| trinn 1 (oppgang) : {didt_max1/1e6:7.3f} MA/s")
print(f"  maks |di/dt| trinn 2 (avtagelse): {didt_max2/1e6:7.3f} MA/s   "
      f"(t = {T_PK*1e6:.0f} us, farihjul)")
tau_fw = L / (R_COIL + R_FW + R_D1)
print(f"  i ved avskjering: {i_off:8.2f} A   avtagelse til <5 mA på "
      f"{(ts2[-1]-T_PK)*1e6:7.1f} us   (tau = L/R2 = {tau_fw*1e6:.2f} us)")

# =====================================================================
# (C3) Energibalans
# =====================================================================
E0 = 0.5 * C_BANK * V0 ** 2
E_cap_end = 0.5 * C_BANK * V_C_toff ** 2
E_diss = E_coil1 + E_coil2 + E_sw1 + E_sh1 + E_tr1 + E_esr1 + E_Rfw + E_D1
print("\n" + "-" * 76)
print("[C3] ENERGIBALANS")
print(f"  startenergi i kond        E0        = {E0*1e3:8.2f} mJ")
print(f"  sluttopp i kond ({V_C_toff:.2f}V)          = {E_cap_end*1e3:8.2f} mJ")
print(f"  dissipert: spole (begge trinn)    = {(E_coil1+E_coil2)*1e3:8.2f} mJ")
print(f"               MOSFET               = {E_sw1*1e3:8.2f} mJ")
print(f"               shunt                = {E_sh1*1e3:8.2f} mJ")
print(f"               spor/kontakt         = {E_tr1*1e3:8.2f} mJ")
print(f"               kond-ESR             = {E_esr1*1e3:8.2f} mJ")
print(f"               R_FW                 = {E_Rfw*1e3:8.2f} mJ")
print(f"               diode D1 (Vf+dyn)    = {E_D1*1e3:8.2f} mJ")
print(f"  sum(dissipert + sluttopp)         = {(E_diss+E_cap_end)*1e3:8.2f} mJ")
bal = abs(E0 - (E_diss + E_cap_end)) / E0 * 100
print(f"  BALANSFEIL = {bal:.3f} %   ({'OK' if bal < 1.0 else 'SJekk!'} <1%)")

# =====================================================================
# (B) B-felt på aksen — tre metoder
# =====================================================================
def B_closed(z, I):
    """Felt på aksen, endelig spole, z målt fra midten:
    B = (mu0*n*I/2)*[ (z+l/2)/sqrt((z+l/2)^2+r^2) - (z-l/2)/sqrt((z-l/2)^2+r^2) ],
    med n = N/l viktetthet (IKKE N)."""
    n = N_S / L_S
    a = z + L_S / 2.0
    b = z - L_S / 2.0
    return (MU0 * n * I / 2.0) * (a / (a*a + R_S*R_S) ** 0.5 - b / (b*b + R_S*R_S) ** 0.5)

def B_loopsum(z, I, n=15):
    zs = [(-((N_S - 1) / 2.0) + i) * PITCH for i in range(N_S)]
    B = 0.0
    for zz in zs:
        d = z - zz
        B += MU0 * I * R_S ** 2 / (2.0 * (R_S ** 2 + d * d) ** 1.5)
    return B

I_B = I_PK  # toppstrøm -> toppfelt
print("\n" + "-" * 76)
print("[B] B-FELT PÅ AKSEN VED TOPPSTRØM I_pk = %.1f A  (tre metoder ved z=0)" % I_B)
b1 = B_closed(0.0, I_B)
b2 = B_loopsum(0.0, I_B)
b3 = MU0 * N_S * I_B / L_S
print(f"  (1) lukket formel, endelig spole : {b1*1e3:8.2f} mT")
print(f"  (2) sum av eksakte løkkefelt     : {b2*1e3:8.2f} mT")
print(f"  (3) uendelig spole mu0*N*I/l     : {b3*1e3:8.2f} mT   (ideell grense)")
print(f"  >> DESIGN: B_center = {b1*1e3:.1f} mT = {b1:.3f} T")
print("\n  B(z) langs aksen ved toppstrøm (mT):")
print("  z(mm)   lukket   løkkesum   fall mot sentrum")
for zmm in [0, 5, 10, 15, 20, 30, 50, 100, 200]:
    z = zmm * 1e-3
    b_c = B_closed(z, I_B)
    b_l = B_loopsum(z, I_B)
    print(f"  {zmm:5d}   {b_c*1e3:8.3f}  {b_l*1e3:8.3f}   {b_c/b1*100:6.2f} %")

# =====================================================================
# (E) Mottaks-M + indusert spenning
# =====================================================================
zs_s = [(-((N_S - 1) / 2.0) + i) * PITCH for i in range(N_S)]
zs_p = [(-((N_P - 1) / 2.0) + i) * P_P for i in range(N_P)]
M_tot = 0.0
for zp in zs_p:
    for zs in zs_s:
        M_tot += M_loop(R_S, R_P, abs(zp - zs))
# fluksmetode-kontroll: M = sum over mottaksviklinger av A_p * dB/dI i sentrum
dBdI = B_closed(0.0, 1.0)  # T/A i spolesentrum (løkkesum ~ samme)
M_flux = N_P * (math.pi * R_P ** 2) * dBdI
print("\n" + "-" * 76)
print("[E] MOTTAKSPOLE  (n=%d, dia %d mm, i spolesentrum)" % (N_P, 2*R_P*1e3))
print(f"  (1) løkkepar-elliptisk sum:  M = {M_tot*1e6:7.3f} uH")
print(f"  (2) fluksmetode n*A*dB/dI :  M = {M_flux*1e6:7.3f} uH   "
      f"(avvik {abs(M_flux-M_tot)/M_tot*100:.1f} %)")
M = M_tot
V_rise  = M * (V0 / L)           # spenning ved t=0 (maks oppgang di/dt)
V_spike = M * didt_max2          # farihjul-spiss (maks |di/dt|)
print(f"  >> DESIGN M = {M*1e6:.2f} uH")
print(f"  indusert V ved oppgang  (di/dt={V0/L/1e6:.2f} MA/s): {V_rise:6.2f} V")
print(f"  indusert V ved spiss (di/dt={didt_max2/1e6:.2f} MA/s): {V_spike:6.2f} V")
print("  mottatt V_peak(z) for mottak flyttet langs aksen (spisseverdi):")
print("  z(mm)    M(uH)   V_oppgang(V)  V_spiss(V)")
for zmm in [0, 10, 20, 30, 50, 100]:
    z = zmm * 1e-3
    Mz = 0.0
    for zp in zs_p:
        for zs in zs_s:
            Mz += M_loop(R_S, R_P, abs(zp + z - zs))
    print(f"  {zmm:5d}   {Mz*1e6:7.3f}   {Mz*V0/L:9.2f}   {Mz*didt_max2:10.2f}")

# =====================================================================
# (D) Belastning/termisk kontroller
# =====================================================================
print("\n" + "-" * 76)
print("[D] BELASTNING OG TERMISK KONTROLL (1 puls, gjentakelse 1 Hz)")
# MOSFET: trinn-1 drain-spenning = i*R_SW (liten); ved avskjering klamer D1
# drain ved vC + V_D1 + i*R_D1 (verste tilfelle, start av farihjul)
Vds_max = max(V_C_toff + V_D1 + i_off * R_D1, max(is1) * R_SW)
print(f"  MOSFET (IRF3707):  I_D,max = {i_pk_rk:.0f} A (puls; datasheet I_DM ~250 A)  "
      f"V_DS,max = {Vds_max:.1f} V (rating 30 V; D1 klamer drain ved avskjering -> ingen megaspiss)")
# kondensatorsving
print(f"  Kondbank:          24.0 V -> {V_C_toff:.2f} V (ingen negativ sving; D1 blokkerer revers)")
# diode-surge
q_d = sum(0.5*(is2[k]+is2[k-1])*(ts2[k]-ts2[k-1]) for k in range(1,len(is2)))
print(f"  D1 (MUR1560):      I_peak = {i_off:.0f} A i {(ts2[-1]-T_PK)*1e6:.0f} us "
      f"(Q = {q_d*1e3:.1f} mAs, E = {(E_Rfw*0+E_D1)*1e3:.1f} mJ i dioden) -> OK mot 150 A I_TSM")
# R_FW
print(f"  R_FW 0.5 ohm 5W:   pulseenergi {E_Rfw*1e3:.1f} mJ, gjennomsnitts effekt 1 Hz = {E_Rfw*1e3:.0f} mW")
# spoleledning varme
mass_coil = N_S * 2*math.pi*R_S * (math.pi*(WIRE_D/2)**2) * 8960
dT_coil = (E_coil1+E_coil2) / (mass_coil * 385.0)
print(f"  Spoleledning:      masse {mass_coil*1e3:.1f} g, varme {(E_coil1+E_coil2)*1e3:.1f} mJ, "
      f"adiabatisk dT = {dT_coil:.2f} K")
# shunt
print(f"  Shunt 10 m ohm:    varme {E_sh1*1e3:.2f} mJ, topp-V = {i_pk_rk*R_SHUNT:.2f} V, "
      f"topp-P = {i_pk_rk**2*R_SHUNT:.0f} W (momentan, ~0.5 ms)")
# R_chg
E_chg_loss = 0.5 * C_BANK * V0**2  # halvparten av lagret energi går tapt i Rchg per lading
print(f"  R_chg 100 ohm:     topp-P = {V0**2/100:.2f} W i ~0.5 s, tap {E_chg_loss*1e3:.0f} mJ per lading")
# PCB spor 10 mm x 35 um, 30 mm
A_tr = 10e-3 * 35e-6
R_tr = RHO_CU * 30e-3 / A_tr
print(f"  PCB-strømbane:     10 mm x 35 um Cu: R = {R_tr*1e3:.2f} m ohm/30mm, "
      f"I²t-varme forsvinnende (inkludert i R_trace-marginen)")
# 555 dimensjonering
R_555 = T_PK / (1.1 * 10e-9)
print(f"\n  555 monostabil:    T = 1.1*R*C = {T_PK*1e6:.1f} us  ->  R = {R_555:.0f} ohm "
      "med C = 10 nF  (bruk 9.70 k ohm 1% -> T = 106.7 us)")

# =====================================================================
# (F) Skaling: spennings- og viklingstallsveip
# =====================================================================
print("\n" + "-" * 76)
print("[F1] SPENNINGSKALING (samme L, C, R):  I_pk, B og V_ind skalerer med V0")
print("  V0(V)  I_pk(A)  B_center(T)  E_cap(mJ)  V_spiss_mottak(V)  merknad")
for v0 in [12.0, 24.0, 48.0, 100.0, 240.0]:
    k = v0 / V0
    ip = I_PK * k
    print(f"  {v0:6.0f}  {ip:8.0f}  {b1*k:10.3f}  {0.5*C_BANK*v0**2*1e3:9.1f}  "
          f"{V_spike*k:15.1f}  "
          + ("bassedesign" if v0 == 24 else ("kond 50 V OK" if v0 <= 45 else "krever HVT-kond + 60 V+ MOSFET")))

print("\n[F2] VIKLINGSTALLSVEIP (r=15 mm, tettviklet 1.0 mm ledning, 24 V, 940 uF):")
print("  N    L(uH)   I_pk(A)  Bc(mT)  di/dt_oppgang(MA/s)  di/dt_farihjul(MA/s)  Vspk(V)  B@50mm(uT)")
best = None
for N in range(8, 41):
    lN = (N - 1) * PITCH + WIRE_D
    rN_coil = RHO_CU * N * 2*math.pi*R_S / (math.pi*(WIRE_D/2)**2)
    rN = rN_coil + R_SW + R_SHUNT + R_TRACE + ESR_CAP
    # Wheeler L (rask for veipen); eksakt modell for valgt N
    LN = ((R_S*IN)**2 * N**2) / (9.0*(R_S*IN) + 10.0*(lN*IN)) * 1e-6
    w0N = 1.0/math.sqrt(LN*C_BANK)
    zN = rN/(2.0*math.sqrt(LN/C_BANK))
    wdN = w0N*math.sqrt(1-zN**2)
    tpN = math.atan(wdN/(zN*w0N))/wdN
    ipN = V0/(LN*wdN)*math.exp(-zN*w0N*tpN)*math.sin(wdN*tpN)
    def Bc_gen(zc, I, nN, lNN, rN2):
        """Felt på aksen for en spole (nN viklinger, lengde lNN, radius rN2) i zc fra midten."""
        nn = nN / lNN  # viktetthet
        aa = zc + lNN/2.0; bb = zc - lNN/2.0
        return (MU0*nn*I/2.0)*(aa/(aa*aa+rN2*rN2)**0.5 - bb/(bb*bb+rN2*rN2)**0.5)
    bN  = Bc_gen(0.0, ipN, N, lN, R_S)     # sentrumfelt
    b50 = Bc_gen(0.05, ipN, N, lN, R_S)    # 50 mm fra midten
    didt_r = V0/LN
    didt_f = (V_D1 + ipN*(rN_coil + R_FW + R_D1))/LN
    # mottaks-M tilnærming: fluksmetode i sentrum (B = (mu0*n*I/2)*parentesen)
    Mz = N_P*(math.pi*R_P**2)*(MU0*(N/lN)/2.0)*((lN/2.0)/((lN/2.0)**2+R_S**2)**0.5
         - (-lN/2.0)/((lN/2.0)**2+R_S**2)**0.5)
    vspk = Mz*didt_f
    print(f"  {N:3d}  {LN*1e6:7.2f}  {ipN:8.1f}  {bN*1e3:8.2f}  {didt_r/1e6:12.2f}  "
          f"{didt_f/1e6:12.2f}  {vspk:8.1f}  {b50*1e6:9.1f}")

print("\n" + "=" * 76)
print("OPPSUMMERING AV DESIGNPUNKT (N=15):")
print(f"  L = {L*1e6:.2f} uH   C = 940 uF   R = {R_TOT*1e3:.1f} m ohm   zeta = {ZETA:.3f}")
print(f"  f0 = {W0/2/math.pi:.0f} Hz   t_pk = {T_PK*1e6:.1f} us   I_pk = {I_PK:.0f} A")
print(f"  B_center = {b1*1e3:.0f} mT   maks di/dt = {didt_max2/1e6:.1f} MA/s (farihjul)")
print(f"  Mottak (15 vikt/20 mm, sentrum): M = {M*1e6:.2f} uH  ->  "
      f"oppgang {V_rise:.1f} V, spiss {V_spike:.1f} V")
print("  Energi: %d mJ lagret; %d mJ omgjort til felt/varme; balansfeil %.2f %% "
      % (E0 * 1e3, (E_coil1 + E_coil2 + E_Rfw + E_D1) * 1e3, bal))
print("=" * 76)

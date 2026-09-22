# Teori for testversjonen – fullstendig RLC-analyse

## 1. Kretsbeskrivelse

Kretsen består av en kondensator C = 1000 µF som lades til V₀ = 9 V, og deretter kobles over en spole med induktans L ≈ 10 µH og total seriemotstand R ≈ 0,5 Ω (inkludert ledningsmotstand, spoleresistans og eventuell kontaktmotstand). Vi ser bort fra parasittiske kapasitanser.

## 2. Differensialligning og initialbetingelser

Etter at bryteren lukkes ved t = 0, gir Kirchhoffs spenningslov:

$$L \frac{di}{dt} + Ri + \frac{1}{C} \int_0^t i(\tau) d\tau - V_0 = 0$$

Deriveres for å eliminere integralet:

$$L \frac{d^2 i}{dt^2} + R \frac{di}{dt} + \frac{1}{C} i = 0 \quad \text{for } t > 0$$

Initialbetingelser:
- i(0) = 0 (strømmen kan ikke endres øyeblikkelig gjennom en spole)
- $\frac{di}{dt}(0) = \frac{V_0}{L}$ (spenningen over spolen ved t=0⁺ er V₀, fordi kondensatorspenningen fortsatt er V₀ og det ikke går strøm i motstanden)

## 3. Karakteristisk ligning og røtter

Vi antar løsning på formen $i(t) = A e^{st}$. Den karakteristiske ligningen blir:

$$L s^2 + R s + \frac{1}{C} = 0$$

$$s^2 + \frac{R}{L} s + \frac{1}{LC} = 0$$

Definer:
- Dempingskoeffisient: $\alpha = \frac{R}{2L} = \frac{0.5}{2 \cdot 10^{-5}} = 25\,000\ \text{s}^{-1}$
- Udempet egenfrekvens: $\omega_0 = \frac{1}{\sqrt{LC}} = \frac{1}{\sqrt{10^{-5} \cdot 10^{-3}}} = 10\,000\ \text{rad/s}$

Røttene er:

$$s_{1,2} = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2}$$

Med $\alpha^2 - \omega_0^2 = 6.25 \times 10^8 - 1 \times 10^8 = 5.25 \times 10^8\ \text{s}^{-2}$, får vi $\sqrt{\alpha^2 - \omega_0^2} = \sqrt{5.25 \times 10^8} \approx 22\,912.88\ \text{s}^{-1}$.

Altså:
- $s_1 = -25\,000 + 22\,912.88 = -2\,087.12\ \text{s}^{-1}$
- $s_2 = -25\,000 - 22\,912.88 = -47\,912.88\ \text{s}^{-1}$

Siden begge røttene er reelle og negative, er kretsen **overdempet**.

## 4. Tidsdomeneløsning

Generell løsning for overdempet tilfelle:

$$i(t) = A_1 e^{s_1 t} + A_2 e^{s_2 t}$$

Bruk initialbetingelsene:

1. i(0) = 0 ⇒ $A_1 + A_2 = 0$ ⇒ $A_2 = -A_1$
2. $\frac{di}{dt}(0) = A_1 s_1 + A_2 s_2 = \frac{V_0}{L}$

Sett inn $A_2 = -A_1$:

$$A_1 (s_1 - s_2) = \frac{V_0}{L} \Rightarrow A_1 = \frac{V_0}{L(s_1 - s_2)}$$

Dermed:

$$i(t) = \frac{V_0}{L(s_1 - s_2)} \left( e^{s_1 t} - e^{s_2 t} \right)$$

Siden $s_1 - s_2 = 2\sqrt{\alpha^2 - \omega_0^2} = 2\beta$, der $\beta = 22\,912.88\ \text{s}^{-1}$, kan vi skrive:

$$i(t) = \frac{V_0}{2L\beta} \left( e^{s_1 t} - e^{s_2 t} \right)$$

Med våre tall:

$$i(t) = \frac{9}{2 \cdot 10^{-5} \cdot 22\,912.88} \left( e^{-2\,087.12 t} - e^{-47\,912.88 t} \right) \approx 19.64 \left( e^{-2\,087.12 t} - e^{-47\,912.88 t} \right)\ \text{A}$$

(For å unngå forvirring: faktoren 19.64 er kun en mellomregning; den faktiske toppstrømmen finnes nedenfor.)

## 5. Toppstrøm og tid for toppstrøm

Toppstrømmen inntreffer når den deriverte er null:

$$\frac{di}{dt} = \frac{V_0}{2L\beta} \left( s_1 e^{s_1 t} - s_2 e^{s_2 t} \right) = 0$$

$$s_1 e^{s_1 t_{\text{peak}}} = s_2 e^{s_2 t_{\text{peak}}}$$

$$e^{(s_1 - s_2) t_{\text{peak}}} = \frac{s_2}{s_1}$$

$$t_{\text{peak}} = \frac{\ln(s_2/s_1)}{s_1 - s_2} = \frac{\ln(47\,912.88 / 2\,087.12)}{-45\,825.76} \approx \frac{\ln(22.95)}{-45\,825.76} \approx \frac{3.133}{-45\,825.76} \approx -6.84 \times 10^{-5}\ \text{s}$$

Fjerner fortegnsfeil (vi har byttet fortegn i nevneren): $t_{\text{peak}} = \frac{\ln(s_2/s_1)}{s_2 - s_1}$ gir positiv tid. Korrekt:

$$t_{\text{peak}} = \frac{\ln(s_2/s_1)}{s_2 - s_1} = \frac{3.133}{45\,825.76} \approx 6.84 \times 10^{-5}\ \text{s} = 68.4\ \mu\text{s}$$

Sett inn i strømutrykket:

$$I_{\text{peak}} = \frac{9}{2 \cdot 10^{-5} \cdot 22\,912.88} \left( e^{-2\,087.12 \cdot 68.4\times10^{-6}} - e^{-47\,912.88 \cdot 68.4\times10^{-6}} \right)$$

Beregn eksponentene:
- $e^{-0.1428} \approx 0.867$
- $e^{-3.277} \approx 0.0377$

$$I_{\text{peak}} \approx 19.64 \cdot (0.867 - 0.0377) \approx 19.64 \cdot 0.8293 \approx 16.3\ \text{A}$$

**Dette er et teoretisk estimat.** Målt strøm kan avvike betydelig på grunn av usikkerhet i R og L.

## 6. Oppførsel ved t = 0 og stasjonærtilstand

- Ved t = 0⁺: i = 0, di/dt = V₀/L = 9/10⁻⁵ = 900 000 A/s. Strømmen stiger altså ekstremt raskt i starten.
- Når t → ∞: i(t) → 0 fordi begge eksponentialledd går mot null. Kondensatoren er utladet.

## 7. Sensitivitet for komponentparametere

- Hvis R er lavere (f.eks. 0.3 Ω), kan kretsen bli underdempet. Da vil strømmen svinge.
- Hvis L er høyere (f.eks. 20 µH), øker dempingen og toppstrømmen reduseres.
- Kondensatorens kapasitans har mindre innvirkning på dempingen, men påvirker energien.

Uten nøyaktige målinger av R og L kan den faktiske responsen variere mye.

## 8. Begrensninger ved modellen

- Spolens induktans og motstand er ikke konstante; skin-effekt og nærhetseffekt kan endre dem under den raske pulsen.
- Kontaktmotstand i brytere og ledninger er variabel.
- Parasittisk kapasitans i spolen og ledningene kan påvirke responsen ved svært høye frekvenser.
- Modellen forutsetter ideelle komponenter uten ikke-lineariteter.

## 9. Konklusjon

Den matematiske modellen for testversjonen er konsistent og gir en overdempet respons med en teoretisk toppstrøm på ca. 16 A. For å verifisere modellen må R og L måles, og strømpulsen observeres med oscilloskop.

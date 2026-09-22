# Teori for testversjonen

## RLC-utladning – overdempet respons
Når kondensatoren ($C = 1000\,\mu\text{F}$) lades til $V_0 = 9\,\text{V}$ og deretter kobles over spolen ($L \approx 10\,\mu\text{H}$ for 10 vindinger, 5 cm diameter), dannes en serie RLC-krets. Med total motstand $R \approx 0.5\,\Omega$ (ledningsmotstand + spole) er kretsen **overdempet** fordi:

$$R > 2\sqrt{\frac{L}{C}}$$

$$2\sqrt{\frac{10\times10^{-6}}{1000\times10^{-6}}} = 2\sqrt{0.01} = 0.2\ \Omega$$

Siden $0.5\,\Omega > 0.2\,\Omega$, vil strømmen ikke svinge. Den karakteristiske ligningen har to reelle røtter:

$$s_{1,2} = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2}$$

der $\alpha = \frac{R}{2L} = \frac{0.5}{2\cdot10^{-5}} = 25\,000\ \text{s}^{-1}$ og $\omega_0 = \frac{1}{\sqrt{LC}} \approx 10\,000\ \text{rad/s}$.

Med $\beta = \sqrt{\alpha^2 - \omega_0^2} = \sqrt{25\,000^2 - 10\,000^2} \approx 22\,912.88\ \text{s}^{-1}$ får vi:

$$s_1 = -25\,000 + 22\,912.88 = -2\,087.12\ \text{s}^{-1}$$
$$s_2 = -25\,000 - 22\,912.88 = -47\,912.88\ \text{s}^{-1}$$

Strømmen er gitt av (med positiv retning fra kondensatorens plusspol gjennom spolen):

$$i(t) = \frac{V_0}{2L\beta} \left(e^{s_1 t} - e^{s_2 t}\right)$$

Toppstrømmen inntreffer ved $t_{\text{peak}} = \frac{\ln(s_2/s_1)}{s_1 - s_2} = \frac{\ln(47\,912.88/2\,087.12)}{45\,825.76} \approx 68.4\,\mu\text{s}$ og er:

$$I_{\text{peak}} = \frac{9}{2 \cdot 10^{-5} \cdot 22\,912.88} \left(e^{-2\,087.12 \cdot 68.4\times10^{-6}} - e^{-47\,912.88 \cdot 68.4\times10^{-6}}\right) \approx 16.3\ \text{A}$$

**Merk:** Dette er et teoretisk estimat basert på ideelle komponenter. Målt strøm kan avvike betydelig.

## Magnetfelt
For en sirkulær spole med $N=10$, radius $r=2.5\,\text{cm}$, og teoretisk toppstrøm $I=16.3\,\text{A}$:
$$B = \frac{\mu_0 N I}{2r} = \frac{4\pi\times10^{-7} \cdot 10 \cdot 16.3}{2 \cdot 0.025} \approx 4.1 \times 10^{-3}\,\text{T} = 4.1\,\text{mT}.$$

## Indusert spenning
Pickup-spolen (20 vindinger, radius 1.5 cm, areal $A \approx 7.1\times10^{-4}\,\text{m}^2$) plasseres 1 cm fra spolen. Feltet er estimert til $B \approx 1.5\,\text{mT}$ (avtar raskt med avstand). Stigetiden til strømmen er omtrent $t_{\text{peak}} \approx 68\,\mu\text{s}$.
$$\mathcal{E} = -N_p A \frac{\Delta B}{\Delta t} \approx -20 \cdot 7.1\times10^{-4} \cdot \frac{1.5\times10^{-3}}{68\times10^{-6}} \approx -0.31\,\text{V}.$$
Denne spenningen er fortsatt lavere enn en standard LEDs fremspenning (~1.8 V). Det er derfor **ikke sikkert** at LED-en vil blinke synlig. En LED-blinking er en hypotese som må testes. For pålitelig deteksjon anbefales oscilloskop.

## Pulsvarighet
Den dominerende tidskonstanten er $1/|s_1| \approx 479\,\mu\text{s}$. Den raske komponenten har tidskonstant $1/|s_2| \approx 20.9\,\mu\text{s}$. Pulsvarigheten (f.eks. bredden der strømmen er over 10% av toppverdien) krever numerisk løsning og er ikke beregnet her.

## Forventet pulsform på oscilloskop
Du vil se en enkel puls: en rask stigning (ca. 68 µs til toppen) etterfulgt av en langsommere eksponentiell nedgang.

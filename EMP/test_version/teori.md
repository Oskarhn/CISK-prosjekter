# Teori for testversjonen

## RLC-utladning – overdempet respons
Når kondensatoren ($C = 1000\,\mu\text{F}$) lades til $V_0 = 9\,\text{V}$ og deretter kobles over spolen ($L \approx 10\,\mu\text{H}$ for 10 vindinger, 5 cm diameter), dannes en serie RLC-krets. Med total motstand $R \approx 0.5\,\Omega$ (ledningsmotstand + spole) er kretsen **overdempet** fordi:

$$R > 2\sqrt{\frac{L}{C}}$$

$$2\sqrt{\frac{10\times10^{-6}}{1000\times10^{-6}}} = 2\sqrt{0.01} = 0.2\ \Omega$$

Siden $0.5\,\Omega > 0.2\,\Omega$, vil strømmen ikke svinge. Den karakteristiske ligningen har to reelle røtter:

$$s_{1,2} = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2}$$

der $\alpha = \frac{R}{2L} = \frac{0.5}{2\cdot10^{-5}} = 25\,000\ \text{s}^{-1}$ og $\omega_0 = \frac{1}{\sqrt{LC}} \approx 10\,000\ \text{rad/s}$.

Røttene blir:
$$s_1 \approx -2\,300\ \text{s}^{-1}, \quad s_2 \approx -47\,700\ \text{s}^{-1}$$

Strømmen er gitt av:
$$i(t) = \frac{V_0}{L(s_2 - s_1)} \left(e^{s_1 t} - e^{s_2 t}\right)$$

Med fortegnskonvensjon der positiv strøm går fra kondensatorens positive terminal gjennom spolen, gir dette en positiv strømpuls som starter på null, stiger til et maksimum, og avtar eksponentielt.

Toppstrømmen inntreffer ved $t_{\text{peak}} = \frac{\ln(s_2/s_1)}{s_1 - s_2} \approx 70\,\mu\text{s}$ og er omtrent:
$$I_{\text{peak}} \approx \frac{V_0}{L s_2} \approx 1.9\ \text{A}$$
(Dette er et teoretisk estimat, ikke en målt verdi.)

## Magnetfelt
For en sirkulær spole med $N=10$, radius $r=2.5\,\text{cm}$, og en antatt toppstrøm på $1.9\,\text{A}$:
$$B = \frac{\mu_0 N I}{2r} = \frac{4\pi\times10^{-7} \cdot 10 \cdot 1.9}{2 \cdot 0.025} \approx 4.8 \times 10^{-4}\,\text{T} = 0.48\,\text{mT}.$$

## Indusert spenning
Pickup-spolen (20 vindinger, radius 1.5 cm, areal $A \approx 7.1\times10^{-4}\,\text{m}^2$) plasseres 1 cm fra spolen. Feltet er ca. $B \approx 0.2\,\text{mT}$ (avtar raskt med avstand). Stigetiden til strømmen er omtrent $t_{\text{peak}} \approx 70\,\mu\text{s}$.
$$\mathcal{E} = -N_p A \frac{\Delta B}{\Delta t} \approx -20 \cdot 7.1\times10^{-4} \cdot \frac{0.2\times10^{-3}}{70\times10^{-6}} \approx -0.041\,\text{V}.$$
Denne spenningen er betydelig lavere enn en standard LEDs fremspenning (~1.8 V). Det er derfor **ikke sikkert** at LED-en vil blinke synlig. En LED-blinking er en hypotese som må testes. For pålitelig deteksjon anbefales oscilloskop.

## Pulsvarighet
Pulsvarigheten kan defineres på flere måter. Den dominerende tidskonstanten er $1/|s_1| \approx 435\,\mu\text{s}$, men den raske komponenten $1/|s_2| \approx 21\,\mu\text{s}$ bestemmer den initielle stigningen. En vanlig definisjon av pulsvarighet (f.eks. bredden der strømmen er over 10% av toppverdien) krever numerisk løsning og er ikke beregnet her.

## Forventet pulsform på oscilloskop
I stedet for en dempet sinus vil du se en enkel puls: en rask stigning etterfulgt av en langsommere eksponentiell nedgang.

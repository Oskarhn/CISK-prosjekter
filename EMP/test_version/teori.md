# Teori for testversjonen

## RLC-utladning – overdempet respons
Når kondensatoren (C = 1000 µF) lades til 9 V og deretter kobles over spolen (L ≈ 10 µH for 10 vindinger, 5 cm diameter), dannes en serie RLC-krets. Med total motstand R ≈ 0,5 Ω (ledningsmotstand + spole) er kretsen **overdempet** fordi:

$$R > 2\sqrt{\frac{L}{C}}$$

$$2\sqrt{\frac{10\times10^{-6}}{1000\times10^{-6}}} = 2\sqrt{0.01} = 0.2\ \Omega$$

Siden 0,5 Ω > 0,2 Ω, vil strømmen ikke svinge. I stedet får vi en enkel, ikke-oscillerende strømpuls som stiger raskt og deretter avtar eksponentielt. Den generelle løsningen for overdempet tilfelle er:

$$i(t) = \frac{V_0}{L(s_2 - s_1)} \left(e^{s_1 t} - e^{s_2 t}\right)$$

der $s_1$ og $s_2$ er de reelle røttene til den karakteristiske ligningen:

$$s_{1,2} = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2}$$

med $\alpha = R/(2L) = 0.5/(2\cdot10^{-5}) = 25\,000\ \text{s}^{-1}$ og $\omega_0 = 1/\sqrt{LC} \approx 10\,000\ \text{rad/s}$.

Toppstrømmen blir lavere enn i et underdempet tilfelle, typisk 1–2 A.

## Magnetfelt
For en sirkulær spole med $N=10$, radius $r=2.5\,\text{cm}$, strøm $I=1.5\,\text{A}$:
$$B = \frac{\mu_0 N I}{2r} = \frac{4\pi\times10^{-7} \cdot 10 \cdot 1.5}{2 \cdot 0.025} \approx 3.8 \times 10^{-4}\,\text{T} = 0.38\,\text{mT}.$$

## Indusert spenning
Pickup-spolen (20 vindinger, radius 1.5 cm, areal $A \approx 7.1\times10^{-4}\,\text{m}^2$) plasseres 1 cm fra spolen. Feltet er ca. $B \approx 0.15\,\text{mT}$ (avtar raskt). Stigetiden til strømmen er omtrent $1/\alpha \approx 40\,\mu\text{s}$.
$$\mathcal{E} = -N_p A \frac{\Delta B}{\Delta t} \approx -20 \cdot 7.1\times10^{-4} \cdot \frac{0.15\times10^{-3}}{40\times10^{-6}} \approx -0.053\,\text{V}.$$
Denne spenningen er lavere enn en standard LEDs fremspenning (~1.8 V). Det er derfor **ikke sikkert** at LED-en vil blinke synlig. En LED-blinking er en hypotese som må testes. For pålitelig deteksjon anbefales oscilloskop.

## Forventet pulsform på oscilloskop
I stedet for en dempet sinus vil du se en enkel puls: en rask stigning etterfulgt av en eksponentiell nedgang. Pulsens bredde er omtrent $2/\alpha \approx 80\,\mu\text{s}$.

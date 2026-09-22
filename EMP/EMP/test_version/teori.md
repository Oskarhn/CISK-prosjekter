# Teori for testversjonen

## RLC-utladning
Når kondensatoren (C = 1000 µF) lades til 9 V og deretter kobles over spolen (L ≈ 10 µH for 10 vindinger, 5 cm diameter), dannes en serie RLC-krets. Strømmen er gitt av:
$$i(t) = \frac{V_0}{\omega L} e^{-\alpha t} \sin(\omega t)$$
der $\omega = \sqrt{1/LC - \alpha^2}$, $\alpha = R/(2L)$.

Med $L \approx 10\,\mu\text{H}$, $C = 1000\,\mu\text{F}$, $R \approx 0.5\,\Omega$ (ledningsmotstand + spole):
- $\omega_0 = 1/\sqrt{LC} \approx 10\,000\,\text{rad/s}$ → $f \approx 1.6\,\text{kHz}$.
- $Z_0 = \sqrt{L/C} \approx 0.1\,\Omega$.
- Toppstrøm: $I_{\text{peak}} \approx V_0 / Z_0 = 9 / 0.1 = 90\,\text{A}$ (teoretisk). I praksis begrenser motstanden strømmen til ca. 2–5 A.

## Magnetfelt
For en sirkulær spole med $N=10$, radius $r=2.5\,\text{cm}$, strøm $I=2\,\text{A}$:
$$B = \frac{\mu_0 N I}{2r} = \frac{4\pi\times10^{-7} \cdot 10 \cdot 2}{2 \cdot 0.025} \approx 5.0 \times 10^{-4}\,\text{T} = 0.5\,\text{mT}.$$

## Indusert spenning
Pickup-spolen (20 vindinger, radius 1.5 cm, areal $A \approx 7.1\times10^{-4}\,\text{m}^2$) plasseres 1 cm fra spolen. Feltet er ca. $B \approx 0.2\,\text{mT}$ (avtar raskt). Stigetid $\Delta t \approx 50\,\mu\text{s}$.
$$\mathcal{E} = -N_p A \frac{\Delta B}{\Delta t} \approx -20 \cdot 7.1\times10^{-4} \cdot \frac{0.2\times10^{-3}}{50\times10^{-6}} \approx -0.057\,\text{V}.$$
Dette er nok til å lyse en LED svakt (LED trenger ~1.8 V, men pulsen er kort; i praksis kan spenningen være høyere pga. raskere stigetid). Med oscilloskop kan du se en tydelig puls.

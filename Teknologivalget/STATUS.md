# Tjenestestatus

Sist dokumentert: **10. august 2026** for spillservere. Medieserverdetaljer er fra **mars 2026**.

Statusen nedenfor er et historisk øyeblikksbilde, ikke en automatisk monitor.

| Tjeneste | Status | Endepunkt | Versjon |
|---|---|---|---|
| Minecraft – Optimalisert | 🟢 Online | `mc.sky-net.no:25567` | `26.2` |
| Minecraft – All The Mods 10 | 🟢 Online | `mc.sky-net.no:25568` | Minecraft `1.21.1`, modpack `7.3` |
| Minecraft – Cobbleverse | 🔴 Offline | `mc.sky-net.no:25572` | Minecraft `1.21.1`, modpack `1.7.42` |
| Terraria – Modded | 🟢 Online | `65.21.209.174:7779` | tModLoader `2026.06.3.4` |
| Jellyfin-stack | Historisk bekreftet oppsett | Ikke publisert | Docker-basert |
| Coolify | Evaluering | Ikke satt i produksjon i denne dokumentasjonen | Selvhostet PaaS |

## Tolkning av status

- 🟢 betyr at tjenesten var rapportert online ved siste manuelle oppdatering.
- 🔴 betyr at tjenesten var rapportert offline ved siste manuelle oppdatering.
- `Historisk bekreftet oppsett` betyr at installasjon og konfigurasjon er dokumentert, men at repositoryet ikke hevder sanntidsstatus.
- Kapasitetsstyring gjør at enkelte spillservere kan være stoppet selv om konfigurasjonen er driftsklar.

Kjør [`scripts/check-game-servers.sh`](scripts/check-game-servers.sh) for en enkel TCP-test fra en maskin med `nc`/netcat. En åpen port viser bare at noe svarer på TCP; den erstatter ikke en faktisk klienttest.


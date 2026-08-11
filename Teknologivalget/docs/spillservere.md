# Spillservere

## Status 10. august 2026

| Server | Status | Adresse | Serverversjon |
|---|---|---|---|
| Minecraft – Optimalisert | 🟢 Online | `mc.sky-net.no:25567` | `26.2` |
| Minecraft – All The Mods 10 | 🟢 Online | `mc.sky-net.no:25568` | Minecraft `1.21.1`, modpack `7.3` |
| Minecraft – Cobbleverse | 🔴 Offline | `mc.sky-net.no:25572` | Minecraft `1.21.1`, modpack `1.7.42` |
| Terraria – Modded | 🟢 Online | `65.21.209.174:7779` | tModLoader `2026.06.3.4` |

Vanilla Terraria inngår ikke i oversikten fordi det ikke fantes en slik aktiv tjeneste.

## Klientkrav

### Minecraft – Optimalisert

Vanilla-basert/optimalisert instans. Klient og server må bruke kompatibel versjon `26.2` slik den var oppgitt i serveroversikten.

### All The Mods 10

Klienten må bruke Minecraft `1.21.1` og modpack-versjon `7.3`. Serveren inneholder tillegg utover en ren vanilla-installasjon, og klientpakken må derfor være riktig installert før tilkobling.

### Cobbleverse

Klienten må bruke Minecraft `1.21.1` og modpack-versjon `1.7.42`. Tjenesten var oppdatert, men markert offline i siste status.

### Terraria – Modded

Serveren bruker tModLoader `2026.06.3.4`. Den dokumenterte modlisten omfatter:

- Fargo's Souls Mod
- Fargo's Mutant Mod
- Luminance
- Calamity Mod
- Calamity Mod Music
- Recipe Browser
- Boss Checklist
- Boss Cursor
- Town NPC Checklist
- SerousCommonLib
- Magic Storage
- Smarter Cursor
- Loot Beams
- Better Blending
- ItemMagnetPlus

Klientens tModLoader- og modversjoner må samsvare med serveren.

## Ressursstyring

Ikke alle instansene kjører nødvendigvis samtidig. Dette er et bevisst valg for å prioritere CPU og RAM til serverne som faktisk brukes.

En server som er offline kan derfor være:

- stoppet for å frigjøre ressurser
- under oppdatering
- midlertidig ute av drift
- klar til å startes ved forespørsel

Statusmeldingen til brukerne må skille disse årsakene når det er relevant.

## Oppdateringsarbeid

En modpack-oppdatering omfatter mer enn å bytte versjonsnummer:

1. bekreft ønsket server- og klientversjon
2. ta backup av world, config og modliste
3. stopp instansen kontrollert
4. oppdater serverpakken og eventuelle tillegg
5. start med loggobservasjon
6. kontroller world load og mod-feil
7. test med riktig klient
8. oppdater Discord-oversikten

ATM10 og Cobbleverse var ferdig oppdatert ved statusoppdateringen 10. august 2026.

## Historiske tjenester

Satisfactory har vært nevnt som et tidligere serverområde, men aktiv adresse, versjon og produksjonsstatus er ikke dokumentert i dette repositoryet. Den står derfor ikke i den aktive statusoversikten.


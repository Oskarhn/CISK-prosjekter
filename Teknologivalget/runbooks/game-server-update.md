# Runbook: spillserveroppdatering

## Omfang

Prosedyren gjelder Minecraft- og Terraria-instanser med mods eller modpacks.

## Før endring

1. Bekreft eksakt server-, loader- og modpack-versjon.
2. Last ned fra prosjektets offisielle kanal.
3. Les changelog for world migration, fjernede mods og nye dependencies.
4. Varsle brukere og stopp nye innlogginger.
5. Kjør save/flush og stopp serveren kontrollert.
6. Ta kopi av world, config, modliste og startparametre.

## Test

1. Oppdater en kopi eller staging-instans når risikoen er høy.
2. Følg loggen fra første linje.
3. Kontroller at world åpnes uten manglende registry-objekter.
4. Koble til med klienten og riktig modpack.
5. Test bevegelse, inventories, chunks og sentrale mods/plugins.
6. Kontroller RAM, CPU og disk-I/O.

## Produksjon

1. Flytt kontrollert versjon til produksjon.
2. Start og gjenta smoke test.
3. Publiser adresse, Minecraft/tModLoader-versjon og modpack-versjon.
4. Behold pre-update-backup til oppdateringen er stabil.

## Rollback-kriterier

- world kan ikke lastes
- klienter får systematisk version/mod mismatch
- sentrale mods mangler data
- crash loop eller ukontrollert minnebruk
- alvorlig lag som ikke fantes før oppdatering


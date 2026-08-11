# Prosjekthistorikk

## 2026-03-04 – serveransvar og plattformvalg

Ansvar for en server til Teknologiutvalget ble etablert. En Seagate Barracuda 8 TB var tilgjengelig for lagring, og Proxmox ble vurdert som hypervisor.

## 2026-03-07 – medieserver og Docker-storage

HP ProDesk 600 G4 med Ubuntu og NVMe ble dokumentert. Root brukte omtrent 100 GB av LVM-oppsettet, og et logical volume på omtrent 688 GB ble montert på `/dockerdata`.

Jellyfin brukte separate mapper for config, cache og media. Prowlarr-containeren ble startet, og Jellyseerr ble koblet til Jellyfin.

## 2026-03-22 – utvidelse med 5 TB-disk

En 5 TB HDD ble formatert med ext4, montert på `/media/storage` og lagt inn i `/etc/fstab`. Mappestruktur for `movies`, `series` og `downloads` ble opprettet eller planlagt.

## 2026 – spillserverdrift

Minecraft- og Terraria-instanser ble driftet med forskjellige versjoner og modpacks. Ressursbruk ble styrt ved at ikke alle tjenester nødvendigvis kjørte samtidig.

## 2026-08-10 – samlet brukerstatus

Serveroversikten ble oppdatert med:

- Minecraft Optimalisert `26.2` online
- All The Mods 10 `1.21.1` / `7.3` online
- Cobbleverse `1.21.1` / `1.7.42` offline
- Terraria tModLoader `2026.06.3.4` online

ATM10 og Cobbleverse var ferdig oppdatert. Vanilla Terraria ble fjernet fra oversikten fordi tjenesten ikke fantes.

## 2026-08-11 – dokumentasjon og plattformresearch

Arbeidet ble samlet i et offentlig portfolio-repository. Coolify-materiale ble gjennomgått med fokus på Git-basert deployment, Docker, TLS, persistent storage, remote servers og driftsansvar. Rå tredjepartstranskripsjoner ble holdt utenfor repositoryet.


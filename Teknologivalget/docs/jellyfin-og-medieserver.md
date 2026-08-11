# Jellyfin og medieserver

## Bekreftet oppsett

Medieserveren ble satt opp på en HP ProDesk 600 G4 med Ubuntu og Docker.

| Komponent | Dokumentert verdi |
|---|---|
| Systemdisk | NVMe, ca. `931.5 GB` |
| Root logical volume | ca. `100 GB` |
| Ledig plass i volume group ved oppsett | ca. `828 GB` |
| Logical volume for Docker-data | ca. `688 GB`, montert på `/dockerdata` |
| Mediedisk | `5 TB` HDD, ext4 |
| Mediediskens mount point | `/media/storage` via `/etc/fstab` |
| Containerplattform | Docker / Docker Compose |

Disk-UUID og andre maskinspesifikke identifiers er utelatt fra det offentlige repositoryet.

## Mappestruktur

Det første dokumenterte Jellyfin-oppsettet brukte:

```text
/dockerdata/jellyfin/
├── cache/
├── config/
└── media/
```

Jellyfin-containeren kunne lese filmområdet som `/media/movies`.

Etter at 5 TB-disken ble lagt til, ble lagringsstrukturen planlagt rundt:

```text
/media/storage/
├── downloads/
├── movies/
└── series/
```

`config` og annen liten, viktig applikasjonsdata passer på NVMe/LVM. Store mediefiler passer på HDD. Cache kan regenereres og trenger normalt ikke samme backup-prioritet.

## Tjenester

| Tjeneste | Dokumentert status | Rolle |
|---|---|---|
| Jellyfin | Konfigurert | Media library og streaming |
| Jellyseerr | Koblet til Jellyfin med API key | Forespørsler og brukerflyt |
| Prowlarr | Container startet | Felles administrasjon av indexers |
| Radarr | Vurdert, ikke bekreftet ferdig | Film-automatisering |
| Sonarr | Vurdert, ikke bekreftet ferdig | Serie-automatisering |
| Bazarr | Vurdert | Undertekster |
| qBittorrent / SABnzbd | Vurdert | Downloader |
| Gluetun | Vurdert | VPN isolation for downloader |

## Volumes og permissions

Den viktigste egenskapen er at data ligger på hosten. Containerne skal bare få tilgang til mappene de trenger.

Sikre kontroller som kan kjøres uten å endre systemet:

```bash
lsblk -f
findmnt /dockerdata
findmnt /media/storage
df -h /dockerdata /media/storage
stat /dockerdata/jellyfin/config /media/storage
docker compose ps
docker compose logs --tail=100 jellyfin
```

UID/GID må være konsistente mellom containers som skal lese og skrive de samme filene. Brede rettigheter som `chmod -R 777` skjuler problemet og skal unngås.

## Integrasjoner

Jellyseerr ble koblet til Jellyfin med en API key. Nøkkelen skal ligge som secret eller environment variable utenfor Git. Dersom en nøkkel har vært vist i terminalhistorikk, skjermbilde eller commit, skal den roteres.

Prowlarr startet som egen container. Før Radarr/Sonarr kobles til må URL-er, container-nettverk, paths og API keys være konsistente. `localhost` inne i en container peker på containeren selv, ikke automatisk på en annen container eller hosten.

## Drift

Før en containeroppdatering:

1. noter nåværende image tag og status
2. ta backup av `config`
3. kontroller ledig diskplass
4. hent nytt image
5. recreat containeren uten å slette volumes
6. test bibliotek, avspilling og integrasjoner
7. kontroller logs for permission- eller path-feil

## Backup-prioritet

1. Jellyfin-konfigurasjon og metadata
2. Jellyseerr- og Prowlarr-konfigurasjon
3. Compose-fil og sanitisert oversikt over environment variables
4. eventuelle databaser i stacken
5. media etter verdi og hvor enkelt det kan erstattes
6. cache trenger normalt ikke backup

Se [backup og gjenoppretting](backup-og-gjenoppretting.md) og [storage-runbook](../runbooks/storage.md).


# Jellyfin og media-stack

## Runtime

- Ubuntu på HP ProDesk 600 G4
- Docker / Docker Compose
- persistent data under `/dockerdata`
- separat 5 TB mediedisk på `/media/storage`

## Bekreftede komponenter

```text
Jellyseerr --API--> Jellyfin
Prowlarr  --container startet
Jellyfin  --media--> /media/movies
```

API key er ikke lagret i repositoryet.

## Data

```text
/dockerdata/jellyfin/config
/dockerdata/jellyfin/cache
/dockerdata/jellyfin/media
/media/storage/movies
/media/storage/series
/media/storage/downloads
```

De to siste delene representerer utviklingen fra opprinnelig NVMe/LVM-lagring til en egen stor mediedisk. Faktiske container-mounts skal alltid kontrolleres mot gjeldende Compose-fil før en migrering.

## Safe checks

```bash
findmnt /dockerdata /media/storage
df -h /dockerdata /media/storage
docker compose ps
docker compose logs --tail=100 jellyfin
```

Se [full dokumentasjon](../../docs/jellyfin-og-medieserver.md).


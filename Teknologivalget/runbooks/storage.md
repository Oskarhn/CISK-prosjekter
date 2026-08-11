# Runbook: storage og disk full

## Symptomer

- container kan ikke skrive eller restarter
- databasefeil eller korrupte midlertidige filer
- Jellyfin mister bibliotek når et mount mangler
- spillserver klarer ikke lagre world
- Docker build feiler med `no space left on device`

## Kontroller

```bash
df -h
df -i
lsblk -f
findmnt
docker system df
sudo du -xhd1 /var/lib/docker 2>/dev/null | sort -h
sudo du -xhd1 /dockerdata 2>/dev/null | sort -h
sudo du -xhd1 /media/storage 2>/dev/null | sort -h
```

`du` kan bruke tid på store filsystemer. Kjør det målrettet.

## Trygg respons

1. Stopp unødvendige writes dersom filsystemet er kritisk fullt.
2. Bekreft at alle forventede disker faktisk er montert.
3. Finn hvilken kategori som vokser: logs, cache, images, downloads, world eller database.
4. Roter eller komprimer logs med systemets normale mekanisme.
5. Fjern bare cache/build-artefakter som er dokumentert regenererbare.
6. Flytt eller utvid data kontrollert dersom problemet er reell kapasitet.
7. Start tjenestene én om gangen og test skriving.

## Ikke gjør

- ikke slett ukjente Docker volumes
- ikke kjør aggressiv `docker system prune -a --volumes` på en produksjonshost
- ikke slett world- eller databasefiler for å frigjøre plass
- ikke start Jellyfin dersom `/media/storage` skulle vært montert, men ikke er det
- ikke anta at en snapshot er en ekstern backup

## Etter hendelsen

- dokumenter rotårsak
- legg inn varsling før samme terskel
- juster retention eller kapasitet
- verifiser siste backup og tjenestens data


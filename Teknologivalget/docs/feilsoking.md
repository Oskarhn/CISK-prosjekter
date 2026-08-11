# Feilsøking

## Metode

Feilsøking gjøres fra nederste avhengighet og oppover:

1. host og ressurser
2. storage og permissions
3. container/prosess
4. lokal port og tjenestelogger
5. firewall/NAT/DNS
6. klientversjon og applikasjonsflyt

Å endre flere lag samtidig gjør det vanskelig å vite hva som faktisk løste feilen.

## Første kontroller på Linux/Docker

```bash
uptime
free -h
df -h
df -i
lsblk -f
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker compose ps
docker compose logs --tail=200
ss -lntup
```

Kommandoene er i hovedsak read-only. Vurder logginnhold før det deles offentlig.

## Tjenesten kjører, men er ikke tilgjengelig

Kontroller i denne rekkefølgen:

- lytter prosessen på forventet port?
- er porten bundet til riktig interface?
- svarer den fra samme host?
- blokkerer host firewall?
- peker NAT/port-forwarding til riktig intern adresse?
- peker DNS til riktig offentlig adresse?
- bruker klienten riktig port og protokoll?

## Container starter ikke

Vanlige årsaker:

- ugyldig environment variable
- image tag finnes ikke
- path mangler på hosten
- feil UID/GID eller permissions
- porten er allerede i bruk
- disk eller inode-tabell er full
- database eller annen dependency er ikke klar

Les først containerens exit code og de siste logglinjene. Ikke slett volumes som et generelt feilsøkingstiltak.

## Jellyfin ser ikke media

- kontroller at host-path finnes og er montert
- sammenlign bind mount med pathen Jellyfin bruker inne i containeren
- kontroller execute-bit på parent directories og read-permission på filer
- test med containerens faktiske UID/GID
- kontroller at 5 TB-disken er montert; en tom mount directory kan ellers se ut som «manglende bibliotek»

## Modpack-server feiler etter oppdatering

- sammenlign server- og klientversjon
- les første egentlige exception, ikke bare siste følgefeil
- kontroller manglende dependencies og loader-versjon
- test med backupkopi av world
- rollback serverpakke og config dersom world-formatet tillater det
- publiser kjent feil før flere brukere forsøker tilfeldige klientendringer

## Disk full

Følg [`../runbooks/storage.md`](../runbooks/storage.md). Ikke slett world-data, databaser eller ukjente Docker volumes for å frigjøre plass raskt.


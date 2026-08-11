# Videre arbeid

Oppgavene er rangert etter hva som gir størst driftsverdi og dokumenterbarhet.

## Prioritet 1 – inventar og gjenoppretting

- dokumenter faktisk host-/VM-/LXC-inventar internt
- registrer CPU, RAM, storage, autostart og owner per tjeneste
- etabler datert backup-jobb for world-data og applikasjonsconfig
- gjennomfør og dokumenter en full restore-test
- legg inn SMART- og diskplassvarsling

## Prioritet 2 – standardisert drift

- bruk eksplisitte image- og modpack-versjoner
- opprett vedlikeholdsvindu og enkel change log
- automatiser read-only health checks
- dokumenter rollback per spillserver
- samle sanitiserte service-definisjoner når de er kontrollert mot produksjon

## Prioritet 3 – plattformpilot

- opprett isolert Coolify test-VM
- deploy en ufarlig demoapp fra Git
- test custom domain, TLS, secret-håndtering og logs
- test databasebackup og restore
- mål CPU/RAM/disk under build
- gjennomfør en sikkerhetsgjennomgang før produksjonsbruk

## Prioritet 4 – forbedret nettverk

- dokumenter trust boundaries og management-tilgang internt
- begrens offentlig eksponerte porter
- vurder VPN for administrasjon
- bruk tjenestenavn og subdomains konsekvent
- vurder overvåking fra en separat host

## Ferdigkriterium

En oppgave er ikke ferdig bare fordi tjenesten starter. Den er ferdig når konfigurasjon, data, tilgang, monitoring, backup, restore og brukerkommunikasjon er kontrollert.


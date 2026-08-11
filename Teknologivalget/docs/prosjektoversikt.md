# Prosjektoversikt

## Bakgrunn

Teknologiutvalget hadde behov for en plattform som kunne brukes til spillservere, interne tjenester og selvhostede applikasjoner. Arbeidet har bestått av både praktisk drift og vurdering av hvordan tjenestene bør isoleres, lagres og gjøres tilgjengelige.

Det har vært to konkrete driftsområder:

1. spillservere for studenter og andre brukere
2. en egen Docker-basert medieserver med Jellyfin og relaterte tjenester

I tillegg er Proxmox og Coolify undersøkt som byggesteiner for en mer samlet plattform.

## Mitt ansvar

Arbeidet som er dokumentert i repositoryet omfatter:

- Linux-administrasjon og bruk av SSH
- oppsett og drift av Docker-tjenester
- partisjonering, LVM, ext4 og permanente mounts
- tjenesteintegrasjon gjennom API key uten å publisere nøkkelen
- versjons- og statusoversikt for spillservere
- oppdatering av modpacks og klientkrav
- brukerinformasjon i Discord
- vurdering av virtualisering, `deployment` og service isolation
- dokumentasjon, runbooks og sikker publisering

## Konkrete leveranser

### Medieserver

En HP ProDesk 600 G4 ble satt opp med Ubuntu, en NVMe-disk på omtrent 1 TB og Docker. Root-filsystemet brukte en mindre del av en LVM volume group, mens omtrent 688 GB ble satt av til `/dockerdata`. Jellyfin fikk egne mapper for `config`, `cache` og `media`.

Senere ble en 5 TB HDD formatert med ext4 og montert permanent på `/media/storage`. Mappestrukturen ble planlagt rundt `movies`, `series` og `downloads` for å skille bibliotek og innkommende data.

Prowlarr ble startet som container, og Jellyseerr ble koblet til Jellyfin med API-basert integrasjon. Radarr, Sonarr, Bazarr, qBittorrent, SABnzbd og Gluetun ble vurdert som mulige utvidelser, men de omtales ikke som ferdig implementert uten egen bekreftelse.

### Spillservere

Fire aktive eller driftsklare tjenestekonfigurasjoner er dokumentert:

- Minecraft – Optimalisert
- Minecraft – All The Mods 10
- Minecraft – Cobbleverse
- Terraria – Modded med tModLoader

Serverne har ulike klientkrav og ressursbehov. Ikke alle kjører nødvendigvis samtidig. Statusmeldingen til brukerne forklarer derfor både aktuell status, versjon, adresse og hvordan man ber om oppstart eller hjelp.

### Plattformvurdering

En Seagate Barracuda 8 TB var tilgjengelig som mulig serverlagring da Proxmox ble vurdert. Repositoryet beskriver målbildet for virtualisering, men publiserer ikke et oppdiktet produksjonsinventar når VM-er, LXC-ID-er og ressursfordeling ikke er dokumentert.

Coolify ble undersøkt som et selvhostet PaaS-lag over Linux og Docker. Evalueringen omfatter Git-basert `deployment`, Dockerfile/Docker Compose, automatiske deploys, TLS, persistent storage, databaser, logs og fjernadministrasjon av servere via SSH.

## Resultat

Prosjektet viser en kombinasjon av praktisk systemadministrasjon og bevisst plattformdesign. Den viktigste læringen har vært at selve installasjonen bare er én del av jobben: vedvarende lagring, oppgraderingsrutiner, statuskommunikasjon, backup og sikker håndtering av secrets avgjør om løsningen faktisk kan driftes over tid.


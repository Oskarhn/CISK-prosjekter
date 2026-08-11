# Kompetanse og ansvar

## Teknisk arbeid

| Område | Praktisk erfaring i prosjektet |
|---|---|
| Linux | Ubuntu-administrasjon, filsystem, brukere, permissions, SSH og systemkontroll |
| Storage | LVM, ext4, mount points, `/etc/fstab`, kapasitetsplanlegging og mappestruktur |
| Containers | Docker, Docker Compose, volumes, bind mounts, logs og tjenesteintegrasjon |
| Nettverk | DNS-navn, TCP-porter, tjenesteendepunkter og avgrensning av management-tilgang |
| Spillservere | Instanser, versjoner, modpacks, klientkrav, oppdatering og ressursstyring |
| Medietjenester | Jellyfin, Jellyseerr, Prowlarr og planlegging av en utvidet media-stack |
| Plattformdesign | Vurdering av Proxmox, Coolify, service isolation og persistent storage |
| Sikkerhet | Secret-håndtering, minste eksponering, sanitization og hendelsesrutiner |
| Drift | Statuskommunikasjon, runbooks, endringskontroll og troubleshooting |

## Ansvar utover installasjon

Prosjektet har også krevd prioritering. Flere tunge spillservere kan ikke alltid kjøre samtidig, og oppdateringer kan påvirke både world-data og klientkompatibilitet. Derfor inngår følgende i driftsansvaret:

- velge hvilke tjenester som skal kjøre
- dokumentere versjon før og etter oppdatering
- informere brukerne om nedetid og klientkrav
- holde data adskilt fra container/runtime
- stoppe og feilsøke kontrollert når en oppdatering feiler
- unngå å publisere sensitive detaljer i åpne kanaler

## Faglig utvikling

Arbeidet har gitt erfaring med overgangen fra «det kjører på min maskin» til en tjeneste som andre faktisk er avhengige av. Det innebærer å tenke på kapasitet, observability, backup, rollback, dokumentasjon og sikkerhet samtidig som tjenesten skal være enkel å bruke.


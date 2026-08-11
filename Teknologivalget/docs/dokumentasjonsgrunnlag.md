# Dokumentasjonsgrunnlag

Et portfolio-repository er bare nyttig dersom det er tydelig hva som faktisk ble gjort. Dokumentasjonen bruker derfor følgende nivåer:

| Nivå | Betydning | Eksempel |
|---|---|---|
| Bekreftet | Oppsett eller status er eksplisitt dokumentert | Jellyfin-mounts, Prowlarr startet, spillserverversjoner |
| Historisk | Var bekreftet på en bestemt dato, men er ikke sanntidsovervåket | Online/offline-status 10. august 2026 |
| Evaluering | Teknologien er undersøkt eller planlagt, uten påstand om produksjonssetting | Coolify og detaljert Proxmox-målbilde |

## Kilder som er brukt

- egne notater fra installasjon og feilsøking
- tidligere dokumenterte kommandoer, mounts og tjenestestatuser
- serveroversikt laget for Discord
- teknisk research om Coolify, Docker, selvhosting og Git-basert deployment

Rå videotranskripsjoner er ikke lagt inn i repositoryet. De er brukt som research, men er tredjepartsinnhold og ville gitt lite verdi som driftsdokumentasjon.

## Sanitization

Følgende er bevisst fjernet eller generalisert:

- credentials, API keys og private SSH keys
- interne adresser og management-endepunkter
- full disk-UUID og maskinspesifikke identifiers
- personopplysninger og logger
- konfigurasjon som kan gi unødvendig angrepsflate

Offentlige spilladresser er beholdt fordi de allerede er beregnet på sluttbrukere.

## Kjente dokumentasjonsgrenser

- Eksakte Proxmox node-navn, VM-/LXC-ID-er og resource allocations er ikke tatt med uten bekreftet inventar.
- Radarr, Sonarr, Bazarr, downloader og VPN-lag omtales som mulige utvidelser, ikke som ferdig drift.
- Tjenestestatus er et datert øyeblikksbilde.
- Backup-prinsipper er dokumentert, men en vellykket restore-test skal registreres separat når den er gjennomført.


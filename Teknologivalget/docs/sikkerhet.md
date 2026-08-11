# Sikkerhet

## Verdier som skal beskyttes

- administratorkontoer og SSH keys
- API keys mellom tjenester
- spillverdener og konfigurasjon
- Jellyfin-metadata og brukerinformasjon
- Docker- og Coolify-konfigurasjon
- DNS-konto og eventuelle certificate keys
- backups

## Viktigste trusler

| Trussel | Konsekvens | Kontroll |
|---|---|---|
| Credential leak | Uautorisert administrasjon | Secrets utenfor Git, rotation og MFA |
| Eksponert management UI | Angrep direkte mot kontrollplanet | VPN/trusted network, firewall og TLS |
| Sårbar container/image | Kompromittert workload | Pinning, oppdatering og minst mulige privileges |
| Feil permissions | Datatap eller uautorisert lesing | Korrekt UID/GID og avgrensede mounts |
| Mod/plugin fra ukjent kilde | Supply-chain-angrep | Verifiser kilde, versjon og endringslogg |
| Manglende backup | Tap av world/config | Flere kopier og restore-test |
| Full disk | Tjenestestans eller korrupsjon | Kapasitetskontroll og varsling |
| Felles feildomene | Flere tjenester faller samtidig | Isolasjon med VM/container og resource limits |

## Hardening-prinsipper

### Linux

- installer sikkerhetsoppdateringer kontrollert
- deaktiver unødvendige tjenester
- bruk SSH keys fremfor passord der det er praktisk
- begrens `sudo` og root-bruk
- logg innloggingsforsøk og administrative endringer
- bruk host firewall i tillegg til eventuell perimeter firewall

### Docker

- bruk vedlikeholdte images og eksplisitte tags
- ikke kjør privileged uten dokumentert behov
- mount bare nødvendige paths
- ikke bruk Docker socket i en container uten å forstå at det normalt gir host-kontroll
- hold secrets utenfor compose-filen og repositoryet
- sett resource limits der workloaden kan løpe løpsk

### Spillservere

- whitelist eller tilgangskontroll når målgruppen er avgrenset
- begrens operatørrettigheter
- ta backup før modpack- og world-oppdateringer
- bruk plugins/mods fra kjente kilder
- valider konfigurasjonsendringer i staging eller kopi av world når risikoen er høy

### Jellyfin

- ikke eksponer admin-konto unødvendig
- bruk egne brukere og minste nødvendige tilgang
- gi containeren read-only tilgang til media der skrivetilgang ikke kreves
- beskytt API keys og roter dem ved mistanke om lekkasje

## Secret-håndtering

En offentlig compose-eksempel kan vise variabelnavnet, men ikke verdien:

```text
JELLYFIN_API_KEY=<settes-utenfor-git>
```

Hvis en secret blir committet:

1. sperr eller roter secreten umiddelbart
2. vurder om den er brukt av uvedkommende
3. fjern den fra gjeldende filer og historikk
4. dokumenter hendelsen uten å gjenta secretverdien
5. oppdater forebyggende kontroll

## Offentlig portfolio kontra intern runbook

Dette repoet beskriver prinsippene og de brukerrettede endepunktene. Eksakte firewall-regler, private adresser, kontoer, restore-lokasjoner og beredskapskontakter skal ligge i en tilgangsbegrenset intern runbook.


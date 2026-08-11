# Backup og gjenoppretting

## Status og mål

Repositoryet dokumenterer hva som skal beskyttes og hvordan restore bør testes. Det påstår ikke at en komplett 3-2-1-løsning er ferdig før en datert restore-test finnes.

## Prioritering

| Data | Prioritet | Begrunnelse |
|---|---|---|
| Spillverdener | Høy | Unike brukerdata som ikke enkelt kan gjenskapes |
| Serverconfig og modliste | Høy | Nødvendig for korrekt restart og klientkompatibilitet |
| Jellyfin/Jellyseerr/Prowlarr config | Høy | Kontoer, metadata og integrasjoner |
| Compose-/deployment-definisjoner | Høy | Gjør tjenestene reproduserbare |
| Databaser | Høy | Krever konsistent dump eller applikasjonsstopp |
| Mediefiler | Avhenger av kilde | Stor datamengde; prioriter etter hvor erstattbare filene er |
| Cache og byggartefakter | Lav | Kan normalt regenereres |

## Backup-prinsipp

Målet er minst:

- én arbeidskopi
- én lokal backup på separat storage
- én kopi utenfor samme host eller fysiske lokasjon

Snapshots er nyttige før endringer, men er ikke alene en backup. De deler ofte samme maskin og storage som originalen.

## Konsistens

- stopp spillserveren eller bruk en dokumentert save/flush før world kopieres
- bruk database dump eller applikasjonskonsistent metode for databaser
- kopier compose/config sammen med versjonsinformasjon
- ikke ta backup av en fil mens en applikasjon skriver den uten å vite at formatet tåler det

## Restore-test

En backup er ikke verifisert før den er gjenopprettet.

1. velg en isolert testlokasjon
2. hent siste og én eldre backup
3. kontroller checksum eller arkivintegritet
4. gjenopprett config og data
5. start tjenesten uten å eksponere den offentlig
6. test login, world load eller bibliotek
7. mål tidsbruk og noter mangler
8. slett testdata sikkert etterpå

## Minimum metadata per backup

- dato og klokkeslett
- tjeneste og versjon
- hvilke paths/databaser som inngår
- om tjenesten var stoppet eller quiesced
- checksum
- lagringssted
- resultat fra siste restore-test


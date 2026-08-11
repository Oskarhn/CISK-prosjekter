# Drift og vedlikehold

## Normal drift

Drift handler om å oppdage avvik før en bruker må rapportere dem. Kontroller bør dekke:

- om prosess/container kjører
- om riktig port svarer
- om tjenesten fungerer med faktisk klient
- ledig diskplass og inode-forbruk
- feil i logs
- tilgjengelige oppdateringer
- backup-resultat

## Foreslått kontrollfrekvens

| Frekvens | Kontroll |
|---|---|
| Ved endring | Funksjonstest, logs, versjon og statusmelding |
| Ukentlig | Diskplass, containerstatus, feil i logs og backup-resultat |
| Månedlig | OS-/image-oppdateringer, kontoer, secrets og SMART-status |
| Kvartalsvis | Restore-test, eksponerte porter og dokumentasjonsgjennomgang |

Frekvensen er et driftsmål. Den skal tilpasses hvor kritisk tjenesten er og hvor raskt den endrer seg.

## Endringsprosedyre

1. Beskriv hvorfor endringen gjøres.
2. Registrer nåværende versjon og konfigurasjon.
3. Vurder påvirkning på brukere, lagring og klientkompatibilitet.
4. Ta relevant backup.
5. Definer rollback før endringen starter.
6. Gjør én logisk endring om gangen.
7. Test teknisk og med faktisk klient.
8. Oppdater status og dokumentasjon.

## Ressursprioritering

Spillserverne har ulike CPU- og RAM-behov. Når kapasiteten er begrenset, prioriteres aktive servere. Dette er bedre enn å overcommitte hosten til det punktet hvor alle tjenester får dårlig ytelse.

Ved oppstart av en tung modpack-server bør man kontrollere:

- tilgjengelig RAM før oppstart
- CPU load og eventuell steal/host contention
- disk-I/O under world load
- garbage collection eller out-of-memory i loggen
- ytelsen til andre tjenester på samme host

## Kommunikasjon

En god statusmelding skal svare på:

- hva tjenesten heter
- om den er online eller offline
- hvilken adresse og port som brukes
- hvilken server- og klientversjon som kreves
- om modpack må installeres
- hvordan brukeren melder feil eller ber om oppstart

Den publiserte Discord-malen ligger i [`../services/game-servers/discord-serveroversikt.md`](../services/game-servers/discord-serveroversikt.md).

## Vedlikeholdsvindu

Planlagt vedlikehold bør varsles med starttid, forventet varighet, berørte tjenester og om klienten må oppdateres. Etterpå publiseres resultat og eventuelle kjente feil.


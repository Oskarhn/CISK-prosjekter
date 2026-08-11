# Proxmox

## Status

Proxmox ble vurdert som virtualiseringsplattform da Teknologiutvalget skulle få en mer samlet serverløsning. En Seagate Barracuda 8 TB var tilgjengelig som mulig lagringsdisk.

Det finnes ikke tilstrekkelig publiserbart grunnlag for å hevde eksakte node-navn, VM-/LXC-ID-er, bridge-navn eller resource allocations. Denne siden dokumenterer derfor beslutningsgrunnlaget og det planlagte driftsmønsteret, ikke et oppdiktet inventar.

## Hvorfor Proxmox var aktuelt

- isolere spillservere fra web- og medietjenester
- kunne restarte eller oppgradere én workload uten å påvirke alle andre
- få sentral styring av VM-er, LXC containers, snapshots og konsolltilgang
- fordele CPU, RAM og disk eksplisitt
- gjøre migrering og gjenoppretting mer forutsigbar

## Foreslått rollefordeling

| Rolle | Egnet format | Begrunnelse |
|---|---|---|
| Docker/Coolify | Egen Linux VM | Tydelig grense rundt et kraftig management plane |
| Spillservere | VM eller LXC per risikoprofil | Enklere resource limits og uavhengige restarts |
| Monitoring/backup | Egen liten VM/LXC eller ekstern tjeneste | Skal ikke forsvinne sammen med workloaden som feiler |
| Router/firewall | Egen fysisk enhet, eventuelt egen VM | Skal ikke blandes direkte med medieserveren |

Hvis pfSense virtualiseres, krever designet separate VMer og minst to fysiske NIC-er. Router-funksjonen skal ikke kjøre inne i samme operativsystem som Jellyfin eller andre applikasjoner.

## Storage-design

8 TB-disken er egnet for kapasitet, men én disk er ikke en backup. Før den brukes må følgende bestemmes:

- om disken skal presenteres direkte til en VM eller forvaltes av hypervisoren
- filsystem og eierskap
- hvilke data som kan gjenopprettes fra andre kilder
- hvor konfigurasjon og world-data sikkerhetskopieres
- SMART-overvåking og varsling
- restore-prosedyre ved disk- eller hostfeil

Medieinnhold og spillverdener har ulik verdi. World-data og konfigurasjon bør ha hyppigere backup enn store, erstattbare mediefiler.

## Nettverk

Et produksjonsoppsett bør minst skille mellom:

- management traffic for Proxmox og SSH
- offentlig eller port-forwarded service traffic
- intern trafikk mellom applikasjon og database
- backup traffic

Proxmox web UI skal ikke eksponeres direkte mot Internett. Management skjer fra et betrodd nett eller gjennom VPN, med MFA der det støttes.

## Sjekkliste før migrering

1. Dokumenter host-hardware, firmware, NIC-er og diskhelse.
2. Lag et faktisk inventar med VM/LXC, CPU, RAM, disk og autostart-rekkefølge.
3. Ta applikasjonskonsistent backup av world-data og containerkonfigurasjon.
4. Verifiser at backupen kan leses på en annen maskin.
5. Flytt én workload om gangen.
6. Test nettverk, DNS, ports og persistent storage.
7. La gammel løsning være tilgjengelig til den nye er verifisert.
8. Registrer avvik og oppdater runbooks.

## Relevante driftskontroller

- regelmessig `pveversion` og oppdateringskontroll
- SMART-status og temperatur på fysiske disker
- ledig kapasitet på alle storage targets
- status på backup jobs
- feil i systemlogg og kernel
- verifisert autostart etter vedlikeholdsreboot

Kontrollene er målkrav. De skal først markeres som implementert når jobber, varsling og restore-test er dokumentert.


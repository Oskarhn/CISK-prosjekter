# Runbook: incident response

## 1. Bekreft og avgrens

- hvilken tjeneste er berørt?
- når startet problemet?
- er det tilgjengelighetsfeil, datatap eller mulig kompromittering?
- påvirkes én container, hosten eller flere tjenester?

## 2. Bevar informasjon

- noter klokkeslett og observerte symptomer
- ta vare på relevante logs
- registrer prosesser, aktive tilkoblinger og versjoner
- ikke publiser secrets eller persondata i issue/Discord

## 3. Begrens skade

Ved sikkerhetshendelse kan det være nødvendig å stoppe ekstern tilgang, sperre konto/token eller isolere en workload. Bevar samtidig nok informasjon til å forstå hendelsen.

## 4. Gjenopprett

- fjern rotårsaken, ikke bare symptomet
- patch eller bytt kompromittert credential
- gjenopprett fra verifisert backup ved behov
- start avhengigheter i riktig rekkefølge
- test teknisk og med faktisk klient

## 5. Kommuniser

En statusmelding bør inneholde:

- hvilke tjenester som er berørt
- starttid for hendelsen
- om data kan være påvirket
- midlertidig løsning
- neste forventede oppdatering

## 6. Etteranalyse

Dokumenter tidslinje, root cause, impact, hva som fungerte, hva som manglet og konkrete preventive actions. Ikke legg utnyttbare detaljer i offentlig dokumentasjon mens sårbarheten fortsatt er aktiv.


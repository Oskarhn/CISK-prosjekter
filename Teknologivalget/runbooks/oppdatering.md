# Runbook: oppdatering og rollback

## Før oppdatering

- registrer nåværende versjon/image digest
- les release notes og kjente breaking changes
- kontroller backup-resultat
- definer funksjonstest
- skriv ned rollback-steg
- varsle brukerne dersom nedetid forventes

## Gjennomføring

1. Stopp writes eller tjenesten når konsistens krever det.
2. Ta fersk backup/snapshot i riktig rekkefølge.
3. Oppdater én komponent.
4. Start tjenesten og følg logs.
5. Kjør helse- og funksjonstest.
6. Fortsett bare dersom testen består.

## Rollback

Rollback skal bruke den registrerte forrige versjonen og den tilhørende konfigurasjonen. Dersom oppdateringen har migrert database eller world-format, må kompatibiliteten bekreftes før gammel versjon startes.

## Etterarbeid

- registrer ny versjon og dato
- noter avvik og tidsbruk
- oppdater status til brukerne
- behold relevant backup etter retention-reglene
- oppdater runbook hvis den faktiske prosedyren avvek


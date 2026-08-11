# Runbook: tjenesteoppstart

## Formål

Starte en tidligere stoppet tjeneste uten å overbelaste hosten eller publisere feil status.

## Prosedyre

1. Identifiser tjenesten og forventet versjon.
2. Kontroller host load, ledig RAM og diskplass.
3. Kontroller at nødvendige mounts er aktive.
4. Kontroller at ingen annen prosess allerede bruker porten.
5. Start tjenesten med dens normale service manager eller Compose-prosjekt.
6. Følg loggen til tjenesten er klar.
7. Test lokalt og deretter med faktisk klient.
8. Kontroller at andre workloads fortsatt har nok ressurser.
9. Oppdater statusmeldingen.

## Read-only kontroller

```bash
uptime
free -h
df -h
findmnt
ss -lntup
docker compose ps
```

## Avbryt oppstart dersom

- et nødvendig mount mangler
- disken er full eller nesten full
- backup/migrering pågår
- riktig versjon ikke kan fastslås
- oppstarten gir gjentatte crashes eller påvirker andre tjenester kraftig


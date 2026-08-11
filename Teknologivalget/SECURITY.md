# Security policy

Dette er et offentlig dokumentasjonsrepository. Produksjonsdata og secrets skal ikke publiseres her.

## Ikke legg inn

- passord, API keys, tokens eller private SSH keys
- `.env`-filer med reelle verdier
- interne IP-adresser eller full nettverkstopologi
- komplette firewall-regler fra produksjon
- personopplysninger, brukerlogger eller mediefiler
- world-data, backups eller database-dumper

Eksempelverdier skal være tydelig fiktive. Reelle secrets som ved et uhell blir committet skal roteres; det er ikke nok å slette dem i en senere commit.

## Rapportering

Ikke legg detaljer om en aktiv sårbarhet i en offentlig issue. Bruk GitHubs private vulnerability reporting eller ta direkte kontakt med repository-eier dersom denne funksjonen ikke er aktivert.

## Før publisering

Kjør:

```bash
./scripts/verify-public-repo.sh
```

Scriptet er en enkel ekstra kontroll. Manuell gjennomgang er fortsatt nødvendig.


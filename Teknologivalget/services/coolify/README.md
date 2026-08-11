# Coolify

Status: **evaluert, ikke dokumentert som produksjonssatt**.

Coolify ble undersøkt som et selvhostet PaaS for Git-basert deployment av webapplikasjoner og interne tjenester.

## Ønsket arbeidsflyt

```text
Git push
  -> webhook/deploy
  -> build eller ferdig container image
  -> application container
  -> domain + TLS
  -> logs og health check
```

## Krav før produksjon

- egen Linux VM
- begrenset management-tilgang
- backup og restore-test
- secrets utenfor Git
- persistent volumes for stateful tjenester
- måling av ressursbruk under builds
- dokumentert oppdatering og rollback

Se [evalueringen](../../docs/coolify-evaluering.md).


# Nettverk

## Publiserbare service mappings

```text
mc.sky-net.no:25567  -> Minecraft Optimalisert
mc.sky-net.no:25568  -> Minecraft All The Mods 10
mc.sky-net.no:25572  -> Minecraft Cobbleverse
65.21.209.174:7779   -> Terraria Modded
```

## Trust boundaries

- `public service`: spillport som sluttbrukere kan nå
- `management`: SSH, hypervisor og admin UI; ikke offentlig
- `application`: intern kommunikasjon mellom containers/tjenester
- `backup`: kopiering til separat storage eller lokasjon

En port skal ha en dokumentert owner, protokoll og tjeneste. Når en server tas permanent ut av drift, fjernes også tilhørende forwarding og firewall-regel.

Se [nettverk og domener](../../docs/nettverk-og-domener.md).


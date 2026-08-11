# Storage

## Dokumenterte lagringsområder

| Område | Type | Bruk |
|---|---|---|
| Ubuntu root | LVM på ca. 1 TB NVMe | Operativsystem |
| `/dockerdata` | ca. 688 GB logical volume | Containerkonfigurasjon, cache og tidlig mediedata |
| `/media/storage` | 5 TB ext4 HDD | `movies`, `series` og `downloads` |
| Seagate Barracuda 8 TB | Fysisk disk | Tilgjengelig/vurdert for serverplattformen |

## Prinsipper

- konfigurasjon og unike data prioriteres i backup
- cache og midlertidige filer kan regenereres
- mount points skal verifiseres før containers starter
- én stor disk gir kapasitet, ikke redundans
- LVM-snapshots og Proxmox snapshots erstatter ikke ekstern backup

Se [storage-runbook](../../runbooks/storage.md).


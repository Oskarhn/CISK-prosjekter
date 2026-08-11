# Proxmox-plattform

Proxmox ble vurdert som hypervisor for å samle workloads uten å blande alle tjenester i samme operativsystem. En Seagate Barracuda 8 TB var tilgjengelig som mulig storage.

## Dokumentert

- behov for en serverplattform for Teknologiutvalget
- 8 TB lagringsdisk tilgjengelig
- Proxmox vurdert for virtualisering og service isolation
- pfSense/router skal holdes separat fra medieserveren, med egne VMer og NIC-er dersom det virtualiseres

## Ikke publisert som fakta

- node-navn og management-IP
- VM-/LXC-ID-er
- CPU/RAM per workload
- bridge-, VLAN- og firewall-konfigurasjon
- backup-targets

Disse feltene skal fylles fra et kontrollert produksjonsinventar, ikke rekonstrueres fra antakelser.

Se [den tekniske vurderingen](../../docs/proxmox.md) for målarkitektur, storage, nettverk og migreringssjekkliste.


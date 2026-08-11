#!/usr/bin/env bash

set -u

if ! command -v nc >/dev/null 2>&1; then
  echo "Feil: nc/netcat er ikke installert." >&2
  echo "Fedora: sudo dnf install nmap-ncat" >&2
  echo "Debian/Ubuntu: sudo apt install netcat-openbsd" >&2
  exit 2
fi

targets=(
  "Minecraft Optimalisert|mc.sky-net.no|25567"
  "Minecraft All The Mods 10|mc.sky-net.no|25568"
  "Minecraft Cobbleverse|mc.sky-net.no|25572"
  "Terraria Modded|65.21.209.174|7779"
)

failed=0

for target in "${targets[@]}"; do
  IFS='|' read -r name host port <<< "${target}"

  if nc -z -w 3 "${host}" "${port}" >/dev/null 2>&1; then
    printf 'OK    %-30s %s:%s\n' "${name}" "${host}" "${port}"
  else
    printf 'FEIL  %-30s %s:%s\n' "${name}" "${host}" "${port}"
    failed=1
  fi
done

echo
echo "Merk: testen kontrollerer bare TCP-tilkobling, ikke login eller versjonsmatch."
exit "${failed}"


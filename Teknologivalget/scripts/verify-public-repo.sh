#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

if ! command -v rg >/dev/null 2>&1; then
  echo "Feil: ripgrep (rg) er nødvendig for kontrollen." >&2
  exit 2
fi

failed=0

echo "Kontrollerer filnavn som ofte inneholder secrets ..."
while IFS= read -r path; do
  echo "Mistenkelig fil: ${path}" >&2
  failed=1
done < <(
  find . -type f \
    \( -name '.env' -o -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name '*.pfx' \) \
    -not -path './.git/*'
)

echo "Kontrollerer vanlige secret-mønstre ..."
if rg -n --hidden \
  -g '!.git/**' \
  -g '!scripts/verify-public-repo.sh' \
  -e 'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY' \
  -e 'gh[pousr]_[A-Za-z0-9_]{20,}' \
  -e 'AKIA[0-9A-Z]{16}' \
  -e 'sk-[A-Za-z0-9_-]{20,}' \
  -e '(password|passwd|api[_-]?key|token)[[:space:]]*[:=][[:space:]]*[^<[:space:]][^[:space:]]{7,}' \
  .; then
  echo "Mulig secret funnet. Kontroller treffene manuelt." >&2
  failed=1
fi

echo "Kontrollerer uløste merge-markører ..."
if rg -n --hidden -g '!.git/**' '^(<<<<<<<|=======|>>>>>>>)' .; then
  echo "Uløste merge-markører funnet." >&2
  failed=1
fi

if [[ "${failed}" -ne 0 ]]; then
  echo "Kontrollen feilet." >&2
  exit 1
fi

echo "Kontrollen fant ingen åpenbare problemer. Gjør fortsatt en manuell review før push."


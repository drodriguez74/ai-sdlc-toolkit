#!/usr/bin/env bash
# upgrade.sh — Upgrade the installed toolkit in place. Backs up before applying.
# Never deletes user override folders or .ai-sdlc data.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_HOME="${TOOLKIT_HOME:-${HOME}/.copilot/ai-sdlc-toolkit}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="${HOME}/.copilot/ai-sdlc-toolkit.bak.${TIMESTAMP}"

FROM_VERSION=""
while [ $# -gt 0 ]; do
  case "$1" in
    --from-version) FROM_VERSION="$2"; shift 2 ;;
    *) echo "Unknown flag: $1"; exit 2 ;;
  esac
done

if [ ! -d "${TOOLKIT_HOME}" ]; then
  echo "ERROR: no existing install at ${TOOLKIT_HOME}. Run install.sh first."
  exit 1
fi

CURRENT_VERSION="$(cat "${TOOLKIT_HOME}/VERSION" 2>/dev/null || echo unknown)"
NEW_VERSION="$(cat "${SCRIPT_DIR}/VERSION" 2>/dev/null || echo unknown)"

if [ -n "${FROM_VERSION}" ] && [ "${FROM_VERSION}" != "${CURRENT_VERSION}" ]; then
  echo "ERROR: --from-version=${FROM_VERSION} but installed is ${CURRENT_VERSION}"
  exit 1
fi

echo "==> Upgrading ${CURRENT_VERSION} -> ${NEW_VERSION}"
echo "==> Backup: ${BACKUP_DIR}"
cp -R "${TOOLKIT_HOME}" "${BACKUP_DIR}"

# Apply new files, but never delete user content.
# We do NOT use --delete; we overwrite default files but leave overrides intact.
if command -v rsync >/dev/null 2>&1; then
  rsync -a \
    --exclude='.git/' \
    --exclude='manifest.json' \
    --exclude='node_modules/' \
    --exclude='.DS_Store' \
    "${SCRIPT_DIR}/" "${TOOLKIT_HOME}/"
else
  cp -R "${SCRIPT_DIR}/." "${TOOLKIT_HOME}/"
fi

# Re-resolve manifest.
sed "s|__TOOLKIT_HOME__|${TOOLKIT_HOME}|g" \
  "${TOOLKIT_HOME}/manifest.json.tpl" > "${TOOLKIT_HOME}/manifest.json"

chmod +x "${TOOLKIT_HOME}"/*.sh 2>/dev/null || true
find "${TOOLKIT_HOME}/tools" -type f \( -name "*.sh" -o -name "*.py" \) \
  -exec chmod +x {} \; 2>/dev/null || true

# Refresh managed blocks in any linked projects we know about.
# Linked projects are not tracked centrally; users should re-run
# refresh-project-links.sh per repo. We refresh the global awareness files only.
if [ -x "${TOOLKIT_HOME}/install.sh" ]; then
  # Re-running install.sh refreshes the global awareness blocks idempotently.
  "${TOOLKIT_HOME}/install.sh" >/dev/null
fi

# Re-run doctor.
"${TOOLKIT_HOME}/doctor.sh" || {
  echo "WARNING: doctor.sh reported failures after upgrade."
  echo "Backup is at: ${BACKUP_DIR}"
  exit 1
}

echo "==> Upgrade complete."
echo "    Backup at: ${BACKUP_DIR}"
echo "    Re-run refresh-project-links.sh in each linked repo to update links."

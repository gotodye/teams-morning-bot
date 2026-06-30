#!/usr/bin/env bash
# Write Telegram settings to .env and optionally sync to GitHub Actions.
#
# Interactive:
#   ./scripts/set_telegram_env.sh
#
# One-liner (方案 A — 同步到 GitHub):
#   TELEGRAM_BOT_TOKEN='123456:ABC...' SYNC_GITHUB=y ./scripts/set_telegram_env.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
ENV_FILE="$ROOT/.env"
REPO="${GITHUB_REPO:-gotodye/teams-morning-bot}"
DEFAULT_CHAT_ID="-1002236690168"

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ROOT/.env.example" "$ENV_FILE"
  echo "[OK] 已從 .env.example 建立 .env"
fi

if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]]; then
  TOKEN="$TELEGRAM_BOT_TOKEN"
else
  read -rsp "TELEGRAM_BOT_TOKEN: " TOKEN
  echo
fi
TOKEN="$(echo "$TOKEN" | tr -d '[:space:]')"
if [[ -z "$TOKEN" ]]; then
  echo "[ERROR] Token 不可為空" >&2
  exit 1
fi

if [[ -n "${TELEGRAM_CHAT_ID:-}" ]]; then
  CHAT_ID="$TELEGRAM_CHAT_ID"
else
  read -rp "TELEGRAM_CHAT_ID [Enter=$DEFAULT_CHAT_ID]: " CHAT_ID
  CHAT_ID="${CHAT_ID:-$DEFAULT_CHAT_ID}"
fi

python3 - <<PY
from pathlib import Path

env_file = Path("$ENV_FILE")
lines = env_file.read_text(encoding="utf-8").splitlines()
values = {
    "TELEGRAM_BOT_TOKEN": "$TOKEN",
    "TELEGRAM_CHAT_ID": "$CHAT_ID",
    "ENABLE_TELEGRAM": "true",
}
out: list[str] = []
seen = set()

for line in lines:
    key = None
    for candidate in values:
        if line.strip().startswith("#") and f"{candidate}=" in line:
            key = candidate
            break
        if line.startswith(f"{candidate}=") or line.startswith(f"# {candidate}="):
            key = candidate
            break
    if key:
        out.append(f"{key}={values[key]}")
        seen.add(key)
    else:
        out.append(line)

for key, value in values.items():
    if key not in seen:
        out.append(f"{key}={value}")

env_file.write_text("\n".join(out) + "\n", encoding="utf-8")
PY

echo "[OK] 已寫入 .env"

export TELEGRAM_BOT_TOKEN="$TOKEN"
export TELEGRAM_CHAT_ID="$CHAT_ID"
export ENABLE_TELEGRAM=true
python3 scripts/verify_telegram.py

if command -v gh >/dev/null 2>&1; then
  if [[ "${SYNC_GITHUB:-}" == "y" || "${SYNC_GITHUB:-}" == "Y" ]]; then
    printf '%s' "$TOKEN" | gh secret set TELEGRAM_BOT_TOKEN -R "$REPO"
    gh variable set TELEGRAM_CHAT_ID --body "$CHAT_ID" -R "$REPO"
    gh variable set ENABLE_TELEGRAM --body "true" -R "$REPO"
    echo "[OK] 已同步 GitHub: TELEGRAM_BOT_TOKEN (secret) + TELEGRAM_CHAT_ID (variable)"
  else
    read -rp "是否同步到 GitHub Secret? (y/N): " SYNC
    if [[ "$SYNC" == "y" || "$SYNC" == "Y" ]]; then
      printf '%s' "$TOKEN" | gh secret set TELEGRAM_BOT_TOKEN -R "$REPO"
      gh variable set TELEGRAM_CHAT_ID --body "$CHAT_ID" -R "$REPO"
      gh variable set ENABLE_TELEGRAM --body "true" -R "$REPO"
      echo "[OK] 已同步 GitHub: TELEGRAM_BOT_TOKEN (secret) + TELEGRAM_CHAT_ID (variable)"
    fi
  fi
else
  echo "[INFO] 未安裝 gh CLI，略過 GitHub 同步"
fi

echo ""
echo "測試發送："
echo '  SKIP_WORKDAY_CHECK=true python3 main.py'

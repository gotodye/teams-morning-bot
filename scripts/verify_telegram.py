#!/usr/bin/env python3
"""Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID when Telegram delivery is enabled."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def _telegram_enabled() -> bool:
    return os.environ.get("ENABLE_TELEGRAM", "true").lower() != "false"


def _telegram_configured() -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    return bool(token and chat_id)


def main() -> int:
    if not _telegram_enabled():
        print("[SKIP] ENABLE_TELEGRAM=false — Telegram verification skipped")
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if not token and not chat_id:
        print("[SKIP] Telegram not configured — Teams-only mode")
        return 0

    if not token or not chat_id:
        missing = "TELEGRAM_BOT_TOKEN" if not token else "TELEGRAM_CHAT_ID"
        print(f"[WARN] {missing} 未設定 — Telegram 將略過，Teams 推播不受影響")
        return 0

    response = requests.get(
        f"https://api.telegram.org/bot{token}/getMe",
        timeout=15,
    )
    data = response.json()
    if not data.get("ok"):
        print("[FAIL] getMe:", data)
        return 1

    user = data["result"]
    print(f"[OK] Bot: @{user.get('username', '?')} ({user.get('first_name', '')})")

    chat_resp = requests.get(
        f"https://api.telegram.org/bot{token}/getChat",
        params={"chat_id": chat_id},
        timeout=15,
    )
    chat_data = chat_resp.json()
    if chat_data.get("ok"):
        chat = chat_data["result"]
        title = chat.get("title") or chat.get("type") or "?"
        print(f"[OK] Chat: {title} (id={chat.get('id')})")
        return 0

    print("[FAIL] getChat:", chat_data.get("description", chat_data))
    print("       請確認 Bot 已加入群組，且 Chat ID 正確")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID from .env."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def main() -> int:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if not token:
        print("[FAIL] TELEGRAM_BOT_TOKEN 未設定")
        return 1

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

    if not chat_id:
        print("[WARN] TELEGRAM_CHAT_ID 未設定")
        return 0

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

    print("[WARN] getChat:", chat_data.get("description", chat_data))
    print("       請確認 Bot 已加入群組，且 Chat ID 正確")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

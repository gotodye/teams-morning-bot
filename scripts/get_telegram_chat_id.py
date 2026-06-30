#!/usr/bin/env python3
"""List Telegram chat IDs from recent bot updates."""

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
    if not token:
        print("[ERROR] TELEGRAM_BOT_TOKEN 未設定", file=sys.stderr)
        return 1

    response = requests.get(
        f"https://api.telegram.org/bot{token}/getUpdates",
        timeout=15,
    )
    data = response.json()
    if not data.get("ok"):
        print("[ERROR] getUpdates:", data, file=sys.stderr)
        return 1

    chats: dict[int, str] = {}
    for update in data.get("result", []):
        for key in ("message", "channel_post", "edited_message"):
            message = update.get(key)
            if not message:
                continue
            chat = message.get("chat") or {}
            chat_id = chat.get("id")
            if chat_id is None:
                continue
            label = (
                chat.get("title")
                or chat.get("username")
                or chat.get("first_name")
                or chat.get("type")
                or "?"
            )
            chats[int(chat_id)] = str(label)

    if not chats:
        print(
            "找不到任何訊息。\n"
            "請先把 Bot 加入群組，在群組內 @Bot 或發一則訊息，再重試。"
        )
        return 1

    print("Chat ID 列表：")
    for chat_id, label in sorted(chats.items()):
        print(f"  {chat_id}  ({label})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

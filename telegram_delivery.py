"""Send morning messages to Telegram groups via Bot API."""

from __future__ import annotations

import html
import logging
import os
import re
from datetime import date

import requests

from messages import build_card_subtitle, build_card_title

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"
CAPTION_LIMIT = 1024
MESSAGE_LIMIT = 4096


def telegram_configured() -> bool:
    if os.environ.get("ENABLE_TELEGRAM", "true").lower() == "false":
        return False
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    return bool(token and chat_id)


def _markdown_to_html(text: str) -> str:
    """Convert Teams-style **bold** to Telegram HTML (skip _italic_ to avoid URL issues)."""
    parts = re.split(r"(\*\*.+?\*\*)", text, flags=re.DOTALL)
    rendered: list[str] = []
    for part in parts:
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            rendered.append(f"<b>{html.escape(part[2:-2], quote=False)}</b>")
        else:
            rendered.append(html.escape(part, quote=False))
    return "".join(rendered)


def _build_header_html(
    today: date,
    source: str,
    *,
    weekday_name: str,
    static_format: str | None = None,
) -> str:
    title = build_card_title(today, source, weekday_name, static_format=static_format)
    subtitle = build_card_subtitle(
        today, source, weekday_name, static_format=static_format
    )
    return (
        f"<b>{html.escape(title, quote=False)}</b>\n"
        f"<i>{html.escape(subtitle, quote=False)}</i>"
    )


def build_telegram_html(
    message: str,
    today: date,
    source: str,
    *,
    weekday_name: str,
    static_format: str | None = None,
) -> str:
    header = _build_header_html(
        today, source, weekday_name=weekday_name, static_format=static_format
    )
    body_html = _markdown_to_html(message)
    if not message.strip():
        return header
    return f"{header}\n\n{body_html}"


def _split_text(text: str, limit: int) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks: list[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= limit:
            chunks.append(remaining)
            break
        split_at = remaining.rfind("\n\n", 0, limit)
        if split_at < limit // 2:
            split_at = remaining.rfind("\n", 0, limit)
        if split_at < limit // 2:
            split_at = limit
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    return chunks


def _api_post(token: str, method: str, payload: dict) -> None:
    url = TELEGRAM_API.format(token=token, method=method)
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API {method} failed: {data}")


def send_to_telegram(
    message: str,
    today: date,
    source: str = "static",
    image_url: str | None = None,
    *,
    weekday_name: str,
    static_format: str | None = None,
) -> None:
    """Send the morning message to a Telegram group or channel."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        raise RuntimeError(
            "Telegram is not configured — set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID"
        )

    text = build_telegram_html(
        message,
        today,
        source,
        weekday_name=weekday_name,
        static_format=static_format,
    )

    if image_url:
        if len(text) <= CAPTION_LIMIT:
            _api_post(
                token,
                "sendPhoto",
                {
                    "chat_id": chat_id,
                    "photo": image_url,
                    "caption": text,
                    "parse_mode": "HTML",
                },
            )
            logger.info("Message with image sent to Telegram!")
            return

        title_only = _build_header_html(
            today,
            source,
            weekday_name=weekday_name,
            static_format=static_format,
        )
        _api_post(
            token,
            "sendPhoto",
            {
                "chat_id": chat_id,
                "photo": image_url,
                "caption": title_only[:CAPTION_LIMIT],
                "parse_mode": "HTML",
            },
        )
        body_html = _markdown_to_html(message)
        for chunk in _split_text(body_html, MESSAGE_LIMIT):
            _api_post(
                token,
                "sendMessage",
                {"chat_id": chat_id, "text": chunk, "parse_mode": "HTML"},
            )
        logger.info("Message with image (split) sent to Telegram!")
        return

    for chunk in _split_text(text, MESSAGE_LIMIT):
        _api_post(
            token,
            "sendMessage",
            {"chat_id": chat_id, "text": chunk, "parse_mode": "HTML"},
        )
    logger.info("Message sent to Telegram!")

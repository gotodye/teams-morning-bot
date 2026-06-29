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


def _api_post(token: str, method: str, payload: dict) -> dict:
    url = TELEGRAM_API.format(token=token, method=method)
    response = requests.post(url, json=payload, timeout=30)
    data = response.json()
    if not response.ok or not data.get("ok"):
        description = data.get("description", response.text)
        raise RuntimeError(f"Telegram API {method} failed: {description}")
    return data


def _send_message(
    token: str,
    chat_id: str,
    text: str,
    *,
    parse_mode: str | None = "HTML",
) -> None:
    payload: dict = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        _api_post(token, "sendMessage", payload)
    except RuntimeError as exc:
        if parse_mode and "parse" in str(exc).lower():
            logger.warning("Telegram HTML failed — retrying as plain text")
            _api_post(token, "sendMessage", {"chat_id": chat_id, "text": text})
            return
        raise


def _send_photo_bytes(
    token: str,
    chat_id: str,
    image_bytes: bytes,
    *,
    caption: str | None = None,
) -> None:
    url = TELEGRAM_API.format(token=token, method="sendPhoto")
    data: dict = {"chat_id": chat_id}
    if caption:
        data["caption"] = caption[:CAPTION_LIMIT]
        data["parse_mode"] = "HTML"
    response = requests.post(
        url,
        data=data,
        files={"photo": ("theme.jpg", image_bytes)},
        timeout=60,
    )
    body = response.json()
    if not response.ok or not body.get("ok"):
        raise RuntimeError(
            f"Telegram API sendPhoto (upload) failed: {body.get('description', response.text)}"
        )


def _send_photo_url(
    token: str,
    chat_id: str,
    image_url: str,
    *,
    caption: str | None = None,
) -> None:
    payload: dict = {"chat_id": chat_id, "photo": image_url}
    if caption:
        payload["caption"] = caption[:CAPTION_LIMIT]
        payload["parse_mode"] = "HTML"
    _api_post(token, "sendPhoto", payload)


def _send_photo_with_fallback(
    token: str,
    chat_id: str,
    image_url: str,
) -> None:
    """Telegram often cannot fetch Unsplash/Pexels URLs — download and upload instead."""
    try:
        _send_photo_url(token, chat_id, image_url)
        logger.info("Telegram photo sent via URL")
        return
    except RuntimeError as exc:
        logger.warning("Telegram sendPhoto URL failed: %s", exc)

    try:
        response = requests.get(
            image_url,
            timeout=30,
            headers={"User-Agent": "teams-morning-bot/1.0"},
        )
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            raise RuntimeError(f"Unexpected content type: {content_type or 'unknown'}")
        _send_photo_bytes(token, chat_id, response.content)
        logger.info("Telegram photo sent via upload")
    except Exception as exc:
        logger.warning("Telegram photo skipped after all attempts: %s", exc)


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

    logger.info("Telegram: sending text to chat_id=%s (source=%s)", chat_id, source)
    for chunk in _split_text(text, MESSAGE_LIMIT):
        _send_message(token, chat_id, chunk)

    if image_url:
        _send_photo_with_fallback(token, chat_id, image_url)

    logger.info("Message sent to Telegram!")


def telegram_status_line() -> str:
    """One-line status for logs / CI diagnostics."""
    if os.environ.get("ENABLE_TELEGRAM", "true").lower() == "false":
        return "Telegram disabled (ENABLE_TELEGRAM=false)"
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token and not chat_id:
        return "Telegram skipped (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID not set)"
    if not token:
        return "Telegram misconfigured (TELEGRAM_BOT_TOKEN missing)"
    if not chat_id:
        return "Telegram misconfigured (TELEGRAM_CHAT_ID missing)"
    return f"Telegram enabled (chat_id={chat_id})"

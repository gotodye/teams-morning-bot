#!/usr/bin/env python3
"""Teams 晨間推播機器人 — 週一至週五自動發送正能量問候（排除台灣國定假日）。"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import holidays
import requests
from dotenv import load_dotenv

from messages import MANAGEMENT_QUOTES, MESSAGES, PHILOSOPHY_QUOTES
from image_search import find_theme_image

load_dotenv()

if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

TZ_TAIWAN = ZoneInfo("Asia/Taipei")
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DEFAULT_AI_WORKDAY_INTERVAL = 10
DEFAULT_MANAGEMENT_QUOTE_WEEKDAY = 2  # Wednesday — weekly management wisdom day


def get_today() -> date:
    """取得台灣時區的今日日期，測試時可用 OVERRIDE_DATE 覆寫。"""
    override = os.environ.get("OVERRIDE_DATE", "").strip()
    if override:
        return date.fromisoformat(override)
    return datetime.now(TZ_TAIWAN).date()


def is_workday(today: date) -> bool:
    """
    判斷今天是否為工作日。
    - 週六、週日 → 非工作日
    - 台灣國定假日 → 非工作日
    """
    if today.weekday() >= 5:
        logger.info("Weekend (%s) — skipping.", WEEKDAY_NAMES[today.weekday()])
        return False

    tw_holidays = get_tw_holidays(today.year)
    if today in tw_holidays:
        logger.info("Taiwan public holiday (%s) — skipping.", tw_holidays.get(today))
        return False

    return True


def get_tw_holidays(*years: int) -> holidays.HolidayBase:
    """取得台灣國定假日集合（支援跨年度查詢）。"""
    unique_years = sorted(set(years))
    return holidays.TW(years=unique_years)


def is_tw_workday(day: date, tw_holidays: holidays.HolidayBase) -> bool:
    """判斷指定日期是否為台灣工作日。"""
    return day.weekday() < 5 and day not in tw_holidays


def count_workdays_since(start: date, end: date) -> int:
    """計算從 start（不含）到 end（含）之間的工作日數。"""
    if end <= start:
        return 0

    years = range(start.year, end.year + 1)
    tw_holidays = get_tw_holidays(*years)
    count = 0
    current = start + timedelta(days=1)
    while current <= end:
        if is_tw_workday(current, tw_holidays):
            count += 1
        current += timedelta(days=1)
    return count


def get_biweek_key(today: date) -> str:
    """以 ISO 週為基準，每兩週為一個週期。"""
    year, week, _ = today.isocalendar()
    biweek = (week - 1) // 2
    return f"{year}-B{biweek:02d}"


def get_biweek_workdays(today: date) -> list[date]:
    """List all workdays in the current two-week ISO period."""
    year, week, _ = today.isocalendar()
    biweek_start_week = ((week - 1) // 2) * 2 + 1
    biweek_monday = date.fromisocalendar(year, biweek_start_week, 1)
    biweek_end = biweek_monday + timedelta(days=13)

    tw_holidays = get_tw_holidays(biweek_monday.year, biweek_end.year)
    return [
        day
        for offset in range(14)
        if is_tw_workday(day := biweek_monday + timedelta(days=offset), tw_holidays)
    ]


def get_biweek_special_day(today: date, slot: str) -> date | None:
    """Pick one workday per biweek for a special slot (ai, philosophy)."""
    workdays = get_biweek_workdays(today)
    if not workdays:
        return None

    seed = hashlib.md5(f"{get_biweek_key(today)}:{slot}".encode()).hexdigest()
    index = int(seed, 16) % len(workdays)

    if slot == "philosophy" and len(workdays) > 1:
        ai_seed = hashlib.md5(f"{get_biweek_key(today)}:ai".encode()).hexdigest()
        ai_index = int(ai_seed, 16) % len(workdays)
        if index == ai_index:
            index = (index + 1) % len(workdays)

    return workdays[index]


def get_ai_day_in_biweek(today: date) -> date | None:
    """Pick one workday per biweek for AI-generated messages."""
    return get_biweek_special_day(today, "ai")


def get_philosophy_day_in_biweek(today: date) -> date | None:
    """Pick one workday per biweek for philosopher quotes."""
    return get_biweek_special_day(today, "philosophy")


def should_use_ai(today: date) -> bool:
    """
    判斷今天是否使用方案 B（AI 生成）。
    預設採雙週週期隨機選一天；亦可透過環境變數調整或強制指定。
    """
    forced = os.environ.get("FORCE_MESSAGE_TYPE", "").lower()
    if forced == "ai":
        return True
    if forced in ("static", "management", "philosophy"):
        return False

    mode = os.environ.get("MESSAGE_MODE", "mixed").lower()
    if mode == "static":
        return False
    if mode == "ai":
        return True

    strategy = os.environ.get("AI_SCHEDULE_STRATEGY", "biweekly").lower()
    if strategy == "workday_interval":
        interval = int(os.environ.get("AI_WORKDAY_INTERVAL", DEFAULT_AI_WORKDAY_INTERVAL))
        workday_number = count_workdays_since(date(2024, 1, 1), today)
        return workday_number % interval == 0

    ai_day = get_ai_day_in_biweek(today)
    return ai_day == today


def is_management_quote_day(today: date) -> bool:
    """Once per week: management quote day for leadership, mindset, and work skills."""
    forced = os.environ.get("FORCE_MESSAGE_TYPE", "").lower()
    if forced == "management":
        return True
    if forced in ("ai", "static", "philosophy"):
        return False

    mgmt_weekday = int(
        os.environ.get("MANAGEMENT_QUOTE_WEEKDAY", DEFAULT_MANAGEMENT_QUOTE_WEEKDAY)
    )
    return today.weekday() == mgmt_weekday


def is_philosophy_quote_day(today: date) -> bool:
    """Once per biweek: a meaningful quote from a renowned philosopher."""
    forced = os.environ.get("FORCE_MESSAGE_TYPE", "").lower()
    if forced == "philosophy":
        return True
    if forced in ("ai", "static", "management"):
        return False

    philosophy_day = get_philosophy_day_in_biweek(today)
    return philosophy_day == today


def _pick_from_pool(pool: list[str], today: date) -> str:
    strategy = os.environ.get("MESSAGE_STRATEGY", "random").lower()
    if strategy == "random":
        return random.choice(pool)
    return pool[today.toordinal() % len(pool)]


def pick_management_quote(today: date) -> str:
    """Weekly management wisdom from renowned leaders and authors."""
    return _pick_from_pool(MANAGEMENT_QUOTES, today)


def pick_philosophy_quote(today: date) -> str:
    """Biweekly philosophy wisdom from renowned philosophers."""
    return _pick_from_pool(PHILOSOPHY_QUOTES, today)


def pick_static_message(today: date) -> str:
    """Scheme A: pick a creative greeting from the static database."""
    message = _pick_from_pool(MESSAGES, today)
    weekday_name = WEEKDAY_NAMES[today.weekday()]
    return message.replace("{weekday}", weekday_name)


def generate_ai_message(today: date) -> str:
    """Scheme B: call LLM API to generate a creative English morning greeting."""
    provider = os.environ.get("AI_PROVIDER", "openai").lower()
    weekday_name = WEEKDAY_NAMES[today.weekday()]

    weekday_themes = {
        0: "Monday blues — energize the team with wit and encouragement",
        1: "Tuesday momentum — steady progress and team spirit",
        2: "Wednesday midweek — humor and a fresh perspective",
        3: "Thursday push — weekend is near, finish strong",
        4: "Friday celebration — acknowledge the week's effort",
    }
    theme = weekday_themes.get(today.weekday(), "general weekday greeting")

    prompt = (
        f"Today is {today.strftime('%B %d, %Y')}, {weekday_name}. "
        f"Theme: {theme}. "
        "Write a creative, witty morning greeting for colleagues in English. "
        "Be warm, original, and slightly playful — avoid clichés. "
        "You may include one emoji. Keep it under 50 words. "
        "Output the greeting only, no title."
    )

    if provider == "gemini":
        return _call_gemini(prompt)
    return _call_openai(prompt)


def _call_openai(prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("使用 AI 方案需要設定 OPENAI_API_KEY 環境變數")

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a beloved office morning-bot who writes creative, "
                        "witty English greetings that make colleagues smile."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 200,
            "temperature": 0.9,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def _call_gemini(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("使用 Gemini 方案需要設定 GEMINI_API_KEY 環境變數")

    model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 200,
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def build_message(today: date) -> tuple[str, str]:
    """
    Build today's message. Returns (message, source).
    Sources: management | philosophy | ai | static
    """
    if is_management_quote_day(today):
        logger.info("Management quote day — famous leader quote")
        return pick_management_quote(today), "management"

    if is_philosophy_quote_day(today):
        logger.info("Philosophy quote day — famous philosopher quote")
        return pick_philosophy_quote(today), "philosophy"

    if should_use_ai(today):
        logger.info("AI-generated creative message")
        try:
            return generate_ai_message(today), "ai"
        except Exception:
            logger.warning("AI failed — falling back to static message", exc_info=True)
            return pick_static_message(today), "static"

    logger.info("Static creative message")
    return pick_static_message(today), "static"


def _is_powerautomate_webhook(webhook_url: str) -> bool:
    return "powerplatform.com" in webhook_url or "powerautomate" in webhook_url


def _resolve_webhook_format(webhook_url: str) -> str:
    """Resolve payload format: adaptive, messagecard, or simple."""
    fmt = os.environ.get("TEAMS_WEBHOOK_FORMAT", "auto").lower()
    if fmt != "auto":
        return fmt
    if _is_powerautomate_webhook(webhook_url):
        return "adaptive"
    return "messagecard"


def _build_adaptive_card(
    title: str,
    subtitle: str,
    message: str,
    image_url: str | None,
) -> dict:
    """Build Adaptive Card — most reliable image rendering in Teams."""
    body: list[dict] = [
        {
            "type": "TextBlock",
            "text": title,
            "weight": "Bolder",
            "size": "Large",
            "wrap": True,
        },
        {
            "type": "TextBlock",
            "text": subtitle,
            "isSubtle": True,
            "spacing": "Small",
            "wrap": True,
        },
    ]
    if image_url:
        body.append(
            {
                "type": "Image",
                "url": image_url,
                "size": "Stretch",
                "altText": "Today's theme image",
                "spacing": "Medium",
            }
        )
    body.append(
        {
            "type": "TextBlock",
            "text": message,
            "wrap": True,
            "spacing": "Medium",
        }
    )
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": body,
    }


def _wrap_adaptive_card(card: dict) -> dict:
    """Teams / Power Automate standard envelope for Adaptive Cards."""
    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card,
            }
        ],
    }


def _build_teams_payload(
    message: str,
    today: date,
    source: str,
    image_url: str | None,
    webhook_url: str,
) -> dict:
    """Build payload for Adaptive Card, MessageCard, or plain text."""
    weekday_name = WEEKDAY_NAMES[today.weekday()]
    badges = {
        "ai": " ✨ AI Crafted",
        "management": " 💼 Management Moment",
        "philosophy": " 🪶 Philosophy Moment",
    }
    badge = badges.get(source, "")
    title = f"☀️ Good Morning! Happy {weekday_name}{badge}"
    subtitle = today.strftime("%B %d, %Y")

    webhook_format = _resolve_webhook_format(webhook_url)

    if webhook_format == "simple":
        body = f"**{title}**\n_{subtitle}_\n\n{message}"
        if image_url:
            body += f"\n\n![Today's Theme]({image_url})"
        return {"text": body}

    if webhook_format == "adaptive":
        card = _build_adaptive_card(title, subtitle, message, image_url)
        payload = _wrap_adaptive_card(card)
        # Extra fields for Power Automate templates that map individual fields
        payload["title"] = title
        payload["text"] = message
        payload["subtitle"] = subtitle
        if image_url:
            payload["image"] = image_url
            payload["imageUrl"] = image_url
        payload["card"] = card
        # Power Automate webhook template checks Body?['Attachments'] (capital A)
        if payload.get("attachments"):
            payload["Attachments"] = payload["attachments"]
        return payload

    theme_colors = {
        "static": "0078D4",
        "ai": "6264A7",
        "management": "C19A6B",
        "philosophy": "2D6A4F",
    }
    section: dict = {
        "activityTitle": title,
        "activitySubtitle": subtitle,
        "text": message,
    }
    if image_url:
        section["images"] = [{"image": image_url, "title": "Today's Theme"}]

    return {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": theme_colors.get(source, "0078D4"),
        "summary": f"Morning Boost — {today.isoformat()}",
        "sections": [section],
    }


def send_to_teams(
    message: str,
    today: date,
    source: str = "static",
    image_url: str | None = None,
) -> None:
    """Send message to Teams via Incoming Webhook or Power Automate."""
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError("Please set TEAMS_WEBHOOK_URL environment variable")

    payload = _build_teams_payload(message, today, source, image_url, webhook_url)

    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=15,
    )
    response.raise_for_status()
    logger.info("Message sent to Teams!")


def run_for_date(today: date) -> int:
    """執行指定日期的推播。"""
    skip_check = os.environ.get("SKIP_WORKDAY_CHECK", "").lower() == "true"
    if not skip_check and not is_workday(today):
        logger.info("Non-workday — exiting.")
        return 0

    message, source = build_message(today)
    image_url = find_theme_image(today, message, source)
    if image_url:
        logger.info("Theme image found")
    else:
        logger.info("No image found — text only")

    logger.info("Message (%s): %s", source, message)
    send_to_teams(message, today, source, image_url)
    return 0


def main() -> int:
    today = get_today()
    logger.info("Taiwan time date: %s", today.isoformat())

    try:
        return run_for_date(today)
    except Exception:
        logger.exception("發送失敗")
        return 1


if __name__ == "__main__":
    sys.exit(main())

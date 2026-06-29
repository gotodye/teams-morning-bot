#!/usr/bin/env python3
"""Teams 晨間推播機器人 — 週一至週五自動發送正能量問候（排除台灣國定假日）。"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import holidays
import requests
from dotenv import load_dotenv

from articles import pick_article
from interactions import pick_interaction
from content_batch import (
    half_year_key,
    pick_management as batch_pick_management,
    pick_philosophy as batch_pick_philosophy,
    pick_static as batch_pick_static,
)
from messages import (
    build_card_subtitle,
    build_card_title,
)
from static_messages import StaticPick
from image_search import find_theme_image
from news import find_major_news
from telegram_delivery import send_to_telegram, telegram_configured, telegram_status_line

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
PLACEHOLDER_WEBHOOK_URL = (
    "https://prod-00.eastus.logic.azure.com/workflows/validate-only-placeholder"
)


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


def get_week_key(today: date) -> str:
    """ISO calendar week identifier."""
    year, week, _ = today.isocalendar()
    return f"{year}-W{week:02d}"


def get_week_workdays(today: date) -> list[date]:
    """List all workdays in the current ISO calendar week (Mon–Sun)."""
    year, week, _ = today.isocalendar()
    monday = date.fromisocalendar(year, week, 1)
    tw_holidays = get_tw_holidays(monday.year, (monday + timedelta(days=6)).year)
    return [
        monday + timedelta(days=offset)
        for offset in range(7)
        if is_tw_workday(day := monday + timedelta(days=offset), tw_holidays)
    ]


def _management_days_in_week(today: date) -> set[date]:
    mgmt_weekday = int(
        os.environ.get("MANAGEMENT_QUOTE_WEEKDAY", DEFAULT_MANAGEMENT_QUOTE_WEEKDAY)
    )
    return {d for d in get_week_workdays(today) if d.weekday() == mgmt_weekday}


def get_article_day_in_week(today: date) -> date | None:
    """Pick one workday per week for article insight summaries."""
    return _pick_week_slot(today, "article", _management_days_in_week(today))


def get_ai_day_in_week(today: date) -> date | None:
    """Pick one workday per week for AI-generated messages."""
    excluded = _management_days_in_week(today)
    article_day = _pick_week_slot(today, "article", excluded)
    if article_day:
        excluded.add(article_day)
    return _pick_week_slot(today, "ai", excluded)


def _pick_week_slot(today: date, slot: str, excluded: set[date]) -> date | None:
    candidates = [d for d in get_week_workdays(today) if d not in excluded]
    if not candidates:
        return None
    seed = hashlib.md5(f"{get_week_key(today)}:{slot}".encode()).hexdigest()
    return candidates[int(seed, 16) % len(candidates)]


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


def _pick_biweek_slot(today: date, slot: str, excluded: set[date]) -> date | None:
    workdays = [d for d in get_biweek_workdays(today) if d not in excluded]
    if not workdays:
        return None
    seed = hashlib.md5(f"{get_biweek_key(today)}:{slot}".encode()).hexdigest()
    return workdays[int(seed, 16) % len(workdays)]


def get_biweek_special_day(today: date, slot: str) -> date | None:
    """Pick one workday per biweek for a special slot (legacy / ai biweekly strategy)."""
    return _pick_biweek_slot(today, slot, set())


def get_ai_day_in_biweek(today: date) -> date | None:
    """Pick one workday per biweek for AI-generated messages."""
    return _pick_biweek_slot(today, "ai", set())


def get_philosophy_day_in_biweek(today: date) -> date | None:
    """Pick one workday per biweek for philosopher quotes."""
    excluded: set[date] = set()
    article_day = get_article_day_in_week(today)
    if article_day:
        excluded.add(article_day)
    return _pick_biweek_slot(today, "philosophy", excluded)


def get_interaction_day_in_biweek(today: date) -> date | None:
    """Pick one workday per biweek for channel interaction prompts."""
    excluded: set[date] = set()
    article_day = get_article_day_in_week(today)
    if article_day:
        excluded.add(article_day)
    philosophy_day = _pick_biweek_slot(today, "philosophy", excluded)
    if philosophy_day:
        excluded.add(philosophy_day)
    return _pick_biweek_slot(today, "interaction", excluded)


def should_use_ai(today: date) -> bool:
    """
    判斷今天是否使用方案 B（AI 生成）。
    預設每週一個工作日；亦可透過環境變數調整或強制指定。
    """
    forced = os.environ.get("FORCE_MESSAGE_TYPE", "").lower()
    if forced == "ai":
        return True
    if forced in ("static", "management", "philosophy", "article", "interaction"):
        return False

    mode = os.environ.get("MESSAGE_MODE", "mixed").lower()
    if mode == "static":
        return False
    if mode == "ai":
        return True

    strategy = os.environ.get("AI_SCHEDULE_STRATEGY", "weekly").lower()
    if strategy == "workday_interval":
        interval = int(os.environ.get("AI_WORKDAY_INTERVAL", DEFAULT_AI_WORKDAY_INTERVAL))
        workday_number = count_workdays_since(date(2024, 1, 1), today)
        return workday_number % interval == 0

    if strategy == "biweekly":
        ai_day = get_ai_day_in_biweek(today)
        return ai_day == today

    ai_day = get_ai_day_in_week(today)
    return ai_day == today


def is_article_insight_day(today: date) -> bool:
    """Once per week: famous article summary with link."""
    forced = os.environ.get("FORCE_MESSAGE_TYPE", "").lower()
    if forced == "article":
        return True
    if forced in ("ai", "static", "management", "philosophy", "interaction"):
        return False

    article_day = get_article_day_in_week(today)
    return article_day == today


def is_interaction_day(today: date) -> bool:
    """Once per biweek: invite the channel to reply in-thread (occasionally Forms)."""
    forced = os.environ.get("FORCE_MESSAGE_TYPE", "").lower()
    if forced == "interaction":
        return True
    if forced in ("ai", "static", "management", "philosophy", "article"):
        return False

    interaction_day = get_interaction_day_in_biweek(today)
    return interaction_day == today


def is_management_quote_day(today: date) -> bool:
    """Once per week: management quote day for leadership, mindset, and work skills."""
    forced = os.environ.get("FORCE_MESSAGE_TYPE", "").lower()
    if forced == "management":
        return True
    if forced in ("ai", "static", "philosophy", "article", "interaction"):
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
    if forced in ("ai", "static", "management", "article", "interaction"):
        return False

    philosophy_day = get_philosophy_day_in_biweek(today)
    return philosophy_day == today


def resolve_message_source(today: date) -> str | None:
    """
    Return the scheduled message source for a calendar day.
    Mirrors build_message() priority without generating text.
    Returns None for non-workdays.
    """
    if not is_workday(today):
        return None
    if is_management_quote_day(today):
        return "management"
    if is_article_insight_day(today):
        return "article"
    if is_philosophy_quote_day(today):
        return "philosophy"
    if is_interaction_day(today):
        return "interaction"
    if should_use_ai(today):
        return "ai"
    return "static"


def pick_management_quote(today: date) -> str:
    """Weekly management wisdom — half-year batch, sequential, no repeats within period."""
    return batch_pick_management(today)


def pick_philosophy_quote(today: date) -> str:
    """Biweekly philosophy — half-year batch, sequential."""
    return batch_pick_philosophy(today)


def pick_static_message_text(today: date) -> StaticPick:
    """Static B+ — half-year batch, sequential."""
    return batch_pick_static(today)


def _static_fallback(today: date) -> tuple[str, str, dict[str, str]]:
    pick = pick_static_message_text(today)
    return pick.text, "static", _image_meta_from_pick(pick)


def _image_meta_from_pick(pick: StaticPick) -> dict[str, str]:
    meta: dict[str, str] = {"static_format": pick.static_format}
    if pick.mood:
        meta["mood"] = pick.mood
    if pick.image_query:
        meta["image_query"] = pick.image_query
    return meta


def build_message(today: date) -> tuple[str, str, dict[str, str]]:
    """
    Build today's message. Returns (message, source, image_meta).
    Sources: management | article | philosophy | interaction | ai | static
    """
    if is_management_quote_day(today):
        logger.info("Management quote day — famous leader quote")
        return pick_management_quote(today), "management", {}

    if is_article_insight_day(today):
        logger.info("Article insight day — famous article summary")
        try:
            return generate_article_insight(today), "article", {}
        except Exception:
            logger.warning("Article insight failed — falling back to static", exc_info=True)
            return _static_fallback(today)

    if is_philosophy_quote_day(today):
        logger.info("Philosophy quote day — famous philosopher quote")
        return pick_philosophy_quote(today), "philosophy", {}

    if is_interaction_day(today):
        logger.info("Interaction day — biweekly channel prompt")
        return build_interaction_message(today), "interaction", {}

    if should_use_ai(today):
        logger.info("AI-generated creative message")
        try:
            return generate_ai_message(today), "ai", {}
        except Exception:
            logger.warning("AI failed — falling back to static message", exc_info=True)
            return _static_fallback(today)

    logger.info("Static creative message (B+) [%s]", half_year_key(today))
    return _static_fallback(today)


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


def _extract_gemini_text(data: dict) -> str:
    """Extract visible text from a Gemini generateContent response."""
    candidate = data["candidates"][0]
    finish_reason = candidate.get("finishReason")
    if finish_reason == "MAX_TOKENS":
        logger.warning("Gemini response truncated (finishReason=MAX_TOKENS)")

    parts = candidate.get("content", {}).get("parts", [])
    text = "".join(
        part["text"]
        for part in parts
        if part.get("text") and not part.get("thought")
    ).strip()
    if not text:
        raise RuntimeError(
            f"Gemini returned empty text (finishReason={finish_reason})"
        )
    return text


def _gemini_generation_config() -> dict:
    """Generation settings tuned for short greetings on Gemini 3.x."""
    model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    config: dict = {
        "temperature": 0.9,
        "maxOutputTokens": 1024,
    }
    # Gemini 3 models spend thinking tokens from the same output budget.
    if model.startswith("gemini-3"):
        config["thinkingConfig"] = {"thinkingLevel": "minimal"}
    else:
        config["thinkingConfig"] = {"thinkingBudget": 0}
    return config


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
            "generationConfig": _gemini_generation_config(),
        },
        timeout=30,
    )
    response.raise_for_status()
    return _extract_gemini_text(response.json())


def _truncate_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text.strip()
    return " ".join(words[:max_words]).rstrip(".,;:") + "…"


def generate_article_insight(today: date) -> str:
    """Weekly article summary with link (summary capped at 100 words)."""
    article = pick_article(today)
    prompt = (
        f'Write a concise English summary of the article "{article["title"]}" '
        f'from {article["source"]}. Topic: {article["topic"]}. '
        "Highlight one practical takeaway for work performance or a positive life "
        "mindset. Maximum 100 words. Output the summary only — no title, no link, "
        "no markdown."
    )

    try:
        provider = os.environ.get("AI_PROVIDER", "openai").lower()
        if provider == "gemini":
            summary = _call_gemini(prompt)
        else:
            summary = _call_openai(prompt)
    except Exception:
        logger.warning("Article summary AI failed — using fallback", exc_info=True)
        summary = article["fallback_summary"]

    summary = _truncate_words(summary, 100)
    return (
        f'📚 **{article["title"]}**\n'
        f'_{article["source"]}_\n\n'
        f"{summary}\n\n"
        f'📖 Read more: {article["url"]}'
    )


def build_interaction_message(today: date) -> str:
    """Biweekly team interaction — reply in channel; Forms link when configured."""
    interaction = pick_interaction(today)
    forms_url = os.environ.get("INTERACTION_FORMS_URL", "").strip()

    use_forms = interaction["kind"] == "forms" and forms_url
    body = interaction["body"] if use_forms else (
        interaction["channel_fallback"] or interaction["body"]
    )

    lines = [
        f'📣 **{interaction["headline"]}**',
        "",
        body,
        "",
    ]

    if use_forms:
        lines.extend([
            f"📋 **Quick pulse (30 sec):** {forms_url}",
            "",
            "_Optional: share a highlight in the thread too — we read every reply!_",
        ])
    else:
        if interaction["kind"] == "forms" and not forms_url:
            logger.info(
                "INTERACTION_FORMS_URL not set — using channel-reply fallback"
            )
        lines.append(
            "👇 **Reply in this thread** — read each other's answers when you have a minute!"
        )

    return "\n".join(lines)


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
    *,
    static_format: str | None = None,
) -> dict:
    """Build payload for Adaptive Card, MessageCard, or plain text."""
    weekday_name = WEEKDAY_NAMES[today.weekday()]
    title = build_card_title(
        today, source, weekday_name, static_format=static_format
    )
    subtitle = build_card_subtitle(
        today, source, weekday_name, static_format=static_format
    )

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
        "article": "E85D04",
        "interaction": "5B5FC7",
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
    *,
    static_format: str | None = None,
) -> None:
    """Send message to Teams via Incoming Webhook or Power Automate."""
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError("Please set TEAMS_WEBHOOK_URL environment variable")

    payload = _build_teams_payload(
        message, today, source, image_url, webhook_url, static_format=static_format
    )

    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=15,
    )
    response.raise_for_status()
    logger.info("Message sent to Teams!")


def _would_use_ai_today(today: date) -> bool:
    """Whether build_message would attempt AI generation for this date."""
    forced = os.environ.get("FORCE_MESSAGE_TYPE", "").lower()
    if forced == "ai":
        return True
    if forced in ("static", "management", "philosophy", "article", "interaction"):
        return False
    if is_management_quote_day(today) or is_philosophy_quote_day(today) or is_article_insight_day(today) or is_interaction_day(today):
        return False
    return should_use_ai(today)


def _audit_configuration(today: date) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for environment and schedule checks."""
    errors: list[str] = []
    warnings: list[str] = []

    webhook = os.environ.get("TEAMS_WEBHOOK_URL", "").strip()
    if not webhook:
        warnings.append(
            "TEAMS_WEBHOOK_URL not set — payload preview uses a placeholder URL "
            "(fine for GitHub Actions if the secret is configured there)"
        )
    elif not webhook.startswith("https://"):
        errors.append("TEAMS_WEBHOOK_URL must start with https://")

    provider = os.environ.get("AI_PROVIDER", "openai").lower()
    if _would_use_ai_today(today):
        key_name = "GEMINI_API_KEY" if provider == "gemini" else "OPENAI_API_KEY"
        if not os.environ.get(key_name, "").strip():
            errors.append(f"AI is scheduled today but {key_name} is not set")

    skip_check = os.environ.get("SKIP_WORKDAY_CHECK", "").lower() == "true"
    if not skip_check and not is_workday(today):
        warnings.append(
            f"Today ({today.isoformat()}, {WEEKDAY_NAMES[today.weekday()]}) is not a "
            "workday — a normal run would skip without sending"
        )

    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if tg_token and not tg_chat:
        errors.append("TELEGRAM_BOT_TOKEN is set but TELEGRAM_CHAT_ID is missing")
    elif tg_chat and not tg_token:
        errors.append("TELEGRAM_CHAT_ID is set but TELEGRAM_BOT_TOKEN is missing")
    elif telegram_configured():
        logger.info("Telegram delivery enabled for chat %s", tg_chat)

    return errors, warnings


def _preview_text(text: str, limit: int = 240) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return f"{compact[: limit - 3]}..."


def run_validate_only(today: date) -> int:
    """Exercise the full pipeline without posting to Teams."""
    logger.info("Validate-only mode — no message will be sent to Teams")

    errors, warnings = _audit_configuration(today)
    for warning in warnings:
        logger.warning("Config: %s", warning)
    for error in errors:
        logger.error("Config: %s", error)

    ai_scheduled = _would_use_ai_today(today)

    try:
        message, source, image_meta = build_message(today)
    except Exception:
        logger.exception("build_message failed")
        return 1

    static_format = image_meta.get("static_format") or None

    if ai_scheduled and source != "ai":
        warnings.append("AI was scheduled but fell back to a static message — check API keys or logs above")

    news_appendix = ""
    if os.environ.get("ENABLE_MAJOR_NEWS", "true").lower() != "false":
        try:
            news_appendix = find_major_news(today) or ""
            if news_appendix:
                logger.info("Major news appendix would be appended (%d chars)", len(news_appendix))
            else:
                logger.info("Major news check complete — nothing above threshold")
        except Exception:
            logger.warning("Major news check failed", exc_info=True)
            warnings.append("Major news fetch failed — see log for details")
    else:
        logger.info("Major news disabled (ENABLE_MAJOR_NEWS=false)")

    if news_appendix:
        message += news_appendix

    image_url: str | None = None
    if os.environ.get("ENABLE_IMAGES", "true").lower() != "false":
        try:
            image_url = find_theme_image(
                today,
                message,
                source,
                image_query=image_meta.get("image_query") or None,
                mood=image_meta.get("mood") or None,
            )
            if image_url:
                logger.info("Theme image found: %s", image_url)
            else:
                logger.info("No theme image found — text-only card")
        except Exception:
            logger.warning("Theme image search failed", exc_info=True)
            warnings.append("Image search failed — see log for details")
    else:
        logger.info("Images disabled (ENABLE_IMAGES=false)")

    webhook = os.environ.get("TEAMS_WEBHOOK_URL", "").strip() or PLACEHOLDER_WEBHOOK_URL
    try:
        payload = _build_teams_payload(
            message, today, source, image_url, webhook, static_format=static_format
        )
        json.dumps(payload, ensure_ascii=False)
    except Exception:
        logger.exception("Payload build failed")
        return 1

    webhook_format = _resolve_webhook_format(webhook)
    if webhook_format == "adaptive":
        if payload.get("attachments") and not payload.get("Attachments"):
            errors.append("Adaptive payload missing Attachments alias for Power Automate")
        if not payload.get("card"):
            errors.append("Adaptive payload missing card field")

    logger.info("--- Validation summary ---")
    logger.info("Date: %s (%s)", today.isoformat(), WEEKDAY_NAMES[today.weekday()])
    logger.info("Message source: %s", source)
    if static_format:
        logger.info("Static format: %s", static_format)
    try:
        from content_batch import half_year_key, occurrence_in_half_year

        logger.info("Content batch: %s", half_year_key(today))
        if source in ("management", "philosophy", "article", "interaction", "static"):
            logger.info(
                "Half-year %s occurrence: %d",
                source,
                occurrence_in_half_year(today, source),
            )
    except Exception:
        pass
    logger.info("Webhook format: %s", webhook_format)
    logger.info("Message preview: %s", _preview_text(message))
    logger.info("Image: %s", image_url or "(none)")
    logger.info("Payload keys: %s", ", ".join(sorted(payload.keys())))
    if webhook_format == "adaptive":
        attachment_count = len(payload.get("attachments") or [])
        logger.info("Adaptive attachments: %d", attachment_count)

    for warning in warnings:
        logger.warning("WARN: %s", warning)
    for error in errors:
        logger.error("FAIL: %s", error)

    if errors:
        logger.error("Validation failed (%d error(s), %d warning(s))", len(errors), len(warnings))
        return 1

    logger.info("Validation passed (%d warning(s)) — no message was sent", len(warnings))
    if telegram_configured():
        logger.info("Telegram is configured — would also send to chat %s", os.environ.get("TELEGRAM_CHAT_ID", ""))
    return 0


def run_for_date(today: date) -> int:
    """執行指定日期的推播。"""
    skip_check = os.environ.get("SKIP_WORKDAY_CHECK", "").lower() == "true"
    if not skip_check and not is_workday(today):
        logger.info("Non-workday — exiting.")
        return 0

    message, source, image_meta = build_message(today)
    static_format = image_meta.get("static_format") or None
    news_appendix = find_major_news(today)
    if news_appendix:
        message += news_appendix
        logger.info("Major news appended")

    image_url = find_theme_image(
        today,
        message,
        source,
        image_query=image_meta.get("image_query") or None,
        mood=image_meta.get("mood") or None,
    )
    if image_url:
        logger.info("Theme image found")
    else:
        logger.info("No image found — text only")

    logger.info("Message (%s): %s", source, message)
    logger.info(telegram_status_line())
    send_to_teams(message, today, source, image_url, static_format=static_format)

    if telegram_configured():
        weekday_name = WEEKDAY_NAMES[today.weekday()]
        send_to_telegram(
            message,
            today,
            source,
            image_url,
            weekday_name=weekday_name,
            static_format=static_format,
        )
    else:
        logger.warning(telegram_status_line())

    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Teams morning bot — weekday greetings to Microsoft Teams.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Run the full pipeline (message, news, image, payload) without sending to Teams",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    today = get_today()
    logger.info("Taiwan time date: %s", today.isoformat())

    if args.validate_only:
        os.environ.setdefault("SKIP_WORKDAY_CHECK", "true")
        return run_validate_only(today)

    try:
        return run_for_date(today)
    except Exception:
        logger.exception("發送失敗")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""Fetch and score major breaking news for TW, VN, ID, and HK."""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from email.utils import parsedate_to_datetime
from typing import Iterable
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

import requests

logger = logging.getLogger(__name__)

TZ_TAIWAN = ZoneInfo("Asia/Taipei")
DEFAULT_MAJOR_NEWS_THRESHOLD = 70
DEFAULT_NEWS_CUTOFF_HOUR = 9
DEFAULT_NEWS_START_HOUR = 21

REGION_LABELS = {
    "TW": "Taiwan",
    "HK": "Hong Kong",
    "VN": "Vietnam",
    "ID": "Indonesia",
}

REGION_FEEDS = {
    "TW": "https://news.google.com/rss?hl=en&gl=TW&ceid=TW:en",
    "HK": "https://news.google.com/rss?hl=en&gl=HK&ceid=HK:en",
    "VN": "https://news.google.com/rss?hl=en&gl=VN&ceid=VN:en",
    "ID": "https://news.google.com/rss?hl=en&gl=ID&ceid=ID:en",
}

GLOBAL_FEEDS = {
    "Reuters World": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
    "Reuters Business": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
}

MAJOR_KEYWORDS: dict[str, int] = {
    "earthquake": 35,
    "typhoon": 35,
    "hurricane": 35,
    "flood": 30,
    "tsunami": 35,
    "wildfire": 28,
    "state of emergency": 35,
    "emergency declared": 32,
    "evacuation": 28,
    "war": 30,
    "invasion": 32,
    "military": 22,
    "sanction": 24,
    "terror": 30,
    "explosion": 26,
    "collapse": 24,
    "blackout": 24,
    "outage": 22,
    "shutdown": 22,
    "suspended trading": 30,
    "market crash": 32,
    "bank failure": 32,
    "bankruptcy": 24,
    "assassination": 30,
    "resigns": 18,
    "impeach": 22,
    "coup": 30,
    "strike": 18,
    "riot": 22,
    "protest": 14,
    "border closure": 26,
    "airport closed": 26,
    "flight cancellations": 22,
    "cyberattack": 24,
    "data breach": 18,
    "pandemic": 24,
    "outbreak": 20,
    "lockdown": 24,
    "tariff": 18,
    "interest rate hike": 20,
    "central bank": 16,
    "missile": 28,
    "nuclear": 26,
}

EXCLUDE_KEYWORDS = (
    "celebrity",
    "gossip",
    "trailer",
    "box office",
    "premiere",
    "match",
    "game",
    "championship",
    "score",
    "goal",
    "transfer rumor",
    "dating",
    "fashion week",
    "recipe",
    "horoscope",
    "lottery",
    "opinion:",
    "editorial:",
    "how to",
    "review:",
)

REGION_TERMS: dict[str, tuple[str, ...]] = {
    "TW": ("taiwan", "taipei", "tsmc", "formosa"),
    "HK": ("hong kong", "hkma", "hang seng"),
    "VN": ("vietnam", "hanoi", "ho chi minh", "saigon"),
    "ID": ("indonesia", "jakarta", "java", "bali"),
}


@dataclass(frozen=True)
class NewsItem:
    title: str
    url: str
    published: datetime
    source: str
    region: str


def _enabled() -> bool:
    return os.environ.get("ENABLE_MAJOR_NEWS", "true").lower() != "false"


def get_news_window(now: datetime | None = None) -> tuple[datetime, datetime]:
    """Previous day 21:00 through today 09:00, Taiwan time."""
    now = now or datetime.now(TZ_TAIWAN)
    if now.tzinfo is None:
        now = now.replace(tzinfo=TZ_TAIWAN)
    else:
        now = now.astimezone(TZ_TAIWAN)

    cutoff_hour = int(os.environ.get("NEWS_CUTOFF_HOUR", DEFAULT_NEWS_CUTOFF_HOUR))
    start_hour = int(os.environ.get("NEWS_START_HOUR", DEFAULT_NEWS_START_HOUR))

    end = datetime.combine(now.date(), time(cutoff_hour, 0), tzinfo=TZ_TAIWAN)
    start = datetime.combine(now.date() - timedelta(days=1), time(start_hour, 0), tzinfo=TZ_TAIWAN)
    return start, end


def _parse_published(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=TZ_TAIWAN)
        return parsed.astimezone(TZ_TAIWAN)
    except (TypeError, ValueError):
        return None


def _normalize_title(title: str) -> str:
    cleaned = re.sub(r"[^\w\s]", " ", title.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def _title_tokens(title: str) -> set[str]:
    stopwords = {
        "the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "after",
        "as", "is", "are", "with", "from", "by", "over", "amid", "says", "say",
    }
    return {token for token in _normalize_title(title).split() if token not in stopwords and len(token) > 2}


def _titles_match(a: str, b: str) -> bool:
    tokens_a = _title_tokens(a)
    tokens_b = _title_tokens(b)
    if not tokens_a or not tokens_b:
        return False
    overlap = len(tokens_a & tokens_b)
    return overlap >= min(3, max(2, min(len(tokens_a), len(tokens_b)) // 2))


def _fetch_rss(url: str, source: str, region: str) -> list[NewsItem]:
    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "teams-morning-bot/1.0"},
    )
    response.raise_for_status()
    root = ElementTree.fromstring(response.content)
    channel = root.find("channel")
    if channel is None:
        return []

    items: list[NewsItem] = []
    for item in channel.findall("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        published = _parse_published(item.findtext("pubDate") or "")
        if not title or not link or published is None:
            continue
        items.append(
            NewsItem(
                title=title,
                url=link,
                published=published,
                source=source,
                region=region,
            )
        )
    return items


def _fetch_all_items() -> list[NewsItem]:
    items: list[NewsItem] = []
    for region, feed_url in REGION_FEEDS.items():
        try:
            fetched = _fetch_rss(feed_url, f"Google News {REGION_LABELS[region]}", region)
            items.extend(fetched)
            logger.info("Fetched %s regional headlines from %s", len(fetched), region)
        except Exception:
            logger.warning("Failed to fetch Google News feed for %s", region, exc_info=True)

    for source, feed_url in GLOBAL_FEEDS.items():
        try:
            fetched = _fetch_rss(feed_url, source, "GLOBAL")
            items.extend(fetched)
            logger.info("Fetched %s headlines from %s", len(fetched), source)
        except Exception:
            logger.warning("Failed to fetch global feed %s", source, exc_info=True)

    return items


def _in_window(item: NewsItem, start: datetime, end: datetime) -> bool:
    return start <= item.published <= end


def _matches_region(item: NewsItem) -> str | None:
    if item.region in REGION_LABELS:
        return item.region

    haystack = item.title.lower()
    for region, terms in REGION_TERMS.items():
        if any(term in haystack for term in terms):
            return region
    return None


def _keyword_score(title: str) -> tuple[int, list[str]]:
    lowered = title.lower()
    score = 0
    hits: list[str] = []
    for keyword, weight in MAJOR_KEYWORDS.items():
        if keyword in lowered:
            score += weight
            hits.append(keyword)
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in lowered:
            score -= 25
    return score, hits


def _source_confirmation_score(item: NewsItem, items: Iterable[NewsItem]) -> int:
    confirmations = 0
    for other in items:
        if other.url == item.url:
            continue
        if other.source == item.source:
            continue
        if _titles_match(item.title, other.title):
            confirmations += 1
    return min(20, confirmations * 10)


def score_news_item(item: NewsItem, items: list[NewsItem]) -> tuple[int, list[str]]:
    score, hits = _keyword_score(item.title)
    reasons = list(hits)

    region = _matches_region(item)
    if region:
        score += 8
        reasons.append(f"region:{REGION_LABELS[region]}")

    confirmations = _source_confirmation_score(item, items)
    if confirmations:
        score += confirmations
        reasons.append("multi-source")

    if item.source.startswith("Reuters"):
        score += 8
        reasons.append("reuters")

    return score, reasons


def _pick_best_item(items: list[NewsItem], threshold: int) -> NewsItem | None:
    if not items:
        return None

    scored: list[tuple[int, NewsItem, list[str]]] = []
    for item in items:
        score, reasons = score_news_item(item, items)
        scored.append((score, item, reasons))
        logger.info("News score %s (%s): %s", score, item.source, item.title)

    scored.sort(key=lambda row: (row[0], row[1].published), reverse=True)
    best_score, best_item, best_reasons = scored[0]
    if best_score < threshold:
        logger.info("No major news above threshold %s (best=%s)", threshold, best_score)
        return None

    logger.info(
        "Selected major news (%s): %s | reasons=%s",
        best_score,
        best_item.title,
        ", ".join(best_reasons),
    )
    return best_item


def _format_news_appendix(item: NewsItem) -> str:
    region = _matches_region(item) or item.region
    region_label = REGION_LABELS.get(region, "Asia-Pacific")
    return (
        "\n\n---\n\n"
        f"📰 **Major News — {region_label}**\n"
        f"{item.title}\n"
        f"_Source: {item.source}_"
    )


def find_major_news(today: date | None = None) -> str | None:
    """
    Return an English appendix for a major news item, or None if nothing qualifies.
    """
    if not _enabled():
        logger.info("Major news disabled")
        return None

    now = datetime.now(TZ_TAIWAN)
    if today and today != now.date():
        now = datetime.combine(today, time(8, 0), tzinfo=TZ_TAIWAN)

    start, end = get_news_window(now)
    threshold = int(os.environ.get("MAJOR_NEWS_THRESHOLD", DEFAULT_MAJOR_NEWS_THRESHOLD))
    logger.info("Major news window: %s to %s", start.isoformat(), end.isoformat())

    try:
        all_items = _fetch_all_items()
    except Exception:
        logger.warning("Major news fetch failed", exc_info=True)
        return None

    candidates = [
        item
        for item in all_items
        if _in_window(item, start, end) and _matches_region(item) is not None
    ]
    logger.info("Major news candidates in window: %s", len(candidates))

    best = _pick_best_item(candidates, threshold)
    if not best:
        return None
    return _format_news_appendix(best)

"""依訊息主題從網路搜尋合適的晨間配圖。"""

from __future__ import annotations

import hashlib
import logging
import os
import random
from datetime import date

import requests

logger = logging.getLogger(__name__)

WEEKDAY_KEYWORDS: dict[int, list[str]] = {
    0: ["monday motivation", "sunrise office", "fresh start"],
    1: ["tuesday coffee", "morning workspace", "teamwork"],
    2: ["wednesday energy", "midweek smile", "happy office"],
    3: ["thursday motivation", "almost weekend", "sunset hope"],
    4: ["friday celebration", "weekend vibes", "happy friday office"],
}

THEME_KEYWORDS: list[list[str]] = [
    ["sunrise", "golden morning", "new day"],
    ["coffee cup", "morning light", "cozy office"],
    ["sunflower", "positive energy", "bright day"],
    ["teamwork", "colleagues smile", "office plants"],
    ["rainbow", "hope", "blue sky"],
    ["cute animal", "funny pet", "happy dog"],
    ["nature landscape", "green hills", "peaceful morning"],
    ["books", "learning", "curiosity"],
]

MANAGEMENT_KEYWORDS: list[str] = [
    "leadership teamwork office",
    "business strategy success",
    "professional growth mindset",
    "executive coaching inspiration",
    "collaboration meeting professional",
]

PHILOSOPHY_KEYWORDS: list[str] = [
    "ancient philosophy statue",
    "meditation wisdom nature",
    "classical greek philosophy",
    "stoic philosophy sunrise",
    "library books wisdom thoughtful",
]

ARTICLE_KEYWORDS: list[str] = [
    "reading book coffee morning",
    "library study inspiration",
    "open book sunlight desk",
    "learning growth professional",
    "journal notebook thoughtful",
]

INTERACTION_KEYWORDS: list[str] = [
    "team collaboration chat office",
    "colleagues talking coffee break",
    "group discussion teamwork",
    "friendly workplace conversation",
    "team meeting smile diverse",
]


def build_search_query(today: date, message: str, source: str) -> str:
    """Build image search keywords from weekday, message, and source type."""
    if source == "management":
        digest = int(hashlib.md5(message.encode()).hexdigest(), 16)
        return MANAGEMENT_KEYWORDS[digest % len(MANAGEMENT_KEYWORDS)]

    if source == "philosophy":
        digest = int(hashlib.md5(message.encode()).hexdigest(), 16)
        return PHILOSOPHY_KEYWORDS[digest % len(PHILOSOPHY_KEYWORDS)]

    if source == "article":
        digest = int(hashlib.md5(message.encode()).hexdigest(), 16)
        return ARTICLE_KEYWORDS[digest % len(ARTICLE_KEYWORDS)]

    if source == "interaction":
        digest = int(hashlib.md5(message.encode()).hexdigest(), 16)
        return INTERACTION_KEYWORDS[digest % len(INTERACTION_KEYWORDS)]

    weekday_pool = WEEKDAY_KEYWORDS.get(today.weekday(), ["morning greeting"])
    digest = int(hashlib.md5(message.encode()).hexdigest(), 16)
    theme_pool = THEME_KEYWORDS[digest % len(THEME_KEYWORDS)]

    weekday_kw = weekday_pool[digest % len(weekday_pool)]
    theme_kw = theme_pool[(digest // len(THEME_KEYWORDS)) % len(theme_pool)]

    if source == "ai":
        return f"{weekday_kw} {theme_kw}"
    return f"{weekday_kw} {theme_kw} cheerful"


def _search_unsplash(query: str) -> str | None:
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not access_key:
        return None

    response = requests.get(
        "https://api.unsplash.com/search/photos",
        params={"query": query, "per_page": 10, "orientation": "landscape"},
        headers={"Authorization": f"Client-ID {access_key}"},
        timeout=15,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        return None

    photo = random.choice(results[:5])
    return photo["urls"]["regular"]


def _search_pexels(query: str) -> str | None:
    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        return None

    response = requests.get(
        "https://api.pexels.com/v1/search",
        params={"query": query, "per_page": 10, "orientation": "landscape"},
        headers={"Authorization": api_key},
        timeout=15,
    )
    response.raise_for_status()
    results = response.json().get("photos", [])
    if not results:
        return None

    photo = random.choice(results[:5])
    return photo["src"]["large"]


def _search_wikimedia(query: str) -> str | None:
    """免 API Key 的備援圖片來源（Wikimedia Commons）。"""
    response = requests.get(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action": "query",
            "generator": "search",
            "gsrsearch": f"{query} filetype:bitmap",
            "gsrnamespace": "6",
            "gsrlimit": "10",
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": "800",
            "format": "json",
        },
        timeout=15,
        headers={"User-Agent": "teams-morning-bot/1.0"},
    )
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {})
    candidates: list[str] = []
    for page in pages.values():
        imageinfo = page.get("imageinfo", [])
        if imageinfo and imageinfo[0].get("thumburl"):
            candidates.append(imageinfo[0]["thumburl"])

    if not candidates:
        return None
    return random.choice(candidates)


def _fallback_picsum(query: str) -> str:
    """Reliable public image fallback when search APIs are unavailable."""
    seed = hashlib.md5(query.encode()).hexdigest()[:12]
    return f"https://picsum.photos/seed/morning-{seed}/800/400"


def validate_image_url(url: str) -> bool:
    """Verify image URL is reachable before sending to Teams."""
    headers = {"User-Agent": "teams-morning-bot/1.0"}
    try:
        response = requests.head(
            url, timeout=8, allow_redirects=True, headers=headers
        )
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            if content_type.startswith("image/"):
                return True

        # Some CDNs (e.g. Wikimedia) reject HEAD — try a lightweight GET.
        response = requests.get(
            url,
            timeout=8,
            allow_redirects=True,
            stream=True,
            headers=headers,
        )
        content_type = response.headers.get("Content-Type", "")
        return response.status_code == 200 and content_type.startswith("image/")
    except Exception:
        return False


def find_theme_image(today: date, message: str, source: str) -> str | None:
    """
    搜尋符合主題的公開圖片 URL。
    優先順序：Unsplash → Pexels → Wikimedia Commons → Picsum 備援。
    """
    if os.environ.get("ENABLE_IMAGES", "true").lower() == "false":
        return None

    query = build_search_query(today, message, source)
    logger.info("Image search keywords: %s", query)

    providers = [
        ("Unsplash", _search_unsplash),
        ("Pexels", _search_pexels),
        ("Wikimedia", _search_wikimedia),
    ]
    for name, search_fn in providers:
        try:
            url = search_fn(query)
            if url and validate_image_url(url):
                logger.info("Image source: %s -> %s", name, url)
                return url
            if url:
                logger.warning("Image URL failed validation, skipping: %s", url)
        except Exception:
            logger.warning("Image search failed (%s)", name, exc_info=True)

    fallback = _fallback_picsum(query)
    if validate_image_url(fallback):
        logger.info("Image source: Picsum fallback -> %s", fallback)
        return fallback

    logger.warning("All image providers failed for query: %s", query)
    return None

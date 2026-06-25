"""Half-year content batches — sequential picks with no repeats within a period."""

from __future__ import annotations

import json
import logging
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from static_messages import StaticPick

logger = logging.getLogger(__name__)

BATCHES_DIR = Path(__file__).resolve().parent / "content" / "batches"
DEFAULT_BATCH_ID = "2026-H1"

_batch_cache: dict[str, dict[str, Any]] = {}


def half_year_key(today: date) -> str:
    """Calendar half-year identifier, e.g. 2026-H1 (Jan–Jun) or 2026-H2 (Jul–Dec)."""
    return f"{today.year}-H{1 if today.month <= 6 else 2}"


def half_year_range(today: date) -> tuple[date, date]:
    if today.month <= 6:
        return date(today.year, 1, 1), date(today.year, 6, 30)
    return date(today.year, 7, 1), date(today.year, 12, 31)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _legacy_batch() -> dict[str, Any]:
    """Build batch dict from legacy Python modules (fallback)."""
    from articles import ARTICLES
    from interactions import INTERACTIONS
    from messages import MANAGEMENT_QUOTES, PHILOSOPHY_QUOTES
    from static_messages import STATIC_BY_WEEKDAY, STATIC_GENERAL

    static: list[dict[str, Any]] = []
    seen: set[str] = set()
    for pool in list(STATIC_BY_WEEKDAY.values()) + [STATIC_GENERAL]:
        for item in pool:
            text = item["text"]
            if text in seen:
                continue
            seen.add(text)
            static.append(dict(item))

    return {
        "management": list(MANAGEMENT_QUOTES),
        "philosophy": list(PHILOSOPHY_QUOTES),
        "static": static,
        "articles": list(ARTICLES),
        "interactions": list(INTERACTIONS),
        "_meta": {"period": "legacy", "source": "python_modules"},
    }


def _write_batch_dir(batch_dir: Path, data: dict[str, Any], period: str) -> None:
    batch_dir.mkdir(parents=True, exist_ok=True)
    for key in ("management", "philosophy", "static", "articles", "interactions"):
        if key in data:
            (batch_dir / f"{key}.json").write_text(
                json.dumps(data[key], ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    manifest = {
        "period": period,
        "exported_on": date.today().isoformat(),
        "source": "content_batch._write_batch_dir",
        "counts": {
            key: len(data[key])
            for key in ("management", "philosophy", "static", "articles", "interactions")
            if key in data
        },
    }
    (batch_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _ensure_batch_on_disk(period: str) -> Path | None:
    """Create batch JSON from legacy pools on first run (Phase 1 bootstrap)."""
    batch_dir = BATCHES_DIR / period
    if batch_dir.is_dir() and (batch_dir / "manifest.json").is_file():
        return batch_dir
    try:
        legacy = _legacy_batch()
        _write_batch_dir(batch_dir, legacy, period)
        logger.info("Created initial content batch at %s", batch_dir)
        return batch_dir
    except Exception:
        logger.exception("Failed to bootstrap content batch %s", period)
        return None


def load_batch(today: date) -> dict[str, Any]:
    """Load the content batch for today's calendar half-year."""
    period = half_year_key(today)
    if period in _batch_cache:
        return _batch_cache[period]

    batch_dir = BATCHES_DIR / period
    if not batch_dir.is_dir():
        if period == DEFAULT_BATCH_ID:
            _ensure_batch_on_disk(period)
            batch_dir = BATCHES_DIR / period
        elif (BATCHES_DIR / DEFAULT_BATCH_ID).is_dir():
            logger.warning(
                "Content batch %s not found — using %s until a new batch is added",
                period,
                DEFAULT_BATCH_ID,
            )
            batch_dir = BATCHES_DIR / DEFAULT_BATCH_ID
        else:
            _ensure_batch_on_disk(DEFAULT_BATCH_ID)
            batch_dir = BATCHES_DIR / DEFAULT_BATCH_ID
            logger.warning(
                "Content batch %s not found — bootstrapped and using %s",
                period,
                DEFAULT_BATCH_ID,
            )

    if not batch_dir.is_dir():
        logger.warning("No batch directory on disk — using in-memory legacy pools")
        data = _legacy_batch()
        data["_meta"] = {"period": "legacy", "source": "python_modules"}
        _batch_cache[period] = data
        return data

    data: dict[str, Any] = {}
    for name in ("management", "philosophy", "static", "articles", "interactions"):
        path = batch_dir / f"{name}.json"
        if path.is_file():
            data[name] = _load_json(path)

    manifest_path = batch_dir / "manifest.json"
    data["_meta"] = _load_json(manifest_path) if manifest_path.is_file() else {"period": period}

    if not data.get("management"):
        logger.warning("Batch %s is incomplete — merging legacy pools", batch_dir.name)
        legacy = _legacy_batch()
        for key, value in legacy.items():
            data.setdefault(key, value)

    _batch_cache[period] = data
    logger.info(
        "Loaded content batch %s (management=%d philosophy=%d static=%d)",
        data["_meta"].get("period", batch_dir.name),
        len(data.get("management", [])),
        len(data.get("philosophy", [])),
        len(data.get("static", [])),
    )
    return data


def occurrence_in_half_year(today: date, source: str) -> int:
    """How many times this source has occurred from half-year start through today."""
    from main import resolve_message_source

    start, _ = half_year_range(today)
    count = 0
    current = start
    while current <= today:
        if resolve_message_source(current) == source:
            count += 1
        current += timedelta(days=1)
    return count


def _sequential_index(today: date, source: str, pool_size: int) -> int:
    n = occurrence_in_half_year(today, source)
    if n <= 0:
        n = 1
    if n > pool_size:
        logger.warning(
            "Half-year %s occurrence %d exceeds pool size %d — wrapping to repeat",
            source,
            n,
            pool_size,
        )
    return (n - 1) % pool_size


def pick_management(today: date) -> str:
    pool = load_batch(today)["management"]
    return pool[_sequential_index(today, "management", len(pool))]


def pick_philosophy(today: date) -> str:
    pool = load_batch(today)["philosophy"]
    return pool[_sequential_index(today, "philosophy", len(pool))]


def pick_static(today: date) -> StaticPick:
    pool = load_batch(today)["static"]
    entry = pool[_sequential_index(today, "static", len(pool))]
    return StaticPick(
        text=entry["text"],
        static_format=entry["format"],
        mood=entry.get("mood"),
        image_query=entry.get("image_query"),
    )


def pick_article_entry(today: date) -> dict[str, Any]:
    pool = load_batch(today)["articles"]
    return pool[_sequential_index(today, "article", len(pool))]


def pick_interaction_entry(today: date) -> dict[str, Any]:
    pool = load_batch(today)["interactions"]
    return pool[_sequential_index(today, "interaction", len(pool))]

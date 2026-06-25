#!/usr/bin/env python3
"""批次發送測試訊息 — 模擬連續數個工作日的晨間推播。"""

from __future__ import annotations

import logging
import os
import sys
import time
from datetime import date, timedelta

from main import build_message, find_theme_image, get_today, is_workday, send_to_teams

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def next_workdays(start: date, count: int) -> list[date]:
    """從 start 起找連續 count 個工作日。"""
    days: list[date] = []
    current = start
    while len(days) < count:
        if is_workday(current):
            days.append(current)
        current += timedelta(days=1)
    return days


def send_test_batch(count: int = 5, delay_seconds: int = 3) -> int:
    dry_run = os.environ.get("DRY_RUN", "").lower() == "true"
    webhook = os.environ.get("TEAMS_WEBHOOK_URL")
    if not webhook and not dry_run:
        logger.error("請先設定 TEAMS_WEBHOOK_URL，或加上 DRY_RUN=true 預覽模式")
        return 1

    start = get_today()
    workdays = next_workdays(start, count)
    logger.info("即將%s %d 則測試訊息：%s", "預覽" if dry_run else "發送", count, ", ".join(d.isoformat() for d in workdays))

    failed = 0
    for index, day in enumerate(workdays, start=1):
        forced = "ai" if index == count and os.environ.get("OPENAI_API_KEY") else ""
        if forced:
            os.environ["FORCE_MESSAGE_TYPE"] = "ai"
        else:
            os.environ.pop("FORCE_MESSAGE_TYPE", None)

        try:
            message, source, image_meta = build_message(day)
            image_url = find_theme_image(
                day,
                message,
                source,
                image_query=image_meta.get("image_query") or None,
                mood=image_meta.get("mood") or None,
            )
            static_format = image_meta.get("static_format") or None
            logger.info("[%d/%d] %s (%s)", index, count, day.isoformat(), source)
            logger.info("  訊息：%s", message)
            logger.info("  配圖：%s", image_url or "（無）")

            if not dry_run:
                send_to_teams(
                    message, day, source, image_url, static_format=static_format
                )
                logger.info("[%d/%d] 發送成功", index, count)
        except Exception:
            logger.exception("[%d/%d] %s失敗：%s", index, count, "預覽" if dry_run else "發送", day.isoformat())
            failed += 1

        if not dry_run and index < count:
            time.sleep(delay_seconds)

    os.environ.pop("FORCE_MESSAGE_TYPE", None)
    logger.info("測試完成：成功 %d / 失敗 %d", count - failed, failed)
    return 1 if failed else 0


if __name__ == "__main__":
    batch_count = int(os.environ.get("TEST_BATCH_COUNT", "5"))
    delay = int(os.environ.get("TEST_BATCH_DELAY", "3"))
    sys.exit(send_test_batch(batch_count, delay))

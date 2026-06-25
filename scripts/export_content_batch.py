#!/usr/bin/env python3
"""Export legacy Python content pools into content/batches/<period>/*.json."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from articles import ARTICLES  # noqa: E402
from interactions import INTERACTIONS  # noqa: E402
from messages import MANAGEMENT_QUOTES, PHILOSOPHY_QUOTES  # noqa: E402
from static_messages import STATIC_BY_WEEKDAY, STATIC_GENERAL  # noqa: E402


def flatten_static() -> list[dict]:
    static: list[dict] = []
    seen: set[str] = set()
    for pool in list(STATIC_BY_WEEKDAY.values()) + [STATIC_GENERAL]:
        for item in pool:
            text = item["text"]
            if text in seen:
                continue
            seen.add(text)
            static.append(dict(item))
    return static


def export_batch(period: str) -> Path:
    out_dir = ROOT / "content" / "batches" / period
    out_dir.mkdir(parents=True, exist_ok=True)

    static = flatten_static()
    files = {
        "management.json": MANAGEMENT_QUOTES,
        "philosophy.json": PHILOSOPHY_QUOTES,
        "static.json": static,
        "articles.json": ARTICLES,
        "interactions.json": INTERACTIONS,
    }
    for name, payload in files.items():
        (out_dir / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    manifest = {
        "period": period,
        "exported_on": date.today().isoformat(),
        "source": "scripts/export_content_batch.py",
        "counts": {key.replace(".json", ""): len(val) for key, val in files.items()},
        "notes": (
            "Phase 1 batch. Sequential half-year indexing in content_batch.py. "
            "Expand articles to 26+ before 2026-H2 for zero-repeat article days."
        ),
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return out_dir


def main() -> int:
    period = sys.argv[1] if len(sys.argv) > 1 else "2026-H1"
    out = export_batch(period)
    print(f"Exported batch to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

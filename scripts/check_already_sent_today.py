#!/usr/bin/env python3
"""Return whether the morning workflow already succeeded today (Taipei time)."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

WORKFLOW_FILE = "teams_bot.yml"
TZ = ZoneInfo("Asia/Taipei")


def _github_get(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def prior_successful_runs_today(
    *,
    token: str,
    repo: str,
    current_run_id: str,
    today: str,
) -> list[str]:
    url = (
        f"https://api.github.com/repos/{repo}/actions/workflows/"
        f"{WORKFLOW_FILE}/runs?status=success&per_page=30"
    )
    data = _github_get(url, token)
    prior: list[str] = []
    for run in data.get("workflow_runs", []):
        run_id = str(run.get("id", ""))
        if not run_id or run_id == current_run_id:
            continue
        created = run.get("created_at", "")
        if not created:
            continue
        created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        if created_dt.astimezone(TZ).date().isoformat() == today:
            prior.append(run_id)
    return prior


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
    force_type = os.environ.get("FORCE_MESSAGE_TYPE", "").strip()
    output_file = os.environ.get("GITHUB_OUTPUT", "")

    if not token or not repo or not run_id:
        print(
            "Missing GITHUB_TOKEN, GITHUB_REPOSITORY, or GITHUB_RUN_ID",
            file=sys.stderr,
        )
        return 1

    today = datetime.now(TZ).date().isoformat()

    if force_type:
        send = True
        print(f"force_message_type={force_type!r} — sending despite prior runs")
    else:
        try:
            prior = prior_successful_runs_today(
                token=token,
                repo=repo,
                current_run_id=run_id,
                today=today,
            )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            print(f"GitHub API error {exc.code}: {body}", file=sys.stderr)
            return 1

        send = not prior
        if send:
            print(f"No successful run yet today ({today}) — sending")
        else:
            print(
                f"Already sent today ({today}) — skipping "
                f"(prior successful run(s): {', '.join(prior)})"
            )

    if output_file:
        with open(output_file, "a", encoding="utf-8") as fh:
            fh.write(f"send={'true' if send else 'false'}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

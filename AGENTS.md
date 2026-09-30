# AGENTS.md

## Cursor Cloud specific instructions

This repo is a single Python 3.12 CLI/batch job — **Teams Morning Bot**. There is no web
server, database, or Docker stack; the only runnable entrypoint is `main.py` (plus the
`test_batch.py` helper). Production runs on GitHub Actions; local dev just runs the script.

### Environment
- Dependencies are installed into a virtualenv at `.venv/` (created by the startup update
  script). Run the app with `.venv/bin/python ...` (or activate with
  `source .venv/bin/activate`). The `.venv/` dir is gitignored.
- `python3-venv` (system package `python3.12-venv`) is required to create the venv; the
  base VM already has it after first setup. Runtime deps are pinned in `requirements.txt`.

### Running / testing (no standard lint or unit-test suite exists)
- Lint proxy: `.venv/bin/python -m py_compile *.py scripts/*.py` (there is no configured
  linter such as ruff/flake8).
- Pipeline smoke test (no external send): `.venv/bin/python main.py --validate-only`.
  This builds the message, fetches news, searches for an image, and builds the Teams
  payload. It exits 0 with only a warning when `TEAMS_WEBHOOK_URL` is unset.
- Batch preview without sending: `DRY_RUN=true SKIP_WORKDAY_CHECK=true python test_batch.py`
  (`test_batch.py` is a plain script, not pytest).

### Non-obvious gotchas
- The bot only sends on Taiwan workdays (Mon–Fri, excluding TW holidays). For any local
  run/preview on a weekend/holiday you MUST set `SKIP_WORKDAY_CHECK=true`, otherwise
  `main.py` exits early without doing anything. `--validate-only` sets this automatically.
- Use `OVERRIDE_DATE=YYYY-MM-DD` to simulate a specific date, and `FORCE_MESSAGE_TYPE`
  (`management|article|philosophy|interaction|ai|static`) to force a theme regardless of
  the schedule.
- Actually sending requires a real `TEAMS_WEBHOOK_URL` secret (Power Automate webhook);
  it is not present in this environment. To exercise the real send path end-to-end without
  Teams, point `TEAMS_WEBHOOK_URL` at a local HTTP endpoint that returns 200 — the bot
  POSTs the card JSON and calls `raise_for_status()`.
- AI greetings/article summaries need `OPENAI_API_KEY` (or `GEMINI_API_KEY` with
  `AI_PROVIDER=gemini`); when unset they cleanly fall back to static content, so setup is
  not blocked. `ENABLE_MAJOR_NEWS`/`ENABLE_IMAGES` fetch from the public internet and can
  be set to `false` to speed up or isolate runs.
- The many `.bat`/`.ps1` files are Windows-only helpers and are not used on this Linux VM.

# Teams 晨間推播機器人 — 交接文件

> 最後更新：2026-08-01  
> 儲存庫：https://github.com/gotodye/teams-morning-bot  
> 負責人（原）：gotodye / Angus

---

## 1. 專案概述

| 項目 | 說明 |
|------|------|
| **用途** | 每週一至五 **08:00（台北時間）** 自動發送晨間問候到 Microsoft Teams 頻道 |
| **同步推播** | 可選同步到 Telegram 群組 **Thaimoney friends** |
| **執行環境** | GitHub Actions（雲端，不需本機開機） |
| **假日處理** | 週末 + 台灣國定假日自動跳過（`holidays` 套件） |
| **相關專案** | HR 快報已獨立至 [teams-hr-newsletter](https://github.com/gotodye/teams-hr-newsletter) |

### 訊息流程

```
cron-job.org（08:00 台北，主要）
    ↓ workflow_dispatch
GitHub Actions → main.py
    ↓                          ↓
Teams Webhook              Telegram Bot API
    ↓                          ↓
Power Automate Flow        Telegram 群組
    ↓
Teams 頻道

GitHub schedule（09:00 台北，備援）
    ↓ 若當日已有成功 run → 跳過
```

---

## 2. 帳號與外部服務清單

| 服務 | 用途 | 登入／管理位置 |
|------|------|----------------|
| **GitHub** | 程式碼、Secrets、Actions | https://github.com/gotodye/teams-morning-bot |
| **cron-job.org** | 08:00 準時觸發 workflow | https://console.cron-job.org/ |
| **Microsoft Teams** | 接收晨間訊息 | Teams → 目標頻道 → Workflows |
| **Telegram** | 同步推播 | Bot：`@EUIHkbot`（Angus_B） |
| **OpenAI / Gemini** | AI 問候、文章摘要（選填） | API Key 存在 GitHub Secrets |
| **Unsplash / Pexels** | 配圖（選填） | API Key 存在 GitHub Secrets |

---

## 3. GitHub 設定

### 3.1 Secrets（Settings → Secrets and variables → Actions → Secrets）

| Secret | 必填 | 說明 |
|--------|------|------|
| `TEAMS_WEBHOOK_URL` | ✅ | Teams / Power Automate Webhook URL |
| `TELEGRAM_BOT_TOKEN` | 選填 | Telegram Bot Token（[@BotFather](https://t.me/BotFather)） |
| `OPENAI_API_KEY` | 選填 | AI 問候、文章摘要 |
| `GEMINI_API_KEY` | 選填 | 備用 AI 提供者 |
| `UNSPLASH_ACCESS_KEY` | 選填 | 高品質配圖 |
| `PEXELS_API_KEY` | 選填 | 備用配圖來源 |

### 3.2 Variables（Settings → Secrets and variables → Actions → Variables）

| Variable | 預設值 | 說明 |
|----------|--------|------|
| `TELEGRAM_CHAT_ID` | `-1002236690168` | Telegram 群組 ID |
| `ENABLE_TELEGRAM` | `true` | 設 `false` 可關閉 TG 同步 |
| `MESSAGE_MODE` | `mixed` | `mixed` / `static` / `ai` |
| `AI_PROVIDER` | `openai` | `openai` 或 `gemini` |
| `AI_SCHEDULE_STRATEGY` | `weekly` | AI 出現頻率 |
| `MANAGEMENT_QUOTE_WEEKDAY` | `2` | 管理金句日（0=週一，2=週三） |
| `ENABLE_IMAGES` | `true` | 是否附配圖 |
| `ENABLE_MAJOR_NEWS` | `true` | 是否附加重大新聞 |
| `MAJOR_NEWS_THRESHOLD` | `70` | 新聞評分門檻 |
| `TEAMS_WEBHOOK_FORMAT` | `auto` | `auto` / `adaptive` / `messagecard` / `simple` |

完整清單見 [README.md](../README.md)。

---

## 4. 排程機制（重要）

### 4.1 雙重觸發

| 來源 | 時間（台北） | 觸發方式 | 角色 |
|------|-------------|----------|------|
| **cron-job.org** | 08:00 週一至五 | `workflow_dispatch` | **主要**（準時） |
| **GitHub schedule** | 09:00 週一至五* | `schedule` cron `0 1 * * 1-5` UTC | **備援**（漏跑時補發） |

\* GitHub 免費版排程可能延遲 1～3 小時（實際常見 **12:00 左右**），屬正常現象。

### 4.2 防重複發送

腳本 `scripts/check_already_sent_today.py` 在每次 workflow 開始時：

1. 查詢 GitHub API：今日（台北日期）是否已有**成功的** `teams_bot.yml` run
2. 若有 → 跳過（log：`Already sent today — skipping`）
3. 若無 → 正常發送

手動測試若要強制再發：Run workflow 時選擇 `force_message_type`（例如 `static`）。

### 4.3 cron-job.org 設定

| 欄位 | 值 |
|------|-----|
| URL | `https://api.github.com/repos/gotodye/teams-morning-bot/actions/workflows/teams_bot.yml/dispatches` |
| Method | POST |
| Schedule | `0 8 * * 1-5` |
| Timezone | `Asia/Taipei` |
| Body | `{"ref":"main"}` |
| Header `Authorization` | `Bearer <GitHub_Fine-grained_Token>` |
| Header `Accept` | `application/vnd.github+json` |
| Header `X-GitHub-Api-Version` | `2022-11-28` |

Token 權限需：**Actions → Read and write**、**Metadata → Read**。

詳細步驟：[cloud_schedule.md](cloud_schedule.md)

---

## 5. Telegram 設定

| 項目 | 值 |
|------|-----|
| Bot | `@EUIHkbot`（Angus_B） |
| 群組 | Thaimoney friends |
| Chat ID | `-1002236690168` |

### 設定／更新 Token

```powershell
# Windows
.\scripts\set_telegram_env.ps1

# Linux / macOS
TELEGRAM_BOT_TOKEN='你的Token' SYNC_GITHUB=y ./scripts/set_telegram_env.sh
```

### 驗證

```bash
python scripts/verify_telegram.py
python scripts/get_telegram_chat_id.py   # 查群組 Chat ID
```

CI 行為：Token + Chat ID 都設定時才嚴格驗證；未設定時 Teams 推播不受影響。

---

## 6. Teams Webhook 設定

1. Teams 頻道 → **⋯** → **Workflows**
2. 選 **Post to a channel when a webhook request is received**
3. 複製 Webhook URL → 存入 GitHub Secret `TEAMS_WEBHOOK_URL`

### 配圖顯示（Power Automate）

若圖片不顯示，將 Workflow 發送動作改為 **Post adaptive card in a chat or channel**，內容使用 `@{triggerBody()?['card']}`。

---

## 7. 主題日曆（MESSAGE_MODE=mixed）

每個工作日只發**一種**主題，優先順序如下：

| 優先 | 主題 | 頻率 |
|------|------|------|
| 1 | 💼 管理金句 | 每週 1 天（預設週三） |
| 2 | 📚 文章摘要 | 每週 1 工作日 |
| 3 | 🪶 哲學金句 | 每兩週 1 工作日 |
| 4 | 📣 頻道互動 | 每兩週 1 工作日 |
| 5 | ✨ AI 問候 | 每週 1 工作日 |
| 6 | 靜態創意問候 | 其餘工作日 |

另可附加 **📰 Major News**（台灣／香港／越南／印尼，評分 ≥ 70）。

---

## 8. 日常維運

### 8.1 手動測試

GitHub → **Actions** → **Teams Morning Bot** → **Run workflow**

| 選項 | 用途 |
|------|------|
| `skip_workday_check` | 週末／假日也強制發送（測試用） |
| `force_message_type` | 強制指定主題（`ai` / `static` / `management` 等） |

### 8.2 本機測試

```powershell
cd C:\Users\Angus\Projects\teams-morning-bot
.\run_local.ps1          # 互動式選單
.\trigger_morning_bot.bat # 觸發遠端 workflow
```

```bash
# 僅驗證、不發送
python main.py --validate-only

# 強制發送（需 .env 設定 TEAMS_WEBHOOK_URL）
SKIP_WORKDAY_CHECK=true python main.py
```

### 8.3 每日確認（可選）

1. GitHub Actions 是否有 **08:00 左右**的 `workflow_dispatch` success
2. Teams / Telegram 是否收到訊息
3. 若 08:00 無 run → 查 cron-job.org History；09:00～13:00 備援應補發或跳過

---

## 9. 疑難排解

| 現象 | 可能原因 | 處理 |
|------|----------|------|
| 某天完全沒發送 | cron-job.org 漏跑 | 查 cron-job History；確認 Token 未過期 |
| 同一天發兩則 | 舊版 dedup 失效（已修） | 現已用 API dedup；確認 main 有 PR #4 |
| 08:00 + 12:00 各一則 | 備援排程延遲且 dedup 未生效 | 已修（PR #4）；備援 run 應顯示 `Already sent today` |
| Workflow 失敗 `[FAIL] TELEGRAM_BOT_TOKEN` | Secret 未設定 | 已修（PR #1）；或補設 Token |
| 有 run 但 Teams 沒訊息 | 國定假日跳過 | log 查 `Taiwan public holiday — skipping` |
| 有 run 但 Teams 沒訊息 | Webhook 失效 | 重新建立 Workflow、更新 Secret |
| cron-job 401 | GitHub Token 過期 | 重新產生 Fine-grained Token |
| 配圖不顯示 | Webhook 格式 | 設 `TEAMS_WEBHOOK_FORMAT=adaptive` 或改 PA 動作 |

### cron-job.org 檢查清單

1. Job 是否 **Enabled**
2. 時區 **Asia/Taipei**、排程 **`0 8 * * 1-5`**
3. History 中失敗日的 HTTP 狀態碼
4. **Run now** 測試 → GitHub Actions 是否出現新 run

---

## 10. 已知事件紀錄

| 日期 | 事件 | 原因 | 修復 |
|------|------|------|------|
| 2026-06-30 | Workflow 失敗 | `TELEGRAM_BOT_TOKEN` 未設定，CI 驗證阻擋 | PR #1：未設定時跳過 TG 驗證 |
| 2026-07-20 | 週一完全沒發送 | cron-job.org 未觸發（0 run） | PR #3：加 GitHub 09:00 備援 |
| 2026-07-21 | 同一天發兩則（08:00 + 12:17） | 08:00 用舊 workflow，備援無 cache | PR #4：改用 API dedup |
| 2026-07-31 起 | 備援正常跳過 | schedule run 7s，`Already sent today` | dedup 運作正常 |

---

## 11. 程式碼結構

```
teams-morning-bot/
├── main.py                          # 主程式：主題日曆、發送邏輯
├── telegram_delivery.py             # Telegram 發送（含圖片 fallback）
├── messages.py                      # 靜態／管理／哲學金句
├── articles.py                      # 文章摘要題庫
├── interactions.py                  # 頻道互動題庫
├── news.py                          # 重大新聞
├── image_search.py                  # 配圖搜尋
├── content_batch.py                 # 半年批次內容（sequential 不重複）
├── static_messages.py               # 靜態問候 B+ 強化版
├── scripts/
│   ├── check_already_sent_today.py  # 防重複（GitHub API）
│   ├── verify_telegram.py           # CI Telegram 驗證
│   ├── get_telegram_chat_id.py      # 查 Chat ID
│   ├── set_telegram_env.ps1         # Windows 一鍵設定 TG
│   └── set_telegram_env.sh          # Linux/macOS 一鍵設定 TG
├── .github/workflows/
│   ├── teams_bot.yml                # 正式晨間推播
│   └── teams_ai_test.yml            # AI 測試 workflow
└── docs/
    ├── HANDOVER.md                  # 本文件
    ├── cloud_schedule.md            # 雲端排程詳細設定
    ├── windows_schedule.md          # Windows 本機排程（不建議）
    └── power_automate_schedule.md   # PA 排程（不建議）
```

---

## 12. 合併 PR 紀錄（近期）

| PR | 內容 |
|----|------|
| #1 | Telegram CI 未設定時不阻擋 Teams |
| #2 | Telegram 設定腳本與文件 |
| #3 | GitHub 09:00 備援排程 |
| #4 | API 防重複（取代 Cache） |

---

## 13. 交接檢查清單

- [ ] 確認 GitHub Secrets 完整（至少 `TEAMS_WEBHOOK_URL`、`TELEGRAM_BOT_TOKEN`）
- [ ] 確認 Variables（`TELEGRAM_CHAT_ID`、 `ENABLE_TELEGRAM=true`）
- [ ] 登入 cron-job.org，確認 job Enabled、History 正常
- [ ] cron-job 使用的 GitHub Token 未過期（Actions: Read and write）
- [ ] Teams Webhook / Power Automate Flow 仍有效
- [ ] Telegram Bot 仍在群組內（`@EUIHkbot`）
- [ ] 停用 Windows 本機排程（若曾設定）：`.\disable_windows_schedule.bat`
- [ ] 手動 Run workflow 測試一次（勾選 `skip_workday_check`）
- [ ] 確認 Teams + Telegram 皆收到測試訊息

---

## 14. 聯絡與參考

- **GitHub Repo**：https://github.com/gotodye/teams-morning-bot  
- **Actions 紀錄**：https://github.com/gotodye/teams-morning-bot/actions  
- **cron-job.org**：https://console.cron-job.org/  
- **BotFather**：https://t.me/BotFather  
- **GitHub Token 管理**：https://github.com/settings/personal-access-tokens  

---

*本文件由 Cloud Agent 依 2026-07～08 維運紀錄整理，後續變更請同步更新此文件。*

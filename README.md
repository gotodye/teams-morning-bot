# Teams 晨間推播機器人

每天週一至週五（排除台灣國定假日）早上 **08:00（台灣時間）** 自動發送晨間問候到 Microsoft Teams 群組。

> HR 戰略決策快報已獨立至 [teams-hr-newsletter](https://github.com/gotodye/teams-hr-newsletter)。

## 功能特色

- 透過 Teams Incoming Webhook（Power Automate）發送訊息
- **可選同步推播到 Telegram 群組**（同一則晨間內容，設定 Bot Token + Chat ID 即可）
- 自動排除週末與台灣國定假日（使用 `holidays` 套件）
- **六種主題輪替**（預設 `MESSAGE_MODE=mixed`）：管理金句、文章摘要、哲學金句、頻道互動、AI 問候、靜態創意問候（詳見下方「主題日曆」）
- **重大新聞附加**：台灣／香港／越南／印尼重大事件達門檻時，附加在當日主題訊息後方
- **主題配圖**：依主題類型與內容自動搜尋網路圖片，附在 Teams 卡片中一併發送
- 也可強制切換為純靜態或純 AI 模式
- **cron-job.org 雲端排程**（週一至五 08:00 台北，不需電腦開機）

## 專案結構

```
teams-morning-bot/
├── main.py                              # 主程式：主題日曆、Teams / Telegram 發送
├── telegram_delivery.py                 # Telegram Bot API 發送
├── messages.py                          # 靜態問候、管理金句、哲學金句資料庫
├── articles.py                          # 每週文章摘要題庫
├── interactions.py                      # 每兩週頻道互動題庫
├── news.py                              # 重大新聞抓取與評分
├── image_search.py                      # 主題配圖搜尋
├── requirements.txt
├── .github/workflows/teams_bot.yml      # GitHub Actions（workflow_dispatch）
├── docs/cloud_schedule.md               # 雲端排程（cron-job.org，推薦）
├── docs/windows_schedule.md             # Windows 本機排程（需開機）
├── docs/power_automate_schedule.md      # PA 排程（HTTP 需 Premium）
└── README.md
```

## 正式佈建（GitHub Actions）

### 步驟 1：建立 Teams Webhook（必做）

Microsoft 已改用 **Workflows** 取代舊版 Incoming Webhook：

1. 開啟 Teams，進入要接收推播的**頻道**
2. 點頻道名稱旁的 **「⋯」** → **Workflows**（工作流程）
3. 搜尋 **webhook**
4. 選 **「Post to a channel when a webhook request is received」**
5. 確認目標頻道正確 → 點 **Add workflow** / **儲存**
6. **複製產生的 Webhook URL**（很長，以 `https://` 開頭）

> 若公司政策封鎖 Workflows，請聯繫 IT 管理員開通。

### 步驟 2：一鍵部署到 GitHub

在 PowerShell 執行：

```powershell
cd C:\Users\Angus\Projects\teams-morning-bot

# 安裝 GitHub CLI（若尚未安裝）
winget install GitHub.cli
gh auth login

# 一鍵部署（建立 repo、推送程式碼、設定 Secret）
.\deploy.ps1
```

腳本會引導你貼上 Webhook URL，並可立即觸發測試發送。

### 步驟 3：確認運作

部署完成後前往 GitHub 儲存庫的 **Actions** 分頁：

- 點 **Teams Morning Bot** → **Run workflow** 手動測試
- 成功後 Teams 頻道會收到訊息

### 步驟 4：雲端排程（不需電腦開機）

正式排程由 **cron-job.org** 在週一至五 **08:00 台北** 觸發 GitHub `workflow_dispatch`（準時、不需電腦開機）。

👉 完整設定步驟見 **[docs/cloud_schedule.md](docs/cloud_schedule.md)**

若曾設定 Windows 本機排程，請停用以免重複發送：

```powershell
cd C:\Users\Angus\Projects\teams-morning-bot
.\disable_windows_schedule.bat
```

本機手動觸發：`.\trigger_morning_bot.bat`

---

## 快速開始（手動設定）

### 1. 取得 Teams Webhook URL

請參考上方「步驟 1：建立 Teams Webhook」。

### 2. Fork / Push 此專案到你的 GitHub

```bash
git clone https://github.com/<你的帳號>/teams-morning-bot.git
cd teams-morning-bot
```

### 3. 設定 GitHub Secrets

前往 GitHub 儲存庫 → **Settings** → **Secrets and variables** → **Actions**

#### Secrets（敏感資料，必填）

| Secret 名稱 | 說明 | 必填 |
|---|---|---|
| `TEAMS_WEBHOOK_URL` | Teams Incoming Webhook URL | ✅ 必填 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token（[@BotFather](https://t.me/BotFather) 取得） | 選填（要同步發 TG 時必填） |

#### Secrets（Telegram 同步推播，選填）

| Secret / Variable | 說明 |
|---|---|
| `TELEGRAM_CHAT_ID` | 目標群組 Chat ID（Secret 或 Variable 皆可） |
| `ENABLE_TELEGRAM` | `true` / `false`（預設 `true`；有 Token + Chat ID 時才會發送） |

> **取得 Chat ID**：把 Bot 加入群組後，在群組發一則訊息，再執行 `python scripts/get_telegram_chat_id.py`（需在本機 `.env` 設定 `TELEGRAM_BOT_TOKEN`）。

#### Secrets（混合模式建議設定）

| Secret 名稱 | 說明 |
|---|---|
| `OPENAI_API_KEY` | OpenAI API Key（`AI_PROVIDER=openai` 時使用） |
| `GEMINI_API_KEY` | Google Gemini API Key（`AI_PROVIDER=gemini` 時使用） |

> 混合模式下，即使未設定 AI Key 也能正常運作（AI 日與文章摘要日會自動 fallback 為靜態訊息）。

#### Variables（非敏感設定，選填）

前往 **Settings** → **Secrets and variables** → **Actions** → **Variables** 分頁：

| Variable 名稱 | 預設值 | 說明 |
|---|---|---|
| `MESSAGE_MODE` | `mixed` | `mixed`（完整主題日曆）、`static`（僅靜態問候）、`ai`（每天 AI 問候） |
| `MESSAGE_STRATEGY` | `random` | 靜態訊息選取方式：`random`（隨機）或 `sequential`（依日期輪流） |
| `AI_SCHEDULE_STRATEGY` | `weekly` | AI 出現頻率：`weekly`（每週 1 工作日）、`biweekly`（每兩週 1 天）、`workday_interval`（每 N 個工作日） |
| `AI_WORKDAY_INTERVAL` | `10` | 當 `AI_SCHEDULE_STRATEGY=workday_interval` 時，每 N 個工作日觸發一次 AI |
| `MANAGEMENT_QUOTE_WEEKDAY` | `2` | 管理金句固定星期（0=週一 … 4=週五，預設 2=週三） |
| `AI_PROVIDER` | `openai` | `openai` 或 `gemini` |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI 模型名稱 |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini 模型名稱 |
| `ENABLE_IMAGES` | `true` | 是否附帶主題配圖 |
| `ENABLE_MAJOR_NEWS` | `true` | 是否附加重大新聞區塊 |
| `MAJOR_NEWS_THRESHOLD` | `70` | 重大新聞評分門檻（0–100） |
| `INTERACTION_FORMS_URL` | — | 頻道互動日可選的 Microsoft Forms 連結 |
| `TEAMS_WEBHOOK_FORMAT` | `auto` | `auto`、`adaptive`、`messagecard`、`simple` |
| `UNSPLASH_ACCESS_KEY` | — | Unsplash API（圖片品質最佳，選填 Secret） |
| `PEXELS_API_KEY` | — | Pexels API（選填 Secret） |

### 4. 啟用 GitHub Actions

Push 程式碼後，前往 **Actions** 分頁確認 workflow 已啟用。可點選 **Teams Morning Bot** → **Run workflow** 手動測試。

## 排程說明

| 元件 | 角色 |
|------|------|
| **cron-job.org**（雲端） | 每週一至五 **08:00 台北** 觸發 workflow_dispatch |
| **GitHub Actions** | 執行 `main.py`（讀 Secrets、AI、圖片） |
| **Send webhook alerts to HK-ALL** | 收到 webhook → 發到 Teams 頻道 |

設定教學：[docs/cloud_schedule.md](docs/cloud_schedule.md)  
準時 08:00 升級：同文件內 **cron-job.org** 方案。

假日判斷由 Python 腳本在執行時處理；排程在國定假日若仍觸發，程式也會自動跳過發送。

## 主題日曆

預設 `MESSAGE_MODE=mixed` 時，每個工作日只會發送**一種**主題。系統依下列**優先順序**決定當天內容（高優先者勝出，其餘略過）：

| 優先 | 主題 | 頻率 | 來源 | Teams 標題標記 |
|------|------|------|------|----------------|
| 1 | 💼 管理金句 | 每週 1 天（預設週三） | `messages.py` 名人原句 | `💼 Management Moment` |
| 2 | 📚 文章摘要 | 每週 1 工作日 | `articles.py` + AI 摘要 | `📚 Article Insight` |
| 3 | 🪶 哲學金句 | 每兩週 1 工作日 | `messages.py` 哲學家語錄 | `🪶 Philosophy Moment` |
| 4 | 📣 頻道互動 | 每兩週 1 工作日 | `interactions.py` 提問／Forms | `📣 Let's Connect` |
| 5 | ✨ AI 問候 | **每週 1 工作日**（`AI_SCHEDULE_STRATEGY=weekly`） | LLM 即時生成英文問候 | `✨ AI Crafted` |
| 6 | 靜態創意問候 | 其餘工作日 | `messages.py` 金句／幽默／冷知識 | （無額外標記） |

### 日期怎麼選？

- **管理金句**：固定星期（預設週三，`MANAGEMENT_QUOTE_WEEKDAY=2`）
- **文章摘要**：每 ISO 週從工作日中**確定性**挑 1 天（避開管理金句日）
- **AI 問候**：每 ISO 週從工作日中**確定性**挑 1 天（避開管理金句日與文章日）
- **哲學金句**：每兩週從工作日中挑 1 天（避開當週文章日）
- **頻道互動**：每兩週從工作日中挑 1 天（避開文章日與哲學日）
- **靜態問候**：以上皆非時的預設

> 特殊主題的日期以 ISO 週／雙週 + MD5 種子計算，同一週期內結果穩定、可重現。國定假日會從候選工作日中自動排除。

### 重大新聞（附加層）

不取代當日主題，而是在主訊息**後方附加** `📰 Major News` 區塊：

- 監測區域：台灣、香港、越南、印尼
- 時間窗：前一日 21:00 ～ 當日 09:00（台北時間）
- 評分 ≥ `MAJOR_NEWS_THRESHOLD`（預設 70）才顯示
- 可用 `ENABLE_MAJOR_NEWS=false` 關閉

### Fallback 與覆寫

- AI 日或文章日 API 失敗 → 自動改發靜態創意問候
- 本機／CI 測試可用 `FORCE_MESSAGE_TYPE` 強制指定：`management`、`article`、`philosophy`、`interaction`、`ai`、`static`
- GitHub Actions 手動 Run workflow 也可在介面選擇 `force_message_type`

### 靜態 vs AI 問候的差異

| | 靜態創意問候 | AI 問候 |
|---|---|---|
| 內容 | 事先寫好的英文金句庫（約 56+ 則） | 當天呼叫 OpenAI／Gemini 即時生成 |
| 頻率 | 大多數工作日 | 每週 1 天（維持現狀） |
| 穩定性 | 同一天內容可預期 | 每次執行可能略有不同 |
| 成本 | 無 API 費用 | 每次約一次 LLM 呼叫 |

## 主題配圖說明

圖片搜尋依「星期主題 + 訊息內容」組合英文關鍵字，無需額外 API Key 也能透過 Wikimedia Commons 取得配圖。若設定 `UNSPLASH_ACCESS_KEY` 或 `PEXELS_API_KEY`，圖片品質會更好。

**Power Automate 使用者（穩定顯示圖片）**：程式已改為發送 **Adaptive Card** 格式。請在 Power Automate 編輯你的 Workflow：

1. 開啟 Teams → 頻道 → Workflows → 編輯現有 workflow
2. 將發送動作改為 **「Post adaptive card in a chat or channel」**（在聊天室或頻道中發佈卡片）
3. Adaptive Card 內容使用運算式：`@{triggerBody()?['card']}`
4. 儲存 workflow 後，到 GitHub Actions 手動 Run workflow 測試

若圖片仍不顯示，可在 GitHub Variables 設定 `TEAMS_WEBHOOK_FORMAT=adaptive`（預設 auto 已自動判斷）。

## 批次測試發送

設定好 Webhook 後，可一次發送連續 5 個工作日的測試訊息：

```bash
set TEAMS_WEBHOOK_URL=https://your-webhook-url
set TEST_BATCH_COUNT=5
python test_batch.py
```

每次發送間隔 3 秒（可用 `TEST_BATCH_DELAY` 調整），最後一則若有 OpenAI Key 會強制使用 AI 模式測試。

## 本機測試（一鍵執行）

在專案資料夾開啟 PowerShell，執行：

```powershell
cd C:\Users\Angus\Projects\teams-morning-bot
.\run_local.ps1
```

腳本會自動安裝套件、載入 `.env`，並提供三種模式：
1. **預覽模式**（不需 Webhook，推薦第一次）
2. **發送單則測試**
3. **批次發送 5 則測試**

### 設定 Webhook URL

編輯 `.env` 檔，填入你的 URL：

```powershell
notepad .env
```

在 `TEAMS_WEBHOOK_URL=` 後面貼上 Webhook 連結即可。

## 本機測試（手動）

```bash
pip install -r requirements.txt

# 混合模式（預設）— 依主題日曆自動判斷
set TEAMS_WEBHOOK_URL=https://your-webhook-url
python main.py

# 強制測試各主題
set FORCE_MESSAGE_TYPE=management
python main.py
set FORCE_MESSAGE_TYPE=article
python main.py
set FORCE_MESSAGE_TYPE=philosophy
python main.py
set FORCE_MESSAGE_TYPE=interaction
python main.py
set FORCE_MESSAGE_TYPE=ai
set OPENAI_API_KEY=sk-...
python main.py
set FORCE_MESSAGE_TYPE=static
python main.py

# 純 AI 模式（每天都用 AI 問候）
set MESSAGE_MODE=ai
set OPENAI_API_KEY=sk-...
python main.py
```

> Linux / macOS 請將 `set` 改為 `export`。

## 授權

MIT License

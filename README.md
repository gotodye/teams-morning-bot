# Teams 晨間推播機器人

每天週一至週五（排除台灣國定假日）早上 **08:00（台灣時間）** 自動發送晨間問候到 Microsoft Teams 群組。

另含 **HR 戰略決策快報** 模組：每日 **07:00（台灣時間）** 自動抓取 HBR、Josh Bersin、McKinsey 等來源，生成 CHRO 風格快報並發送至 Teams。

## 功能特色

- 透過 Teams Incoming Webhook 發送訊息
- 自動排除週末與台灣國定假日（使用 `holidays` 套件）
- **混合模式（預設）**：多數日子使用靜態金句（方案 A），約每兩週隨機一天改用 AI 生成（方案 B）
- **主題配圖**：依訊息內容自動搜尋網路圖片，附在 Teams 卡片中一併發送
- 也可強制切換為純靜態或純 AI 模式
- **HR 戰略快報**：每日自動生成 350–400 字 CHRO Newsletter，向上管理 CEO
- GitHub Actions 定時排程，免費雲端執行

## 專案結構

```
teams-morning-bot/
├── main.py                          # 晨間問候主程式
├── hr_main.py                       # HR 戰略快報主程式
├── hr_sources.py                    # 全球 HR 媒體 RSS 抓取
├── hr_newsletter.py                 # CHRO 快報 AI 生成
├── messages.py                      # 方案 A 靜態訊息資料庫
├── requirements.txt
├── .github/workflows/teams_bot.yml      # 晨間問候排程（週一至五 08:00）
├── .github/workflows/hr_newsletter.yml  # HR 快報排程（每日 07:00）
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
- 之後每週一至五 **08:00 台灣時間** 自動發送

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

#### Secrets（混合模式建議設定）

| Secret 名稱 | 說明 |
|---|---|
| `OPENAI_API_KEY` | OpenAI API Key（`AI_PROVIDER=openai` 時使用） |
| `GEMINI_API_KEY` | Google Gemini API Key（`AI_PROVIDER=gemini` 時使用） |

> 混合模式下，即使未設定 AI Key 也能正常運作（AI 日會自動 fallback 為靜態訊息）。

#### Variables（非敏感設定，選填）

前往 **Settings** → **Secrets and variables** → **Actions** → **Variables** 分頁：

| Variable 名稱 | 預設值 | 說明 |
|---|---|---|
| `MESSAGE_MODE` | `mixed` | `mixed`（A+B 混合）、`static`（僅 A）、`ai`（僅 B） |
| `MESSAGE_STRATEGY` | `random` | 靜態訊息選取方式：`random`（隨機）或 `sequential`（依日期輪流） |
| `AI_SCHEDULE_STRATEGY` | `biweekly` | AI 出現頻率：`biweekly`（每兩週隨機一天）或 `workday_interval`（每 N 個工作日） |
| `AI_WORKDAY_INTERVAL` | `10` | 當 `AI_SCHEDULE_STRATEGY=workday_interval` 時，每 N 個工作日觸發一次 AI（10 ≈ 兩週） |
| `AI_PROVIDER` | `openai` | `openai` 或 `gemini` |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI 模型名稱 |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini 模型名稱 |
| `ENABLE_IMAGES` | `true` | 是否附帶主題配圖 |
| `UNSPLASH_ACCESS_KEY` | — | Unsplash API（圖片品質最佳，選填 Secret） |
| `PEXELS_API_KEY` | — | Pexels API（選填 Secret） |

### 4. 啟用 GitHub Actions

Push 程式碼後，前往 **Actions** 分頁確認 workflow 已啟用。可點選 **Teams Morning Bot** → **Run workflow** 手動測試。

## 排程說明

Workflow 使用 cron 表達式 `0 0 * * 1-5`：

- **UTC 時間**：每週一至五 00:00
- **台灣時間（UTC+8）**：每週一至五 **08:00**

> GitHub Actions 排程可能延遲 5–15 分鐘，屬正常現象。

假日判斷由 Python 腳本在執行時處理，即使 GitHub Actions 在國定假日觸發，程式也會自動跳過發送。

## 混合模式說明

預設 `MESSAGE_MODE=mixed` 的運作邏輯：

1. 每個兩週週期內，系統會**隨機挑選一個工作日**作為 AI 生成日（方案 B）
2. 其餘工作日使用靜態金句／笑話／冷知識（方案 A），預設隨機選取
3. 若 AI 當日 API 呼叫失敗，自動 fallback 為靜態訊息，不影響推播
4. AI 生成的訊息會在 Teams 卡片標題顯示「✨ AI 特製」
5. 每則訊息會自動搜尋一張符合主題的配圖（Unsplash → Pexels → Wikimedia）

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

```
兩週週期範例（10 個工作日）：
Mon Tue Wed Thu Fri | Mon Tue Wed Thu Fri
 A   A   A   A   B   |  A   A   A   A   A
                      ↑ 隨機選一天為 AI
```

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

# 混合模式（預設）— 自動判斷今天用 A 或 B
set TEAMS_WEBHOOK_URL=https://your-webhook-url
python main.py

# 強制測試 AI 生成
set FORCE_MESSAGE_TYPE=ai
set OPENAI_API_KEY=sk-...
python main.py

# 強制測試靜態訊息
set FORCE_MESSAGE_TYPE=static
python main.py

# 純 AI 模式（每天都用 AI）
set MESSAGE_MODE=ai
set OPENAI_API_KEY=sk-...
python main.py
```

> Linux / macOS 請將 `set` 改為 `export`。

---

## HR 戰略決策快報（每日 07:00）

### 運作方式

1. 每日自動抓取 HBR、Josh Bersin、McKinsey、Google News HR 等來源（近 48 小時）
2. 以 CHRO 人設與三段式格式，透過 AI 生成 350–400 字快報
3. 透過 Teams Adaptive Card 發送（**建議發給 CEO 個人私訊**，見下方設定）

### 發送給「某一個人」而非頻道

Teams Webhook 本身不能指定收件人，需用 **Power Automate** 建立「Webhook → 個人聊天」流程。

**完整圖文教學：** [`docs/hr_teams_dm_setup.md`](docs/hr_teams_dm_setup.md)

快速摘要：

1. Power Automate 建立「收到 Webhook 要求時」觸發的流程
2. 新增動作：**在聊天室或頻道中張貼卡片**
3. 張貼位置選 **聊天室（Chat）**，收件人選 **CEO / 老闆**
4. 卡片內容填：`@{triggerBody()?['card']}`
5. 複製 Webhook URL → 設為 `HR_TEAMS_WEBHOOK_URL`

> 收件人只在 Power Automate 裡設定，程式與 GitHub Secret **不需要**填 Email。

### 排程

Workflow：`HR Strategic Newsletter`

- **Cron**：`0 23 * * *`（UTC 23:00 = 台灣時間次日 **07:00**）
- 支援 `workflow_dispatch` 手動觸發測試

### GitHub Secrets / Variables

| 名稱 | 說明 | 必填 |
|---|---|---|
| `HR_TEAMS_WEBHOOK_URL` | 發給**個人**的 Power Automate Webhook URL | ✅ **必填**（見 `docs/hr_teams_dm_setup.md`） |
| `OPENAI_API_KEY` | OpenAI API Key | ✅（或改用 Gemini） |
| `GEMINI_API_KEY` | Gemini API Key | 選填 |

### 本機測試

```powershell
cd C:\Users\Angus\Projects\teams-morning-bot

# 預覽模式（不發送 Teams，需在 .env 設定 API Key）
.\preview_hr.bat

# 實際發送
set OPENAI_API_KEY=sk-...
set HR_TEAMS_WEBHOOK_URL=https://your-webhook-url
python hr_main.py
```

### Power Automate 設定（個人私訊）

請依 [`docs/hr_teams_dm_setup.md`](docs/hr_teams_dm_setup.md) 設定「Webhook → 個人聊天」。

動作使用 **「Post adaptive card in a chat or channel」**：
- 張貼位置：**Chat（聊天室）**，不是 Channel
- 收件人：指定那位主管
- Adaptive Card：`@{triggerBody()?['card']}`

## 授權

MIT License

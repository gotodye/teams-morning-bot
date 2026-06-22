# Power Automate 定時觸發（08:00 台灣時間）

晨間 bot 改由 **Power Automate 準時排程**，再透過 GitHub API 觸發 `teams_bot.yml`。  
GitHub Actions 只負責執行 `main.py`（讀 Secrets、呼叫 AI、發 Webhook），**不再使用 GitHub cron**。

```
Power Automate（每週一至五 08:00 台北）
  → HTTP POST GitHub workflow_dispatch
  → GitHub Actions 執行 main.py
  → POST Teams Webhook
  → 現有 flow「Send webhook alerts to HK-ALL」發到頻道
```

假日仍由 `main.py` 判斷：即使週一～五有觸發，台灣國定假日也會自動跳過發送。

---

## 步驟 1：建立 GitHub Token（只需一次）

1. 開啟 https://github.com/settings/personal-access-tokens/new  
2. 選 **Fine-grained token**
3. **Repository access**：Only select → `teams-morning-bot`
4. **Permissions**：
   - **Actions**：Read and write（觸發 workflow）
   - **Metadata**：Read
5. 產生並複製 token（`github_pat_...` 或 `ghp_...`）

> 此 token 只給 Power Automate 觸發 workflow，**不要** commit 到 git。

---

## 步驟 2：在 Power Automate 建立排程 Flow

### 2.1 建立新 flow

1. 開啟 https://make.powerautomate.com  
2. **Create** → **Scheduled cloud flow**
3. Flow 名稱：`Teams Morning Bot Schedule`
4. **Starting** 選一個週一的 08:00
5. **Repeat every**：`1 Day`
6. **Time zone**：`(UTC+08:00) Taipei, Taiwan` 或 `Taipei Standard Time`
7. 建立後，在 Recurrence 進階設定勾選只在 **週一～週五** 執行（若介面有 **On these days** / **Days of week**）

### 2.2 新增 HTTP 動作

在 Recurrence 下方新增 **HTTP** 動作：

| 欄位 | 值 |
|------|-----|
| **Method** | `POST` |
| **URI** | `https://api.github.com/repos/gotodye/teams-morning-bot/actions/workflows/teams_bot.yml/dispatches` |
| **Headers** | 見下方 |
| **Body** | 見下方 |

**Headers**（各新增一列）：

| Key | Value |
|-----|-------|
| `Accept` | `application/vnd.github+json` |
| `X-GitHub-Api-Version` | `2022-11-28` |
| `Authorization` | `Bearer ` 後面接你的 GitHub token（建議用 PA 的 **Secret** 變數，不要寫死在流程裡） |

**Body**（選 JSON）：

```json
{
  "ref": "main"
}
```

### 2.3 儲存並測試

1. **Save** flow  
2. 點 **Test** → **Manually** → **Test**  
3. 到 GitHub → **Actions** → **Teams Morning Bot**，應出現新的 run  
4. Teams 頻道應收到訊息（若當天是工作日且非國定假日）

---

## 步驟 3：關閉舊的 GitHub cron（已完成）

`teams_bot.yml` 已移除 `schedule:`，不會再被 GitHub 延遲排程。  
手動測試仍可用：**Actions → Teams Morning Bot → Run workflow**。

---

## 本機測試觸發（等同 PA 行為）

已安裝 `gh` 且已登入時：

```powershell
cd C:\Users\Angus\Projects\teams-morning-bot
.\trigger_morning_bot.ps1
```

或：

```powershell
gh workflow run teams_bot.yml --repo gotodye/teams-morning-bot
```

---

## 疑難排解

| 問題 | 處理 |
|------|------|
| HTTP 401 | Token 無效或過期，重新產生 PAT |
| HTTP 403 | PAT 缺少 Actions: Write |
| HTTP 404 | 確認 repo 名稱與 workflow 檔名 `teams_bot.yml` |
| PA 有跑但 Teams 沒訊息 | 看 GitHub Actions log；常見為假日跳過或 Secret 未設 |
| 仍下午才收到 | 確認已 push 新版 `teams_bot.yml`（無 cron），且舊 schedule 已停用 |

---

## 與現有 Webhook Flow 的關係

| Flow | 用途 |
|------|------|
| **Send webhook alerts to HK-ALL** | 收到 webhook → 發 Adaptive Card 到 Teams（維持不變） |
| **Teams Morning Bot Schedule**（新建） | 每週一至五 08:00 → 觸發 GitHub Actions |

兩個 flow 分工：一個**排程**，一個**發訊息**。

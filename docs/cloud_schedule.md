# 雲端排程（不需電腦開機）

晨間 bot 在 **GitHub Actions 雲端**執行 `main.py`，你的電腦關機也沒關係。

```
雲端排程（週一至五）
  → GitHub Actions 執行 main.py
  → POST Teams Webhook
  → flow「Send webhook alerts to HK-ALL」發到頻道
```

假日仍由 `main.py` 判斷：即使觸發了，台灣國定假日也會自動跳過發送。

---

## 方案比較

| 方案 | 需開機 | 08:00 準時 | 費用 | 建議 |
|------|--------|-----------|------|------|
| **GitHub cron**（已啟用） | 否 | 可能延遲 1～5 小時 | 免費 | 零設定，先上線 |
| **cron-job.org** | 否 | 準時 | 免費 | 要準時 08:00 時改用 |
| Windows 排程 | 是 | 準時 | 免費 | 不建議 |
| Power Automate HTTP | 否 | 準時 | 需 Premium | 不建議 |

---

## 方案 A：GitHub cron（備援，已啟用）

`teams_bot.yml` 已設定 **備援排程**（與 cron-job.org 並用）：

```yaml
schedule:
  - cron: "0 1 * * 1-5"   # UTC 01:00 = 台北 09:00（週一至五）
```

| 觸發來源 | 時間（台北） | 角色 |
|----------|-------------|------|
| **cron-job.org** | 08:00 週一至五 | 主要（準時） |
| **GitHub schedule** | 09:00 週一至五 | 備援（若 08:00 漏跑） |

Workflow 使用 **GitHub Actions API** 查詢「今日（台北日期）是否已有成功的 workflow run」：若 08:00 已成功發送，09:00 備援會自動跳過，避免同一天發兩則（即使備援排程在 Cache 部署前觸發也能正確判斷）。

**優點**：cron-job.org 漏跑時（例如 2026-07-20 週一），GitHub 備援仍可補發。  
**缺點**：GitHub 免費版排程為「盡力而為」，實際可能 **10:00～13:00** 才跑（你之前遇過約 13:16）。

### 停用 Windows 本機排程（建議）

雲端排程啟用後，請關掉本機任務，避免重複發送：

```powershell
Unregister-ScheduledTask -TaskName "Teams Morning Bot Schedule" -Confirm:$false
```

或執行：

```powershell
.\disable_windows_schedule.bat
```

---

## 方案 B：cron-job.org（準時 08:00，推薦升級）

若需要 **準時 08:00** 且 **不需開機**，用免費的 [cron-job.org](https://console.cron-job.org/) 在雲端呼叫 GitHub API。

### 1. 建立 GitHub Token

1. 開啟 https://github.com/settings/personal-access-tokens/new  
2. **Fine-grained token**  
3. Repository：`teams-morning-bot`  
4. Permissions：**Actions → Read and write**、**Metadata → Read**  
5. 產生並複製 token（只顯示一次）

### 2. 建立 cron-job

1. 註冊 https://console.cron-job.org/  
2. **CREATE CRONJOB**  
3. 設定：

| 欄位 | 值 |
|------|-----|
| Title | Teams Morning Bot 08:00 |
| URL | `https://api.github.com/repos/gotodye/teams-morning-bot/actions/workflows/teams_bot.yml/dispatches` |
| Schedule | 自訂：`0 8 * * 1-5` |
| Timezone | `Asia/Taipei` |
| Request method | **POST** |

4. **Headers**（新增兩筆）：

| Header | Value |
|--------|-------|
| `Accept` | `application/vnd.github+json` |
| `Authorization` | `Bearer <你的_GitHub_Token>` |
| `X-GitHub-Api-Version` | `2022-11-28` |

5. **Request body**（選 JSON / raw）：

```json
{"ref":"main"}
```

6. 儲存並 **Enable**

### 3. 避免重複發送

cron-job.org 與 GitHub schedule **可同時啟用**。Workflow 會用 GitHub API 查詢當日是否已有成功 run，不會因兩個排程各發一則。

若仍出現重複，請確認沒有同時開 Windows 本機排程。

### 4. 測試

在 cron-job.org 點 **Run now**，再到 GitHub Actions 確認有新 run。

---

## 疑難排解

| 問題 | 處理 |
|------|------|
| 雲端有跑但 Teams 沒訊息 | 看 Actions log；常見為國定假日跳過或 Webhook Secret |
| **某天完全沒發送** | 見下方「cron-job.org 檢查清單」；GitHub 09:00 備援應可補發 |
| GitHub cron 太晚才跑 | 正常現象；主要仍靠 cron-job.org 08:00 |
| 同一天發兩則 | 同時開了 Windows 本機排程；或 dedup 腳本無法讀取 Actions API（看 log） |
| cron-job 401 | Token 權限需 Actions: Write |

### cron-job.org 檢查清單（某天漏跑時）

以 **2026-07-20（週一）漏跑** 為例：GitHub Actions 當天 **0 筆 run**，代表 cron-job.org **未成功觸發** workflow。

1. 登入 https://console.cron-job.org/
2. 找到 **Teams Morning Bot 08:00**（或類似名稱）的 cron job
3. 點 **History / 執行紀錄**，查看 **7/20 08:00** 是否有紀錄：
   - **無紀錄** → job 可能被停用、排程錯誤、或帳號問題
   - **Failed / 401** → GitHub Token 過期或權限不足（需 **Actions: Read and write**）
   - **Failed / 404** → workflow 檔名或 repo 路徑錯誤
   - **Success 但 GitHub 無 run** → 檢查 POST body 是否為 `{"ref":"main"}`，URL 是否為  
     `https://api.github.com/repos/gotodye/teams-morning-bot/actions/workflows/teams_bot.yml/dispatches`
4. 確認 **Enabled**、時區 **Asia/Taipei**、排程 **`0 8 * * 1-5`**
5. 點 **Run now** 測試 → 到 GitHub Actions 確認有新 run
6. Token 過期時到 https://github.com/settings/personal-access-tokens 重新產生並更新 cron-job Headers

合併備援排程後，即使 cron-job 漏跑，**09:00 GitHub 備援**仍應在當日補發（除非兩者都失敗）。

---

## 與其他文件

- [windows_schedule.md](windows_schedule.md) — 本機排程（需開機）
- [power_automate_schedule.md](power_automate_schedule.md) — PA（HTTP 需 Premium）

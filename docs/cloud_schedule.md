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

## 方案 A：GitHub cron（目前已啟用）

`teams_bot.yml` 已設定：

```yaml
schedule:
  - cron: "0 0 * * 1-5"   # UTC 00:00 = 台北 08:00
```

**優點**：推送後自動運作，不需本機、不需額外帳號。  
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

使用 cron-job.org 後，請從 `teams_bot.yml` **移除** `schedule:` 區塊（只保留 `workflow_dispatch`），否則同一天可能發兩次。

### 4. 測試

在 cron-job.org 點 **Run now**，再到 GitHub Actions 確認有新 run。

---

## 疑難排解

| 問題 | 處理 |
|------|------|
| 雲端有跑但 Teams 沒訊息 | 看 Actions log；常見為國定假日跳過或 Webhook Secret |
| GitHub cron 太晚才跑 | 正常現象；改用 cron-job.org |
| 同一天發兩則 | 同時開了 GitHub cron + cron-job 或 Windows 排程；只留一種 |
| cron-job 401 | Token 權限需 Actions: Write |

---

## 與其他文件

- [windows_schedule.md](windows_schedule.md) — 本機排程（需開機）
- [power_automate_schedule.md](power_automate_schedule.md) — PA（HTTP 需 Premium）

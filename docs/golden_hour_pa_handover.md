# Golden Hour Rate 推播 — Power Automate 交接文件

> 建立日期：2026-08-01  
> 相關 Agent：[Gh 提醒未發送](https://cursor.com/agents/bc-62379260-137b-4d51-8428-3c71a18c6bee)  
> **注意：** 本問題與 `teams-morning-bot` / GitHub Actions 無關，全部在 **Power Automate + SharePoint List** 端。

---

## 1. 背景

| 項目 | 說明 |
|------|------|
| 系統 | SharePoint / Microsoft List 驅動 + Power Automate 推播 |
| 功能 | **Golden Hour Rate** 活動提醒（含四小時前通知） |
| Flow 數量 | **2 個推播 flow**（排程檢查型 + 另一推播，名稱待補） |
| 通知通道 | Teams / 東訊（依 flow 設定） |
| 與本 repo 關係 | **無程式碼關聯**；晨間 bot、HR 快報為獨立系統 |

---

## 2. 問題摘要

- 使用者設定活動 **15:00–17:00**，預期 **11:00** 收到四小時前提醒，但未收到。
- Power Automate **28 天執行歷程全部「失敗」**，每次僅跑 **2–9 秒**。
- 今天新建的 List 項目同樣未觸發通知（因 flow 在查詢階段就失敗，非 List 未驅動）。

---

## 3. 根本原因（已確認）

**Flow 1** 的 SharePoint 動作 **`Get_today_items`** 的 **Filter Query 語法錯誤**。

### 錯誤訊息

```
運算式 'Endtime gt 2026-07-31T05:00:23.7689783Z' 無效。
Creating query failed.
```

### 原因說明

| 問題 | 說明 |
|------|------|
| 日期未加單引號 | OData 要求 `'2026-07-31T05:00:23Z'` 格式，不可裸寫 datetime |
| 可能欄位名稱 | 使用 `Endtime`；需與 List **內部欄位名**完全一致（大小寫、`End_x0020_time` 等） |
| 排程 vs 建立時間 | 若僅早上排程跑一次，11:00 後才建的項目會錯過；但本次主因是 **查詢失敗**，非時間問題 |

---

## 4. 修正方式

### 4.1 Flow 1：`Get_today_items` — Filter Query（必改）

**路徑：** Power Automate → 編輯 flow → **Get_today_items** → 顯示進階選項 → **Filter Query**

**四小時前提醒（建議）：**

```
Endtime gt '@{formatDateTime(utcNow(), 'yyyy-MM-ddTHH:mm:ssZ')}' and Starttime le '@{formatDateTime(addHours(utcNow(), 4), 'yyyy-MM-ddTHH:mm:ssZ')}' and Starttime gt '@{formatDateTime(utcNow(), 'yyyy-MM-ddTHH:mm:ssZ')}'
```

**最小修正（僅「尚未結束」）：**

```
Endtime gt '@{formatDateTime(utcNow(), 'yyyy-MM-ddTHH:mm:ssZ')}'
```

**重點：**

- 日期前後必須有 **單引號** `'...'`
- 使用 `formatDateTime`，避免 `.7689783` 過長小數
- 邏輯運算子用小寫 `and` / `or`
- 欄位名以 List **欄位設定 URL** 的 `Field=` 為準

### 4.2 查 List 欄位內部名稱

1. SharePoint List → 欄位 → **欄位設定**
2. 看網址 `Field=EndTime` 或 `Field=End_x0020_time`
3. Filter Query 必須使用相同名稱

### 4.3 Flow 2（第二個推播 flow）

| 觸發類型 | 檢查重點 |
|----------|----------|
| **Recurrence + Get items** | 同上，Filter Query 日期加引號 |
| **When an item is created** | Delay Until、時區 Taipei、Send 連線 |
| **活動開始時推播** | `Starttime le '@{formatDateTime(utcNow(), ...)}'` 且 `Endtime gt ...` |

若有 **已提醒** 欄位，可加上：`and Reminded eq 0`

### 4.4 修正後驗證

1. **儲存** flow  
2. **測試** → **手動** → **執行流程**  
3. 確認 `Get_today_items` 為綠色且筆數 > 0  
4. 確認 Teams / 東訊收到測試訊息  
5. 執行歷程不再出現 `Creating query failed`

---

## 5. 兩個 Flow 檢查清單

| # | 檢查項 | Flow 1 | Flow 2 |
|---|--------|--------|--------|
| 1 | 狀態為「開啟」 | ☐ | ☐ |
| 2 | 最近 run 成功（非全失敗） | ☐ | ☐ |
| 3 | Filter Query 日期有單引號 | ☐ | ☐ |
| 4 | Recurrence 時區 `(UTC+08:00) Taipei` | ☐ | ☐ |
| 5 | SharePoint 連線有效 | ☐ | ☐ |
| 6 | Teams / 東訊 Send 連線有效 | ☐ | ☐ |
| 7 | List 今日項目：開始/結束/提醒時數正確 | ☐ | ☐ |

**待補：** Flow 1、Flow 2 的**正式名稱**、SharePoint **List 名稱與 URL**。

---

## 6. 排程設計建議（避免再漏提醒）

若目前僅 **每天 08:00 / 13:01** 等固定時間跑排程，**11:00 四小時前提醒**可能漏掉當天稍晚才建立的項目。

| 方案 | 作法 |
|------|------|
| **A（推薦）** | `When an item is created` → 計算 `ReminderTime = Starttime - 4h` → **Delay Until** → 發送 |
| **B** | Recurrence **每 1 小時** → Get items 篩「過去 1 小時內該提醒且未提醒」 |
| **C** | 增加 **11:00** 獨立 Recurrence（與現有排程並存） |

---

## 7. 排查紀錄（Cursor Cloud Agent）

| 嘗試 | 結果 |
|------|------|
| 搜尋 `teams-morning-bot` / `teams-hr-newsletter` | 無 Golden Hour / List 驅動程式碼 |
| Cloud VM 開 Chrome → make.powerautomate.com | 停在 Microsoft 登入頁，無法代登入 |
| 使用者本機 Chrome | Agent **無法**操作使用者電腦瀏覽器 |
| Remote Desktop（Take control） | 需使用者在 VM 內手動登入 Microsoft 一次 |
| 使用者手機 PA 執行歷程截圖 | 確認 28 天全失敗 + `Get_today_items` 錯誤 |

---

## 8. 與其他系統區隔

| 系統 | Repo / 觸發 | 時間 | 說明 |
|------|-------------|------|------|
| 晨間推播 | `teams-morning-bot` + cron-job.org | 週一至五 08:00 | Teams + Telegram |
| HR 快報 | `teams-hr-newsletter` + cron-job.org | 每日 06:00 | Teams 私訊 |
| **Golden Hour 推播** | **Power Automate + List** | 依 List / 排程 | **本文件主題** |

---

## 9. 接手人待辦（Priority）

1. **[P0]** 修正 Flow 1 `Get_today_items` Filter Query（見 §4.1）  
2. **[P0]** 手動測試 Flow 1，確認執行成功  
3. **[P1]** 檢查 Flow 2 是否有相同 Filter Query 問題  
4. **[P1]** 補齊本文件 §5 中 Flow 名稱、List URL  
5. **[P2]** 評估排程改為每小時或 Delay Until（§6）  
6. **[P2]** List 增加「已提醒」欄位，避免重複推播  

---

## 10. 參考連結

- [Power Automate — SharePoint 提醒 flow](https://learn.microsoft.com/en-us/power-automate/create-sharepoint-reminder-flows)
- [Cursor Cloud Agent 能力（Remote Desktop）](https://cursor.com/docs/cloud-agent/capabilities)
- Power Automate 入口：https://make.powerautomate.com

---

## 11. 聯絡 / 上下文

- GitHub 帳號：`gotodye`
- 原始需求：List 驅動 Golden Hour Rate 東訊訊息提醒；四小時前通知未發；今天新建項目未驅動
- Agent 對話：https://cursor.com/agents/bc-62379260-137b-4d51-8428-3c71a18c6bee

---

*文件版本：1.0 — 若 Flow 名稱、List 結構確認後請更新 §5、§9。*

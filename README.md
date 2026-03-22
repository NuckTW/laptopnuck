# nuck001 — LAPTOP-Nuck Python Telegram Bot

橘貓/右腦 | Windows | Python + Gemini 2.5 Flash

> **2026-03-22 架構更新**：原本使用 OpenClaw 框架，因 Windows + Gemini 組合無法可靠執行程式碼，已全面改為純 Python Telegram Bot。

---

## 功能

| 功能 | 說明 |
|------|------|
| Telegram | 透過 Telegram Bot 接收/發送訊息 |
| 對話記憶 | 持久化本地記憶（最近 20 則 + 長期記憶） |
| Gmail | 讀取未讀信件、寄送郵件 |
| Google Calendar | 查看/新增行程 |
| Google Drive | 搜尋雲端檔案 |
| Google Sheets | 讀取/寫入試算表 |
| 圖片分析 | Gemini Vision OCR（監工日報表自動辨識） |
| 智慧路由 | 自動判斷要呼叫哪個服務 |

---

## 架構

```
使用者 (Telegram: 8407969817)
        │
        ▼
bot.py (Python 3.x)
        │
        ├─ Gemini 2.5 Flash (對話 + Vision)
        ├─ Google OAuth2 (token.json)
        │   Gmail / Calendar / Drive / Sheets
        └─ 本地記憶 (memory_store.json)
```

---

## 快速啟動 (LAPTOP-Nuck)

### 前置需求
- Windows 10/11
- Python 3.10+
- `pip install python-telegram-bot google-auth-oauthlib google-api-python-client google-generativeai`

### 環境變數

```powershell
$env:GEMINI_API_KEY = "你的 Gemini API Key"
$env:TELEGRAM_TOKEN = "你的 Telegram Bot Token"
```

### 啟動

```powershell
cd D:\ai\laptopnuck
python bot.py
```

---

## Google OAuth 設定

1. 從 Google Cloud Console 下載 `credentials.json`，放在本目錄根目錄
2. 第一次執行 `python google_auth.py` 完成瀏覽器授權
3. 授權後 `token.json` 自動產生（gitignored）

---

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `bot.py` | 主程式，Telegram bot + 智慧路由 + 記憶 |
| `google_services.py` | Google API 封裝（Gmail/Calendar/Drive/Sheets） |
| `google_auth.py` | OAuth2 授權工具 |
| `upload_report.py` | 手動上傳監工日報表到 Google Sheets |
| `run_google.py` | CLI Google API 測試工具 |
| `google_api_server.py` | HTTP API Bridge（備用，port 8766） |
| `soul.md` | nuck001 身分與準則 |
| `agents.md` | 工作手冊與記憶規則 |

---

## 開發紀錄

詳細開發過程與架構演變請見 [PROGRESS.md](PROGRESS.md)。

**重要結論（2026-03-22）：**
OpenClaw 在 Windows + Gemini 的組合下，Skill 的 `exec:` 語法無法真正執行程式碼，Gemini 回報「沒有執行權限」。嘗試過 5 種方案均失敗，最終決定放棄 OpenClaw 框架，改用純 Python bot 直接整合所有功能。

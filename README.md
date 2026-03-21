# nuck001 — LAPTOP-Nuck OpenClaw Agent

橘貓/右腦 | Windows | OpenClaw + Claude

## 快速部署 (LAPTOP-Nuck)

### 前置需求
- Windows 10/11
- [Node.js v20+](https://nodejs.org/)
- [Git](https://git-scm.com/)

### 第一次安裝

```powershell
# 1. 用 git clone 或 git pull 取得最新代碼
git clone https://github.com/NuckTW/<repo> C:\ai\laptopnuck
cd C:\ai\laptopnuck

# 2. 執行安裝腳本 (會自動刪除舊版 OpenClaw 並安裝新版)
.\setup.ps1

# 3. 填入憑證
notepad .env          # 填入 ANTHROPIC_API_KEY, TELEGRAM_TOKEN 等
# 放入 credentials.json (Google OAuth)

# 4. 啟動
openclaw
```

### 正常重啟

```powershell
cd C:\ai\laptopnuck
git pull
openclaw
```

---

## 功能

| 功能 | 說明 |
|------|------|
| Telegram | 透過 Telegram Bot 接收/發送訊息 |
| Gmail | 讀取未讀信件、寄送郵件 |
| Google Calendar | 查看/新增行程 |
| Google Drive | 搜尋/讀取雲端檔案 |
| Google Sheets | 讀取/寫入試算表 |
| 上網查資料 | DuckDuckGo 搜尋 + 讀取網頁內容 |
| 開啟網站 | Playwright 瀏覽器自動化 |
| 記憶系統 | 持久化本地記憶 |

---

## 環境變數 (.env)

複製 `.env.example` 為 `.env` 並填入：

```
ANTHROPIC_API_KEY=       # Anthropic API Key (Claude)
TELEGRAM_TOKEN=          # Telegram Bot Token
TELEGRAM_ALLOWED_IDS=8407969817
GOOGLE_CLIENT_ID=        # Google OAuth Client ID
GOOGLE_CLIENT_SECRET=    # Google OAuth Client Secret
```

## Google OAuth 設定

1. 從 Google Cloud Console 下載 `credentials.json`
2. 放在本目錄根目錄
3. 第一次啟動會自動開啟瀏覽器進行授權
4. 授權後 `token.json` 自動產生（gitignored）

---

## 架構

```
Telegram ↔ OpenClaw (LAPTOP-Nuck)
              ├── Claude (Anthropic API)
              ├── Skills (ClawHub)
              │   ├── agent-browser      (網站瀏覽)
              │   ├── playwright-cli     (瀏覽器自動化)
              │   ├── memory-setup       (持久記憶)
              │   ├── skill-vetter       (技能安全審查)
              │   ├── find-skills        (技能搜尋)
              │   └── skill-creator      (建立新技能)
              ├── Custom Skills
              │   ├── telegram-bot       (Telegram API)
              │   └── google-services    (Google APIs)
              └── Memory: ~/.openclaw/memory/
```

---

## 關於 OpenClaw

OpenClaw（龍蝦）是一個開源 AI agent 作業系統，以 TypeScript 構建，設計用於 24/7 自主運行。
- 官網: https://openclaw.ai
- 技能市場: https://clawhub.ai

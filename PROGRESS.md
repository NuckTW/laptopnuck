# Progress Log — nuck001 (LAPTOP-Nuck)

## 2026-03-21

### 初始架構建立

**完成項目：**
- 建立完整 OpenClaw 專案架構
- `setup.ps1` — 一鍵安裝腳本（自動刪舊版 OpenClaw + 安裝新版 + ClawHub skills）
- `.env.example` — 環境變數範本（ANTHROPIC_API_KEY, TELEGRAM_TOKEN, Google OAuth）
- `.gitignore` — 排除敏感檔案（.env, credentials.json, token.json）
- `CLAUDE.md` — 專案說明文件
- `README.md` — 快速部署指南（繁中）
- `skills/telegram-bot.md` — 自定義 Telegram Bot API 技能
- `skills/google-services.md` — 自定義 Google 服務技能（Gmail/Calendar/Drive/Sheets）
- `openclaw-config/settings.json.example` — OpenClaw 設定範本

**架構：**
- 平台：LAPTOP-Nuck (Windows)
- Framework：OpenClaw (https://openclaw.ai)
- LLM：Claude (Anthropic API)
- 通訊：Telegram Bot
- ClawHub skills：skill-vetter, find-skills, skill-creator, agent-browser, playwright-cli, memory-setup

**待完成：**
- [ ] 在 LAPTOP-Nuck 執行 `setup.ps1` 完成安裝
- [ ] 填入 `.env` 真實憑證
- [ ] 完成 Google OAuth2 授權
- [ ] 測試 Telegram Bot 連線
- [ ] 測試網頁瀏覽功能

---

## 2026-03-21 (2)

### 新增 Soul / User / Agents 設定

**完成項目：**
- `soul.md` — nuck001 身分、準則、行為規範（橘貓右腦版本）
- `user.md` — 主人 NuckTW 完整資料（職業、專案、溝通偏好）
- `agents.md` — 工作手冊（記憶管理、安全邊界、互動規則、心跳任務）
- 更新 `openclaw-config/settings.json.example` systemPrompt

**API Keys 清單（3組）：**
- `ANTHROPIC_API_KEY` — console.anthropic.com
- `TELEGRAM_TOKEN` — @BotFather
- `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` — Google Cloud Console

---

## 2026-03-21 (3)

### 更新 LLM、身分、新增生圖功能

**完成項目：**
- LLM 從 Anthropic Claude 改為 **Google Gemini 2.5 Flash**
- 新增 `OPENAI_API_KEY` 用於生圖
- nuck001 形象更新為**賽博龐克俄羅斯虎斑貓**
- `skills/image-generation.md` -- OpenAI DALL-E 3 生圖技能
- 更新 `.env.example`、`settings.json.example`、`soul.md`

**API Keys 最終清單（3組）：**
- `GEMINI_API_KEY` -- Google AI Studio
- `OPENAI_API_KEY` -- platform.openai.com
- `TELEGRAM_TOKEN` -- @BotFather
- `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` -- Google Cloud Console

---

## 2026-03-21 (4)

### nuck001 成功上線

**完成：**
- OpenClaw 2026.3.13 安裝完成
- ClawHub skills: skill-vetter, skill-creator, memory-setup 安裝成功
- 自定義 skills: telegram-bot, google-services, image-generation 註冊完成
- Onboarding: Gemini 2.5 Flash + Telegram Bot + Google Search 設定完成
- Hooks 啟用：boot-md, session-memory
- Telegram 配對完成（user ID: 8407969817）
- Gateway 穩定運行，bot 已回應訊息

**待補裝 skills（rate limit 後）：**
- [ ] find-skills
- [ ] agent-browser
- [ ] playwright-cli

**完成：**
- [x] push 到 GitHub（NuckTW/laptopnuck）
- [x] 在 LAPTOP-Nuck 執行 setup.ps1
- [x] 填入 .env 憑證 + 放入 credentials.json
- [x] 完成 Google OAuth2 授權（token.json at D:\ai\laptop\token.json）
- [x] 測試 Telegram Bot — 成功回應

---

## 2026-03-21 (5)

### Google OAuth2 完成 + 監工日報表 OCR 成功

**完成：**
- Google OAuth2 授權完成，token.json 產生於 D:\ai\laptop\token.json
- google-services.md 更新絕對路徑（TOKEN_PATH / CREDS_PATH）
- nuck001 成功 OCR 監工日報表圖片：
  - 日期：115/3/18（星期二），第 387 天，晴天
  - 工頭：朱，水錶：546
  - 工種：粗工、泥作、鐵工、電工等
- GitHub repo NuckTW/laptopnuck 建立並 push 完成

**完成：**
- [x] 同步 google-services.md → ~/.openclaw/skills/ 並重啟 gateway
- [x] 測試 Google Sheets 上傳（監工日報表 OCR → Sheets 成功）
  - 試算表名稱：監工日報表，工作表 tab：日報
  - upload_report.py 自動偵測 tab 名稱

**待完成：**
- [ ] 測試 Google Drive 上傳（原始圖片，以日期為檔名）
- [ ] 補裝 ClawHub skills：find-skills, agent-browser, playwright-cli

---

## 2026-03-22

### Google API Bridge + 架構完整化

**完成：**
- `google_api_server.py` — FastAPI server (port 8766) 常駐，提供 Google API HTTP 介面
  - GET  /gmail/unread
  - POST /gmail/send
  - GET  /calendar/events
  - POST /calendar/events
  - GET  /drive/search
  - GET  /sheets/read
  - POST /sheets/append
- `skills/google-services.md` 改為 curl 呼叫 localhost:8766（不再需要 Python 執行環境）
- `upload_report.py` 修正 tab 名稱自動偵測（支援中文 locale「日報」）
- OCR 測試成功（115/3/18, 115/3/30 兩份日報皆正確辨識）
- Google Sheets 上傳成功（手動執行 upload_report.py）

**目前常駐程序（LAPTOP-Nuck 開機後需啟動）：**
1. `python D:\ai\laptop\google_api_server.py` — Google API Bridge (port 8766)
2. `openclaw gateway` — OpenClaw Gateway (port 18789)

**待完成：**
- [ ] 確認 google-services.md curl 版本已被 gateway 載入（Gmail/Calendar 測試）
- [ ] 讓 nuck001 自動上傳監工日報表（OCR → 直接呼叫 /sheets/append）
- [ ] 補裝 ClawHub skills：find-skills, agent-browser, playwright-cli

---

## 現有架構（2026-03-22）

```
使用者 (Telegram: 8407969817)
        │
        ▼
OpenClaw Gateway (port 18789)
LLM: Google Gemini 2.5 Flash
        │
        ├─ 圖片 → Gemini Vision OCR → 回傳結果
        ├─ Google 服務 → curl http://localhost:8766/...
        ├─ 生圖 → OpenAI DALL-E 3 API
        └─ 一般對話 → Gemini 2.5 Flash

Google API Bridge (port 8766)
python google_api_server.py
        │
        └─ Google APIs (OAuth2: token.json)
           Gmail / Calendar / Drive / Sheets

Skills:
- telegram-bot.md       (Telegram Bot API)
- google-services.md    (→ localhost:8766 curl)
- image-generation.md   (DALL-E 3)
- skill-vetter          (ClawHub)
- skill-creator         (ClawHub)
- memory-setup          (ClawHub)

Hooks:
- boot-md               (載入 soul/user/agents.md)
- session-memory        (對話記憶存檔)
```

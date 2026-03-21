# nuck001 — LAPTOP-Nuck OpenClaw Agent

## Identity
- **Agent name**: nuck001（橘貓/右腦）
- **Platform**: LAPTOP-Nuck (Windows)
- **Framework**: OpenClaw (https://openclaw.ai)
- **Language**: 繁體中文
- **LLM**: Claude (Anthropic)

## Capabilities
1. **Telegram** — receive and send messages via Telegram Bot API
2. **Google Services** — Gmail (read/send), Calendar (view/create), Drive (search/read), Sheets (read/write)
3. **Web Search** — search the web via DuckDuckGo or Google
4. **Web Browsing** — open and read actual websites (Playwright via agent-browser / playwright-cli)
5. **Memory** — persistent local memory (memory-setup skill)
6. **Skill discovery** — find and vet new skills from ClawHub (find-skills, skill-vetter)
7. **Skill creation** — create new SKILL.md skills (skill-creator)

## Architecture

```
Telegram User (ID: 8407969817)
        ↕
OpenClaw Gateway (LAPTOP-Nuck)
        |
    Agent Runtime
    ├── LLM: Claude (Anthropic API)
    ├── Skills: telegram-bot, google-services, agent-browser,
    │           playwright-cli, memory-setup, skill-vetter,
    │           find-skills, skill-creator
    ├── Memory: ~/.openclaw/memory/
    └── Credentials: .env + credentials.json + token.json
```

## Key Files
- `setup.ps1` — one-click setup + old OpenClaw cleanup
- `.env` — secrets (API keys, tokens) — **gitignored**
- `credentials.json` — Google OAuth2 app credentials — **gitignored**
- `token.json` — Google OAuth2 user token (auto-generated) — **gitignored**
- `skills/telegram-bot.md` — custom Telegram skill
- `skills/google-services.md` — custom Google services skill
- `openclaw-config/settings.json.example` — OpenClaw config template

## Deployment to LAPTOP-Nuck

### First-time setup
```powershell
# On LAPTOP-Nuck PowerShell (as Administrator):
git clone https://github.com/NuckTW/<repo> laptopnuck
cd laptopnuck
.\setup.ps1
# Then edit .env with real credentials
# Place credentials.json for Google OAuth
# Start: openclaw
```

### Normal restart
```powershell
cd laptopnuck
git pull
openclaw
```

## Google OAuth
- Scopes: Gmail, Calendar, Drive, Sheets
- credentials.json: from Google Cloud Console (project: nuck002)
- First run: browser will open for OAuth consent at http://localhost:3000/oauth/callback
- token.json: auto-saved after OAuth, gitignored

## Telegram Bot
- Token: stored in `.env` as `TELEGRAM_TOKEN`
- Allowed user IDs: `TELEGRAM_ALLOWED_IDS=8407969817`
- OpenClaw connects automatically when started

## ClawHub Skills Installed
| Skill | Purpose |
|-------|---------|
| skill-vetter | Vet skills for security before installing |
| find-skills | Discover new skills from ClawHub |
| skill-creator | Create new SKILL.md skills |
| agent-browser | Multi-step web browsing with session isolation |
| playwright-cli | Browser automation (Chromium) |
| memory-setup | Persistent agent memory |

## User Info
- GitHub: NuckTW
- Telegram ID: 8407969817
- Language: 繁體中文
- Deployed remotely via Chrome Remote Desktop → LAPTOP-Nuck

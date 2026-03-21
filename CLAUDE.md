# nuck001 — LAPTOP-Nuck OpenClaw Agent

## Identity
- **Agent name**: nuck001（虎斑貓）
- **Platform**: LAPTOP-Nuck (Windows)
- **Framework**: OpenClaw (https://openclaw.ai)
- **Language**: 繁體中文
- **LLM**: Google Gemini 2.5 Flash

## Capabilities
1. **Telegram** — receive and send messages via Telegram Bot API
2. **Google Services** — Gmail (read/send), Calendar (view/create), Drive (search/read), Sheets (read/write)
3. **Web Search** — search the web
4. **Web Browsing** — open and read websites (Playwright via agent-browser / playwright-cli)
5. **Image Generation** — DALL-E 3 via OpenAI API, send result via Telegram
6. **Memory** — persistent local memory (memory-setup skill)
7. **Skill discovery** — find and vet new skills from ClawHub
8. **Skill creation** — create new SKILL.md skills

## Architecture

```
Telegram User (ID: 8407969817)
        |
OpenClaw (LAPTOP-Nuck)
        |
    Agent Runtime
    |- LLM: Gemini 2.5 Flash
    |- Skills: telegram-bot, google-services, image-generation,
    |          agent-browser, playwright-cli, memory-setup,
    |          skill-vetter, find-skills, skill-creator
    |- Memory: ~/.openclaw/memory/
    |- Config: soul.md, user.md, agents.md
    `- Credentials: .env + credentials.json + token.json
```

## Key Files
- `setup.ps1` — one-click setup script
- `soul.md` — agent identity and principles
- `user.md` — owner profile
- `agents.md` — work handbook (memory, security, interaction rules)
- `.env` — secrets (gitignored)
- `credentials.json` — Google OAuth2 (gitignored)
- `token.json` — Google OAuth2 token (gitignored, auto-generated)
- `skills/telegram-bot.md` — Telegram skill
- `skills/google-services.md` — Google services skill
- `skills/image-generation.md` — DALL-E 3 image generation skill
- `openclaw-config/settings.json.example` — OpenClaw config template

## API Keys Required
- `GEMINI_API_KEY` — Google AI Studio
- `OPENAI_API_KEY` — OpenAI platform (DALL-E image generation)
- `TELEGRAM_TOKEN` — Telegram BotFather
- `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` — Google Cloud Console

## Deployment to LAPTOP-Nuck

### First-time setup
```powershell
git clone https://github.com/NuckTW/laptopnuck C:\ai\laptopnuck
cd C:\ai\laptopnuck
powershell -ExecutionPolicy Bypass -File .\setup.ps1
# Edit .env and place credentials.json
# Start: openclaw
```

### Normal restart
```powershell
cd C:\ai\laptopnuck
git pull
openclaw
```

## User Info
- GitHub: NuckTW
- Telegram ID: 8407969817
- Language: 繁體中文

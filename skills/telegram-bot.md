---
name: telegram-bot
description: Send and receive Telegram messages via Bot API. Use when the user wants to send a Telegram message, check messages, or interact via Telegram.
---

# Telegram Bot Skill

You can communicate with the user via Telegram using the Bot API.

## Environment Variables Required
- `TELEGRAM_TOKEN` — Telegram Bot API token
- `TELEGRAM_ALLOWED_IDS` — Comma-separated list of allowed Telegram user IDs

## Sending a Message

Use the following pattern to send a message via Telegram Bot API:

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"CHAT_ID\", \"text\": \"MESSAGE\", \"parse_mode\": \"Markdown\"}"
```

Replace `CHAT_ID` with the target user's Telegram ID and `MESSAGE` with the text to send.

## Sending a Photo

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendPhoto" \
  -F chat_id="CHAT_ID" \
  -F photo=@"/path/to/image.png" \
  -F caption="Caption text"
```

## Sending a Document/File

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendDocument" \
  -F chat_id="CHAT_ID" \
  -F document=@"/path/to/file.pdf"
```

## Getting Updates (check incoming messages)

```bash
curl -s "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getUpdates?limit=10&offset=-10"
```

## Security
- Always validate that the sender's `from.id` is in the allowed list (`TELEGRAM_ALLOWED_IDS`) before processing commands.
- Never expose the bot token in logs or responses.

## How to Apply
When the user asks you to notify them, send a result, or communicate via Telegram, use the curl commands above.
For longer text, split into chunks under 4096 characters.

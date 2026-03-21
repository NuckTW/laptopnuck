---
name: google-services
description: Access Gmail, Google Calendar, Google Drive, and Google Sheets. Use when the user asks about email, calendar events, files, or spreadsheets.
---

# Google Services Skill

Google API Bridge is running at **http://localhost:8766**
Use `curl` to call it. No Python needed.

## Gmail

**List unread emails:**
```bash
curl http://localhost:8766/gmail/unread?max=10
```

**Send email:**
```bash
curl -X POST http://localhost:8766/gmail/send \
  -H "Content-Type: application/json" \
  -d '{"to": "recipient@gmail.com", "subject": "Subject", "body": "Message body"}'
```

## Google Calendar

**List upcoming events:**
```bash
curl http://localhost:8766/calendar/events?max=10
```

**Create event:**
```bash
curl -X POST http://localhost:8766/calendar/events \
  -H "Content-Type: application/json" \
  -d '{"summary": "Event Title", "start": "2026-03-22T10:00:00+08:00", "end": "2026-03-22T11:00:00+08:00", "location": "台南"}'
```
Returns `link` field as proof of creation.

## Google Drive

**Search files:**
```bash
curl "http://localhost:8766/drive/search?q=keyword&max=10"
```

## Google Sheets

**Read sheet:**
```bash
curl "http://localhost:8766/sheets/read?sheet_id=SHEET_ID&range=A1:Z100"
```

**Append rows:**
```bash
curl -X POST http://localhost:8766/sheets/append \
  -H "Content-Type: application/json" \
  -d '{"sheet_id": "SHEET_ID", "rows": [["col1", "col2", "col3"]]}'
```

## How to Apply
- Always confirm success and return a human-readable summary of what was done.
- For Calendar events, always return the event `link` as proof of creation.
- If the bridge returns an error, report it to the user.
- The bridge runs on localhost:8766 — it is always available when the agent is running.

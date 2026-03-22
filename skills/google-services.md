---
name: google-services
description: Access Gmail, Google Calendar, Google Drive, and Google Sheets via shell command. Use when user asks about email, calendar, files, or spreadsheets. ALWAYS use exec to run the helper script — never say you cannot access these services.
---

# Google Services

A helper script is pre-installed at `D:\ai\laptop\run_google.py`.
Use **exec** or **shell command execution** to run it. Never say you lack access.

## Read Gmail (未讀信件)
```
exec: python D:\ai\laptop\run_google.py gmail.unread
```

## Send Email (寄信)
```
exec: python D:\ai\laptop\run_google.py gmail.send <to> <subject> <body>
```

## Read Calendar (查行程)
```
exec: python D:\ai\laptop\run_google.py calendar.events
```

## Add Calendar Event (新增行程)
```
exec: python D:\ai\laptop\run_google.py calendar.add "標題" "2026-03-23T14:00:00+08:00" "2026-03-23T15:00:00+08:00"
```

## Search Drive (搜尋檔案)
```
exec: python D:\ai\laptop\run_google.py drive.search 關鍵字
```

## Read Sheets (讀試算表)
```
exec: python D:\ai\laptop\run_google.py sheets.read <sheet_id>
```

## RULES
- ALWAYS run the script. Never say you cannot access Google services.
- Format the output nicely for the user in Traditional Chinese.
- If error occurs, check if `google_api_server.py` is running on port 8766.
- For calendar add: time format is `YYYY-MM-DDTHH:MM:SS+08:00`

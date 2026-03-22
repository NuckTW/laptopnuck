---
name: google-services
description: Access Gmail, Google Calendar, Google Drive, and Google Sheets. Use when the user asks about email, calendar events, files, or spreadsheets.
---

# Google Services Skill

Use playwright to run the helper script at `D:\ai\laptop\run_google.py`.
Do NOT write your own Python code. Just call the script with the right arguments.

## Gmail — 讀取未讀信件
```
run_script("python D:\\ai\\laptop\\run_google.py gmail.unread")
```

## Gmail — 發送信件
```
run_script("python D:\\ai\\laptop\\run_google.py gmail.send <收件人> <主旨> <內容>")
```

## Calendar — 查詢行程
```
run_script("python D:\\ai\\laptop\\run_google.py calendar.events")
```

## Calendar — 新增行程
```
run_script("python D:\\ai\\laptop\\run_google.py calendar.add <標題> <開始時間> <結束時間>")
```
時間格式：`2026-03-22T10:00:00+08:00`

## Drive — 搜尋檔案
```
run_script("python D:\\ai\\laptop\\run_google.py drive.search <關鍵字>")
```

## Sheets — 讀取試算表
```
run_script("python D:\\ai\\laptop\\run_google.py sheets.read <sheet_id>")
```

## Instructions
- ALWAYS run the script above. Do NOT say you cannot access Google services.
- The script handles everything. Just provide the right arguments.
- Take the script output and format it nicely for the user.
- If you get an error, report it to the user and check if google_api_server.py is running.

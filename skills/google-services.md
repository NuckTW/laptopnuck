---
name: google-services
description: Access Gmail, Google Calendar, Google Drive, and Google Sheets. Use when the user asks about email, calendar events, files, or spreadsheets.
---

# Google Services Skill

A local Google API Bridge runs at **http://localhost:8766**.
Use `exec()` to call it with Python.

## Gmail

**List unread emails — run this:**
```
exec(command='''python -c "import requests,json; r=requests.get('http://localhost:8766/gmail/unread',params={'max':10}); print(json.dumps(r.json(),ensure_ascii=False))"''')
```

**Send email — run this:**
```
exec(command='''python -c "import requests,json; r=requests.post('http://localhost:8766/gmail/send',json={'to':'RECIPIENT','subject':'SUBJECT','body':'BODY'}); print(json.dumps(r.json(),ensure_ascii=False))"''')
```

## Google Calendar

**List upcoming events — run this:**
```
exec(command='''python -c "import requests,json; r=requests.get('http://localhost:8766/calendar/events',params={'max':10}); print(json.dumps(r.json(),ensure_ascii=False))"''')
```

**Create event — run this:**
```
exec(command='''python -c "import requests,json; r=requests.post('http://localhost:8766/calendar/events',json={'summary':'TITLE','start':'2026-03-22T10:00:00+08:00','end':'2026-03-22T11:00:00+08:00','location':'台南'}); print(json.dumps(r.json(),ensure_ascii=False))"''')
```

## Google Drive

**Search files — run this:**
```
exec(command='''python -c "import requests,json; r=requests.get('http://localhost:8766/drive/search',params={'q':'KEYWORD','max':10}); print(json.dumps(r.json(),ensure_ascii=False))"''')
```

## Google Sheets

**Read sheet — run this:**
```
exec(command='''python -c "import requests,json; r=requests.get('http://localhost:8766/sheets/read',params={'sheet_id':'SHEET_ID','range':'A1:Z100'}); print(json.dumps(r.json(),ensure_ascii=False))"''')
```

**Append rows — run this:**
```
exec(command='''python -c "import requests,json; r=requests.post('http://localhost:8766/sheets/append',json={'sheet_id':'SHEET_ID','rows':[['col1','col2']]}); print(json.dumps(r.json(),ensure_ascii=False))"''')
```

## Instructions
- ALWAYS use exec() to run the commands above. Do NOT say you cannot access Google services.
- Replace placeholders (RECIPIENT, SUBJECT, KEYWORD, SHEET_ID, etc.) with actual values.
- Return the result in a human-readable format to the user.
- For Calendar events, always include the event `link` in your response as proof of creation.

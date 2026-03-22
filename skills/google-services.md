---
name: google-services
description: Access Gmail, Google Calendar, Google Drive, and Google Sheets. Use when the user asks about email, calendar events, files, or spreadsheets.
---

# Google Services Skill

A local Google API Bridge runs at **http://localhost:8766**.
To call it, write and execute Python code using the `requests` library.

## Gmail

**List unread emails:**
```python
import requests
r = requests.get("http://localhost:8766/gmail/unread", params={"max": 10})
print(r.json())
```

**Send email:**
```python
import requests
r = requests.post("http://localhost:8766/gmail/send", json={
    "to": "recipient@gmail.com",
    "subject": "Subject",
    "body": "Message body"
})
print(r.json())
```

## Google Calendar

**List upcoming events:**
```python
import requests
r = requests.get("http://localhost:8766/calendar/events", params={"max": 10})
print(r.json())
```

**Create event:**
```python
import requests
r = requests.post("http://localhost:8766/calendar/events", json={
    "summary": "Event Title",
    "start": "2026-03-22T10:00:00+08:00",
    "end": "2026-03-22T11:00:00+08:00",
    "location": "台南"
})
print(r.json())  # Returns link field as proof
```

## Google Drive

**Search files:**
```python
import requests
r = requests.get("http://localhost:8766/drive/search", params={"q": "keyword", "max": 10})
print(r.json())
```

## Google Sheets

**Read sheet:**
```python
import requests
r = requests.get("http://localhost:8766/sheets/read", params={"sheet_id": "SHEET_ID", "range": "A1:Z100"})
print(r.json())
```

**Append rows:**
```python
import requests
r = requests.post("http://localhost:8766/sheets/append", json={
    "sheet_id": "SHEET_ID",
    "rows": [["col1", "col2", "col3"]]
})
print(r.json())
```

## Instructions
- ALWAYS execute the Python code above to get real data. Do not say you cannot access Google services.
- The bridge at localhost:8766 is always running. Use `requests` to call it.
- Return a human-readable summary of the result to the user.
- For Calendar events, always return the event `link` as proof of creation.
- If the bridge returns an error, report it to the user.

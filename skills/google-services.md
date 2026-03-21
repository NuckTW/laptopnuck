---
name: google-services
description: Access Gmail, Google Calendar, Google Drive, and Google Sheets via OAuth2. Use when the user asks about email, calendar events, files, or spreadsheets.
---

# Google Services Skill

You can read and write to the user's Google account via OAuth2.

## Credentials Setup
- `credentials.json` — at `D:\ai\laptop\credentials.json`
- `token.json` — at `D:\ai\laptop\token.json` (already generated)
- Environment: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`

## Load credentials (always use this block first)
```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

TOKEN_PATH = r'D:\ai\laptop\token.json'
CREDS_PATH = r'D:\ai\laptop\credentials.json'

creds = Credentials.from_authorized_user_file(TOKEN_PATH)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open(TOKEN_PATH, 'w') as f:
        f.write(creds.to_json())
```

## OAuth Scopes Available
- `https://www.googleapis.com/auth/gmail.modify` — Read + send Gmail
- `https://www.googleapis.com/auth/calendar` — Read + create Calendar events
- `https://www.googleapis.com/auth/drive` — Read + write Google Drive
- `https://www.googleapis.com/auth/spreadsheets` — Read + write Google Sheets

## Gmail

**List unread emails:**
```python
from googleapiclient.discovery import build
service = build('gmail', 'v1', credentials=creds)
results = service.users().messages().list(userId='me', q='is:unread', maxResults=10).execute()
```

**Send email:**
```python
import base64
from email.mime.text import MIMEText
msg = MIMEText('Hello')
msg['To'] = 'recipient@gmail.com'
msg['Subject'] = 'Subject'
raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
service.users().messages().send(userId='me', body={'raw': raw}).execute()
```

## Google Calendar

**List upcoming events:**
```python
service = build('calendar', 'v3', credentials=creds)
events = service.events().list(
    calendarId='primary', timeMin=now_iso, maxResults=10,
    singleEvents=True, orderBy='startTime'
).execute()
```

**Create event:**
```python
event = {
    'summary': 'Event Title',
    'start': {'dateTime': '2026-03-21T10:00:00+08:00'},
    'end':   {'dateTime': '2026-03-21T11:00:00+08:00'},
}
result = service.events().insert(calendarId='primary', body=event).execute()
# Returns: result['htmlLink'] as confirmation
```

## Google Drive

**Search for files:**
```python
service = build('drive', 'v3', credentials=creds)
results = service.files().list(q="name contains 'keyword'", fields='files(id, name)').execute()
```

## Google Sheets

**Read a sheet:**
```python
service = build('sheets', 'v4', credentials=creds)
result = service.spreadsheets().values().get(
    spreadsheetId='SHEET_ID', range='Sheet1!A1:Z100'
).execute()
rows = result.get('values', [])
```

**Append a row:**
```python
service.spreadsheets().values().append(
    spreadsheetId='SHEET_ID', range='Sheet1!A:Z',
    valueInputOption='USER_ENTERED',
    body={'values': [['col1', 'col2', 'col3']]}
).execute()
```

## How to Apply
When the user asks about email, calendar, files, or spreadsheets — use the appropriate Google API above.
Always confirm success and return a human-readable summary of what was done.
For Calendar events, always return the event link as proof of creation.

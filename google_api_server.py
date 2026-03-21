"""
google_api_server.py — Local Google API bridge for nuck001
Run: python google_api_server.py
Port: 8766
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import base64
from email.mime.text import MIMEText
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = r'D:\ai\laptop\token.json'

app = FastAPI(title='Google API Bridge', version='1.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])


def get_creds():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
    return creds


# ── Gmail ──────────────────────────────────────────────────

@app.get('/gmail/unread')
def gmail_unread(max: int = 10):
    """列出未讀郵件"""
    creds = get_creds()
    svc = build('gmail', 'v1', credentials=creds)
    results = svc.users().messages().list(userId='me', q='is:unread', maxResults=max).execute()
    msgs = results.get('messages', [])
    out = []
    for m in msgs:
        detail = svc.users().messages().get(userId='me', id=m['id'], format='metadata',
            metadataHeaders=['Subject','From','Date']).execute()
        headers = {h['name']: h['value'] for h in detail['payload']['headers']}
        out.append({
            'id': m['id'],
            'subject': headers.get('Subject', ''),
            'from': headers.get('From', ''),
            'date': headers.get('Date', ''),
            'snippet': detail.get('snippet', '')
        })
    return {'count': len(out), 'emails': out}


class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str

@app.post('/gmail/send')
def gmail_send(req: SendEmailRequest):
    """寄送郵件"""
    creds = get_creds()
    svc = build('gmail', 'v1', credentials=creds)
    msg = MIMEText(req.body)
    msg['To'] = req.to
    msg['Subject'] = req.subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = svc.users().messages().send(userId='me', body={'raw': raw}).execute()
    return {'message_id': result['id'], 'status': 'sent'}


# ── Google Calendar ────────────────────────────────────────

@app.get('/calendar/events')
def calendar_events(max: int = 10):
    """列出即將到來的行程"""
    creds = get_creds()
    svc = build('calendar', 'v3', credentials=creds)
    now = datetime.now(timezone.utc).isoformat()
    events = svc.events().list(
        calendarId='primary', timeMin=now, maxResults=max,
        singleEvents=True, orderBy='startTime'
    ).execute()
    items = events.get('items', [])
    out = []
    for e in items:
        start = e['start'].get('dateTime', e['start'].get('date', ''))
        out.append({
            'id': e['id'],
            'summary': e.get('summary', ''),
            'start': start,
            'end': e['end'].get('dateTime', e['end'].get('date', '')),
            'location': e.get('location', ''),
            'link': e.get('htmlLink', '')
        })
    return {'count': len(out), 'events': out}


class CreateEventRequest(BaseModel):
    summary: str
    start: str   # ISO format: 2026-03-22T10:00:00+08:00
    end: str
    location: Optional[str] = ''
    description: Optional[str] = ''

@app.post('/calendar/events')
def calendar_create(req: CreateEventRequest):
    """建立行程"""
    creds = get_creds()
    svc = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': req.summary,
        'start': {'dateTime': req.start, 'timeZone': 'Asia/Taipei'},
        'end': {'dateTime': req.end, 'timeZone': 'Asia/Taipei'},
    }
    if req.location:
        event['location'] = req.location
    if req.description:
        event['description'] = req.description
    result = svc.events().insert(calendarId='primary', body=event).execute()
    return {'event_id': result['id'], 'link': result['htmlLink'], 'status': 'created'}


# ── Google Drive ───────────────────────────────────────────

@app.get('/drive/search')
def drive_search(q: str, max: int = 10):
    """搜尋 Drive 檔案"""
    creds = get_creds()
    svc = build('drive', 'v3', credentials=creds)
    results = svc.files().list(
        q=f"name contains '{q}' and trashed=false",
        fields='files(id, name, mimeType, modifiedTime, webViewLink)',
        pageSize=max
    ).execute()
    return {'files': results.get('files', [])}


# ── Google Sheets ──────────────────────────────────────────

@app.get('/sheets/read')
def sheets_read(sheet_id: str, range: str = 'A1:Z100'):
    """讀取試算表"""
    creds = get_creds()
    svc = build('sheets', 'v4', credentials=creds)
    # 自動取得第一個 tab 名稱
    meta = svc.spreadsheets().get(spreadsheetId=sheet_id).execute()
    tab = meta['sheets'][0]['properties']['title']
    result = svc.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=f'{tab}!{range}'
    ).execute()
    return {'tab': tab, 'values': result.get('values', [])}


class AppendRowRequest(BaseModel):
    sheet_id: str
    rows: List[List[str]]

@app.post('/sheets/append')
def sheets_append(req: AppendRowRequest):
    """新增資料到試算表"""
    creds = get_creds()
    svc = build('sheets', 'v4', credentials=creds)
    meta = svc.spreadsheets().get(spreadsheetId=req.sheet_id).execute()
    tab = meta['sheets'][0]['properties']['title']
    svc.spreadsheets().values().append(
        spreadsheetId=req.sheet_id,
        range=f'{tab}!A:Z',
        valueInputOption='USER_ENTERED',
        body={'values': req.rows}
    ).execute()
    return {'status': 'appended', 'rows': len(req.rows), 'tab': tab}


# ── Health check ───────────────────────────────────────────

@app.get('/')
def health():
    return {'status': 'ok', 'service': 'Google API Bridge', 'port': 8766}


if __name__ == '__main__':
    print('Google API Bridge starting on http://localhost:8766')
    uvicorn.run(app, host='127.0.0.1', port=8766)

"""
upload_report.py — 監工日報表上傳 Google Sheets
使用方式: python upload_report.py
"""

import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime

TOKEN_PATH = r'D:\ai\laptop\token.json'
SHEET_NAME = '監工日報表'

# ── 載入 OAuth token ──────────────────────────────────────
creds = Credentials.from_authorized_user_file(TOKEN_PATH)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open(TOKEN_PATH, 'w') as f:
        f.write(creds.to_json())

sheets_service = build('sheets', 'v4', credentials=creds)
drive_service  = build('drive', 'v3', credentials=creds)

# ── 找或建立試算表 ────────────────────────────────────────
def get_sheet_tab_name(sheet_id):
    """取得試算表第一個工作表的實際名稱"""
    meta = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    return meta['sheets'][0]['properties']['title']

def get_or_create_sheet():
    results = drive_service.files().list(
        q=f"name='{SHEET_NAME}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
        fields='files(id, name)'
    ).execute()
    files = results.get('files', [])
    if files:
        sheet_id = files[0]['id']
        print(f'找到既有試算表: {sheet_id}')
        return sheet_id
    # 建立新試算表
    spreadsheet = sheets_service.spreadsheets().create(body={
        'properties': {'title': SHEET_NAME},
        'sheets': [{'properties': {'title': '監工日報表'}}]
    }).execute()
    sheet_id = spreadsheet['spreadsheetId']
    print(f'新建試算表: {sheet_id}')
    # 寫入表頭
    tab = get_sheet_tab_name(sheet_id)
    headers = [['日期','星期','天數','天氣','工種','上午','下午','合計',
                 '工作進度','材料','廠牌','規格','數量','備註','點工','點工工作','重要記事']]
    sheets_service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range=f'{tab}!A1',
        valueInputOption='USER_ENTERED',
        body={'values': headers}
    ).execute()
    return sheet_id

# ── 要上傳的資料（來自 OCR）────────────────────────────────
data = [
    '115/3/18',   # 日期
    '星期二',      # 星期
    '387',         # 天數
    '晴',          # 天氣
    '粗工/泥作/鐵工/電工',  # 工種
    '',            # 上午
    '',            # 下午
    '',            # 合計
    '清潔',        # 工作進度
    '',            # 材料
    '',            # 廠牌
    '',            # 規格
    '',            # 數量
    '',            # 備註
    '朱',          # 點工
    '',            # 點工工作
    '水錶 546',    # 重要記事
]

# ── 上傳 ─────────────────────────────────────────────────
sheet_id = get_or_create_sheet()
tab = get_sheet_tab_name(sheet_id)
print(f'工作表名稱: {tab}')

sheets_service.spreadsheets().values().append(
    spreadsheetId=sheet_id,
    range=f'{tab}!A:Q',
    valueInputOption='USER_ENTERED',
    body={'values': [data]}
).execute()

print(f'上傳成功！')
print(f'試算表連結: https://docs.google.com/spreadsheets/d/{sheet_id}')

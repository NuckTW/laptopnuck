"""
nuck001 Python Telegram Bot
直接整合 Gemini + Google API Bridge + DALL-E 3
"""
import os
import re
import json
import time
import requests
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ALLOWED_IDS = [int(x) for x in os.getenv("TELEGRAM_ALLOWED_IDS", "").split(",") if x]
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_BRIDGE = "http://localhost:8766"

SYSTEM_PROMPT = """你是 nuck001，NuckTW 的專屬 AI 私人助手，形象是賽博龐克俄羅斯虎斑貓。
你運行在 LAPTOP-Nuck（Windows）上，擁有以下能力：
- 讀取/發送 Gmail 郵件
- 查詢/建立 Google Calendar 行程
- 搜尋 Google Drive 檔案
- 讀寫 Google Sheets
- 分析圖片（Gemini Vision）
- 生成圖片（DALL-E 3）
回答簡潔有力，繁體中文，必要時用表情符號。"""

def tg(method, **kwargs):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    return requests.post(url, **kwargs).json()

def send(chat_id, text, **kwargs):
    return tg("sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown", **kwargs})

def send_photo(chat_id, photo_url):
    return tg("sendPhoto", json={"chat_id": chat_id, "photo": photo_url})

def gemini_chat(messages):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    contents = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in messages]
    r = requests.post(url, json={"contents": contents, "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]}})
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

def gemini_vision(image_bytes, prompt="請分析這張圖片"):
    import base64
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    img_b64 = base64.b64encode(image_bytes).decode()
    r = requests.post(url, json={
        "contents": [{"parts": [
            {"text": prompt},
            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
        ]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]}
    })
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

def dalle3(prompt):
    r = requests.post("https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"model": "dall-e-3", "prompt": prompt, "n": 1, "size": "1024x1024"}
    )
    return r.json()["data"][0]["url"]

def google_api(endpoint, method="get", **kwargs):
    try:
        if method == "get":
            r = requests.get(f"{GOOGLE_BRIDGE}{endpoint}", **kwargs)
        else:
            r = requests.post(f"{GOOGLE_BRIDGE}{endpoint}", **kwargs)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def route(text, chat_history):
    t = text.lower()

    # Gmail
    if any(k in t for k in ["信件", "email", "gmail", "mail", "收件", "未讀"]):
        data = google_api("/gmail/unread", params={"max": 10})
        if "error" in data:
            return f"Gmail 連線失敗：{data['error']}"
        emails = data.get("emails", [])
        if not emails:
            return "目前沒有未讀信件。"
        lines = [f"📬 共 {len(emails)} 封未讀信件：\n"]
        for e in emails:
            lines.append(f"• **{e.get('subject','(無主旨)')}**\n  寄件人：{e.get('from','?')}\n  {e.get('snippet','')[:80]}\n")
        return "\n".join(lines)

    # Calendar
    if any(k in t for k in ["行程", "calendar", "行事曆", "會議", "約", "schedule"]):
        data = google_api("/calendar/events", params={"max": 10})
        if "error" in data:
            return f"Calendar 連線失敗：{data['error']}"
        events = data.get("events", [])
        if not events:
            return "最近沒有行程。"
        lines = ["📅 最近行程：\n"]
        for ev in events:
            lines.append(f"• **{ev.get('summary','(無標題)')}**\n  {ev.get('start','?')} ～ {ev.get('end','?')}\n  {ev.get('location','')}")
        return "\n".join(lines)

    # Drive
    if any(k in t for k in ["drive", "雲端", "檔案", "file", "document"]):
        query = re.search(r"搜尋[「\"]?(.+?)[」\"]?$", text)
        q = query.group(1) if query else text
        data = google_api("/drive/search", params={"q": q, "max": 10})
        if "error" in data:
            return f"Drive 連線失敗：{data['error']}"
        files = data.get("files", [])
        if not files:
            return "沒有找到相關檔案。"
        lines = ["📁 搜尋結果：\n"]
        for f in files:
            lines.append(f"• {f.get('name','?')} ({f.get('mimeType','?')})")
        return "\n".join(lines)

    # Image generation
    if any(k in t for k in ["生圖", "畫圖", "generate image", "dall-e", "生成圖", "畫一張"]):
        prompt = re.sub(r"(生圖|畫圖|生成圖|畫一張)", "", text).strip()
        if not prompt:
            return "請描述你想生成的圖片內容。"
        return ("DALLE3:" + prompt)  # special marker

    # General chat
    chat_history.append({"role": "user", "content": text})
    reply = gemini_chat(chat_history[-20:])
    chat_history.append({"role": "model", "content": reply})
    return reply

def main():
    print(f"🐯 nuck001 Python Bot 啟動")
    offset = 0
    chat_histories = {}

    while True:
        try:
            updates = tg("getUpdates", params={"offset": offset, "timeout": 30})
            for upd in updates.get("result", []):
                offset = upd["id"] + 1
                msg = upd.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                user_id = msg.get("from", {}).get("id")

                if not chat_id or user_id not in ALLOWED_IDS:
                    continue

                if chat_id not in chat_histories:
                    chat_histories[chat_id] = []

                # Photo
                if "photo" in msg:
                    photos = msg["photo"]
                    file_id = photos[-1]["file_id"]
                    caption = msg.get("caption", "請分析這張圖片")
                    file_info = tg("getFile", params={"file_id": file_id})
                    file_path = file_info["result"]["file_path"]
                    img_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
                    img_bytes = requests.get(img_url).content
                    send(chat_id, "🔍 分析中...")
                    reply = gemini_vision(img_bytes, caption)
                    send(chat_id, reply)
                    continue

                text = msg.get("text", "")
                if not text:
                    continue

                if text == "/start":
                    send(chat_id, "🐯 我是 nuck001，賽博龐克俄羅斯虎斑貓！有什麼需要？")
                    continue

                if text == "/reset":
                    chat_histories[chat_id] = []
                    send(chat_id, "✅ 對話記憶已清除")
                    continue

                result = route(text, chat_histories[chat_id])

                if result.startswith("DALLE3:"):
                    prompt = result[7:]
                    send(chat_id, "🎨 生成中...")
                    img_url = dalle3(prompt)
                    send_photo(chat_id, img_url)
                else:
                    send(chat_id, result)

        except KeyboardInterrupt:
            print("Bot 已停止")
            break
        except Exception as e:
            print(f"錯誤: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

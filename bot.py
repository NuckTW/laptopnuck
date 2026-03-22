"""
nuck001 Python Telegram Bot
單一入口：Gemini + Google API + DALL-E 3 + 記憶系統
"""
import os, re, json, time, base64, datetime
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
ALLOWED_IDS      = [int(x) for x in os.getenv("TELEGRAM_ALLOWED_IDS","").split(",") if x]
GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL     = os.getenv("GEMINI_MODEL","gemini-2.5-flash")
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
GOOGLE_BRIDGE    = "http://localhost:8766"
MEMORY_DIR       = Path(__file__).parent / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

# ── 載入身份設定 ──────────────────────────────────────────
def load_md(*filenames):
    parts = []
    for f in filenames:
        p = Path(__file__).parent / f
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))
    return "\n\n".join(parts)

def build_system_prompt():
    identity = load_md("soul.md", "user.md", "agents.md")
    # 載入最近 3 天記憶
    today = datetime.date.today()
    memories = []
    for d in range(3):
        day = today - datetime.timedelta(days=d)
        f = MEMORY_DIR / f"{day}.md"
        if f.exists():
            memories.append(f"## {day}\n" + f.read_text(encoding="utf-8"))
    mem_text = "\n\n".join(memories) if memories else "（無近期記憶）"
    return f"{identity}\n\n---\n# 近期記憶\n{mem_text}"

# ── 記憶存檔 ──────────────────────────────────────────────
def save_memory(text):
    today = datetime.date.today()
    f = MEMORY_DIR / f"{today}.md"
    ts = datetime.datetime.now().strftime("%H:%M")
    with open(f, "a", encoding="utf-8") as fp:
        fp.write(f"\n- [{ts}] {text}\n")

# ── Telegram API ──────────────────────────────────────────
def tg(method, **kwargs):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    r = requests.post(url, **kwargs, timeout=30)
    return r.json()

def send(chat_id, text):
    # 超過 4000 字分段
    for i in range(0, len(text), 4000):
        tg("sendMessage", json={"chat_id": chat_id, "text": text[i:i+4000], "parse_mode": "Markdown"})

def send_photo(chat_id, photo_url):
    tg("sendPhoto", json={"chat_id": chat_id, "photo": photo_url})

# ── Gemini ────────────────────────────────────────────────
def gemini_chat(system_prompt, history):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    contents = []
    for m in history[-20:]:
        contents.append({"role": m["role"], "parts": [{"text": m["content"]}]})
    body = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }
    r = requests.post(url, json=body, timeout=60)
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

def gemini_vision(image_bytes, prompt, system_prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    img_b64 = base64.b64encode(image_bytes).decode()
    r = requests.post(url, json={
        "contents": [{"parts": [
            {"text": prompt},
            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
        ]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }, timeout=60)
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

# ── DALL-E 3 ──────────────────────────────────────────────
def dalle3(prompt):
    r = requests.post("https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"model": "dall-e-3", "prompt": prompt, "n": 1, "size": "1024x1024"},
        timeout=60
    )
    return r.json()["data"][0]["url"]

# ── Google API Bridge ─────────────────────────────────────
def google(endpoint, method="get", **kwargs):
    try:
        fn = requests.get if method=="get" else requests.post
        r = fn(f"{GOOGLE_BRIDGE}{endpoint}", timeout=15, **kwargs)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# ── 智慧路由 ──────────────────────────────────────────────
def route(text, history, system_prompt):
    t = text.lower()

    # Gmail
    if any(k in t for k in ["信件","email","gmail","mail","收件","未讀","寄信","發信"]):
        if any(k in t for k in ["寄","發","send"]):
            return "📝 請提供：收件人、主旨、內容，格式：\n寄給 xxx@gmail.com\n主旨：...\n內容：..."
        data = google("/gmail/unread", params={"max":10})
        if "error" in data:
            return f"❌ Gmail 連線失敗（確認 google_api_server.py 有在跑）：{data['error']}"
        emails = data.get("emails", [])
        if not emails:
            return "📬 目前沒有未讀信件。"
        lines = [f"📬 共 {len(emails)} 封未讀：\n"]
        for e in emails:
            lines.append(f"• *{e.get('subject','(無主旨)')}*\n  寄件人：{e.get('from','?')}\n  {e.get('snippet','')[:100]}\n")
        return "\n".join(lines)

    # Calendar
    if any(k in t for k in ["行程","calendar","行事曆","會議","schedule","今天","明天","這週"]):
        data = google("/calendar/events", params={"max":10})
        if "error" in data:
            return f"❌ Calendar 連線失敗：{data['error']}"
        events = data.get("events", [])
        if not events:
            return "📅 最近沒有行程。"
        lines = ["📅 最近行程：\n"]
        for ev in events:
            lines.append(f"• *{ev.get('summary','(無標題)')}*\n  {ev.get('start','?')}\n  {ev.get('location','')}")
        return "\n".join(lines)

    # Drive
    if any(k in t for k in ["drive","雲端硬碟","搜尋檔案","找檔案"]):
        q = re.sub(r"(drive|雲端硬碟|搜尋檔案|找檔案)", "", text).strip() or text
        data = google("/drive/search", params={"q":q,"max":10})
        if "error" in data:
            return f"❌ Drive 連線失敗：{data['error']}"
        files = data.get("files",[])
        if not files:
            return "📁 找不到相關檔案。"
        return "📁 搜尋結果：\n" + "\n".join(f"• {f.get('name','?')}" for f in files)

    # Image generation
    if any(k in t for k in ["生圖","畫圖","生成圖","畫一張","dall-e"]):
        prompt = re.sub(r"(生圖|畫圖|生成圖|畫一張|dall-e)", "", text).strip()
        return "__DALLE3__:" + (prompt or text)

    # 一般對話 → Gemini
    history.append({"role": "user", "content": text})
    reply = gemini_chat(system_prompt, history)
    history.append({"role": "model", "content": reply})

    # 判斷是否要存記憶（重要訊息）
    keywords = ["記住","記下","重要","提醒","備忘","待辦"]
    if any(k in text for k in keywords):
        save_memory(f"用戶：{text} → 回覆：{reply[:100]}")

    return reply

# ── 主程式 ────────────────────────────────────────────────
def main():
    system_prompt = build_system_prompt()
    print(f"🐯 nuck001 啟動（{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}）")
    print(f"   身份設定：{'已載入' if 'soul' in system_prompt.lower() or len(system_prompt)>200 else '未找到 soul.md'}")
    print(f"   記憶目錄：{MEMORY_DIR}")

    offset = 0
    histories = {}  # chat_id → list

    while True:
        try:
            upds = tg("getUpdates", params={"offset": offset, "timeout": 30})
            for upd in upds.get("result", []):
                offset = upd["id"] + 1
                msg = upd.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                user_id = msg.get("from", {}).get("id")
                if not chat_id or user_id not in ALLOWED_IDS:
                    continue
                if chat_id not in histories:
                    histories[chat_id] = []

                # 照片
                if "photo" in msg:
                    file_id = msg["photo"][-1]["file_id"]
                    caption = msg.get("caption", "請詳細描述這張圖片的內容")
                    fi = tg("getFile", params={"file_id": file_id})
                    fp = fi["result"]["file_path"]
                    img = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{fp}").content
                    send(chat_id, "🔍 分析中...")
                    reply = gemini_vision(img, caption, system_prompt)
                    send(chat_id, reply)
                    save_memory(f"收到圖片分析：{reply[:80]}")
                    continue

                text = msg.get("text", "")
                if not text:
                    continue

                if text == "/start":
                    send(chat_id, "🐯 nuck001 就緒！有什麼需要？\n\n可以問我：信件、行程、生圖、分析圖片...")
                    continue
                if text == "/reset":
                    histories[chat_id] = []
                    send(chat_id, "✅ 對話記憶已清除")
                    continue
                if text == "/status":
                    bridge = "✅ 運行中" if requests.get(f"{GOOGLE_BRIDGE}/health", timeout=3).status_code==200 else "❌ 未啟動" if True else "?"
                    send(chat_id, f"🐯 nuck001 狀態\n• Google Bridge: {bridge}\n• 記憶：{MEMORY_DIR}")
                    continue

                result = route(text, histories[chat_id], system_prompt)

                if result.startswith("__DALLE3__:"):
                    prompt = result[11:]
                    send(chat_id, "🎨 生成中...")
                    try:
                        url = dalle3(prompt)
                        send_photo(chat_id, url)
                    except Exception as e:
                        send(chat_id, f"❌ 生圖失敗：{e}")
                else:
                    send(chat_id, result)

        except KeyboardInterrupt:
            print("\n🐯 Bot 已停止")
            break
        except Exception as e:
            print(f"錯誤: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

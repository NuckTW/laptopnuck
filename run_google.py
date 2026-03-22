"""
nuck001 Google API Helper
nuck001 透過 playwright 呼叫這個腳本
用法：python run_google.py <指令> [參數]

指令：
  gmail.unread          讀取未讀信件
  gmail.send <to> <subject> <body>  發送信件
  calendar.events       查詢行程
  calendar.add <summary> <start> <end>  新增行程
  drive.search <keyword>  搜尋檔案
  sheets.read <sheet_id>  讀試算表
  sheets.append <sheet_id> <json_rows>  寫入試算表
"""
import sys, json, requests

BRIDGE = "http://localhost:8766"

def run(args):
    if not args:
        print("錯誤：請提供指令")
        return

    cmd = args[0]

    if cmd == "gmail.unread":
        r = requests.get(f"{BRIDGE}/gmail/unread", params={"max": 10}, timeout=15)
        data = r.json()
        emails = data.get("emails", [])
        if not emails:
            print("沒有未讀信件")
            return
        print(f"共 {len(emails)} 封未讀信件：")
        for e in emails:
            print(f"- 主旨：{e.get('subject','(無主旨)')}")
            print(f"  寄件人：{e.get('from','?')}")
            print(f"  摘要：{e.get('snippet','')[:120]}")
            print()

    elif cmd == "gmail.send":
        to, subject, body = args[1], args[2], " ".join(args[3:])
        r = requests.post(f"{BRIDGE}/gmail/send", json={"to": to, "subject": subject, "body": body}, timeout=15)
        print(r.json())

    elif cmd == "calendar.events":
        r = requests.get(f"{BRIDGE}/calendar/events", params={"max": 10}, timeout=15)
        data = r.json()
        events = data.get("events", [])
        if not events:
            print("最近沒有行程")
            return
        print("最近行程：")
        for ev in events:
            print(f"- {ev.get('summary','(無標題)')}")
            print(f"  時間：{ev.get('start','?')} ~ {ev.get('end','?')}")
            if ev.get("location"):
                print(f"  地點：{ev.get('location')}")
            print()

    elif cmd == "calendar.add":
        summary = args[1]
        start = args[2]
        end = args[3] if len(args) > 3 else args[2]
        r = requests.post(f"{BRIDGE}/calendar/events", json={
            "summary": summary, "start": start, "end": end
        }, timeout=15)
        data = r.json()
        print(f"行程已建立：{data.get('link', data)}")

    elif cmd == "drive.search":
        q = " ".join(args[1:])
        r = requests.get(f"{BRIDGE}/drive/search", params={"q": q, "max": 10}, timeout=15)
        data = r.json()
        files = data.get("files", [])
        if not files:
            print("找不到相關檔案")
            return
        print(f"找到 {len(files)} 個檔案：")
        for f in files:
            print(f"- {f.get('name','?')}")

    elif cmd == "sheets.read":
        sheet_id = args[1]
        r = requests.get(f"{BRIDGE}/sheets/read", params={"sheet_id": sheet_id, "range": "A1:Z100"}, timeout=15)
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))

    elif cmd == "sheets.append":
        sheet_id = args[1]
        rows = json.loads(args[2])
        r = requests.post(f"{BRIDGE}/sheets/append", json={"sheet_id": sheet_id, "rows": rows}, timeout=15)
        print(r.json())

    else:
        print(f"未知指令：{cmd}")

if __name__ == "__main__":
    try:
        run(sys.argv[1:])
    except Exception as e:
        print(f"錯誤：{e}")

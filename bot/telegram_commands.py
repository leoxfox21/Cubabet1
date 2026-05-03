import requests
from config import TELEGRAM_TOKEN, CHAT_ID


def send_start_report(matches_count, picks, status="🟢 BOT RUNNING"):

    if not isinstance(picks, list):
        picks = []

    top_pick = picks[0] if len(picks) > 0 else None

    msg = f"""
🤖 BOT STATUS REPORT

Status: {status}

📊 Matches detected: {matches_count}
🎯 Picks generated: {len(picks)}
"""

    if top_pick:
        msg += f"""
🔥 TOP PICK

{top_pick.get('match')}
Odds: {top_pick.get('odds')}
Prob: {round(top_pick.get('prob', 0)*100,1)}%
Value: {round(top_pick.get('value', 0)*100,1)}%
Score: {round(top_pick.get('score', 0),3)}
"""
    else:
        msg += "\n⚠️ No picks generated"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        res = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": msg
        })

        if res.status_code != 200:
            print("❌ TELEGRAM ERROR:", res.text)
        else:
            print("✅ STATUS REPORT SENT")

    except Exception as e:
        print("❌ TELEGRAM EXCEPTION:", str(e))
import requests
from config import TELEGRAM_TOKEN, CHAT_ID


def send_message(text):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        print("📤 Sending message...")

        res = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        })

        if res.status_code != 200:
            print("❌ Telegram error:", res.text)
            return False

        print("✅ Message sent")
        return True

    except Exception as e:
        print("❌ Exception sending Telegram message:", str(e))
        return False
import os

ODDS_API_KEY = os.getenv("ODDS_API_KEY")
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def check_config():

    missing = []

    if not ODDS_API_KEY:
        missing.append("ODDS_API_KEY")

    if not FOOTBALL_API_KEY:
        missing.append("FOOTBALL_API_KEY")

    if not TELEGRAM_TOKEN:
        missing.append("TELEGRAM_TOKEN")

    if not CHAT_ID:
        missing.append("CHAT_ID")

    if missing:
        raise Exception(f"❌ Missing env vars: {missing}")
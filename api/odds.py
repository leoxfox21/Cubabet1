import requests
from config import ODDS_API_KEY
from config.leagues import LEAGUES


def get_odds():

    all_matches = []

    for league in LEAGUES:

        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds"

        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "eu",
            "markets": "totals"
        }

        res = requests.get(url, params=params)

        if res.status_code != 200:
            print(f"ERROR {league}:", res.text)
            continue

        try:
            data = res.json()
            if isinstance(data, list):
                all_matches.extend(data)
        except:
            continue

    print("TOTAL MATCHES:", len(all_matches))
    return all_matches
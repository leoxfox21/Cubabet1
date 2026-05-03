import requests
from config import FOOTBALL_API_KEY


def get_team_stats(team_id):

    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}

    res = requests.get(url, headers=headers)
    data = res.json()

    if not isinstance(data, dict):
        return {"attack": 0, "defense": 0}

    matches = data.get("matches", [])[:10]

    scored = []
    conceded = []

    for match in matches:

        home_id = match["homeTeam"]["id"]
        away_id = match["awayTeam"]["id"]

        home_goals = match["score"]["fullTime"]["home"]
        away_goals = match["score"]["fullTime"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if team_id == home_id:
            scored.append(home_goals)
            conceded.append(away_goals)
        else:
            scored.append(away_goals)
            conceded.append(home_goals)

    if not scored:
        return {"attack": 0, "defense": 0}

    return {
        "attack": sum(scored) / len(scored),
        "defense": sum(conceded) / len(conceded)
    }


def get_last_match_goals(team_id):

    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}

    res = requests.get(url, headers=headers)
    data = res.json()

    if not isinstance(data, dict):
        return None

    matches = data.get("matches", [])

    if not matches:
        return None

    # FIX: asegurar orden real
    matches = sorted(matches, key=lambda x: x["utcDate"], reverse=True)

    last = matches[0]

    home = last["score"]["fullTime"]["home"]
    away = last["score"]["fullTime"]["away"]

    if home is None or away is None:
        return None

    return home + away
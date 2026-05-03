import requests
from config import FOOTBALL_API_KEY

TEAM_CACHE = {}


def load_teams():
    url = "https://api.football-data.org/v4/competitions/SA/teams"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}

    res = requests.get(url, headers=headers)
    data = res.json()

    teams = []
    for t in data.get("teams", []):
        teams.append({
            "id": t["id"],
            "name": t["name"].lower()
        })

    return teams


TEAMS = load_teams()


def similarity(a, b):
    a_set = set(a.lower().split())
    b_set = set(b.lower().split())

    inter = len(a_set & b_set)
    union = len(a_set | b_set)

    return inter / union if union > 0 else 0


def find_team_id(team_name):

    team_name = team_name.lower()

    if team_name in TEAM_CACHE:
        return TEAM_CACHE[team_name]

    best_match = None
    best_score = 0

    for team in TEAMS:

        score = similarity(team_name, team["name"])

        if score > best_score:
            best_score = score
            best_match = team

    if best_match and best_score > 0.3:
        TEAM_CACHE[team_name] = best_match["id"]
        return best_match["id"]

    return None
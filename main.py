import json
from datetime import datetime

from api.odds import get_odds
from api.stats import get_team_stats, get_last_match_goals
from api.mapping import find_team_id
from logic.analyzer import analyze_match, get_line_movement
from bot.telegram import send_message
from model.dataset import save_example
from bot.telegram_commands import send_start_report


# -----------------------------
# LOAD / SAVE HISTORY
# -----------------------------

def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# TIME PARSER
# -----------------------------

def parse_match_time(match):
    try:
        dt = match.get("commence_time")
        if not dt:
            return None, None

        parsed = datetime.fromisoformat(dt.replace("Z", "+00:00"))

        return parsed.date().isoformat(), parsed.time().strftime("%H:%M")

    except:
        return None, None


# -----------------------------
# ODDS EXTRACT
# -----------------------------

def extract_odds(match):
    try:
        for bookmaker in match.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] == "totals":
                    for outcome in market.get("outcomes", []):
                        if outcome["name"] == "Over" and outcome["point"] == 2.5:
                            return outcome["price"]
    except:
        pass

    return None


# -----------------------------
# MAIN
# -----------------------------

def main():

    odds_data = get_odds()

    print("MATCHES FOUND:", len(odds_data) if odds_data else 0)

    if not isinstance(odds_data, list):
        print("❌ Invalid odds response")
        print(odds_data)
        return

    history = load_data()
    all_picks = []

    for match in odds_data:

        if not isinstance(match, dict):
            continue

        home_name = match.get("home_team")
        away_name = match.get("away_team")

        if not home_name or not away_name:
            continue

        # league-aware key (IMPORTANT FIX)
        league = match.get("sport_key", "unknown")
        match_name = f"{league}:{home_name} vs {away_name}"

        match_date, match_time = parse_match_time(match)

        # teams
        home_id = find_team_id(home_name)
        away_id = find_team_id(away_name)

        if not home_id or not away_id:
            continue

        # stats
        home_stats = get_team_stats(home_id)
        away_stats = get_team_stats(away_id)

        # analysis
        picks, history = analyze_match(
            match,
            history,
            home_stats,
            away_stats
        )

        all_picks.extend(picks)

        # movement (safe fallback)
        movement = get_line_movement(history, match_name)
        if movement is None:
            movement = 0.01

        # odds
        odds_value = extract_odds(match)

        # dataset
        result_goals = get_last_match_goals(home_id)

        if result_goals is not None and odds_value is not None:
            save_example(
                home_stats,
                away_stats,
                result_goals,
                odds_value,
                movement
            )

        # send picks (with safety filter)
        for pick in picks:

            if pick.get("score", 0) < 0.08:
                continue

            msg = f"""
⚽ SERIE A PICK

{pick['match']}
Over 2.5

Odds: {pick['odds']}

Prob: {round(pick['prob'] * 100, 1)}%
Value: {round(pick['value'] * 100, 1)}%

Movement: {round(pick['movement'], 3)}
Score: {round(pick['score'], 3)}
"""

            send_message(msg)

    # status report
    send_start_report(len(odds_data), all_picks)

    save_data(history)

    print("TOTAL PICKS:", len(all_picks))


if __name__ == "__main__":
    main()
import xgboost as xgb
import numpy as np
import os

MODEL_FILE = "data/model.json"

model = xgb.XGBClassifier()

if os.path.exists(MODEL_FILE):
    model.load_model(MODEL_FILE)
else:
    model = None


def predict(home_stats, away_stats, odds, movement):

    if model is None:
        return 0  # importante: no inventar señal

    home_attack = float(home_stats.get("attack", 0))
    home_defense = float(home_stats.get("defense", 0))
    away_attack = float(away_stats.get("attack", 0))
    away_defense = float(away_stats.get("defense", 0))

    attack_diff = home_attack - away_defense
    away_diff = away_attack - home_defense

    power = home_attack + away_attack
    weakness = home_defense + away_defense

    odds = float(odds) if odds else 0
    movement = float(movement) if movement else 0

    X = np.array([[
        home_attack,
        home_defense,
        away_attack,
        away_defense,
        attack_diff,
        away_diff,
        power,
        weakness,
        odds,
        movement
    ]], dtype=float)

    return float(model.predict_proba(X)[0][1])
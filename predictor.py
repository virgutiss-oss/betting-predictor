import pandas as pd

def predict_match():
    df = pd.read_csv("matches.csv")

    home_wins = df["home_goals"].sum()
    away_wins = df["away_goals"].sum()
    total = home_wins + away_wins

    home_prob = round(home_wins / total, 2)
    away_prob = round(away_wins / total, 2)

    return {
        "home_prob": home_prob,
        "away_prob": away_prob,
        "home_value": home_prob > 0.6,
        "away_value": away_prob > 0.6
    }

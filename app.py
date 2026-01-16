from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

from odds_provider import get_odds

app = Flask(__name__)
CSV_PATH = "matches.csv"

def load_matches():
    df = pd.read_csv(CSV_PATH)
    df["home_goals"] = pd.to_numeric(df["home_goals"])
    df["away_goals"] = pd.to_numeric(df["away_goals"])
    return df

def win_rate(df, team):
    games = df[(df["home"] == team) | (df["away"] == team)]
    if games.empty:
        return 0.5

    wins = (
        ((games["home"] == team) & (games["home_goals"] > games["away_goals"])) |
        ((games["away"] == team) & (games["away_goals"] > games["home_goals"]))
    ).sum()

    return wins / len(games)

def value_bet(prob, odds):
    value = (prob * odds - 1) * 100
    return round(value, 2), value > 0

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_matches()
    leagues = sorted(df["league"].unique())
    teams = []
    result = None

    league = request.form.get("league")

    if league:
        teams = sorted(set(
            df[df["league"] == league]["home"]
        ) | set(
            df[df["league"] == league]["away"]
        ))

    if request.method == "POST" and request.form.get("home"):
        home = request.form["home"]
        away = request.form["away"]

        league_df = df[df["league"] == league]

        home_prob = win_rate(league_df, home)
        away_prob = win_rate(league_df, away)

        odds = get_odds(league, home, away)

        home_value, home_ok = value_bet(home_prob, odds["home_odds"])
        away_value, away_ok = value_bet(away_prob, odds["away_odds"])

        result = {
            "home_prob": round(home_prob * 100, 1),
            "away_prob": round(away_prob * 100, 1),
            "home_odds": odds["home_odds"],
            "away_odds": odds["away_odds"],
            "home_value": home_value,
            "away_value": away_value,
            "home_ok": home_ok,
            "away_ok": away_ok,
            "source": odds["source"]
        }

    return render_template(
        "index.html",
        leagues=leagues,
        teams=teams,
        selected_league=league,
        result=result
    )

@app.route("/api/predict")
def api_predict():
    league = request.args.get("league")
    home = request.args.get("home")
    away = request.args.get("away")

    df = load_matches()
    df = df[df["league"] == league]

    home_prob = win_rate(df, home)
    away_prob = win_rate(df, away)

    odds = get_odds(league, home, away)

    hv, h_ok = value_bet(home_prob, odds["home_odds"])
    av, a_ok = value_bet(away_prob, odds["away_odds"])

    return jsonify({
        "league": league,
        "home": home,
        "away": away,
        "home_prob": round(home_prob * 100, 1),
        "away_prob": round(away_prob * 100, 1),
        "home_odds": odds["home_odds"],
        "away_odds": odds["away_odds"],
        "home_value_percent": hv,
        "away_value_percent": av,
        "home_value": h_ok,
        "away_value": a_ok,
        "odds_source": odds["source"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

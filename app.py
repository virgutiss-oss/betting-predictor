from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
CSV_PATH = "matches.csv"

def load_matches():
    df = pd.read_csv(CSV_PATH)
    df["home_goals"] = pd.to_numeric(df["home_goals"])
    df["away_goals"] = pd.to_numeric(df["away_goals"])
    return df

def predict_probabilities(df, home, away):
    games = df[(df["home"] == home) | (df["away"] == home)]
    opp_games = df[(df["home"] == away) | (df["away"] == away)]

    if games.empty or opp_games.empty:
        return 0.5, 0.5

    def win_rate(team, data):
        wins = (
            ((data["home"] == team) & (data["home_goals"] > data["away_goals"])) |
            ((data["away"] == team) & (data["away_goals"] > data["home_goals"]))
        ).sum()
        return wins / len(data)

    return win_rate(home, games), win_rate(away, opp_games)

def value_bet(prob, odds):
    value = (prob * odds - 1) * 100
    return round(value, 2), value > 0

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_matches()
    leagues = sorted(df["league"].unique())

    result = None
    teams = []
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
        home_odds = float(request.form["home_odds"])
        away_odds = float(request.form["away_odds"])

        league_df = df[df["league"] == league]
        hp, ap = predict_probabilities(league_df, home, away)

        hv, h_ok = value_bet(hp, home_odds)
        av, a_ok = value_bet(ap, away_odds)

        result = {
            "home_prob": round(hp * 100, 1),
            "away_prob": round(ap * 100, 1),
            "home_value": hv,
            "away_value": av,
            "home_ok": h_ok,
            "away_ok": a_ok
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
    home_odds = float(request.args.get("home_odds"))
    away_odds = float(request.args.get("away_odds"))

    df = load_matches()
    df = df[df["league"] == league]

    hp, ap = predict_probabilities(df, home, away)
    hv, h_ok = value_bet(hp, home_odds)
    av, a_ok = value_bet(ap, away_odds)

    return jsonify({
        "home_prob": round(hp * 100, 1),
        "away_prob": round(ap * 100, 1),
        "home_value_percent": hv,
        "away_value_percent": av,
        "home_value": h_ok,
        "away_value": a_ok
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

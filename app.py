from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
CSV_PATH = "matches.csv"

def load_matches():
    df = pd.read_csv(CSV_PATH)
    df["home_goals"] = pd.to_numeric(df["home_goals"], errors="coerce")
    df["away_goals"] = pd.to_numeric(df["away_goals"], errors="coerce")
    df = df.dropna()
    return df

def get_leagues(df):
    return sorted(df["league"].unique())

def get_teams_by_league(df, league):
    teams_home = df[df["league"] == league]["home"]
    teams_away = df[df["league"] == league]["away"]
    return sorted(set(teams_home) | set(teams_away))

def predict_match(df, home, away):
    home_games = df[(df["home"] == home) | (df["away"] == home)]
    away_games = df[(df["home"] == away) | (df["away"] == away)]

    if home_games.empty or away_games.empty:
        return 0, 0, False, False

    def win_rate(team, games):
        wins = (
            ((games["home"] == team) & (games["home_goals"] > games["away_goals"])) |
            ((games["away"] == team) & (games["away_goals"] > games["home_goals"]))
        ).sum()
        return wins / len(games)

    home_prob = win_rate(home, home_games)
    away_prob = win_rate(away, away_games)

    return (
        round(home_prob * 100, 1),
        round(away_prob * 100, 1),
        home_prob > 0.5,
        away_prob > 0.5
    )

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_matches()
    leagues = get_leagues(df)

    selected_league = request.form.get("league")
    teams = []
    result = None

    if selected_league:
        teams = get_teams_by_league(df, selected_league)

    if request.method == "POST" and request.form.get("home"):
        home = request.form.get("home")
        away = request.form.get("away")
        league_df = df[df["league"] == selected_league]
        result = predict_match(league_df, home, away)

    return render_template(
        "index.html",
        leagues=leagues,
        teams=teams,
        selected_league=selected_league,
        result=result
    )

@app.route("/api/predict")
def api_predict():
    league = request.args.get("league")
    home = request.args.get("home")
    away = request.args.get("away")

    if not league or not home or not away:
        return jsonify({"error": "Missing parameters"}), 400

    df = load_matches()
    df = df[df["league"] == league]

    hp, ap, hv, av = predict_match(df, home, away)

    return jsonify({
        "league": league,
        "home": home,
        "away": away,
        "home_prob": hp,
        "away_prob": ap,
        "home_value": hv,
        "away_value": av
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

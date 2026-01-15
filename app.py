from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

CSV_PATH = "matches.csv"


def load_matches():
    return pd.read_csv(CSV_PATH)


def predict_match(home, away):
    df = load_matches()

    home_games = df[(df["home"] == home) | (df["away"] == home)]
    away_games = df[(df["home"] == away) | (df["away"] == away)]

    if len(home_games) == 0 or len(away_games) == 0:
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
    teams = sorted(set(df["home"]).union(set(df["away"])))

    result = None
    if request.method == "POST":
        home = request.form["home"]
        away = request.form["away"]
        result = predict_match(home, away)

    return render_template("index.html", teams=teams, result=result)


@app.route("/stats")
def stats():
    df = load_matches()
    teams = sorted(set(df["home"]).union(set(df["away"])))
    data = []

    for team in teams:
        games = df[(df["home"] == team) | (df["away"] == team)]
        wins = (
            ((games["home"] == team) & (games["home_goals"] > games["away_goals"])) |
            ((games["away"] == team) & (games["away_goals"] > games["home_goals"]))
        ).sum()

        goals = games.apply(
            lambda r: r["home_goals"] if r["home"] == team else r["away_goals"],
            axis=1
        ).mean()

        data.append({
            "team": team,
            "win_rate": round(wins / len(games) * 100, 1),
            "avg_goals": round(goals, 2)
        })

    return render_template("stats.html", data=data)


@app.route("/api/predict")
def api_predict():
    home = request.args.get("home")
    away = request.args.get("away")

    if not home or not away:
        return jsonify({"error": "missing parameters"}), 400

    hp, ap, hv, av = predict_match(home, away)

    return jsonify({
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

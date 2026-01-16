from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

SPORT_FILES = {
    "football": "matches_football.csv",
    "basketball": "matches_basketball.csv",
    "tennis": "matches_tennis.csv",
    "hockey": "matches_hockey.csv"
}

def load_data(sport):
    return pd.read_csv(SPORT_FILES[sport])

def predict_match(sport, home, away):
    df = load_data(sport)

    home_games = df[df["home"] == home]
    away_games = df[df["away"] == away]

    if len(home_games) == 0 or len(away_games) == 0:
        return 0.5, 0.5

    if sport == "football":
        home_score = home_games["home_score"].mean()
        away_score = away_games["away_score"].mean()

    elif sport == "basketball":
        home_score = home_games["home_points"].mean()
        away_score = away_games["away_points"].mean()

    elif sport == "hockey":
        home_score = home_games["home_goals"].mean()
        away_score = away_games["away_goals"].mean()

    elif sport == "tennis":
        home_score = home_games["home_win"].mean()
        away_score = away_games["away_win"].mean()

    total = home_score + away_score
    home_prob = round(home_score / total, 2)
    away_prob = round(away_score / total, 2)

    return home_prob, away_prob

@app.route("/", methods=["GET", "POST"])
def index():
    home_prob = away_prob = None

    if request.method == "POST":
        sport = request.form["sport"]
        home = request.form["home"]
        away = request.form["away"]
        home_prob, away_prob = predict_match(sport, home, away)

    return render_template(
        "index.html",
        home_prob=home_prob,
        away_prob=away_prob
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

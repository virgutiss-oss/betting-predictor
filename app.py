from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "matches.csv")
UPLOAD_FOLDER = BASE_DIR
ALLOWED_EXTENSIONS = {"csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_teams(df):
    return sorted(set(df["home"]).union(set(df["away"])))

def calculate_probabilities(df, home, away):
    filtered = df[
        ((df["home"] == home) & (df["away"] == away)) |
        ((df["home"] == away) & (df["away"] == home))
    ]

    if len(filtered) == 0:
        return 0.0, 0.0

    home_wins = (
        ((filtered["home"] == home) & (filtered["home_goals"] > filtered["away_goals"])).sum()
        + ((filtered["away"] == home) & (filtered["away_goals"] > filtered["home_goals"])).sum()
    )

    away_wins = (
        ((filtered["home"] == away) & (filtered["home_goals"] > filtered["away_goals"])).sum()
        + ((filtered["away"] == away) & (filtered["away_goals"] > filtered["home_goals"])).sum()
    )

    total = len(filtered)
    return round(home_wins / total, 2), round(away_wins / total, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    df = pd.read_csv(DATA_PATH)
    teams = get_teams(df)

    home_prob = away_prob = None
    home_value = away_value = None
    selected_home = selected_away = None

    if request.method == "POST" and "home" in request.form:
        selected_home = request.form["home"]
        selected_away = request.form["away"]

        home_prob, away_prob = calculate_probabilities(df, selected_home, selected_away)
        home_value = home_prob > 0.5
        away_value = away_prob > 0.5

    return render_template(
        "index.html",
        teams=teams,
        home_prob=home_prob,
        away_prob=away_prob,
        home_value=home_value,
        away_value=away_value,
        selected_home=selected_home,
        selected_away=selected_away
    )

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        file.save(DATA_PATH)

    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

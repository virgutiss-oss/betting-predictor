from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)

CSV_PATH = "matches.csv"


def load_matches():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError("matches.csv not found")

    df = pd.read_csv(CSV_PATH)

    required = {"home", "away", "home_goals", "away_goals"}
    if not required.issubset(df.columns):
        raise ValueError("CSV columns invalid")

    return df


def predict_match(home, away):
    df = load_matches()

    home_games = df[df["home"] == home]
    away_games = df[df["away"] == away]

    home_wins = (home_games["home_goals"] > home_games["away_goals"]).sum()
    away_wins = (away_games["away_goals"] > away_games["home_goals"]).sum()

    total = max(len(home_games) + len(away_games), 1)

    home_prob = round(home_wins / total, 2)
    away_prob = round(away_wins / total, 2)

    return {
        "home_win_probability": home_prob,
        "away_win_probability": away_prob,
        "home_value": home_prob > 0.5,
        "away_value": away_prob > 0.5
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/predict")
def api_predict():
    home = request.args.get("home")
    away = request.args.get("away")

    if not home or not away:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        result = predict_match(home, away)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()

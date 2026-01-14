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

    # ===== OVERALL FORM =====
    home_games = df[(df["home"] == home) | (df["away"] == home)]
    away_games = df[(df["home"] == away) | (df["away"] == away)]

    home_wins = (
        ((home_games["home"] == home) & (home_games["home_goals"] > home_games["away_goals"])) |
        ((home_games["away"] == home) & (home_games["away_goals"] > home_games["home_goals"]))
    ).sum()

    away_wins = (
        ((away_games["home"] == away) & (away_games["home_goals"] > away_games["away_goals"])) |
        ((away_games["away"] == away) & (away_games["away_goals"] > away_games["home_goals"]))
    ).sum()

    home_form = home_wins / max(len(home_games), 1)
    away_form = away_wins / max(len(away_games), 1)

    # ===== HEAD TO HEAD =====
    h2h = df[
        ((df["home"] == home) & (df["away"] == away)) |
        ((df["home"] == away) & (df["away"] == home))
    ]

    if len(h2h) > 0:
        home_h2h_wins = (
            ((h2h["home"] == home) & (h2h["home_goals"] > h2h["away_goals"])) |
            ((h2h["away"] == home) & (h2h["away_goals"] > h2h["home_goals"]))
        ).sum()

        away_h2h_wins = (
            ((h2h["home"] == away) & (h2h["home_goals"] > h2h["away_goals"])) |
            ((h2h["away"] == away) & (h2h["away_goals"] > h2h["home_goals"]))
        ).sum()

        home_h2h = home_h2h_wins / len(h2h)
        away_h2h = away_h2h_wins / len(h2h)
    else:
        home_h2h = None
        away_h2h = None

    # ===== WEIGHTED COMBINATION =====
    if home_h2h is not None:
        home_prob = round(0.7 * home_form + 0.3 * home_h2h, 2)
        away_prob = round(0.7 * away_form + 0.3 * away_h2h, 2)
    else:
        home_prob = round(home_form, 2)
        away_prob = round(away_form, 2)

    return {
        "home_win_probability": home_prob,
        "away_win_probability": away_prob,
        "home_value": home_prob > 0.5,
        "away_value": away_prob > 0.5
    }


@app.route("/")
def index():
    df = load_matches()
    teams = sorted(set(df["home"]).union(set(df["away"])))
    return render_template("index.html", teams=teams)


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

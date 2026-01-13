from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "matches.csv")

def calculate_probabilities():
    df = pd.read_csv(DATA_PATH)

    home_wins = (df["home_goals"] > df["away_goals"]).sum()
    away_wins = (df["away_goals"] > df["home_goals"]).sum()
    total = len(df)

    home_prob = round(home_wins / total, 2)
    away_prob = round(away_wins / total, 2)

    return home_prob, away_prob

@app.route("/")
def index():
    home_prob, away_prob = calculate_probabilities()

    return render_template(
        "index.html",
        home_prob=home_prob,
        away_prob=away_prob,
        home_value=home_prob > 0.5,
        away_value=away_prob > 0.5
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

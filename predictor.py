from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    df = pd.read_csv("matches.csv")

    predictions = []

    for _, row in df.iterrows():
        home_prob = round(1 / row["home_odds"], 2)
        away_prob = round(1 / row["away_odds"], 2)

        total = home_prob + away_prob
        home_prob = round(home_prob / total, 2)
        away_prob = round(away_prob / total, 2)

        home_value = home_prob * row["home_odds"] > 1
        away_value = away_prob * row["away_odds"] > 1

        predictions.append({
            "home_team": row["home_team"],
            "away_team": row["away_team"],
            "home_prob": home_prob,
            "away_prob": away_prob,
            "home_value": home_value,
            "away_value": away_value
        })

    return render_template("index.html", predictions=predictions)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

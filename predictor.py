from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    df = pd.read_csv("matches.csv")

    # paprasta statistika
    total_home_goals = df["home_goals"].sum()
    total_away_goals = df["away_goals"].sum()
    games = len(df)

    home_avg = total_home_goals / games
    away_avg = total_away_goals / games

    total = home_avg + away_avg
    home_prob = round(home_avg / total, 2)
    away_prob = round(away_avg / total, 2)

    home_value = home_prob > 0.5
    away_value = away_prob > 0.5

    return render_template(
        "index.html",
        home_prob=home_prob,
        away_prob=away_prob,
        home_value=home_value,
        away_value=away_value
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

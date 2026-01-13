from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    try:
        df = pd.read_csv("matches.csv")

        required_cols = {"home", "away", "home_goals", "away_goals"}
        if not required_cols.issubset(df.columns):
            return f"CSV columns error. Found: {list(df.columns)}"

        teams = pd.unique(df[['home', 'away']].values.ravel())
        stats = {}

        for team in teams:
            home_games = df[df['home'] == team]
            away_games = df[df['away'] == team]

            goals_for = home_games['home_goals'].sum() + away_games['away_goals'].sum()
            goals_against = home_games['away_goals'].sum() + away_games['home_goals'].sum()
            games = len(home_games) + len(away_games)

            if games == 0:
                continue

            stats[team] = {
                "avg_for": goals_for / games,
                "avg_against": goals_against / games
            }

        predictions = []

        teams = list(stats.keys())
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                home = teams[i]
                away = teams[j]

                home_strength = stats[home]["avg_for"]
                away_strength = stats[away]["avg_for"]

                total = home_strength + away_strength
                home_prob = round(home_strength / total, 2)
                away_prob = round(away_strength / total, 2)

                predictions.append({
                    "home_team": home,
                    "away_team": away,
                    "home_prob": home_prob,
                    "away_prob": away_prob,
                    "home_value": home_prob > 0.5,
                    "away_value": away_prob > 0.5
                })

        return render_template("index.html", predictions=predictions)

    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

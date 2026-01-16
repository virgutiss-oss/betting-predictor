from flask import Flask, render_template, request
import pandas as pd

from ml_model import train_model, predict_home_win
from odds_provider import get_all_odds
from arbitrage import find_arbitrage
from roi_tracker import get_roi

app = Flask(__name__)

model = train_model()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        home_avg = float(request.form["home_avg"])
        away_avg = float(request.form["away_avg"])

        home_prob = predict_home_win(model, home_avg, away_avg)
        away_prob = 1 - home_prob

        odds = get_all_odds()
        arb = find_arbitrage(odds)

        result = {
            "home_prob": round(home_prob * 100, 2),
            "away_prob": round(away_prob * 100, 2),
            "arb": arb
        }

    return render_template("index.html", result=result)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", roi=get_roi())

if __name__ == "__main__":
    app.run()

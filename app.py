from flask import Flask, render_template, request
from data import SPORTS_DATA
from ml_model import predict_prob
from odds_provider import get_odds
from arbitrage import check_arbitrage

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    sport = request.form.get("sport")
    league = request.form.get("league")
    home = request.form.get("home")
    away = request.form.get("away")

    if request.method == "POST" and home and away:
        p_home, p_away = predict_prob(1, 1)
        odds = get_odds(sport)

        result = {
            "p_home": round(p_home * 100, 1),
            "p_away": round(p_away * 100, 1),
            "value_home": (p_home * odds["home"]) > 1,
            "value_away": (p_away * odds["away"]) > 1,
            "arbitrage": check_arbitrage(odds["home"], odds["away"])
        }

    return render_template(
        "index.html",
        sports=SPORTS_DATA,
        sport=sport,
        league=league,
        result=result
    )

if __name__ == "__main__":
    app.run()

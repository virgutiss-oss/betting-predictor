from flask import Flask, render_template, request
from data import SPORTS_DATA
from ml_model import predict_prob_by_sport
from odds_provider import get_odds
from alerts import send_alert
from live_matches import get_live_matches
from roi_tracker import get_roi

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    sport = request.form.get("sport")
    league = request.form.get("league")
    home = request.form.get("home")
    away = request.form.get("away")

    if request.method == "POST" and sport and home and away:
        p_home, p_away = predict_prob_by_sport(sport)
        odds = get_odds(sport, home, away)

        value_home = (p_home * odds["home"] - 1) * 100
        value_away = (p_away * odds["away"] - 1) * 100

        if value_home > 5:
            send_alert(f"VALUE BET: {home} {value_home}%")

        result = {
            "p_home": round(p_home * 100, 1),
            "p_away": round(p_away * 100, 1),
            "odds": odds,
            "value_home": round(value_home, 2),
            "value_away": round(value_away, 2)
        }

    return render_template(
        "index.html",
        sports=SPORTS_DATA,
        sport=sport,
        league=league,
        result=result
    )

@app.route("/dashboard")
def dashboard():
    stake, profit, roi = get_roi()
    return render_template("dashboard.html", stake=stake, profit=profit, roi=roi)

@app.route("/live")
def live():
    return render_template("live.html", matches=get_live_matches())

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

from odds_provider import get_odds

app = Flask(__name__)
CSV_PATH = "matches.csv"

# ---------- DATA ----------
def load_matches():
    df = pd.read_csv(CSV_PATH)
    df["home_goals"] = pd.to_numeric(df["home_goals"])
    df["away_goals"] = pd.to_numeric(df["away_goals"])
    return df

def win_rate(df, team):
    games = df[(df["home"] == team) | (df["away"] == team)]
    if games.empty:
        return 0.33

    wins = (
        ((games["home"] == team) & (games["home_goals"] > games["away_goals"])) |
        ((games["away"] == team) & (games["away_goals"] > games["home_goals"]))
    ).sum()

    return wins / len(games)

# ---------- BET MATH ----------
def value_bet(prob, odds):
    value = (prob * odds - 1) * 100
    return round(value, 2), value > 0

def kelly(prob, odds):
    if odds <= 1:
        return 0
    k = (prob * odds - 1) / (odds - 1)
    return round(max(k, 0) * 100, 2)

def arbitrage(home_odds, away_odds):
    arb = (1 / home_odds) + (1 / away_odds)
    return round(arb, 3), arb < 1

# ---------- ROUTES ----------
@app.route("/", methods=["GET", "POST"])
def index():
    df = load_matches()
    leagues = sorted(df["league"].unique())
    teams = []
    result = None

    league = request.form.get("league")

    if league:
        teams = sorted(set(
            df[df["league"] == league]["home"]
        ) | set(
            df[df["league"] == league]["away"]
        ))

    if request.method == "POST" and request.form.get("home"):
        home = request.form["home"]
        away = request.form["away"]

        league_df = df[df["league"] == league]

        hp = win_rate(league_df, home)
        ap = win_rate(league_df, away)
        dp = max(0.05, 1 - hp - ap)

        odds = get_odds(league, home, away)

        hv, h_ok = value_bet(hp, odds["home_odds"])
        av, a_ok = value_bet(ap, odds["away_odds"])
        dv, d_ok = value_bet(dp, odds["draw_odds"])

        hk = kelly(hp, odds["home_odds"])
        ak = kelly(ap, odds["away_odds"])
        dk = kelly(dp, odds["draw_odds"])

        arb_val, arb_ok = arbitrage(odds["home_odds"], odds["away_odds"])

        result = {
            "home_prob": round(hp * 100, 1),
            "draw_prob": round(dp * 100, 1),
            "away_prob": round(ap * 100, 1),

            "home_odds": odds["home_odds"],
            "draw_odds": odds["draw_odds"],
            "away_odds": odds["away_odds"],

            "home_value": hv,
            "draw_value": dv,
            "away_value": av,

            "home_kelly": hk,
            "draw_kelly": dk,
            "away_kelly": ak,

            "home_ok": h_ok,
            "draw_ok": d_ok,
            "away_ok": a_ok,

            "arb_value": arb_val,
            "arb_ok": arb_ok,

            "source": odds["source"],
            "timestamp": odds["timestamp"]
        }

    return render_template(
        "index.html",
        leagues=leagues,
        teams=teams,
        selected_league=league,
        result=result
    )

@app.route("/api/predict")
def api_predict():
    league = request.args.get("league")
    home = request.args.get("home")
    away = request.args.get("away")

    df = load_matches()
    df = df[df["league"] == league]

    hp = win_rate(df, home)
    ap = win_rate(df, away)
    dp = max(0.05, 1 - hp - ap)

    odds = get_odds(league, home, away)

    hv, _ = value_bet(hp, odds["home_odds"])
    av, _ = value_bet(ap, odds["away_odds"])
    dv, _ = value_bet(dp, odds["draw_odds"])

    return jsonify({
        "home_prob": round(hp * 100, 1),
        "draw_prob": round(dp * 100, 1),
        "away_prob": round(ap * 100, 1),
        "home_odds": odds["home_odds"],
        "draw_odds": odds["draw_odds"],
        "away_odds": odds["away_odds"],
        "home_value_percent": hv,
        "draw_value_percent": dv,
        "away_value_percent": av,
        "source": odds["source"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

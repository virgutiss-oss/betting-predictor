import streamlit as st

st.set_page_config(page_title="Betting Predictor", layout="centered")

st.title("⚽🏀 Betting Predictor")
st.caption("Veikia iPhone • Powered by virgutiss-oss")

# =========================
# DUOMENYS (Lygos + komandos)
# =========================

football_leagues = {
    "Premier League (ENG)": [
        "Arsenal", "Chelsea", "Liverpool", "Manchester City",
        "Manchester United", "Tottenham", "Newcastle", "Aston Villa"
    ],
    "La Liga (ESP)": [
        "Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla",
        "Villarreal", "Real Sociedad"
    ],
    "Serie A (ITA)": [
        "Juventus", "Inter", "AC Milan", "Napoli", "Roma", "Lazio"
    ],
    "Bundesliga (GER)": [
        "Bayern Munich", "Dortmund", "Leipzig", "Leverkusen"
    ],
    "Ligue 1 (FRA)": [
        "PSG", "Marseille", "Lyon", "Monaco"
    ]
}

basketball_leagues = {
    "NBA": [
        "Lakers", "Warriors", "Celtics", "Bulls",
        "Heat", "Nuggets", "Bucks", "Suns"
    ],
    "EuroLeague": [
        "Real Madrid", "Barcelona", "Olympiacos",
        "Panathinaikos", "Fenerbahce", "Anadolu Efes", "Zalgiris"
    ],
    "LKL (LTU)": [
        "Zalgiris", "Rytas", "Lietkabelis", "Neptunas"
    ]
}

# =========================
# PASIRINKIMAI
# =========================

sport = st.selectbox("🏟️ Sportas", ["Football", "Basketball"])

if sport == "Football":
    league = st.selectbox("⚽ Lyga", list(football_leagues.keys()))
    teams = football_leagues[league]
else:
    league = st.selectbox("🏀 Lyga", list(basketball_leagues.keys()))
    teams = basketball_leagues[league]

home = st.selectbox("🏠 Home team", teams)
away = st.selectbox("✈️ Away team", [t for t in teams if t != home])

st.divider()

# =========================
# ODDS
# =========================

st.subheader("📊 Bookmaker Odds")
odds_home = st.number_input("Home odds", min_value=1.01, step=0.01)
odds_away = st.number_input("Away odds", min_value=1.01, step=0.01)

# =========================
# PROGNOZĖ
# =========================

def predict_probabilities():
    # paprasta, bet logiška bazė
    base_home = 0.55
    base_away = 0.45

    if sport == "Basketball":
        base_home = 0.58
        base_away = 0.42

    return base_home, base_away

if st.button("🔮 Predict"):
    home_prob, away_prob = predict_probabilities()

    value_home = home_prob * odds_home - 1
    value_away = away_prob * odds_away - 1

    st.success(f"🏠 Home win probability: {home_prob*100:.1f}%")
    st.success(f"✈️ Away win probability: {away_prob*100:.1f}%")

    st.divider()
    st.subheader("💰 Value Bet Analysis")

    if value_home > 0:
        st.info(f"✅ HOME VALUE BET ({value_home*100:.1f}%)")
    else:
        st.warning("❌ Home bet – NO value")

    if value_away > 0:
        st.info(f"✅ AWAY VALUE BET ({value_away*100:.1f}%)")
    else:
        st.warning("❌ Away bet – NO value")

def get_odds(sport, home, away):
    if sport == "Tennis":
        return {"home": 1.95, "away": 1.95}
    if sport == "Basketball":
        return {"home": 2.05, "away": 1.80}
    return {"home": 2.10, "away": 1.85}

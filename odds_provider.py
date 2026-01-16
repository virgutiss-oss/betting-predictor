def get_odds(sport):
    if sport == "Tennis":
        return {"home": 1.90, "away": 1.90}
    if sport == "Basketball":
        return {"home": 2.00, "away": 1.80}
    return {"home": 2.10, "away": 1.85}

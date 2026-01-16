def predict_prob_by_sport(sport):
    if sport == "Football":
        return 0.52, 0.48
    if sport == "Basketball":
        return 0.55, 0.45
    if sport == "Tennis":
        return 0.60, 0.40
    return 0.5, 0.5

import random

def get_all_odds():
    return [
        {"book": "Pinnacle", "home": round(random.uniform(1.8, 2.4), 2), "away": round(random.uniform(1.8, 2.4), 2)},
        {"book": "Betfair", "home": round(random.uniform(1.8, 2.4), 2), "away": round(random.uniform(1.8, 2.4), 2)},
        {"book": "1xBet", "home": round(random.uniform(1.8, 2.4), 2), "away": round(random.uniform(1.8, 2.4), 2)}
    ]

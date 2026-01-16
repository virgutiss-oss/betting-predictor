import random

def get_odds(league, home, away):
    """
    DEMO odds.
    Vėliau čia bus Pinnacle / Betfair API.
    """

    home_odds = round(random.uniform(1.8, 2.6), 2)
    away_odds = round(random.uniform(2.2, 4.2), 2)

    return {
        "home_odds": home_odds,
        "away_odds": away_odds,
        "source": "DEMO"
    }

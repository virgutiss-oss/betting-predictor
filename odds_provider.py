import random
import time

def get_odds(league, home, away):
    return {
        "home_odds": round(random.uniform(1.8, 2.6), 2),
        "draw_odds": round(random.uniform(2.8, 3.6), 2),
        "away_odds": round(random.uniform(2.2, 4.2), 2),
        "source": "DEMO",
        "timestamp": int(time.time())
    }

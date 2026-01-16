def check_arbitrage(home_odds, away_odds):
    return (1/home_odds + 1/away_odds) < 1

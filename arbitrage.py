def find_arbitrage(books):
    best_home = max(books, key=lambda x: x["home"])
    best_away = max(books, key=lambda x: x["away"])

    value = (1 / best_home["home"]) + (1 / best_away["away"])

    return {
        "exists": value < 1,
        "value": round(value, 3),
        "home_book": best_home["book"],
        "away_book": best_away["book"]
    }

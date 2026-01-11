import pandas as pd

class BettingPredictor:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.teams = set(self.data['home']).union(set(self.data['away']))
        self.stats = self.calculate_stats()

    def calculate_stats(self):
        stats = {team: {"games": 0, "points": 0} for team in self.teams}

        for _, row in self.data.iterrows():
            home = row["home"]
            away = row["away"]
            hg = row["home_goals"]
            ag = row["away_goals"]

            stats[home]["games"] += 1
            stats[away]["games"] += 1

            if hg > ag:
                stats[home]["points"] += 3
            elif hg < ag:
                stats[away]["points"] += 3
            else:
                stats[home]["points"] += 1
                stats[away]["points"] += 1

        return stats

    def predict(self, home, away, odds):
        home_strength = self.stats[home]["points"] / self.stats[home]["games"]
        away_strength = self.stats[away]["points"] / self.stats[away]["games"]

        total = home_strength + away_strength
        home_prob = home_strength / total
        away_prob = away_strength / total

        return {
            "home_prob": round(home_prob, 2),
            "away_prob": round(away_prob, 2),
            "home_value": home_prob * odds["home"] > 1,
            "away_value": away_prob * odds["away"] > 1
        }


if __name__ == "__main__":
    predictor = BettingPredictor("matches.csv")

    result = predictor.predict(
        home="TeamA",
        away="TeamB",
        odds={"home": 2.10, "away": 3.40}
    )

    print(result)

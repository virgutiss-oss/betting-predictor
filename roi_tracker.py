import csv

FILE = "bets.csv"

def get_roi():
    try:
        with open(FILE) as f:
            rows = list(csv.reader(f))
            if not rows:
                return 0, 0, 0

            stake = len(rows)
            profit = sum(float(r[0]) for r in rows)
            roi = (profit / stake) * 100 if stake else 0
            return stake, profit, round(roi, 2)
    except:
        return 0, 0, 0

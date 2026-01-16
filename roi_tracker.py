import csv
from datetime import datetime

FILE = "bets.csv"

def log_bet(stake, odds, win):
    profit = stake * odds - stake if win else -stake

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), stake, odds, win, profit])

def get_roi():
    try:
        with open(FILE) as f:
            rows = list(csv.reader(f))
            if not rows:
                return 0, 0, 0

            stake = sum(float(r[1]) for r in rows)
            profit = sum(float(r[4]) for r in rows)
            roi = (profit / stake) * 100 if stake > 0 else 0
            return stake, profit, round(roi, 2)
    except:
        return 0, 0, 0

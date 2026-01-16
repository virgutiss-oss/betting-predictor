import pandas as pd
import os

FILE = "bets.csv"

def get_roi():
    if not os.path.exists(FILE):
        return 0

    df = pd.read_csv(FILE)
    total_stake = df["stake"].sum()
    total_profit = df["profit"].sum()

    if total_stake == 0:
        return 0

    return round((total_profit / total_stake) * 100, 2)

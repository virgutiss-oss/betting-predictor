import pandas as pd
from sklearn.linear_model import LogisticRegression

def train_model():
    df = pd.read_csv("matches.csv")

    df["home_win"] = (df["home_goals"] > df["away_goals"]).astype(int)

    X = df[["home_goals", "away_goals"]]
    y = df["home_win"]

    model = LogisticRegression()
    model.fit(X, y)

    return model

def predict_home_win(model, home_avg, away_avg):
    return model.predict_proba([[home_avg, away_avg]])[0][1]

import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor


BASE_DIR = Path(__file__).resolve().parent.parent.parent

RAINFALL_FILE = (
    BASE_DIR
    / "03_data_and_resources"
    / "curated"
    / "rainfall_demo.csv"
)


df = pd.read_csv(RAINFALL_FILE)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

df["previous_rainfall"] = df["rainfall_mm"].shift(1)
df = df.dropna()

X = df[["previous_rainfall"]]
y = df["rainfall_mm"]


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def predict_next_rainfall():

    latest_rainfall = df["rainfall_mm"].iloc[-1]

    prediction = model.predict(
        [[latest_rainfall]]
    )[0]

    return round(max(0, prediction), 2)


if __name__ == "__main__":

    prediction = predict_next_rainfall()

    print(
        "Predicted next rainfall:",
        prediction,
        "mm"
    )
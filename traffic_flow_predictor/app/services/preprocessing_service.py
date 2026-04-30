import pandas as pd

from app.schemas.request import TrafficRequest
from app.utils.feature_engineering import derive_time_features


class PreprocessingService:
    categorical_cols = ["weather"]
    numeric_cols = ["temperature", "rain", "snow", "holiday", "hour", "weekday", "month"]

    async def transform_request(self, payload: TrafficRequest, feature_columns: list[str], stats: dict) -> pd.DataFrame:
        tf = derive_time_features(payload.date, payload.time)
        row = {
            "temperature": payload.temperature,
            "rain": payload.rain,
            "snow": payload.snow,
            "holiday": int(payload.holiday),
            "hour": tf["hour"],
            "weekday": tf["weekday"],
            "month": tf["month"],
            "weather": payload.weather,
        }
        for col in self.numeric_cols:
            std = stats[col]["std"] or 1.0
            row[col] = (row[col] - stats[col]["mean"]) / std

        df = pd.DataFrame([row])
        df = pd.get_dummies(df, columns=self.categorical_cols)
        return df.reindex(columns=feature_columns, fill_value=0)

    async def prepare_training(self, df: pd.DataFrame):
        df = df.copy()
        df["date_time"] = pd.to_datetime(df["date_time"])
        df["hour"] = df["date_time"].dt.hour
        df["weekday"] = df["date_time"].dt.weekday
        df["month"] = df["date_time"].dt.month
        df["holiday"] = df["holiday"].apply(lambda v: 0 if str(v).lower() in ["none", "no", "0"] else 1)

        x = df[["temperature", "rain", "snow", "holiday", "hour", "weekday", "month", "weather"]]
        y = df["traffic_volume"]

        stats = {
            col: {"mean": float(x[col].mean()), "std": float(x[col].std() or 1.0)}
            for col in self.numeric_cols
        }
        for col in self.numeric_cols:
            x[col] = (x[col] - stats[col]["mean"]) / stats[col]["std"]

        x = pd.get_dummies(x, columns=self.categorical_cols)
        return x, y, list(x.columns), stats

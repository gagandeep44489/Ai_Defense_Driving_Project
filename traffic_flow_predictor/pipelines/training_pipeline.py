import asyncio
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.core.config import settings
from app.infrastructure.models.random_forest_model import RandomForestModel
from app.infrastructure.repository.model_repository import ModelRepository
from app.services.preprocessing_service import PreprocessingService


def build_dataset(path: Path, n: int = 4000):
    rng = np.random.default_rng(42)
    dts = pd.date_range("2025-01-01", periods=n, freq="h")
    weather = rng.choice(["Clear", "Clouds", "Rain", "Snow", "Mist"], size=n, p=[0.4, 0.25, 0.2, 0.1, 0.05])
    holiday = rng.choice(["None", "Holiday"], size=n, p=[0.9, 0.1])
    temp = rng.normal(15, 9, n)
    rain = rng.gamma(1.2, 1.0, n)
    snow = rng.gamma(0.8, 0.7, n)
    hour = dts.hour
    peak = ((hour >= 7) & (hour <= 9)) * 1700 + ((hour >= 16) & (hour <= 19)) * 2200
    vol = (1400 + peak - (weather == "Snow") * 450 - (weather == "Rain") * 220 - (holiday == "Holiday") * 600 + rng.normal(0, 250, n)).clip(150, 7000)
    pd.DataFrame({"date_time": dts, "temperature": temp, "rain": rain, "snow": snow, "weather": weather, "holiday": holiday, "traffic_volume": vol}).to_csv(path, index=False)


async def main():
    if not settings.DATA_PATH.exists():
        build_dataset(settings.DATA_PATH)

    df = pd.read_csv(settings.DATA_PATH)
    prep = PreprocessingService()
    X, y, feature_columns, stats = await prep.prepare_training(df)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestModel()
    await model.train(x_train, y_train)
    preds = await model.predict(x_test)

    print(f"MAE: {mean_absolute_error(y_test, preds):.2f}, R2: {r2_score(y_test, preds):.3f}")
    await ModelRepository(settings.MODEL_PATH).save({"model": model.native_model, "feature_columns": feature_columns, "stats": stats})
    print(f"Saved model at {settings.MODEL_PATH}")


if __name__ == "__main__":
    asyncio.run(main())

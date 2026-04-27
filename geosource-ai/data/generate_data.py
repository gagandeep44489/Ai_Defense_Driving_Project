"""Generate synthetic supplier data for GeoSource AI."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


COUNTRIES = [
    "USA",
    "Mexico",
    "Germany",
    "Japan",
    "China",
    "India",
    "South Korea",
    "Canada",
    "Brazil",
    "Thailand",
]


def derive_risk_label(cost: float, delivery_time: float, reliability_score: float, defect_rate: float, delay_history: int) -> str:
    """Rule-based label generation with mild noise for realism."""
    risk_score = (
        0.25 * (cost / 200.0)
        + 0.25 * (delivery_time / 30.0)
        + 0.25 * (defect_rate / 10.0)
        + 0.15 * (delay_history / 20.0)
        + 0.10 * ((100.0 - reliability_score) / 100.0)
    )

    if risk_score >= 0.55:
        return "High"
    if risk_score >= 0.35:
        return "Medium"
    return "Low"


def generate_dataset(n_rows: int = 600, seed: int = 42) -> pd.DataFrame:
    """Create synthetic supplier records with realistic ranges."""
    rng = np.random.default_rng(seed)

    supplier_ids = [f"SUP-{i:04d}" for i in range(1, n_rows + 1)]
    country = rng.choice(COUNTRIES, size=n_rows)

    # Cost in normalized units (e.g., $/component)
    cost = np.clip(rng.normal(loc=95, scale=30, size=n_rows), 30, 220)
    delivery_time = np.clip(rng.normal(loc=14, scale=5, size=n_rows), 3, 35)
    reliability_score = np.clip(rng.normal(loc=84, scale=10, size=n_rows), 45, 99)
    defect_rate = np.clip(rng.normal(loc=3.0, scale=1.5, size=n_rows), 0.2, 12)
    delay_history = rng.poisson(lam=5, size=n_rows)

    rows = []
    for i in range(n_rows):
        label = derive_risk_label(
            cost=float(cost[i]),
            delivery_time=float(delivery_time[i]),
            reliability_score=float(reliability_score[i]),
            defect_rate=float(defect_rate[i]),
            delay_history=int(delay_history[i]),
        )

        # Inject small stochastic noise (8%)
        if rng.random() < 0.08:
            label = rng.choice(["Low", "Medium", "High"])

        rows.append(
            {
                "supplier_id": supplier_ids[i],
                "country": country[i],
                "cost": round(float(cost[i]), 2),
                "delivery_time": round(float(delivery_time[i]), 2),
                "reliability_score": round(float(reliability_score[i]), 2),
                "defect_rate": round(float(defect_rate[i]), 2),
                "delay_history": int(delay_history[i]),
                "risk_label": label,
            }
        )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    output_path = Path(__file__).resolve().parent / "suppliers.csv"
    df = generate_dataset(n_rows=600)
    df.to_csv(output_path, index=False)
    print(f"Generated dataset: {output_path} ({len(df)} rows)")

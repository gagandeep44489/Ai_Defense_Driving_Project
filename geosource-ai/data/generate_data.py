"""Synthetic supplier data generator."""
import argparse
import numpy as np
import pandas as pd

COUNTRIES = ["US", "DE", "JP", "MX", "CN", "KR", "IN"]


def assign_risk(row: pd.Series) -> str:
    score = (row["defect_rate"] * 2.5) + (row["delay_history"] * 0.08) + ((100 - row["reliability_score"]) * 0.015)
    if score > 2.2:
        return "High"
    if score > 1.2:
        return "Medium"
    return "Low"


def generate(rows: int = 600, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "supplier_id": [f"SUP-{i:04d}" for i in range(rows)],
        "country": rng.choice(COUNTRIES, size=rows, p=[0.17, 0.14, 0.14, 0.16, 0.16, 0.11, 0.12]),
        "cost": rng.normal(540, 130, size=rows).clip(150, 1100),
        "delivery_time": rng.normal(14, 4, size=rows).clip(3, 40),
        "reliability_score": rng.normal(84, 9, size=rows).clip(40, 99),
        "defect_rate": rng.beta(2, 16, size=rows).clip(0.001, 0.25),
        "delay_history": rng.poisson(5, size=rows),
    })
    df["risk_level"] = df.apply(assign_risk, axis=1)
    return df


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--rows", type=int, default=700)
    p.add_argument("--output", type=str, default="data/processed/suppliers.csv")
    args = p.parse_args()
    data = generate(args.rows)
    data.to_csv(args.output, index=False)
    print(f"saved {len(data)} rows to {args.output}")

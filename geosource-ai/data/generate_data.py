"""Synthetic supplier data generator for GeoSource AI."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

COUNTRIES = ["US", "DE", "JP", "MX", "CN", "KR", "IN"]
RISK_LABELS = ["Low", "Medium", "High"]


def compute_risk_score(df: pd.DataFrame) -> pd.Series:
    """Compute normalized operational risk score in [0, 1]."""
    defect = (df["defect_rate"] / 0.20).clip(0, 1)
    delay = (df["delay_history"] / 12).clip(0, 1)
    reliability = ((100 - df["reliability_score"]) / 60).clip(0, 1)
    delivery = ((df["delivery_time"] - 3) / 22).clip(0, 1)
    return 0.35 * defect + 0.25 * delay + 0.25 * reliability + 0.15 * delivery


def assign_balanced_risk(df: pd.DataFrame) -> pd.Series:
    """Assign deterministic class-balanced labels using score quantiles."""
    score = compute_risk_score(df)
    low_t, high_t = score.quantile([1 / 3, 2 / 3]).tolist()
    labels = np.where(score >= high_t, "High", np.where(score >= low_t, "Medium", "Low"))
    return pd.Series(labels, index=df.index)


def validate_risk_classes(df: pd.DataFrame) -> None:
    """Ensure all three risk classes are present."""
    present = set(df["risk_level"].unique().tolist())
    expected = set(RISK_LABELS)
    missing = expected - present
    if missing:
        raise ValueError(f"Missing risk classes in generated data: {sorted(missing)}")


def generate(rows: int = 600, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic supplier dataset with reproducible distributions."""
    if rows < 30:
        raise ValueError("rows must be >= 30 to reliably preserve 3 risk classes")

    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "supplier_id": [f"SUP-{i:04d}" for i in range(rows)],
            "country": rng.choice(COUNTRIES, size=rows, p=[0.17, 0.14, 0.14, 0.16, 0.16, 0.11, 0.12]),
            "cost": rng.normal(540, 130, size=rows).clip(150, 1100),
            "delivery_time": rng.normal(14, 4, size=rows).clip(3, 28),
            "reliability_score": rng.normal(84, 9, size=rows).clip(40, 99),
            "defect_rate": rng.beta(2, 16, size=rows).clip(0.001, 0.25),
            "delay_history": rng.poisson(5, size=rows),
        }
    )
    df["risk_level"] = assign_balanced_risk(df)
    validate_risk_classes(df)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic supplier dataset")
    parser.add_argument("--rows", type=int, default=700)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="data/processed/suppliers.csv")
    args = parser.parse_args()

    data = generate(rows=args.rows, seed=args.seed)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)
    print(f"saved {len(data)} rows to {output_path}")


if __name__ == "__main__":
    main()

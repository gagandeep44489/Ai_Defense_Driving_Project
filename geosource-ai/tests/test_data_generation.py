from data.generate_data import generate


def test_generate_contains_all_risk_classes() -> None:
    df = generate(rows=600, seed=42)
    assert set(df["risk_level"].unique()) == {"Low", "Medium", "High"}
    assert len(df) == 600

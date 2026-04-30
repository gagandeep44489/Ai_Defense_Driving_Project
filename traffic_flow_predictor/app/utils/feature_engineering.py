from datetime import datetime


def derive_time_features(date: str, time: str) -> dict:
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    return {"hour": dt.hour, "weekday": dt.weekday(), "month": dt.month}

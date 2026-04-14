"""Scenario 2: stray dog crossing in urban lane."""

SCENARIO = {
    "id": 2,
    "name": "Stray Dog Crossing",
    "ego_speed_kmph": 32,
    "objects": [
        {"type": "animal", "position": "ahead-left", "distance_m": 10, "speed_kmph": 12},
        {"type": "car", "position": "behind", "distance_m": 20, "speed_kmph": 30},
    ],
}

"""Scenario 3: wrong-side bike approaching."""

SCENARIO = {
    "id": 3,
    "name": "Wrong-side Bike Coming",
    "ego_speed_kmph": 40,
    "objects": [
        {
            "type": "wrong-side vehicle",
            "position": "ahead",
            "distance_m": 18,
            "speed_kmph": 35,
            "direction": "wrong-side",
        },
        {
            "type": "bike",
            "position": "ahead",
            "distance_m": 16,
            "speed_kmph": 35,
            "direction": "wrong-side",
        },
    ],
}

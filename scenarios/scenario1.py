"""Scenario 1: pothole with fast bus behind."""

SCENARIO = {
    "id": 1,
    "name": "Pothole + Bus Behind",
    "ego_speed_kmph": 38,
    "objects": [
        {"type": "pothole", "position": "ahead", "distance_m": 12, "speed_kmph": 0},
        {"type": "bus", "position": "behind", "distance_m": 8, "speed_kmph": 45},
    ],
}

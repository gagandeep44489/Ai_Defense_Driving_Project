"""Map obstacle placement for Saarthi scenarios."""

from __future__ import annotations

from typing import Dict, List


def objects_for_scenario(scenario_id: int) -> List[Dict]:
    base = [
        {"name": "Car", "type": "car", "lon": 75.3412, "lat": 31.1471, "color": [0, 153, 255], "radius": 70},
    ]

    if scenario_id == 1:
        base.extend(
            [
                {"name": "Pothole", "type": "pothole", "lon": 75.34225, "lat": 31.14755, "color": [255, 140, 0], "radius": 85},
                {"name": "Bus Behind", "type": "bus", "lon": 75.34095, "lat": 31.14695, "color": [255, 30, 30], "radius": 95},
            ]
        )
    elif scenario_id == 2:
        base.extend(
            [
                {"name": "Dog", "type": "animal", "lon": 75.34205, "lat": 31.1477, "color": [255, 99, 71], "radius": 90},
                {"name": "Car Behind", "type": "car", "lon": 75.3410, "lat": 31.1469, "color": [255, 30, 30], "radius": 70},
            ]
        )
    else:
        base.extend(
            [
                {"name": "Wrong-side Bike", "type": "bike", "lon": 75.3431, "lat": 31.1473, "color": [255, 0, 0], "radius": 95},
                {"name": "Wrong-side Vehicle", "type": "wrong-side vehicle", "lon": 75.3436, "lat": 31.14735, "color": [255, 0, 0], "radius": 105},
            ]
        )

    return base

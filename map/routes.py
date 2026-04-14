"""Route definitions for Saarthi live map simulation."""

from __future__ import annotations

from typing import Dict, List

BASE_CENTER = {"lat": 31.1471, "lon": 75.3412}


def route_for_scenario(scenario_id: int) -> List[List[float]]:
    """Return [lon, lat] path points near Punjab center."""
    if scenario_id == 1:
        return [
            [75.3412, 31.1471],
            [75.3418, 31.14735],
            [75.3424, 31.1476],
            [75.3430, 31.14785],
            [75.3436, 31.1481],
        ]
    if scenario_id == 2:
        return [
            [75.3412, 31.1471],
            [75.34165, 31.14745],
            [75.3421, 31.1478],
            [75.3426, 31.1481],
            [75.3431, 31.14835],
        ]
    return [
        [75.3412, 31.1471],
        [75.34195, 31.1472],
        [75.3427, 31.14725],
        [75.34345, 31.1473],
        [75.3442, 31.1474],
    ]


def adjust_route_for_decision(route: List[List[float]], decision: str) -> List[List[float]]:
    """Modify route shape for AI decision impact."""
    if decision in {"Avoid", "Avoid pothole without hard braking"}:
        return [[lon + 0.00015, lat + 0.00008] for lon, lat in route]
    if decision == "Turn":
        modified = route.copy()
        if len(modified) > 2:
            modified[2:] = [[lon + 0.0002, lat - 0.0002] for lon, lat in modified[2:]]
        return modified
    if decision == "Brake":
        return route[: max(2, len(route) // 2)]
    return route


def center_view() -> Dict[str, float]:
    return BASE_CENTER.copy()

"""Pydeck map engine for live simulation frames."""

from __future__ import annotations

from typing import Dict, List

import pydeck as pdk

from map.routes import center_view


def _danger_layer(objects: List[Dict], risk: str) -> pdk.Layer:
    danger = [obj for obj in objects if obj["type"] in {"animal", "pothole", "bike", "wrong-side vehicle", "bus"}]
    color = [255, 0, 0, 120] if risk == "High" else [245, 158, 11, 90]
    return pdk.Layer(
        "ScatterplotLayer",
        data=danger,
        get_position="[lon, lat]",
        get_radius="radius * 2.2",
        get_fill_color=color,
        pickable=True,
    )


def build_deck(route: List[List[float]], car_position: List[float], objects: List[Dict], risk: str) -> pdk.Deck:
    car = [{"name": "Saarthi Car 🚗", "lon": car_position[0], "lat": car_position[1], "color": [0, 200, 255], "radius": 120}]
    path_data = [{"name": "planned-route", "path": route}]

    object_layer = pdk.Layer(
        "ScatterplotLayer",
        data=objects,
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
    )

    path_layer = pdk.Layer(
        "PathLayer",
        data=path_data,
        get_path="path",
        get_color=[80, 180, 255],
        width_scale=4,
        width_min_pixels=3,
    )

    car_layer = pdk.Layer(
        "ScatterplotLayer",
        data=car,
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
    )

    view = center_view()
    view_state = pdk.ViewState(latitude=view["lat"], longitude=view["lon"], zoom=14.5, pitch=45, bearing=15)

    tooltip = {
        "html": "<b>{name}</b>",
        "style": {"backgroundColor": "#1f2937", "color": "white"},
    }

    return pdk.Deck(
        layers=[_danger_layer(objects, risk), path_layer, object_layer, car_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/dark-v10",
    )

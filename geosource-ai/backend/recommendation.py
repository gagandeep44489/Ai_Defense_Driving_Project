"""Supplier recommendation logic with graph intelligence."""
from __future__ import annotations

from typing import Dict, List

from backend.graph_model import recommend_from_graph


def recommend_alternatives(supplier_id: str, top_k: int = 3) -> List[Dict]:
    """Graph-aware top-k recommendations for alternate suppliers."""
    return recommend_from_graph(supplier_id=supplier_id, top_k=top_k)

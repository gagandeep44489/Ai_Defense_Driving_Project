import pandas as pd

from backend.core.config import settings
from backend.services.graph_service import GraphService


def test_recommendations_shape() -> None:
    svc = GraphService(settings.graph_path, settings.data_path)
    supplier_id = pd.read_csv(settings.data_path).iloc[0]["supplier_id"]
    recs = svc.recommend(supplier_id, 3)
    assert len(recs) == 3

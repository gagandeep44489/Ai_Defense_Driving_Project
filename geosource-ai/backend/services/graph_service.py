import joblib
import networkx as nx
import pandas as pd


class GraphService:
    def __init__(self, graph_path: str, data_path: str):
        self.graph_path = graph_path
        self.data_path = data_path
        self.graph = self._load_graph()
        self.df = pd.read_csv(data_path)

    def _load_graph(self) -> nx.Graph:
        return joblib.load(self.graph_path)

    def summary(self) -> dict:
        g = self.graph
        return {
            "nodes": g.number_of_nodes(),
            "edges": g.number_of_edges(),
            "density": nx.density(g),
        }

    def recommend(self, supplier_id: str, top_k: int) -> list[dict]:
        src = self.df[self.df.supplier_id == supplier_id].iloc[0]
        candidates: list[dict] = []
        for _, row in self.df.iterrows():
            if row.supplier_id == supplier_id:
                continue
            score = 0.0
            if row.country == src.country:
                score += 0.4
            score += max(0, 1 - abs(row.cost - src.cost) / 1000) * 0.3
            score += max(0, 1 - abs(row.reliability_score - src.reliability_score) / 100) * 0.3
            candidates.append({"supplier_id": row.supplier_id, "score": score, "country": row.country, "risk_level": row.risk_level})
        return sorted(candidates, key=lambda x: x["score"], reverse=True)[:top_k]

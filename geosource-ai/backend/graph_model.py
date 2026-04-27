"""Graph intelligence module for supplier relationship modeling and graph-based recommendations."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import networkx as nx
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "suppliers.csv"


@dataclass
class SupplierGraphArtifacts:
    graph: nx.Graph
    clusters: Dict[str, int]
    embeddings: Dict[str, List[float]]


def _is_similar_cost(a: float, b: float, threshold: float = 15.0) -> bool:
    return abs(a - b) <= threshold


def _is_similar_reliability(a: float, b: float, threshold: float = 8.0) -> bool:
    return abs(a - b) <= threshold


def build_supplier_graph(df: pd.DataFrame) -> nx.Graph:
    """Build supplier graph where edges represent business similarity."""
    g = nx.Graph()

    for _, row in df.iterrows():
        g.add_node(
            row["supplier_id"],
            country=row["country"],
            cost=float(row["cost"]),
            reliability_score=float(row["reliability_score"]),
            risk_label=row["risk_label"],
        )

    records = df.to_dict(orient="records")
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            left, right = records[i], records[j]
            reasons = []
            if left["country"] == right["country"]:
                reasons.append("same_country")
            if _is_similar_cost(float(left["cost"]), float(right["cost"])):
                reasons.append("similar_cost")
            if _is_similar_reliability(float(left["reliability_score"]), float(right["reliability_score"])):
                reasons.append("similar_reliability")

            if reasons:
                g.add_edge(
                    left["supplier_id"],
                    right["supplier_id"],
                    weight=float(len(reasons)),
                    reasons=reasons,
                )

    return g


def detect_clusters(g: nx.Graph) -> Dict[str, int]:
    """Detect graph communities and map supplier_id -> cluster_id."""
    communities = nx.algorithms.community.greedy_modularity_communities(g)
    mapping: Dict[str, int] = {}
    for idx, community in enumerate(communities):
        for node in community:
            mapping[node] = idx
    return mapping


def compute_node_embeddings(g: nx.Graph) -> Dict[str, List[float]]:
    """Create simple graph embeddings using centrality signatures."""
    degree_centrality = nx.degree_centrality(g)
    betweenness_centrality = nx.betweenness_centrality(g)
    clustering_coeff = nx.clustering(g)

    embeddings = {}
    for node in g.nodes:
        embeddings[node] = [
            float(degree_centrality.get(node, 0.0)),
            float(betweenness_centrality.get(node, 0.0)),
            float(clustering_coeff.get(node, 0.0)),
        ]
    return embeddings


def load_graph_artifacts(data_path: Path = DATA_PATH) -> SupplierGraphArtifacts:
    df = pd.read_csv(data_path)
    graph = build_supplier_graph(df)
    clusters = detect_clusters(graph)
    embeddings = compute_node_embeddings(graph)
    return SupplierGraphArtifacts(graph=graph, clusters=clusters, embeddings=embeddings)


def recommend_from_graph(supplier_id: str, top_k: int = 3, data_path: Path = DATA_PATH) -> List[Dict]:
    """Graph-first recommendation: same cluster + weighted business score."""
    df = pd.read_csv(data_path)
    if supplier_id not in set(df["supplier_id"]):
        raise ValueError(f"Supplier '{supplier_id}' not found")

    artifacts = load_graph_artifacts(data_path)
    g = artifacts.graph
    target_cluster = artifacts.clusters.get(supplier_id)
    target_embedding = artifacts.embeddings.get(supplier_id, [0.0, 0.0, 0.0])

    candidate_rows = df[df["supplier_id"] != supplier_id].copy()
    candidate_rows["cluster_id"] = candidate_rows["supplier_id"].map(artifacts.clusters)
    cluster_candidates = candidate_rows[candidate_rows["cluster_id"] == target_cluster]

    if len(cluster_candidates) >= top_k:
        candidate_rows = cluster_candidates.copy()

    # Original weighted score (normalized)
    cost_norm = (candidate_rows["cost"] - candidate_rows["cost"].min()) / (
        candidate_rows["cost"].max() - candidate_rows["cost"].min() + 1e-8
    )
    delivery_norm = (candidate_rows["delivery_time"] - candidate_rows["delivery_time"].min()) / (
        candidate_rows["delivery_time"].max() - candidate_rows["delivery_time"].min() + 1e-8
    )
    reliability_norm = candidate_rows["reliability_score"] / 100.0
    base_score = (0.4 * reliability_norm) - (0.3 * cost_norm) - (0.3 * delivery_norm)

    graph_scores: List[float] = []
    for sid in candidate_rows["supplier_id"]:
        emb = artifacts.embeddings.get(sid, [0.0, 0.0, 0.0])
        dist = sum((a - b) ** 2 for a, b in zip(target_embedding, emb)) ** 0.5
        similarity = 1.0 / (1.0 + dist)
        edge_bonus = 0.0
        if g.has_edge(supplier_id, sid):
            edge_bonus = float(g[supplier_id][sid].get("weight", 0.0)) / 3.0
        graph_scores.append(0.7 * similarity + 0.3 * edge_bonus)

    candidate_rows["base_score"] = base_score
    candidate_rows["graph_score"] = graph_scores
    candidate_rows["recommendation_score"] = 0.55 * candidate_rows["base_score"] + 0.45 * candidate_rows["graph_score"]

    ranked = candidate_rows.sort_values("recommendation_score", ascending=False).head(top_k)
    return ranked[
        [
            "supplier_id",
            "country",
            "cost",
            "delivery_time",
            "reliability_score",
            "defect_rate",
            "delay_history",
            "risk_label",
            "cluster_id",
            "graph_score",
            "recommendation_score",
        ]
    ].to_dict(orient="records")

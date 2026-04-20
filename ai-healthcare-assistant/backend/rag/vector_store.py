from __future__ import annotations

import hashlib
from typing import Dict, List

import faiss
import numpy as np


class InMemoryVectorStore:
    def __init__(self, dim: int = 128) -> None:
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata: list[dict] = []

    def _embed(self, text: str) -> np.ndarray:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        arr = np.frombuffer(digest * (self.dim // len(digest) + 1), dtype=np.uint8)[: self.dim]
        vec = arr.astype(np.float32)
        norm = np.linalg.norm(vec) or 1.0
        return (vec / norm).reshape(1, -1)

    def add_document(self, patient_id: str, text: str) -> None:
        vector = self._embed(text)
        self.index.add(vector)
        self.metadata.append({"patient_id": patient_id, "text": text})

    def query(self, patient_id: str, query_text: str, top_k: int = 3) -> List[str]:
        if self.index.ntotal == 0:
            return []

        vector = self._embed(query_text)
        k = min(top_k, self.index.ntotal)
        _, indices = self.index.search(vector, k)

        results: list[str] = []
        for idx in indices[0]:
            item: Dict = self.metadata[int(idx)]
            if item["patient_id"] == patient_id:
                results.append(item["text"])
        return results


vector_store = InMemoryVectorStore()

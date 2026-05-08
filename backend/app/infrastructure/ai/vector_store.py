from dataclasses import dataclass, field


@dataclass
class VectorDocument:
    meeting_id: int
    title: str
    text: str
    vector: list[float]


class InMemoryVectorStore:
    """Vector store abstraction that can be replaced by ChromaDB or Pinecone adapters."""

    documents: list[VectorDocument] = field(default_factory=list)

    def __init__(self) -> None:
        self.documents = []

    async def upsert(self, document: VectorDocument) -> None:
        self.documents = [doc for doc in self.documents if doc.meeting_id != document.meeting_id]
        self.documents.append(document)

    async def search(self, vector: list[float], limit: int = 5) -> list[tuple[VectorDocument, float]]:
        def score(doc: VectorDocument) -> float:
            return sum(a * b for a, b in zip(doc.vector, vector))

        ranked = sorted(((doc, score(doc)) for doc in self.documents), key=lambda item: item[1], reverse=True)
        return ranked[:limit]


vector_store = InMemoryVectorStore()

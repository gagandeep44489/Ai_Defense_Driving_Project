from app.infrastructure.ai.providers import EmbeddingProvider, RagProvider
from app.infrastructure.ai.vector_store import vector_store
from app.schemas.dtos import SearchResult


class SemanticSearchService:
    def __init__(self) -> None:
        self.embeddings = EmbeddingProvider()
        self.rag = RagProvider()

    async def search(self, query: str, limit: int) -> list[SearchResult]:
        vector = await self.embeddings.embed(query)
        matches = await vector_store.search(vector, limit)
        return [SearchResult(meeting_id=doc.meeting_id, title=doc.title, snippet=doc.text[:240], score=score) for doc, score in matches]

    async def answer(self, query: str) -> str:
        results = await self.search(query, 5)
        return await self.rag.answer(query, [result.snippet for result in results])

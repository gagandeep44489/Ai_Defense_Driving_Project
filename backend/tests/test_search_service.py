import pytest
from app.application.ai.search import SemanticSearchService
from app.infrastructure.ai.providers import EmbeddingProvider
from app.infrastructure.ai.vector_store import VectorDocument, vector_store


@pytest.mark.asyncio
async def test_semantic_search_returns_indexed_meeting():
    vector_store.documents.clear()
    provider = EmbeddingProvider()
    text = "Quarterly planning meeting with action items and deadlines"
    await vector_store.upsert(VectorDocument(meeting_id=1, title="Planning", text=text, vector=await provider.embed(text)))

    results = await SemanticSearchService().search("planning deadlines", 3)

    assert results[0].meeting_id == 1
    assert "Planning" == results[0].title

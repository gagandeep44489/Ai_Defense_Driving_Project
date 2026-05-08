from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.application.ai.search import SemanticSearchService
from app.domain.entities.models import User
from app.schemas.dtos import SearchRequest, SearchResult

router = APIRouter(prefix="/search", tags=["semantic-search"])


@router.post("", response_model=list[SearchResult])
async def semantic_search(payload: SearchRequest, _: User = Depends(get_current_user)):
    return await SemanticSearchService().search(payload.query, payload.limit)


@router.post("/rag", response_model=str)
async def rag_answer(payload: SearchRequest, _: User = Depends(get_current_user)):
    return await SemanticSearchService().answer(payload.query)

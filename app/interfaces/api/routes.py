from fastapi import APIRouter, Depends
from app.application.dto.schemas import ClimateRiskRequest, RecommendationResponse
from app.application.use_cases.generate_recommendation import GenerateRecommendationUseCase
from app.core.security import require_token
from app.interfaces.api.dependencies import get_use_case

router = APIRouter(dependencies=[Depends(require_token)])


@router.post("/recommendations", response_model=RecommendationResponse)
def create_recommendation(request: ClimateRiskRequest, use_case: GenerateRecommendationUseCase = Depends(get_use_case)) -> RecommendationResponse:
    return use_case.execute(request)


@router.post("/bulk-recommendations", response_model=list[RecommendationResponse])
def create_bulk_recommendations(requests: list[ClimateRiskRequest], use_case: GenerateRecommendationUseCase = Depends(get_use_case)) -> list[RecommendationResponse]:
    return [use_case.execute(request) for request in requests]


@router.get("/recommendations/{location}", response_model=list[RecommendationResponse])
def get_recommendations(location: str, use_case: GenerateRecommendationUseCase = Depends(get_use_case)) -> list[RecommendationResponse]:
    return use_case.history(location)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/metrics")
def metrics() -> dict[str, int]:
    return {"requests": 0, "recommendations_generated": 0}

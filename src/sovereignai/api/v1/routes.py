"""Versioned REST routes for authentication, users, and inference."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sovereignai.core.database import Base, engine, get_session
from sovereignai.core.security import create_access_token, create_refresh_token, verify_password
from sovereignai.threat_detection.schemas import NetworkEvent, ThreatPrediction
from sovereignai.threat_detection.service import HeuristicThreatScoringStrategy
from sovereignai.users.models import UserModel
from sovereignai.users.repository import UserRepository
from sovereignai.users.schemas import UserCreate, UserRead
from sovereignai.users.service import UserService

router = APIRouter()
Base.metadata.create_all(bind=engine)

@router.post('/users', response_model=UserRead, tags=['users'])
def create_user(payload: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    """Create a platform user."""
    try: user = UserService(UserRepository(session)).create_user(payload); session.commit()
    except ValueError as exc: raise HTTPException(status_code=409, detail=str(exc)) from exc
    return UserRead(id=user.id, email=user.email, full_name=user.full_name, roles=user.roles.split(','), is_active=user.is_active)

@router.post('/auth/token', tags=['authentication'])
def token(email: str, password: str, session: Session = Depends(get_session)) -> dict[str, str]:
    """Issue access and refresh tokens for valid credentials."""
    user = UserRepository(session).get_by_email(email)
    if user is None or not verify_password(password, user.password_hash): raise HTTPException(status_code=401, detail='invalid credentials')
    roles = user.roles.split(',')
    return {'access_token': create_access_token(user.email, roles), 'refresh_token': create_refresh_token(user.email), 'token_type':'bearer'}

@router.post('/threats/predict', response_model=ThreatPrediction, tags=['threat-detection'])
def predict(event: NetworkEvent) -> ThreatPrediction:
    """Run real-time threat inference against a network event."""
    return HeuristicThreatScoringStrategy().score(event)

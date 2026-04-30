from pydantic import BaseModel


class TrafficResponse(BaseModel):
    prediction: float
    category: str
    cached: bool

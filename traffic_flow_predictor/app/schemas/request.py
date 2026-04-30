from pydantic import BaseModel, Field, field_validator


class TrafficRequest(BaseModel):
    date: str
    time: str
    temperature: float = Field(ge=-80, le=80)
    rain: float = Field(ge=0)
    snow: float = Field(ge=0)
    weather: str
    holiday: bool

    @field_validator("weather")
    @classmethod
    def validate_weather(cls, value: str):
        allowed = {"Clear", "Clouds", "Rain", "Snow", "Mist"}
        if value not in allowed:
            raise ValueError(f"weather must be one of {allowed}")
        return value

"""Threat detection schemas and value objects."""
from enum import StrEnum
from pydantic import BaseModel, Field

class ThreatClass(StrEnum):
    """Supported threat classes."""
    benign='benign'; intrusion='intrusion'; malware='malware'; anomaly='anomaly'; brute_force='brute_force'; data_exfiltration='data_exfiltration'

class NetworkEvent(BaseModel):
    """Normalized network telemetry event for inference."""
    source_ip: str
    destination_ip: str
    source_port: int = Field(ge=0, le=65535)
    destination_port: int = Field(ge=0, le=65535)
    protocol: str
    bytes_sent: int = Field(ge=0)
    bytes_received: int = Field(ge=0)
    duration_seconds: float = Field(ge=0)
    failed_logins: int = Field(default=0, ge=0)

class ThreatPrediction(BaseModel):
    """Prediction returned by the threat scoring pipeline."""
    threat_class: ThreatClass
    risk_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    explanation: list[str]

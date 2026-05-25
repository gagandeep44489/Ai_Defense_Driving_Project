"""Custom application exceptions."""


class GeoSourceError(Exception):
    """Base exception for domain and application errors."""


class ArtifactNotFoundError(GeoSourceError):
    """Raised when required model artifacts are unavailable."""


class PredictionError(GeoSourceError):
    """Raised when prediction cannot be completed."""

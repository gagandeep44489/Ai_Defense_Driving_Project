import re

BIAS_PATTERNS = [
    r"non-compliant patient",
    r"poor background",
    r"uneducated",
]


def sanitize_bias(text: str) -> str:
    sanitized = text
    for pattern in BIAS_PATTERNS:
        sanitized = re.sub(pattern, "[redacted-biased-phrase]", sanitized, flags=re.IGNORECASE)
    return sanitized

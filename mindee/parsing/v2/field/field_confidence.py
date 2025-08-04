from enum import Enum


class FieldConfidence(str, Enum):
    """Confidence level of a field as returned by the V2 API."""

    CERTAIN = "Certain"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

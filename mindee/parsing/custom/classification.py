from mindee.parsing.common.string_dict import StringDict


class ClassificationField:
    """A classification field."""

    value: str
    """The classification value."""
    confidence: float
    """The confidence score"""

    def __init__(self, raw_prediction: StringDict) -> None:
        self.value = raw_prediction["value"]
        self.confidence = raw_prediction["confidence"]

    def __str__(self) -> str:
        return self.value or ""

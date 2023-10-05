from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import FieldPositionMixin


class OcrWord(FieldPositionMixin):
    """A single word."""

    confidence: float
    """The confidence score."""
    text: str
    """The extracted text."""

    def __init__(self, raw_prediction: StringDict) -> None:
        self.confidence = raw_prediction["confidence"]
        self.text = raw_prediction["text"]
        self._set_position(raw_prediction)

    def __str__(self) -> str:
        return self.text

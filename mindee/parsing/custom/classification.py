from typing import List, Optional

from mindee.parsing.standard.base import FieldPositionMixin, TypePredictionField


class ClassificationField:
    """A classification field."""

    value: str
    """The classification value."""
    confidence: float
    """The confidence score"""

    def __init__(self, prediction: TypePredictionField) -> None:
        self.value = prediction["value"]
        self.confidence = prediction["confidence"]

    def __str__(self) -> str:
        return self.value or ""


class ListFieldValue(FieldPositionMixin):
    """A single value or word."""

    content: str
    """The content text"""
    confidence: float = 0.0
    """Confidence score"""

    def __init__(self, prediction: TypePredictionField) -> None:
        self.content = prediction["content"]
        self.confidence = prediction["confidence"]
        self._set_position(prediction)

    def __str__(self) -> str:
        return self.content


class ListField:
    """A list of values or words."""

    confidence: float = 0.0
    """Confidence score"""
    reconstructed: bool
    """Whether the field was reconstructed from other fields."""
    page_id: int
    """The document page on which the information was found."""
    values: List[ListFieldValue]
    """List of word values"""

    def __init__(
        self,
        prediction: TypePredictionField,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        self.values = []
        self.reconstructed = reconstructed
        if page_id is None:
            self.page_id = prediction["page_id"]
        else:
            self.page_id = page_id
        self.confidence = prediction["confidence"]

        for value in prediction["values"]:
            self.values.append(ListFieldValue(value))

    @property
    def contents_list(self) -> List[str]:
        """Return a List of the contents of all values."""
        return [value.content for value in self.values]

    def contents_string(self, separator: str = " ") -> str:
        """
        Return a string representation of all values.

        :param separator: Character(s) to use when concatenating fields.
        """
        return separator.join(self.contents_list)

    def __str__(self) -> str:
        return self.contents_string()

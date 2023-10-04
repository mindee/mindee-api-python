from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import FieldPositionMixin


class ListFieldValueV1(FieldPositionMixin):
    """A single value or word."""

    content: str
    """The content text"""
    confidence: float = 0.0
    """Confidence score"""

    def __init__(self, raw_prediction: StringDict) -> None:
        self.content = raw_prediction["content"]
        self.confidence = raw_prediction["confidence"]
        self._set_position(raw_prediction)

    def __str__(self) -> str:
        return self.content


class ListFieldV1:
    """A list of values or words."""

    confidence: float = 0.0
    """Confidence score"""
    reconstructed: bool
    """Whether the field was reconstructed from other fields."""
    page_id: int
    """The document page on which the information was found."""
    values: List[ListFieldValueV1]
    """List of word values"""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ) -> None:
        self.values = []
        self.reconstructed = reconstructed
        if page_id is None:
            self.page_id = raw_prediction["page_id"]
        else:
            self.page_id = page_id
        self.confidence = raw_prediction["confidence"]

        for value in raw_prediction["values"]:
            self.values.append(ListFieldValueV1(value))

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

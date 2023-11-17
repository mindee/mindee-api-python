from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import FieldPositionMixin


class ListFieldValue(FieldPositionMixin):
    """A single value or word."""

    content: str
    """The content text"""
    confidence: float
    """Confidence score"""
    page_id: Optional[int]
    """Id of the page the field was found on."""

    def __init__(
        self, raw_prediction: StringDict, page_id: Optional[int] = None
    ) -> None:
        self.content = raw_prediction["content"]
        self.confidence = raw_prediction["confidence"]
        self.page_id = page_id
        self._set_position(raw_prediction)

    def __str__(self) -> str:
        return self.content


class ListField:
    """A list of values or words."""

    confidence: float
    """Confidence score"""
    reconstructed: bool
    """Whether the field was reconstructed from other fields."""
    values: List[ListFieldValue]
    """List of word values"""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ) -> None:
        self.values = []
        self.reconstructed = reconstructed

        for value in raw_prediction["values"]:
            if "page_id" in value:
                page_id = value["page_id"]
            self.values.append(ListFieldValue(value, page_id))
        self.confidence = raw_prediction["confidence"]

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

from abc import ABC
from typing import List, Optional

from mindee.error.mindee_error import MindeeProductError
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import FieldPositionMixin


class ListFieldValue(ABC, FieldPositionMixin):
    """A single value or word."""

    content: str
    """The content text"""
    confidence: float
    """Confidence score"""
    page_id: Optional[int]
    """Id of the page the candidate was found on."""

    def __init__(
        self, raw_prediction: StringDict, page_id: Optional[int] = None
    ) -> None:
        self.content = raw_prediction["content"]
        self.confidence = raw_prediction["confidence"]
        self._set_position(raw_prediction)
        self.page_id = page_id

    def __str__(self) -> str:
        return self.content


class ListFieldValueV1(ListFieldValue):
    """Implementation of list field value on Custom V1."""


class ListFieldValueV2(ListFieldValue):
    """Implementation of list field value on Custom V1."""


class ListField(ABC):
    """A list of values or words."""

    confidence: float
    """Confidence score"""
    reconstructed: bool
    """Whether the field was reconstructed from other fields."""
    page_id: Optional[int]
    """The document page on which the information was found."""
    values: List
    """List of word values"""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
    ) -> None:
        self.values = []
        self.reconstructed = reconstructed
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


class ListFieldV1(ListField):
    """Implementation of the list field class for Custom V1."""

    values: List[ListFieldValueV1]
    """List of word values"""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ) -> None:
        super().__init__(raw_prediction, reconstructed)

        if page_id is None:
            if "page_id" in raw_prediction:
                self.page_id = raw_prediction["page_id"]
        else:
            self.page_id = page_id
        for value in raw_prediction["values"]:
            try:
                self.values.append(ListFieldValueV1(value, self.page_id))
            except AttributeError as exc:
                raise MindeeProductError(
                    "Wrong Custom version. Upgrade to CustomV2 to use this endpoint."
                ) from exc


class ListFieldV2(ListField):
    """Implementation of the list field class for Custom V2."""

    values: List[ListFieldValueV2]
    """List of word values"""
    page_id: int
    """The document page on which the information was found."""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ) -> None:
        super().__init__(raw_prediction, reconstructed)
        for value in raw_prediction["values"]:
            p_id = value["page_id"] if "page_id" in value else page_id
            self.values.append(ListFieldValueV2(value, p_id))

        if page_id is None:
            if "page_id" in raw_prediction:
                self.page_id = raw_prediction["page_id"]
        else:
            self.page_id = page_id

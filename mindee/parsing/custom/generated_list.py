from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import FieldPositionMixin


class GeneratedListFieldValue:
    """A single value or word."""

    content: str
    """The content text"""
    page_id: Optional[int]
    """Id of the page the field was found on."""

    def __init__(
        self, raw_prediction: StringDict, page_id: Optional[int] = None
    ) -> None:
        self.content = raw_prediction["content"]
        self.page_id = page_id

    def __str__(self) -> str:
        return self.content


class GeneratedListField:
    """A list of values or words, used in generated APIs."""

    values: List[GeneratedListFieldValue]
    """List of word values"""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ) -> None:
        self.values = []

        for value in raw_prediction["values"]:
            if "page_id" in value:
                page_id = value["page_id"]
            self.values.append(GeneratedListFieldValue(value, page_id))

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

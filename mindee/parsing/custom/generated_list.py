from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict


class GeneratedListFieldValue:
    """A single value or word."""

    content: Optional[str]
    """The content text"""
    page_id: Optional[int]
    """Id of the page the field was found on."""

    def __init__(
        self, raw_prediction: StringDict, page_id: Optional[int] = None
    ) -> None:
        self.content = raw_prediction["value"] if "value" in raw_prediction else None
        self.page_id = page_id

    def __str__(self) -> str:
        return self.content or ""


class GeneratedListField:
    """A list of values or words, used in generated APIs."""

    page_id: Optional[int]
    values: List[GeneratedListFieldValue]
    """List of word values"""

    def __init__(
        self,
        raw_prediction: List[StringDict],
        page_id: Optional[int] = None,
    ) -> None:
        self.values = []

        for value in raw_prediction:
            if value and "page_id" in value and value["page_id"].isdigit():
                page_id = int(value["page_id"])
            self.values.append(GeneratedListFieldValue(value, page_id))

    @property
    def contents_list(self) -> List[str]:
        """Return a List of the contents of all values."""
        return [value.content or "" for value in self.values]

    def contents_string(self, separator: str = " ") -> str:
        """
        Return a string representation of all values.

        :param separator: Character(s) to use when concatenating fields.
        """
        return separator.join(self.contents_list)

    def __str__(self) -> str:
        return self.contents_string()

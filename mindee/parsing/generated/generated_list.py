from typing import List, Optional, Union

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.generated.generated_object import (
    GeneratedObjectField,
    is_generated_object,
)
from mindee.parsing.standard.text import StringField


class GeneratedListField:
    """A list of values or objects, used in generated APIs."""

    page_id: Optional[int]
    """Id of the page the object was found on"""
    values: List[Union[GeneratedObjectField, StringField]]
    """List of word values"""

    def __init__(
        self,
        raw_prediction: List[StringDict],
        page_id: Optional[int] = None,
    ) -> None:
        self.values = []

        for value in raw_prediction:
            if "page_id" in value and value["page_id"] is not None:
                page_id = value["page_id"]
            if is_generated_object(value):
                self.values.append(GeneratedObjectField(value, page_id))
            else:
                value_str = value
                if "value" in value_str and value_str["value"] is not None:
                    value_str["value"] = str(value_str["value"])
                self.values.append(
                    StringField(
                        value_str,
                        page_id=page_id,
                    )
                )

    @property
    def contents_list(self) -> List[str]:
        """Return a List of the contents of all values."""
        return [str(v or "") for v in self.values]

    def contents_string(self, separator: str = " ") -> str:
        """
        Return a string representation of all values.

        :param separator: Character(s) to use when concatenating fields.
        """
        return separator.join(self.contents_list)

    def __str__(self) -> str:
        return self.contents_string()

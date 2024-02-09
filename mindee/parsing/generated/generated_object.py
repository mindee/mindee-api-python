from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.position import PositionField


class GeneratedObjectField:
    """A JSON-like object, with miscellaneous values."""

    page_id: Optional[int]
    """Id of the page the object was found on."""
    confidence: Optional[float]
    """Confidence with which the value was assessed."""
    raw_value: Optional[str]
    """Raw unprocessed value, as it was sent by the server."""
    __printable_values: List[str]
    """List of all printable field names."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ) -> None:
        item_page_id = None
        self.__printable_values = []
        for name, value in raw_prediction.items():
            if name == "page_id":
                item_page_id = value
            elif name in ("polygon", "rectangle", "quadrangle", "bounding_box"):
                self.__setattr__(
                    name,
                    PositionField({name: value}, value_key=name, page_id=item_page_id),
                )
                self.__printable_values.append(name)
            elif name == "confidence":
                self.confidence = value
            elif name == "raw_value":
                self.raw_value = value
            else:
                self.__setattr__(
                    name,
                    str(value) if value is not None else None,
                )
                self.__printable_values.append(name)
            self.page_id = page_id or item_page_id

    def _str_level(self, level=0) -> str:
        """
        ReSTructured-compliant string representation.

        Takes into account level of indentation & displays elements as list elements.

        :param level: level of indent (times 2 spaces).
        """
        indent = "  " + "  " * level
        out_str = ""
        for attr in self.__printable_values:
            value = getattr(self, attr)
            str_value = str(value) if value is not None else ""
            out_str += f"\n{indent}:{attr}: {str_value}"
        return "\n" + indent + (out_str.strip())

    def __str__(self) -> str:
        return self._str_level()


def is_generated_object(str_dict: StringDict) -> bool:
    """
    Checks whether an field is a custom object or not.

    :param str_dict: input dictionary to check.
    """
    common_keys = [
        "value",
        "polygon",
        "rectangle",
        "page_id",
        "confidence",
        "quadrangle",
        "values",
        "raw_value",
    ]
    for key in str_dict.keys():
        if key not in common_keys:
            return True
    return False

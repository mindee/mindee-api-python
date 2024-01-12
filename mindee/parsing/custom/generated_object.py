from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class GeneratedObjectField:
    """A JSON-like object, with miscellaneous values."""

    page_id: Optional[int]
    """Id of the page the object was found on"""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ) -> None:
        item_page_id = None
        for name, value in raw_prediction.items():
            if name == "page_id":
                item_page_id = value
            elif name in ["polygon", "rectangle", "quadrangle", "bounding_box"]:
                self.__setattr__(
                    name,
                    f"Polygon with {len(value)} points." if value is not None else None,
                )
            elif name not in ["confidence", "raw_value"]:
                self.__setattr__(
                    name,
                    str(value) if value is not None else None,
                )
            self.page_id = page_id or item_page_id

    def __str__(self, level=0) -> str:
        """
        String representation.

        Takes into account level of indentation & displays elements as list elements.

        :param level: level of indent (times 2 spaces).
        """
        indent = "  " + "  " * level
        out_str = ""
        for attr in dir(self):
            if not attr.startswith("__") and attr != "page_id":
                value = self.__getattribute__(attr)
                str_value = str(value) if value is not None else ""
                out_str += f"\n  {indent}:{attr}: {str_value}"
        return "\n" + indent + "* " + (out_str.strip())


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

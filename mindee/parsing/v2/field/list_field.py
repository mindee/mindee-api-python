from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.dynamic_field import (
    DynamicField,
    FieldType,
    get_field_type,
)


class ListField(DynamicField):
    """List field containing multiple fields."""

    items: List[DynamicField]
    """Items contained in the list."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(FieldType.LIST, indent_level)

        self.items = []
        for item in raw_response["items"]:
            self.items.append(get_field_type(item))

    def __str__(self) -> str:
        out_str = ""
        indent = " " * self._indent_level
        for item in self.items:
            if item.field_type == FieldType.SIMPLE:
                out_str += f"\n{indent}  * {item}"
            elif item.field_type == FieldType.OBJECT:
                out_str += f"\n{indent}  * {item.multi_str()}"

        return out_str

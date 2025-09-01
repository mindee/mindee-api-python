from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.base_field import BaseField
from mindee.parsing.v2.field.dynamic_field import (
    DynamicField,
    FieldType,
    get_field_type,
)
from mindee.parsing.v2.field.object_field import ObjectField
from mindee.parsing.v2.field.simple_field import SimpleField


class ListField(BaseField):
    """List field containing multiple fields."""

    items: List[DynamicField]
    """Items contained in the list."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(FieldType.LIST, raw_response, indent_level)

        self.items = []
        for item in raw_response["items"]:
            self.items.append(get_field_type(item))

    @property
    def simple_items(self) -> List[SimpleField]:
        """List of items as ``SimpleField``."""
        simple_items = []
        for item in self.items:
            if isinstance(item, SimpleField):
                simple_items.append(item)
            else:
                raise ValueError("List item is not a simple field.")
        return simple_items

    @property
    def object_items(self) -> List[ObjectField]:
        """List of items as ``ObjectField``."""
        object_items = []
        for item in self.items:
            if isinstance(item, ObjectField):
                object_items.append(item)
            else:
                raise ValueError("List item is not an object field.")
        return object_items

    def __str__(self) -> str:
        out_str = ""
        indent = " " * self._indent_level
        for item in self.items:
            if item.field_type == FieldType.SIMPLE:
                out_str += f"\n{indent}  * {item}"
            elif item.field_type == FieldType.OBJECT:
                out_str += f"\n{indent}  * {item.multi_str()}"

        return out_str

from enum import Enum

from mindee.error import MindeeApiV2Error
from mindee.parsing import v2
from mindee.parsing.common.string_dict import StringDict


class FieldType(str, Enum):
    """Field types."""

    OBJECT = "ObjectField"
    LIST = "ListField"
    SIMPLE = "SimpleField"


class DynamicField:
    """Field that can be displayed in rst format."""

    _indent_level: int
    """Indentation level for rst display."""
    field_type: FieldType
    """Field type."""

    def __init__(self, field_type: FieldType, indent_level=0) -> None:
        self.field_type = field_type
        self._indent_level = indent_level

    def multi_str(self) -> str:
        """String representation of the field in a list."""
        return str(self)


def get_field_type(raw_response: StringDict, indent_level: int = 0) -> DynamicField:
    """Get appropriate field types."""
    if isinstance(raw_response, dict):
        if "value" in raw_response:
            field_file = getattr(v2, "simple_field")
            field_class = getattr(field_file, FieldType.SIMPLE.value)
        elif "items" in raw_response:
            field_file = getattr(v2, "list_field")
            field_class = getattr(field_file, FieldType.LIST.value)
        elif "fields" in raw_response:
            field_file = getattr(v2, "object_field")
            field_class = getattr(field_file, FieldType.OBJECT.value)
        else:
            raise MindeeApiV2Error(f"Unrecognized field format in {raw_response}.")
        return field_class(raw_response, indent_level)

    raise MindeeApiV2Error(f"Unrecognized field format {raw_response}.")

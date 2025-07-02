from typing import Dict, List, Union

from mindee.error.mindee_error import MindeeAPIV2Error
from mindee.parsing.common.string_dict import StringDict


class BaseField:
    """Base field class for V2."""

    _indent_level: int
    """Indentation level for rst display."""

    def __init__(self, indent_level=0) -> None:
        self._indent_level = indent_level

    @staticmethod
    def create_field(raw_response: StringDict, indent_level: int = 0) -> "BaseField":
        """Factory function to create appropriate field instances."""
        if isinstance(raw_response, dict):
            if "items" in raw_response:
                return ListField(raw_response, indent_level)
            if "fields" in raw_response:
                return ObjectField(raw_response, indent_level)
            if "value" in raw_response:
                return SimpleField(raw_response, indent_level)
            raise MindeeAPIV2Error("Unrecognized field format.")
        raise MindeeAPIV2Error("Unrecognized field format.")


class ListField(BaseField):
    """List field containing multiple fields."""

    items: List[BaseField]
    """Items contained in the list."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(indent_level)

        self.items = []
        for item in raw_response["items"]:
            if isinstance(item, dict):
                self.items.append(BaseField.create_field(item, 1))
            raise MindeeAPIV2Error("Unrecognized field format.")


class ObjectField(BaseField):
    """Object field containing multiple fields."""

    fields: Dict[str, BaseField]
    """Fields contained in the object."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(indent_level)
        fields: Dict[str, BaseField] = {}
        for field_key, field_value in raw_response.items():
            if isinstance(field_value, dict):
                fields[field_key] = BaseField.create_field(field_value, 1)
            else:
                raise MindeeAPIV2Error("Unrecognized field format.")

    def __str__(self) -> str:
        out_str = ""
        for field_key, field_value in self.fields.items():
            out_str += f"{' ' * self._indent_level}:{field_key}: {field_value}\n"
        return out_str


class SimpleField(BaseField):
    """Simple field containing a single value."""

    value: Union[str, float, bool, None]

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(indent_level)
        self.value = raw_response["value"] if "value" in raw_response else None

    def __str__(self) -> str:
        return f"{' ' * self._indent_level}{self.value}\n"

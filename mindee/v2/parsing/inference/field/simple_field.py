from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import BaseField, FieldType


class SimpleField(BaseField):
    """Simple field containing a single value."""

    value: str | float | bool | None

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(FieldType.SIMPLE, raw_response, indent_level)
        value = raw_response.get("value", None)
        if isinstance(value, int) and not isinstance(value, bool):
            self.value = float(value)
        else:
            self.value = value

    @property
    def string_value(self) -> str | None:
        """Retrieves a string field value as a string."""
        if self.value is not None and not isinstance(self.value, str):
            raise ValueError("Value is not a string")
        return self.value

    @property
    def number_value(self) -> float | None:
        """Retrieves a number field value as a float."""
        if self.value is not None and not isinstance(self.value, float):
            raise ValueError("Value is not a number")
        return self.value

    @property
    def boolean_value(self) -> bool | None:
        """Retrieves a boolean field value as a boolean."""
        if self.value is not None and not isinstance(self.value, bool):
            raise ValueError("Value is not a boolean")
        return self.value

    def __str__(self) -> str:
        if isinstance(self.value, bool):
            return "True" if self.value else "False"
        return str(self.value if self.value is not None else "")

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

    def __str__(self) -> str:
        if isinstance(self.value, bool):
            return "True" if self.value else "False"
        return str(self.value if self.value is not None else "")

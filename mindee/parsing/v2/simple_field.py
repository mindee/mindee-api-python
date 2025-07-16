from typing import Union

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.base_field import BaseField
from mindee.parsing.v2.dynamic_field import FieldType


class SimpleField(BaseField):
    """Simple field containing a single value."""

    value: Union[str, float, bool, None]

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(FieldType.SIMPLE, indent_level)
        self.value = raw_response["value"] = raw_response.get("value", None)

    def __str__(self) -> str:
        return str(self.value)

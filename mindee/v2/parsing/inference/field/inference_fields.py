from collections.abc import Callable

from mindee.parsing.common import StringDict
from mindee.v2.parsing.inference.field.base_field import BaseField, FieldType


class InferenceFields(dict[str, BaseField]):
    """Inference fields dict."""

    def __init__(
        self,
        raw_response: StringDict,
        parser_func: Callable[[StringDict, int], BaseField],
        indent_level: int = 0,
    ) -> None:
        super().__init__()
        for key, value in raw_response.items():
            self[key] = parser_func(value, indent_level)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item) from None

    def __str__(self) -> str:
        str_fields = ""
        for field_key, field_value in self.items():
            if field_value.field_type == FieldType.SIMPLE:
                final_value = f"{field_value}"
                if final_value:
                    final_value = f" {final_value}"
                str_fields += f"\n:{field_key}:{final_value}"
            else:
                str_fields += f"\n:{field_key}:{field_value}"
        return str_fields

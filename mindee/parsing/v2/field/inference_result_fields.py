from typing import Dict

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.dynamic_field import (
    DynamicField,
    FieldType,
    get_field_type,
)


class InferenceResultFields(Dict[str, DynamicField]):
    """Inference fields dict."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0) -> None:
        super().__init__()
        for key, value in raw_response.items():
            field_obj = get_field_type(value, indent_level)
            self[key] = field_obj

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

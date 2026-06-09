from collections.abc import Callable
from typing import TYPE_CHECKING, cast

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import BaseField, FieldType

if TYPE_CHECKING:
    from mindee.v2.parsing.inference.field.list_field import ListField
    from mindee.v2.parsing.inference.field.object_field import ObjectField
    from mindee.v2.parsing.inference.field.simple_field import SimpleField


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

    def get_simple_field(self, field_name: str) -> "SimpleField":
        """Retrieve a simple field by its name."""
        field = self.get(field_name)
        if field and field.field_type == FieldType.SIMPLE:
            return cast("SimpleField", field)
        raise ValueError(f"Field {field_name} is not a SimpleField.")

    def get_object_field(self, field_name: str) -> "ObjectField":
        """Retrieve an object field by its name."""
        field = self.get(field_name)
        if field and field.field_type == FieldType.OBJECT:
            return cast("ObjectField", field)
        raise ValueError(f"Field {field_name} is not an ObjectField.")

    def get_list_field(self, field_name: str) -> "ListField":
        """Retrieve a list field by its name."""
        field = self.get(field_name)
        if field and field.field_type == FieldType.LIST:
            return cast("ListField", field)
        raise ValueError(f"Field {field_name} is not a ListField.")

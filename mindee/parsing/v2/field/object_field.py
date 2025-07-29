from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.base_field import BaseField
from mindee.parsing.v2.field.dynamic_field import FieldType
from mindee.parsing.v2.field.inference_result_fields import InferenceResultFields


class ObjectField(BaseField):
    """Object field containing multiple fields."""

    fields: InferenceResultFields
    """Fields contained in the object."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(FieldType.OBJECT, indent_level)
        inner_fields = raw_response.get("fields", raw_response)

        self.fields = InferenceResultFields(inner_fields, self._indent_level + 1)

    def single_str(self) -> str:
        """String representation of a single object field."""
        out_str = ""
        indent = " " * self._indent_level
        for field_key, field_value in self.fields.items():
            out_str += f"\n{indent}  :{field_key}: {field_value if field_value else ''}"
        return out_str

    def multi_str(self) -> str:
        """String representation of a list object field."""
        out_str = ""
        indent = " " * self._indent_level
        first = True
        for field_key, field_value in self.fields.items():
            if first:
                out_str += f"{indent}:{field_key}: {field_value}"
            else:
                out_str += f"\n{indent}    :{field_key}: {field_value}"
            first = False
        return out_str

    def __str__(self) -> str:
        return self.single_str()

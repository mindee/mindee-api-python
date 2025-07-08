from typing import Dict, List, Union

from mindee.error.mindee_error import MindeeApiV2Error
from mindee.parsing.common.string_dict import StringDict


class BaseField:
    """Base field class for V2."""

    _indent_level: int
    """Indentation level for rst display."""

    def __init__(self, indent_level=0) -> None:
        self._indent_level = indent_level

    @staticmethod
    def create_field(
        raw_response: StringDict, indent_level: int = 0
    ) -> Union["ListField", "ObjectField", "SimpleField"]:
        """Factory function to create appropriate field instances."""
        if isinstance(raw_response, dict):
            if "items" in raw_response:
                return ListField(raw_response, indent_level)
            if "fields" in raw_response:
                return ObjectField(raw_response, indent_level)
            if "value" in raw_response:
                return SimpleField(raw_response, indent_level)
            raise MindeeApiV2Error(f"Unrecognized field format in {raw_response}.")
        raise MindeeApiV2Error(f"Unrecognized field format {raw_response}.")


class InferenceFields(Dict[str, Union["SimpleField", "ObjectField", "ListField"]]):
    """Inference fields dict."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0) -> None:
        super().__init__()
        for key, value in raw_response.items():
            field_obj = BaseField.create_field(value, indent_level)
            self[key] = field_obj

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item) from None

    def __str__(self) -> str:
        str_fields = ""
        for field_key, field_value in self.items():
            str_fields += f":{field_key}: {field_value}"
        return str_fields


class ListField(BaseField):
    """List field containing multiple fields."""

    items: List[Union["ListField", "ObjectField", "SimpleField"]]
    """Items contained in the list."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(indent_level)

        self.items = []
        for item in raw_response["items"]:
            if isinstance(item, dict):
                self.items.append(BaseField.create_field(item, self._indent_level + 2))
            else:
                raise MindeeApiV2Error(f"Unrecognized field format '{item}'.")

    def __str__(self) -> str:
        out_str = ""
        for item in self.items:
            out_str += f"* {str(item)[2:] if item else ''}"
        return "\n" + out_str if out_str else ""


class ObjectField(BaseField):
    """Object field containing multiple fields."""

    fields: InferenceFields
    """Fields contained in the object."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(indent_level)
        inner_fields = raw_response.get("fields", raw_response)

        self.fields = InferenceFields(inner_fields, self._indent_level + 1)

    def __str__(self) -> str:
        out_str = ""
        for field_key, field_value in self.fields.items():
            if isinstance(field_value, ListField):
                value_str = ""
                if len(field_value.items) > 0:
                    value_str = (
                        " " * self._indent_level + str(field_value)
                        if field_value
                        else ""
                    )
                out_str += f"{' ' * self._indent_level}:{field_key}: {value_str}"
            else:
                out_str += f"{' ' * self._indent_level}:{field_key}: {field_value if field_value else ''}"
        return out_str


class SimpleField(BaseField):
    """Simple field containing a single value."""

    value: Union[str, float, bool, None]

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(indent_level)
        self.value = raw_response["value"] = raw_response.get("value", None)

    def __str__(self) -> str:
        return f"{self.value}\n" if self.value else "\n"

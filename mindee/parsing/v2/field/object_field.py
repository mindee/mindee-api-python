from typing import TYPE_CHECKING, cast
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.base_field import BaseField
from mindee.parsing.v2.field.dynamic_field import FieldType
from mindee.parsing.v2.field.inference_fields import InferenceFields

if TYPE_CHECKING:
    from mindee.parsing.v2.field.list_field import ListField
    from mindee.parsing.v2.field.simple_field import SimpleField


class ObjectField(BaseField):
    """Object field containing multiple fields."""

    fields: InferenceFields
    """Fields contained in the object."""

    def __init__(self, raw_response: StringDict, indent_level: int = 0):
        super().__init__(FieldType.OBJECT, raw_response, indent_level)
        inner_fields = raw_response.get("fields", raw_response)

        self.fields = InferenceFields(inner_fields, self._indent_level + 1)

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

    @property
    def simple_fields(self) -> dict[str, "SimpleField"]:
        """
        Extract and return all SimpleField fields from the `fields` attribute.

        :return: A dictionary containing all fields that have a type of `FieldType.SIMPLE`.
        :rtype: dict[str, SimpleField]
        """
        simple_fields = {}
        for field_key, field_value in self.fields.items():
            if field_value.field_type == FieldType.SIMPLE:
                simple_fields[field_key] = cast("SimpleField", field_value)
        return simple_fields

    @property
    def list_fields(self) -> dict[str, "ListField"]:
        """
        Retrieves all ListField fields from the `fields` attribute.

        :return: A dictionary containing all fields of type `LIST`, with keys
            representing field keys and values being the corresponding field
            objects.
        :rtype: dict[str, ListField]
        """
        list_fields = {}
        for field_key, field_value in self.fields.items():
            if field_value.field_type == FieldType.LIST:
                list_fields[field_key] = cast("ListField", field_value)
        return list_fields

    @property
    def object_fields(self) -> dict[str, "ObjectField"]:
        """
        Retrieves all ObjectField fields from the `fields` attribute of the instance.

        :returns: A dictionary containing fields of type `FieldType.OBJECT`. The keys represent
            the field names, and the values are corresponding ObjectField objects.
        :rtype: dict[str, ObjectField]
        """
        object_fields = {}
        for field_key, field_value in self.fields.items():
            if field_value.field_type == FieldType.OBJECT:
                object_fields[field_key] = cast("ObjectField", field_value)
        return object_fields

    def get_simple_field(self, field_name: str) -> "SimpleField":
        """
        Retrieves a SimpleField from the provided field name.

        :param field_name: The name of the field to retrieve.
        :type field_name: str
        :return: The SimpleField object corresponding to the given field name.
        :rtype: SimpleField
        :raises ValueError: If the specified field is not of type SimpleField.
        """
        if self.fields[field_name].field_type != FieldType.SIMPLE:
            raise ValueError(f"Field {field_name} is not a SimpleField.")
        return cast("SimpleField", self.fields[field_name])

    def get_list_field(self, field_name: str) -> "ListField":
        """
        Retrieves the ``ListField`` for the specified field name.

        :param field_name: The name of the field to retrieve.
        :type field_name: str
        :return: The corresponding ``ListField`` for the given field name.
        :rtype: ListField
        :raises ValueError: If the field is not of type ``ListField``.
        """
        if self.fields[field_name].field_type != FieldType.LIST:
            raise ValueError(f"Field {field_name} is not a ListField.")
        return cast("ListField", self.fields[field_name])

    def get_object_field(self, field_name: str) -> "ObjectField":
        """
        Retrieves the `ObjectField` associated with the specified field name.

        :param field_name: The name of the field to retrieve.
        :type field_name: str
        :return: The `ObjectField` associated with the given field name.
        :rtype: ObjectField
        :raises ValueError: If the field specified by `field_name` is not an `ObjectField`.
        """
        if self.fields[field_name].field_type != FieldType.OBJECT:
            raise ValueError(f"Field {field_name} is not an ObjectField.")
        return cast("ObjectField", self.fields[field_name])

    def __str__(self) -> str:
        return self.single_str()

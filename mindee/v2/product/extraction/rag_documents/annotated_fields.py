from typing import TYPE_CHECKING, cast

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import FieldType
from mindee.v2.product.extraction.rag_documents.annotated_base_field import (
    AnnotatedBaseField,
    AnnotatedFieldsType,
)

if TYPE_CHECKING:
    from mindee.v2.product.extraction.rag_documents.annotated_list_field import (
        AnnotatedListField,
    )
    from mindee.v2.product.extraction.rag_documents.annotated_object_field import (
        AnnotatedObjectField,
    )
    from mindee.v2.product.extraction.rag_documents.annotated_simple_field import (
        AnnotatedSimpleField,
    )


class AnnotatedFields(dict[str, AnnotatedFieldsType]):
    """A dictionary of field names and their corresponding annotation."""

    def __init__(self, raw_response: StringDict):
        super().__init__()
        for key, value in raw_response.items():
            self[key] = AnnotatedBaseField.build(value)

    def get_simple_field(self, field_name: str) -> "AnnotatedSimpleField":
        """Retrieve a simple field by its name."""
        field = self.get(field_name)
        if field and field.field_type == FieldType.SIMPLE:
            return cast("AnnotatedSimpleField", field)
        raise ValueError(f"Field {field_name} is not an AnnotatedSimpleField.")

    def get_list_field(self, field_name: str) -> "AnnotatedListField":
        """Retrieve a list field by its name."""
        field = self.get(field_name)
        if field and field.field_type == FieldType.LIST:
            return cast("AnnotatedListField", field)
        raise ValueError(f"Field {field_name} is not an AnnotatedListField.")

    def get_object_field(self, field_name: str) -> "AnnotatedObjectField":
        """Retrieve an object field by its name."""
        field = self.get(field_name)
        if field and field.field_type == FieldType.OBJECT:
            return cast("AnnotatedObjectField", field)
        raise ValueError(f"Field {field_name} is not an AnnotatedObjectField.")

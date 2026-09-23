from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import FieldType
from mindee.v2.product.extraction.rag_documents.annotated_base_field import (
    AnnotatedBaseField,
)
from mindee.v2.product.extraction.rag_documents.annotated_fields import AnnotatedFields
from mindee.v2.product.extraction.rag_documents.annotated_simple_field import (
    AnnotatedSimpleField,
)


@AnnotatedBaseField.register("fields")
class AnnotatedObjectField(AnnotatedBaseField):
    """An ObjectField with additional configuration for annotation."""

    fields: AnnotatedFields

    def __init__(self, raw_response: StringDict):
        super().__init__(FieldType.OBJECT, raw_response)
        self.fields = AnnotatedFields(raw_response["fields"])

    def get_simple_field(self, field_name: str) -> AnnotatedSimpleField:
        """Retrieve a Simple field by its name."""
        return self.fields.get_simple_field(field_name)

    def get_object_field(self, field_name: str) -> "AnnotatedObjectField":
        """Retrieve an Object field by its name."""
        return self.fields.get_object_field(field_name)

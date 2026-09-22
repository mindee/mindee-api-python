from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import FieldType
from mindee.v2.product.extraction.rag_documents.annotated_base_field import (
    AnnotatedBaseField,
)


@AnnotatedBaseField.register("value")
class AnnotatedSimpleField(AnnotatedBaseField):
    """A SimpleField with additional configuration for annotation."""

    value: str | float | bool | None

    def __init__(self, raw_response: StringDict):
        super().__init__(FieldType.SIMPLE, raw_response)
        self.value = raw_response["value"]

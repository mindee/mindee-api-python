from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import FieldType
from mindee.v2.product.extraction.rag_documents.annotated_base_field import (
    AnnotatedBaseField,
)
from mindee.v2.product.extraction.rag_documents.annotated_object_field import (
    AnnotatedObjectField,
)
from mindee.v2.product.extraction.rag_documents.annotated_simple_field import (
    AnnotatedSimpleField,
)


@AnnotatedBaseField.register("items")
class AnnotatedListField(AnnotatedBaseField):
    """A ListField with additional configuration for annotation."""

    items: list[AnnotatedBaseField]

    def __init__(self, raw_response: StringDict):
        super().__init__(FieldType.LIST, raw_response)
        self.items = [AnnotatedBaseField.build(item) for item in raw_response["items"]]

    @property
    def simple_items(self) -> list[AnnotatedSimpleField]:
        """List of items as ``AnnotatedSimpleField``."""
        simple_items = []
        for item in self.items:
            if isinstance(item, AnnotatedSimpleField):
                simple_items.append(item)
            else:
                raise ValueError("List item is not an AnnotatedSimpleField field.")
        return simple_items

    @property
    def object_items(self) -> list[AnnotatedObjectField]:
        """List of items as ``AnnotatedObjectField``."""
        object_items = []
        for item in self.items:
            if isinstance(item, AnnotatedObjectField):
                object_items.append(item)
            else:
                raise ValueError("List item is not an AnnotatedObjectField field.")
        return object_items

from typing import TYPE_CHECKING, ClassVar, TypeAlias, Union

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import FieldType

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

AnnotatedFieldsType: TypeAlias = Union[
    "AnnotatedSimpleField", "AnnotatedObjectField", "AnnotatedListField"
]


class AnnotatedBaseField:
    """Base class for annotated fields."""

    selected: bool = False
    """When true, use the RAG information for the final result. When false, use the Data Schema information."""

    guidelines: str | None = None
    """Guidelines or instructions for processing this field."""

    field_type: FieldType

    _registry: ClassVar[dict[str, type[AnnotatedFieldsType]]] = {}

    def __init__(self, field_type: FieldType, raw_response: StringDict):
        if "selected" in raw_response and raw_response["selected"] is not None:
            self.selected = raw_response["selected"]

        if "guidelines" in raw_response and raw_response["guidelines"] is not None:
            self.guidelines = raw_response.get("guidelines")

        self.field_type = field_type

    @classmethod
    def register(cls, discriminator_key: str):
        """Class decorator: subclasses declare which JSON key identifies them."""

        def decorator(subclass):
            cls._registry[discriminator_key] = subclass
            return subclass

        return decorator

    @classmethod
    def build(cls, raw_response: dict) -> AnnotatedFieldsType:
        """Build an instance of the appropriate subclass."""

        if not isinstance(raw_response, dict):
            raise ValueError("Field must be a dict")
        for key, subclass in cls._registry.items():
            if key in raw_response:
                return subclass(raw_response)
        raise ValueError("Invalid structure for field")

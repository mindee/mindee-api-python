from dataclasses import InitVar, dataclass
from typing import TYPE_CHECKING, ClassVar, TypeAlias, Union

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import FieldType
from mindee.v2.parsing.string_data_class import StringDataClass

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


@dataclass
class AnnotatedBaseField(StringDataClass):
    """Base class for annotated fields."""

    _field_type: ClassVar[FieldType]
    raw_response: InitVar[StringDict]

    selected: bool = False
    """When true, use the RAG information for the final result. When false, use the Data Schema information."""

    guidelines: str | None = None
    """Guidelines or instructions for processing this field."""

    _registry: ClassVar[dict[str, type[AnnotatedFieldsType]]] = {}

    def __post_init__(self, raw_response: StringDict):
        if "selected" in raw_response and raw_response["selected"] is not None:
            self.selected = raw_response["selected"]

        if "guidelines" in raw_response and raw_response["guidelines"] is not None:
            self.guidelines = raw_response.get("guidelines")

    @property
    def field_type(self) -> FieldType:
        """The field type."""
        return self._field_type

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
        raise ValueError(f"Invalid structure for field: '{raw_response}'")

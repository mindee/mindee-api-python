from dataclasses import dataclass, field
from typing import ClassVar

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.field.base_field import FieldType
from mindee.v2.product.extraction.rag_documents.annotated_base_field import (
    AnnotatedBaseField,
)


@AnnotatedBaseField.register("value")
@dataclass
class AnnotatedSimpleField(AnnotatedBaseField):
    """A SimpleField with additional configuration for annotation."""

    _field_type: ClassVar[FieldType] = field(init=False, default=FieldType.SIMPLE)
    value: str | float | bool | None = field(init=False)

    def __post_init__(self, raw_response: StringDict):
        super().__post_init__(raw_response)

        self.value = raw_response["value"]

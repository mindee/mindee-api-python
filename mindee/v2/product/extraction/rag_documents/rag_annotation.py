import json
from dataclasses import InitVar, dataclass, field
from typing import IO

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.string_data_class import StringDataClass
from mindee.v2.product.extraction.rag_documents.annotated_fields import AnnotatedFields

TypeRagAnnotationInput = StringDict | str | bytes | IO[str] | IO[bytes]


@dataclass
class RagAnnotation(StringDataClass):
    """A RAG annotation enriched with field-level configuration."""

    raw_response: InitVar[TypeRagAnnotationInput]

    fields: AnnotatedFields = field(init=False)
    """Annotated fields."""

    def __post_init__(self, raw_response: TypeRagAnnotationInput) -> None:
        if isinstance(raw_response, dict):
            self.fields = AnnotatedFields(raw_response["fields"])
        elif isinstance(raw_response, (str, bytes)):
            self.fields = AnnotatedFields(json.loads(raw_response)["fields"])
        else:
            self.fields = AnnotatedFields(json.load(raw_response)["fields"])

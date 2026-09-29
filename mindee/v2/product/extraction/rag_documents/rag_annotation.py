from dataclasses import InitVar, dataclass, field

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.string_data_class import StringDataClass
from mindee.v2.product.extraction.rag_documents.annotated_fields import AnnotatedFields


@dataclass
class RagAnnotation(StringDataClass):
    """A RAG annotation enriched with field-level configuration."""

    raw_response: InitVar[StringDict]

    fields: AnnotatedFields = field(init=False)
    """Annotated fields."""

    def __post_init__(self, raw_response: StringDict):
        self.fields = AnnotatedFields(raw_response["fields"])

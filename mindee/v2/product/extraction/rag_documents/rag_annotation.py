from mindee.parsing.common.string_dict import StringDict
from mindee.v2.product.extraction.rag_documents.annotated_fields import AnnotatedFields


class RagAnnotation:
    """A RAG annotation enriched with field-level configuration."""

    fields: AnnotatedFields
    """Annotated fields."""

    def __init__(self, raw_response: StringDict):
        self.fields = AnnotatedFields(raw_response["fields"])

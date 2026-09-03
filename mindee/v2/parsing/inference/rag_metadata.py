from mindee.parsing.common.string_dict import StringDict


class RAGMetadata:
    """Metadata about the RAG operation."""

    retrieved_document_id: str | None
    """The UUID of the matched document used during the RAG operation."""

    def __init__(self, raw_response: StringDict):
        self.retrieved_document_id = raw_response["retrieved_document_id"]

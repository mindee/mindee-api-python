from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class RagMetadata:
    """Metadata about the RAG operation."""

    retrieved_document_id: Optional[str]

    def __init__(self, raw_response: StringDict):
        self.retrieved_document_id = raw_response["retrieved_document_id"]

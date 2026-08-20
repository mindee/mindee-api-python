from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.search.base_search_response import BaseSearchResponse
from mindee.v2.parsing.search.search_rag_documents import SearchRagDocuments


class RagDocumentSearchResponse(BaseSearchResponse):
    """RAG documents search response."""

    rag_documents: SearchRagDocuments
    """Paginated list of matching RAG documents."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.rag_documents = SearchRagDocuments(raw_response["rag_documents"])

    def body_lines(self) -> list[str]:
        """List of strings representing the search response."""
        return ["RAG Documents", "################", str(self.rag_documents)]

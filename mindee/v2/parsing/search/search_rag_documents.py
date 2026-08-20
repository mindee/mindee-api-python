from mindee.v2.parsing.search.search_rag_document import SearchRagDocument


class SearchRagDocuments(list[SearchRagDocument]):
    """List of RAG documents."""

    def __init__(self, raw_response: list[dict]) -> None:
        super().__init__([SearchRagDocument(item) for item in raw_response])

    def __str__(self) -> str:
        """
        Default string representation.
        """
        if len(self) == 0:
            return "\n"

        lines = []
        for rag_document in self:
            lines.append(f"* :ID: {rag_document.id}")
            lines.append(f"  :Model ID: {rag_document.model_id}")
            lines.append(f"  :Filename: {rag_document.filename}")
            lines.append(f"  :Created At: {rag_document.created_at}")
            lines.append(f"  :Total Matches: {rag_document.total_matches}")
            lines.append(f"  :Last Match At: {rag_document.last_match_at}")
            lines.append(f"  :Status: {rag_document.status}")

        return "\n".join(lines) + "\n"

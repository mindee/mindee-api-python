from datetime import datetime

from mindee.parsing.common.string_dict import StringDict


class SearchRagDocument:
    """Individual RAG document information."""

    id: str
    """Unique identifier of the RAG document."""
    model_id: str
    """Model identifier linked to the RAG document."""
    filename: str
    """Original filename of the uploaded document."""
    created_at: datetime
    """Date and time of the document creation."""
    total_matches: int
    """Number of times this document was used in an inference."""
    last_match_at: datetime | None
    """Date and time of the latest matching inference, if any."""
    status: str
    """Current status of the RAG document."""

    def __init__(self, server_response: StringDict) -> None:
        self.id = server_response["id"]
        self.model_id = server_response["model_id"]
        self.filename = server_response["filename"]
        self.created_at = datetime.fromisoformat(
            server_response["created_at"].replace("Z", "+00:00")
        )
        self.total_matches = server_response["total_matches"]
        self.last_match_at = (
            datetime.fromisoformat(
                server_response["last_match_at"].replace("Z", "+00:00")
            )
            if server_response.get("last_match_at")
            else None
        )
        self.status = server_response["status"]

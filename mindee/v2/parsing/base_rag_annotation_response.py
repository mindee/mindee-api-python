from datetime import datetime

from mindee.parsing.common import CommonResponse
from mindee.parsing.common.string_dict import StringDict


class BaseRagAnnotationResponse(CommonResponse):
    """Base class for all RAG document responses from the V2 API."""

    id: str
    """Unique identifier of the RAG document."""
    filename: str
    """Original filename of the uploaded document."""
    created_at: datetime
    """Date and time of the document creation."""
    status: str
    """Current status of the RAG document."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.id = raw_response["id"]
        self.filename = raw_response["filename"]
        self.created_at = datetime.fromisoformat(
            raw_response["created_at"].replace("Z", "+00:00")
        )
        self.status = raw_response["status"]

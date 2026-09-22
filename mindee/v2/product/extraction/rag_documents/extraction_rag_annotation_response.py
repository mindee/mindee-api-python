from datetime import datetime

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.base_rag_annotation_response import BaseRagAnnotationResponse
from mindee.v2.product.extraction.rag_documents.rag_annotation import RagAnnotation


class ExtractionRagAnnotationResponse(BaseRagAnnotationResponse):
    """Response for a RAG document."""

    model_id: str
    """Model identifier linked to the RAG document."""
    total_matches: int
    """Number of times this document was used in an inference."""
    last_match_at: datetime | None = None
    """Date and time of the latest matching inference, if any."""
    annotation: RagAnnotation | None = None
    """Annotation metadata associated with the document."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.model_id = raw_response["model_id"]
        self.total_matches = raw_response["total_matches"]
        if raw_response.get("last_match_at"):
            self.last_match_at = datetime.fromisoformat(
                raw_response["last_match_at"].replace("Z", "+00:00")
            )
        if raw_response.get("annotation"):
            self.annotation = RagAnnotation(raw_response["annotation"])

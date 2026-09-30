import json
from dataclasses import asdict, dataclass
from typing import Any, ClassVar

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.client_options.base_annotation_parameters import BaseAnnotationParameters
from mindee.v2.product.extraction.rag_documents.extraction_rag_annotation_response import (
    ExtractionRagAnnotationResponse,
)
from mindee.v2.product.extraction.rag_documents.rag_annotation import RagAnnotation


@dataclass(kw_only=True)
class RagDocumentAnnotationParameters(
    BaseAnnotationParameters[ExtractionRagAnnotationResponse]
):
    """Annotation parameters for RAG documents."""

    status: str | None = None
    """New public status to apply to the document (for example, to deactivate it)."""

    annotation: RagAnnotation | StringDict | str | None = None
    """Field-level RAG annotation and guidelines configuration for the document."""

    _slug: ClassVar[str] = "extraction"
    _response_class: type[ExtractionRagAnnotationResponse] = (
        ExtractionRagAnnotationResponse
    )

    def __post_init__(self) -> None:
        if isinstance(self.annotation, str):
            self.annotation = RagAnnotation(json.loads(self.annotation))
        elif isinstance(self.annotation, dict):
            self.annotation = RagAnnotation(self.annotation)

    def get_request_parameters(self) -> dict[str, str | StringDict]:
        """Gets the request parameters for the upload request."""
        parameters: dict[str, Any] = {}

        if self.status:
            parameters["status"] = self.status

        if self.annotation is not None and isinstance(self.annotation, RagAnnotation):
            parameters["annotation"] = asdict(self.annotation)

        return parameters

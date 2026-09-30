from dataclasses import dataclass
from typing import ClassVar

from mindee.v2.client_options.base_rag_document_upload_parameters import (
    BaseRagDocumentUploadParameters,
)
from mindee.v2.product.extraction.rag_documents.extraction_rag_annotation_response import (
    ExtractionRagAnnotationResponse,
)


@dataclass(kw_only=True)
class RagDocumentUploadParameters(
    BaseRagDocumentUploadParameters[ExtractionRagAnnotationResponse]
):
    """Upload parameters for RAG documents."""

    _slug: ClassVar[str] = "extraction"
    _response_class: type[ExtractionRagAnnotationResponse] = (
        ExtractionRagAnnotationResponse
    )

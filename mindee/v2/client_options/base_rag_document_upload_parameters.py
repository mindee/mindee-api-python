from abc import ABC
from dataclasses import dataclass
from typing import Generic

from mindee.v2.parsing.base_rag_annotation_response import TypeRagAnnotationResponse


@dataclass(kw_only=True)
class BaseRagDocumentUploadParameters(ABC, Generic[TypeRagAnnotationResponse]):
    """Base parameters for document upload operations."""

    model_id: str
    """UUID of the model that the uploaded RAG document is linked to."""

    close_file: bool = True
    """Whether to close the file after uploading. Default: True."""

    _response_class: type[TypeRagAnnotationResponse]
    """Response class for the annotation."""

    def get_request_parameters(self) -> dict[str, str]:
        """Gets the request parameters for the upload request."""
        return {"model_id": self.model_id}

    def get_response_class(self) -> type[TypeRagAnnotationResponse]:
        """Gets the response class for the search."""
        return self._response_class

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.base_rag_annotation_response import TypeRagAnnotationResponse


@dataclass(kw_only=True)
class BaseAnnotationParameters(ABC, Generic[TypeRagAnnotationResponse]):
    """Base parameters for document annotations."""

    # Note: DocumentId is included in the request URL path, it is not a parameter.
    document_id: str
    """UID of the annotated document."""

    _response_class: type[TypeRagAnnotationResponse]
    """Response class for the annotation."""

    @abstractmethod
    def get_request_parameters(self) -> dict[str, str | StringDict]:
        """Gets the request parameters for the upload request."""

    def get_response_class(self) -> type[TypeRagAnnotationResponse]:
        """Gets the response class for the search."""
        return self._response_class

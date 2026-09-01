from dataclasses import dataclass
from typing import ClassVar

from mindee.v2.client_options.base_search_parameters import BaseSearchParameters
from mindee.v2.search.rag_documents.rag_document_search_response import (
    RagDocumentSearchResponse,
)


@dataclass(kw_only=True)
class RagDocumentSearchParameters(BaseSearchParameters[RagDocumentSearchResponse]):
    """Search parameters for RAG Documents."""

    model_id: str
    """Model identifier to search in."""

    filename: str | None = None
    """Case-insensitive substring search on filename."""

    _slug: ClassVar[str] = "rag-documents"
    _response_class: type[RagDocumentSearchResponse] = RagDocumentSearchResponse

    def __post_init__(self) -> None:
        if not self.model_id:
            raise ValueError("ModelId is required in RagDocumentSearchParameters")

    def get_request_parameters(self) -> dict[str, str | list[str]]:
        params = super().get_request_parameters()

        params["model_id"] = self.model_id

        if self.filename:
            params["filename"] = self.filename

        return params

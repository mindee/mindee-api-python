from abc import ABC
from dataclasses import dataclass


@dataclass(kw_only=True)
class BaseRagDocumentUploadParameters(ABC):
    """Base parameters for document upload operations."""

    model_id: str
    """UUID of the model that the uploaded RAG document is linked to."""

    def get_request_parameters(self) -> dict[str, str]:
        """Gets the request parameters for the upload request."""
        return {"model_id": self.model_id}

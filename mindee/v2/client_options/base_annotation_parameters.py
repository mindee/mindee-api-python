from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(kw_only=True)
class BaseAnnotationParameters(ABC):
    """Base parameters for document annotations."""

    # Note: DocumentId is included in the request URL path, it is not a parameter.
    document_id: str
    """UID of the annotated document."""

    @abstractmethod
    def get_request_parameters(self) -> dict[str, str]:
        """Gets the request parameters for the upload request."""

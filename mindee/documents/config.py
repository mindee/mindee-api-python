from typing import Dict, List, Optional, Tuple, Type

from mindee.documents.base import Document
from mindee.endpoints import API_KEY_ENV_NAME, Endpoint

_docT = Type[Document]


class DocumentConfig:
    """Configuration for a prediction API."""

    document_type: Optional[str]
    endpoints: List[Endpoint]
    document_class: _docT

    def __init__(
        self,
        document_class: _docT,
        endpoints: List[Endpoint],
        document_type: Optional[str] = None,
    ):
        self.document_type = document_type
        self.document_class = document_class
        self.endpoints = endpoints

    def check_api_keys(self) -> None:
        """Raise an exception unless all API keys are present."""
        for endpoint in self.endpoints:
            if not endpoint.api_key:
                raise RuntimeError(
                    (
                        f"Missing API key for '{endpoint.url_name} v{endpoint.version}',"
                        " check your Client configuration.\n"
                        "You can set this using the "
                        f"'{API_KEY_ENV_NAME}' environment variable."
                    )
                )


DocumentConfigDict = Dict[Tuple[str, str], DocumentConfig]

from typing import Dict, List, Tuple

from mindee.documents.base import TypeDocument
from mindee.endpoints import MINDEE_API_KEY_NAME, Endpoint


class DocumentConfig:
    document_type: str
    endpoints: List[Endpoint]
    document_class: TypeDocument

    def __init__(
        self,
        document_type: str,
        constructor: TypeDocument,
        endpoints: List[Endpoint],
    ):
        self.document_type = document_type
        self.document_class = constructor
        self.endpoints = endpoints

    def check_api_keys(self) -> None:
        """Raise an exception unless all API keys are present."""
        for endpoint in self.endpoints:
            if not endpoint.api_key:
                raise RuntimeError(
                    (
                        f"Missing API key for '{self.document_type}',"
                        "check your Client configuration.\n"
                        "You can set this using the "
                        f"'{MINDEE_API_KEY_NAME}' environment variable."
                    )
                )


DocumentConfigDict = Dict[Tuple[str, str], DocumentConfig]

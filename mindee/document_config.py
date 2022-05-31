from typing import Dict, List, Tuple

from mindee.documents.base import TypeDocument
from mindee.endpoints import Endpoint


class DocumentConfig:
    document_type: str
    endpoints: List[Endpoint]
    singular_name: str
    plural_name: str
    constructor: TypeDocument

    def __init__(
        self,
        document_type: str,
        singular_name: str,
        plural_name: str,
        constructor: TypeDocument,
        endpoints: List[Endpoint],
    ):
        self.document_type = document_type
        self.singular_name = singular_name
        self.plural_name = plural_name
        self.constructor = constructor
        self.endpoints = endpoints

    def check_api_keys(self) -> None:
        """Raise an exception unless all API keys are present."""
        for endpoint in self.endpoints:
            if not endpoint.api_key:
                raise RuntimeError(
                    (
                        f"Missing API key for '{endpoint.key_name}',"
                        "check your Client configuration.\n"
                        "You can set this using the "
                        f"'{endpoint.envvar_key_name}' environment variable."
                    )
                )


DocumentConfigDict = Dict[Tuple[str, str], DocumentConfig]

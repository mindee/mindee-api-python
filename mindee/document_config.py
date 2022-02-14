from typing import Dict, List, Any, Type

from mindee.http import Endpoint, API_TYPE_OFF_THE_SHELF, API_TYPE_CUSTOM
from mindee.documents.base import Document
from mindee.documents.custom_document import CustomDocument


class DocumentConfig:
    document_type: str
    api_type: str
    endpoints: List[Endpoint]
    singular_name: str
    plural_name: str

    constructor: Type[Document]

    def __init__(self, config: Dict[str, Any], api_type: str = API_TYPE_CUSTOM):
        """
        :param config: Object containing config
        :param api_type: API_TYPE_OFF_THE_SHELF or API_TYPE_CUSTOM
        """
        self.api_type = api_type
        self._load_config(config)

    def _load_config(self, config):
        # Check for document_type, singular_name and plural_name in config
        for mandatory_field in ("document_type", "singular_name", "plural_name"):
            if mandatory_field not in config.keys():
                raise AssertionError(
                    "%s key is required in custom_document configuration"
                    % mandatory_field
                )
        self.document_type = config["document_type"]
        self.singular_name = config["singular_name"]
        self.plural_name = config["plural_name"]

        if self.api_type == API_TYPE_CUSTOM:
            self.constructor = CustomDocument
            endpoint = Endpoint(
                owner=config["account_name"],
                url_name=config["document_type"],
                version=config["interface_version"],
            )
            if config["api_key"]:
                endpoint.api_key = config["api_key"]
            else:
                endpoint.set_api_key_from_env()
            self.endpoints = [endpoint]

        elif self.api_type == API_TYPE_OFF_THE_SHELF:
            self.constructor = config["constructor"]
            self.endpoints = config["endpoints"]
            for endpoint in self.endpoints:
                endpoint.set_api_key_from_env()

        else:
            raise RuntimeError("Unknown API type")


DocumentConfigDict = Dict[tuple, DocumentConfig]

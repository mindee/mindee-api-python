from typing import Dict, List, Any
from mindee.http import Endpoint, API_TYPE_OFF_THE_SHELF, API_TYPE_CUSTOM
from mindee.documents.custom_document import CustomDocument


class DocumentConfig:
    api_type: str
    endpoints: List[Endpoint]
    singular_name: str
    plural_name: str

    # Workaround for dynamic class assignment and circular import...
    # Will need a refactor at some point.
    constructor: Any

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
        self.singular_name = config["singular_name"]
        self.plural_name = config["plural_name"]

        if self.api_type == API_TYPE_CUSTOM:
            self.constructor = CustomDocument
            try:
                version = config["interface_version"]
            except KeyError:
                version = "1"
            endpoint = Endpoint(
                owner=config["username"],
                url_name=config["document_type"],
                version=version,
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


DocumentConfigDict = Dict[str, DocumentConfig]


def validate_list(doc_configs: DocumentConfigDict):
    """Validate the configuration list definitions."""
    if len(set([v.singular_name for v in doc_configs.values()])) != len(
        [v.singular_name for v in doc_configs.values()]
    ):
        raise AssertionError(
            "singular_name values must be unique among custom_documents list objects"
        )
    if len(set([v.plural_name for v in doc_configs.values()])) != len(
        [v.plural_name for v in doc_configs.values()]
    ):
        raise AssertionError(
            "plural_name values must be unique among custom_documents list objects"
        )

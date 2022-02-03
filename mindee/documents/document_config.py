from typing import Dict, List, Any
from mindee.documents.base import Endpoint, OFF_THE_SHELF, CUSTOM_DOCUMENT
from mindee.documents.custom_document import CustomDocument


class DocumentConfig:
    # Workaround for dynamic class assignment and circular import...
    # Will need a refactor at some point.
    constructor: Any
    type: str
    endpoints: List[Endpoint]
    singular_name: str
    plural_name: str

    def __init__(self, config: Dict[str, Any], doc_type: str = CUSTOM_DOCUMENT):
        """
        :param config: (dict) Object containing config
        :param doc_type: (string) off_the_shelf or custom_document
        """
        self.type = doc_type

        # Check for document_type, singular_name and plural_name in config
        for mandatory_field in ("document_type", "singular_name", "plural_name"):
            if mandatory_field not in config.keys():
                raise AssertionError(
                    "%s key is required in custom_document configuration"
                    % mandatory_field
                )
        self.singular_name = config["singular_name"]
        self.plural_name = config["plural_name"]

        if self.type == CUSTOM_DOCUMENT:
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
            endpoint.api_key = config["api_key"]
            self.endpoints = [endpoint]

        elif self.type == OFF_THE_SHELF:
            self.constructor = config["constructor"]
            self.endpoints = config["endpoints"]
        else:
            raise RuntimeError("Unknown document type")


DocumentConfigDict = Dict[str, DocumentConfig]


def validate_list(config_list: DocumentConfigDict):
    """Validate the configuration list definitions."""
    if len(set([v.singular_name for v in config_list.values()])) != len(
        [v.singular_name for v in config_list.values()]
    ):
        raise AssertionError(
            "singular_name values must be unique among custom_documents list objects"
        )
    if len(set([v.plural_name for v in config_list.values()])) != len(
        [v.plural_name for v in config_list.values()]
    ):
        raise AssertionError(
            "plural_name values must be unique among custom_documents list objects"
        )

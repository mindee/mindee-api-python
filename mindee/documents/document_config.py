from typing import Dict, Any
from mindee.documents.base import OFF_THE_SHELF, CUSTOM_DOCUMENT
from mindee.documents.custom_document import CustomDocument


class DocumentConfig:
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
            # Check for endpoint URL and API Key in config
            for mandatory_field in ("endpoint", "api_key"):
                if mandatory_field not in config.keys():
                    raise AssertionError(
                        "%s key is required in custom_document configuration"
                        % mandatory_field
                    )
            self.constructor = CustomDocument
            self.required_ots_keys = []
            self.api_key = config["api_key"]
            self.endpoint = config["endpoint"]
        elif self.type == OFF_THE_SHELF:
            self.constructor = config["constructor"]
            self.required_ots_keys = config["required_ots_keys"]


DocumentConfigDict = Dict[str, DocumentConfig]


def validate_list(config_list: DocumentConfigDict):
    """Validate the configuration list definitions."""
    if len(set([v.singular_name for k, v in config_list.items()])) != len(
        [v.singular_name for k, v in config_list.items()]
    ):
        raise AssertionError(
            "singular_name values must be unique among custom_documents list objects"
        )
    if len(set([v.plural_name for k, v in config_list.items()])) != len(
        [v.plural_name for k, v in config_list.items()]
    ):
        raise AssertionError(
            "plural_name values must be unique among custom_documents list objects"
        )

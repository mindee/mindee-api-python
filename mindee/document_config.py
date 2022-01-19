from mindee.documents.custom_document import CustomDocument


class DocumentConfig:
    def __init__(self, config, doc_type="custom_document"):
        """
        :param config: (dict) Object containing config
        :param doc_type: (string) off_the_shelf or custom_document
        """
        self.type = doc_type

        # Check for document_type, singular_name and plural_name in config
        for mandatory_field in ["document_type", "singular_name", "plural_name"]:
            if mandatory_field not in config.keys():
                raise AssertionError(
                    "%s key is required in custom_document configuration"
                    % mandatory_field
                )
        self.singular_name = config["singular_name"]
        self.plural_name = config["plural_name"]

        if self.type == "custom_document":
            # Check for endpoint URL and API Key in config
            for mandatory_field in ["endpoint", "api_key"]:
                if mandatory_field not in config.keys():
                    raise AssertionError(
                        "%s key is required in custom_document configuration"
                        % mandatory_field
                    )
            self.constructor = CustomDocument
            self.api_key_kwargs = None
            self.api_key = config["api_key"]
            self.endpoint = config["endpoint"]
        elif self.type == "off_the_shelf":
            self.constructor = config["constructor"]
            self.api_key_kwargs = config["api_key_kwargs"]

    @staticmethod
    def validate_list(config_list):
        """Validate the configuration list definitions."""
        if len(set([v.singular_name for k, v in config_list.items()])) != len(
            [v.singular_name for k, v in config_list.items()]
        ):
            raise AssertionError(
                "singular_name values must be uniques among custom_documents list objects"
            )
        if len(set([v.plural_name for k, v in config_list.items()])) != len(
            [v.plural_name for k, v in config_list.items()]
        ):
            raise AssertionError(
                "plural_name values must be uniques among custom_documents list objects"
            )

from mindee.parsing.common.string_dict import StringDict


class ClassificationClassifier:
    """Document level classification."""

    document_type: str
    """The document type, as identified on given classification values."""

    def __init__(self, server_response: StringDict):
        self.document_type = server_response["document_type"]

    def __str__(self) -> str:
        return f":Document Type: {self.document_type}"

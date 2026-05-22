from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.inference_response import InferenceResponse


class ClassificationClassifier:
    """Document level classification."""

    document_type: str
    """The document type, as identified on given classification values."""

    extraction_response: InferenceResponse
    """The extraction response associated with the classification."""

    def __init__(self, server_response: StringDict):
        self.document_type = server_response["document_type"]
        if server_response.get("extraction_response") is not None:
            self.extraction_response = InferenceResponse(
                server_response["extraction_response"]
            )

    def __str__(self) -> str:
        return f":Document Type: {self.document_type}"

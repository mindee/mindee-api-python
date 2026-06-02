from typing import Generic

from mindee.v1.parsing.common.api_response import ApiResponse, StringDict
from mindee.v1.parsing.common.document import Document
from mindee.v1.parsing.common.inference import TypeInference


class PredictResponse(Generic[TypeInference], ApiResponse):
    """
    Response of a prediction request.

    This is a generic class, so certain class properties depend on the document type.
    """

    document: Document
    """The document object, properly parsed after being retrieved from the server."""

    def __init__(
        self, inference_type: type[TypeInference], raw_response: StringDict
    ) -> None:
        """
        Container for the raw API response and the parsed document.

        :param inference_type: Type of the inference.
        :param raw_response: json response from HTTP call.
        """
        super().__init__(raw_response)
        self.document = Document(inference_type, raw_response["document"])

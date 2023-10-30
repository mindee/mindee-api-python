from typing import Generic, Type

from mindee.parsing.common.api_response import ApiResponse, StringDict
from mindee.parsing.common.document import Document
from mindee.parsing.common.inference import TypeInference


class PredictResponse(Generic[TypeInference], ApiResponse):
    """
    Response of a prediction request.

    This is a generic class, so certain class properties depend on the document type.
    """

    document: Document
    """The document object, properly parsed after being retrieved from the server."""

    def __init__(
        self, prediction_type: Type[TypeInference], raw_response: StringDict
    ) -> None:
        """
        Container for the raw API response and the parsed document.

        :param input_source: Input object
        :param http_response: json response from HTTP call
        """
        super().__init__(raw_response)
        self.document = Document(prediction_type, raw_response["document"])

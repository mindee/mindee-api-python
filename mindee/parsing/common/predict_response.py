from typing import Generic

from mindee.parsing.common.api_response import ApiResponse, StringDict
from mindee.parsing.common.inference import TypeInference


class PredictResponse(ApiResponse[TypeInference]):
    """
    Response of a prediction request.

    This is a generic class, so certain class properties depend on the document type.
    """

    def __init__(self, prediction_type, raw_response: StringDict) -> None:
        """
        Container for the raw API response and the parsed document.

        :param input_source: Input object
        :param http_response: json response from HTTP call
        """
        super().__init__(prediction_type, raw_response)

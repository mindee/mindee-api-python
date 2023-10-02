from typing import Any, Dict, Optional, Union

from mindee.input.sources import LocalInputSource, UrlInputSource
from mindee.parsing.common.api_request import ApiRequest
from mindee.parsing.common.api_response import ApiResponse
from mindee.parsing.common.document import Document
from mindee.parsing.common.job import Job
from mindee.parsing.standard.config import DocumentConfig


class AsyncPredictResponse(ApiResponse):
    """
    Async Response Wrapper class for a Predict response.

    Links a Job to a future PredictResponse.
    """

    job: Job
    """Job object link to the prediction. As long as it isn't complete, the prediction doesn't exist."""
    document: Optional[Document]

    def __init__(
        self,
        prediction_type,
        http_response: Dict[str, Any]
    ) -> None:
        """
        Container wrapper for a raw API response.

        Inherits and instantiates a normal PredictResponse if the parsing of
        the current queue is both requested and done.

        :param doc_config: DocumentConfig
        :param input_source: Input object
        :param http_response: json response from HTTP call
        """
        self.job = Job(http_response["job"])
        if "document" in http_response and http_response["document"]:
            self.document = Document(prediction_type, http_response["document"])

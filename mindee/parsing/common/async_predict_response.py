from typing import Optional

from mindee.parsing.common.api_response import ApiResponse, StringDict
from mindee.parsing.common.document import Document
from mindee.parsing.common.inference import TypeInference
from mindee.parsing.common.job import Job


class AsyncPredictResponse(ApiResponse[TypeInference]):
    """
    Async Response Wrapper class for a Predict response.

    Links a Job to a future PredictResponse.
    """

    job: Job
    """Job object link to the prediction. As long as it isn't complete, the prediction doesn't exist."""

    def __init__(self, prediction_type, raw_response: StringDict) -> None:
        """
        Container wrapper for a raw API response.

        Inherits and instantiates a normal PredictResponse if the parsing of
        the current queue is both requested and done.

        :param input_source: Input object
        :param raw_response: json response from HTTP call
        """
        super().__init__(prediction_type, raw_response)
        self.job = Job(raw_response["job"])

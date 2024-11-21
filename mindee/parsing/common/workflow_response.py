from typing import Generic, Type

from mindee.parsing.common import Inference, StringDict
from mindee.parsing.common.api_response import ApiResponse
from mindee.parsing.common.execution import Execution
from mindee.parsing.common.prediction import TypePrediction


class WorkflowResponse(Generic[TypePrediction], ApiResponse):
    """Base wrapper for API requests."""

    execution: Execution
    """
    Set the prediction model used to parse the document.
    The response object will be instantiated based on this parameter.
    """

    def __init__(self, inference_type: Type[Inference], raw_response: StringDict):
        super().__init__(raw_response)
        self.execution = Execution(inference_type, raw_response["execution"])

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference import BaseInference
from mindee.parsing.v2.inference_active_options import InferenceActiveOptions
from mindee.parsing.v2.inference_result import InferenceResult


class Inference(BaseInference):
    """Inference object for a V2 API return."""

    result: InferenceResult
    """Result of the inference."""
    active_options: InferenceActiveOptions
    """Active options for the inference."""
    _slug: str = "inferences"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict):
        super().__init__(raw_response)
        self.result = InferenceResult(raw_response["result"])
        self.active_options = InferenceActiveOptions(raw_response["active_options"])

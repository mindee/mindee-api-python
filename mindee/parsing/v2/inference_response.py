from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.inference import Inference
from mindee.v2.parsing.inference.base_inference_response import (
    BaseInferenceResponse,
)


class InferenceResponse(BaseInferenceResponse[Inference]):
    """Represent an inference response from Mindee V2 API."""

    inference: Inference
    """Inference result."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = Inference(raw_response["inference"])

    def __str__(self) -> str:
        return str(self.inference)

    def _set_inference_type(self, inference_response: StringDict):
        return Inference

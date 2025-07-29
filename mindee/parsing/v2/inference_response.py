from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.common_response import CommonResponse
from mindee.parsing.v2.inference import Inference


class InferenceResponse(CommonResponse):
    """Represent an inference response from Mindee V2 API."""

    inference: Inference
    """Inference result."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = Inference(raw_response["inference"])

    def __str__(self) -> str:
        return str(self.inference)

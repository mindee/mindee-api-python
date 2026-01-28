from mindee.v2.parsing.inference.base_inference_response import (
    BaseInferenceResponse,
)
from mindee.v2.parsing.inference.split.split_inference import SplitInference


class SplitResponse(BaseInferenceResponse[SplitInference]):
    """Represent a split inference response from Mindee V2 API."""

    inference: SplitInference
    inference_type = SplitInference

    def _set_inference_type(self, inference_response):
        """
        Sets the inference type.

        :param inference_response: Server response.
        """
        return SplitInference(inference_response)

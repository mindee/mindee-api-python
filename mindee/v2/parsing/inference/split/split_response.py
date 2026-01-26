from typing import override

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.base_inference_response import (
    BaseInferenceResponse,
)
from mindee.v2.parsing.inference.split.split_inference import SplitInference


class SplitResponse(BaseInferenceResponse[SplitInference]):
    """Represent a split inference response from Mindee V2 API."""

    @override
    def _set_inference_type(self, inference_response: StringDict):
        """
        Sets the inference type.

        :param inference_response: Server response.
        """
        return SplitInference(inference_response)

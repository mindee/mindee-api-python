from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.utilities.split.split_inference import SplitInference
from mindee.v2.parsing.inference.utilities.utility_response import UtilityResponse


class SplitResponse(UtilityResponse):
    """Represent a split inference response from Mindee V2 API."""

    inference: SplitInference
    """Inference object for split inference."""

    _slug: str = "split"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = SplitInference(raw_response["inference"])

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference import BaseResponse
from mindee.v2.product.split.split_inference import SplitInference


class SplitResponse(BaseResponse):
    """Represent a split inference response from Mindee V2 API."""

    inference: SplitInference
    """Inference object for split inference."""

    _slug: str = "products/split/results"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = SplitInference(raw_response["inference"])

from mindee.parsing.common import StringDict
from mindee.v2.parsing.inference.base_response import BaseResponse
from mindee.v2.product.extraction.inference import Inference


class InferenceResponse(BaseResponse):
    """Represent an inference response from Mindee V2 API."""

    inference: Inference
    """Inference result."""
    _slug: str = "products/extraction/results"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = Inference(raw_response["inference"])

    def __str__(self) -> str:
        return str(self.inference)

    @classmethod
    def get_result_slug(cls) -> str:
        """Getter for the inference slug."""
        return cls._slug

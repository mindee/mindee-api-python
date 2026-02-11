from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference import BaseResponse
from mindee.v2.product.classification.classification_inference import (
    ClassificationInference,
)


class ClassificationResponse(BaseResponse):
    """Represent a classification inference response from Mindee V2 API."""

    inference: ClassificationInference
    """Inference object for classification inference."""

    _slug: str = "products/classification/results"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = ClassificationInference(raw_response["inference"])

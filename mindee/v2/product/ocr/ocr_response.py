from typing import ClassVar

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.base_inference_response import BaseInferenceResponse
from mindee.v2.product.ocr.ocr_inference import OCRInference


class OCRResponse(BaseInferenceResponse):
    """Represent an OCR inference response from Mindee V2 API."""

    inference: OCRInference
    """Inference object for ocr inference."""

    _slug: ClassVar[str] = "products/ocr/results"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = OCRInference(raw_response["inference"])

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.base_inference import BaseInference
from mindee.v2.product.ocr.ocr_result import OCRResult


class OCRInference(BaseInference):
    """OCR inference result."""

    result: OCRResult
    """Result of a ocr inference."""
    _slug: str = "ocr"
    """Slug of the endpoint."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.result = OCRResult(raw_response["result"])

    def __str__(self) -> str:
        return f"Inference\n#########\n{self.model}\n{self.file}\n{self.result}\n"

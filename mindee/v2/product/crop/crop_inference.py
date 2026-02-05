from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.base_inference import BaseInference
from mindee.v2.product.crop.crop_result import CropResult


class CropInference(BaseInference):
    """Crop inference result."""

    result: CropResult
    """Result of a crop inference."""
    _slug: str = "crop"
    """Slug of the endpoint."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.result = CropResult(raw_response["result"])

    def __str__(self) -> str:
        return f"Inference\n#########\n{self.model}\n{self.file}\n{self.result}\n"

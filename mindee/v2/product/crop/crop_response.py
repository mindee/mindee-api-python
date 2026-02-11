from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference import BaseResponse
from mindee.v2.product.crop.crop_inference import CropInference


class CropResponse(BaseResponse):
    """Represent a crop inference response from Mindee V2 API."""

    inference: CropInference
    """Inference object for crop inference."""

    _slug: str = "products/crop/results"
    """Slug of the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = CropInference(raw_response["inference"])

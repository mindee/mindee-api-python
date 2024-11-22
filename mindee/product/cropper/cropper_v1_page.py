from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.position import PositionField
from mindee.product.cropper.cropper_v1_document import (
    CropperV1Document,
)


class CropperV1Page(CropperV1Document):
    """Cropper API version 1.1 page data."""

    cropping: List[PositionField]
    """List of documents found in the image."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Cropper page.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction=raw_prediction, page_id=page_id)
        self.cropping = [
            PositionField(prediction, page_id=page_id)
            for prediction in raw_prediction["cropping"]
        ]

    def __str__(self) -> str:
        cropping = f"\n { ' ' * 18 }".join(
            [str(item) for item in self.cropping],
        )
        out_str: str = f":Document Cropper: {cropping}\n"
        out_str += f"{super().__str__()}"
        return clean_out_string(out_str)

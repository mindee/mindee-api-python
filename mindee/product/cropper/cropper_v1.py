from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.cropper.cropper_v1_document import (
    CropperV1Document,
)
from mindee.product.cropper.cropper_v1_page import (
    CropperV1Page,
)


class CropperV1(Inference):
    """Cropper API version 1 inference prediction."""

    prediction: CropperV1Document
    """Document-level prediction."""
    pages: List[Page[CropperV1Page]]
    """Page-level prediction(s)."""
    endpoint_name = "cropper"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Cropper v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = CropperV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(CropperV1Page, page))

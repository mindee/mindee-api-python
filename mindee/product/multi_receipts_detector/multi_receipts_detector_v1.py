from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.multi_receipts_detector.multi_receipts_detector_v1_document import (
    MultiReceiptsDetectorV1Document,
)


class MultiReceiptsDetectorV1(Inference):
    """Inference prediction for Multi Receipts Detector, API version 1."""

    prediction: MultiReceiptsDetectorV1Document
    """Document-level prediction."""
    pages: List[Page[MultiReceiptsDetectorV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "multi_receipts_detector"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Multi Receipts Detector v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = MultiReceiptsDetectorV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(MultiReceiptsDetectorV1Document, page))

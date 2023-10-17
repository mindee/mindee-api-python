from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.barcode_reader.barcode_reader_v1_document import (
    BarcodeReaderV1Document,
)


class BarcodeReaderV1(Inference):
    """Inference prediction for Barcode Reader, API version 1."""

    prediction: BarcodeReaderV1Document
    """Document-level prediction."""
    pages: List[Page[BarcodeReaderV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "barcode_reader"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Barcode Reader v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = BarcodeReaderV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(BarcodeReaderV1Document, page))

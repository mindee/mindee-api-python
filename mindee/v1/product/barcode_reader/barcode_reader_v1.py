from typing import List

from mindee.v1.parsing.common.inference import Inference
from mindee.v1.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.v1.product.barcode_reader.barcode_reader_v1_document import (
    BarcodeReaderV1Document,
)


class BarcodeReaderV1(Inference):
    """Barcode Reader API version 1 inference prediction."""

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

        :params raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = BarcodeReaderV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(BarcodeReaderV1Document, page))

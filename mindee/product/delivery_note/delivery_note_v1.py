from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.delivery_note.delivery_note_v1_document import (
    DeliveryNoteV1Document,
)


class DeliveryNoteV1(Inference):
    """Delivery note API version 1 inference prediction."""

    prediction: DeliveryNoteV1Document
    """Document-level prediction."""
    pages: List[Page[DeliveryNoteV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "delivery_notes"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Delivery note v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = DeliveryNoteV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(DeliveryNoteV1Document, page))

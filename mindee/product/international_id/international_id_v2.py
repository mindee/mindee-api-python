from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.international_id.international_id_v2_document import (
    InternationalIdV2Document,
)


class InternationalIdV2(Inference):
    """Inference prediction for International ID, API version 2."""

    prediction: InternationalIdV2Document
    """Document-level prediction."""
    pages: List[Page[InternationalIdV2Document]]
    """Page-level prediction(s)."""
    endpoint_name = "international_id"
    """Name of the endpoint."""
    endpoint_version = "2"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        International ID v2 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = InternationalIdV2Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_production = page["prediction"]
            except KeyError:
                continue
            if page_production:
                self.pages.append(Page(InternationalIdV2Document, page))

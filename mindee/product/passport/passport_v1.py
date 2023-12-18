from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.passport.passport_v1_document import PassportV1Document


class PassportV1(Inference):
    """Inference prediction for Passport, API version 1."""

    prediction: PassportV1Document
    """Document-level prediction."""
    pages: List[Page[PassportV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "passport"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Passport v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = PassportV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_production = page["prediction"]
            except KeyError:
                continue
            if page_production:
                self.pages.append(Page(PassportV1Document, page))

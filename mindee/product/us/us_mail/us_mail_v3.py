from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.us.us_mail.us_mail_v3_document import (
    UsMailV3Document,
)


class UsMailV3(Inference):
    """US Mail API version 3 inference prediction."""

    prediction: UsMailV3Document
    """Document-level prediction."""
    pages: List[Page[UsMailV3Document]]
    """Page-level prediction(s)."""
    endpoint_name = "us_mail"
    """Name of the endpoint."""
    endpoint_version = "3"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        US Mail v3 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = UsMailV3Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(UsMailV3Document, page))

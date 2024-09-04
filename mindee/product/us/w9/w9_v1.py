from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.us.w9.w9_v1_document import (
    W9V1Document,
)
from mindee.product.us.w9.w9_v1_page import (
    W9V1Page,
)


class W9V1(Inference):
    """W9 API version 1 inference prediction."""

    prediction: W9V1Document
    """Document-level prediction."""
    pages: List[Page[W9V1Page]]
    """Page-level prediction(s)."""
    endpoint_name = "us_w9"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        W9 v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = W9V1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(W9V1Page, page))

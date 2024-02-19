from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.resume.resume_v1_document import ResumeV1Document


class ResumeV1(Inference):
    """Inference prediction for Resume, API version 1."""

    prediction: ResumeV1Document
    """Document-level prediction."""
    pages: List[Page[ResumeV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "resume"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Resume v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = ResumeV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_production = page["prediction"]
            except KeyError:
                continue
            if page_production:
                self.pages.append(Page(ResumeV1Document, page))

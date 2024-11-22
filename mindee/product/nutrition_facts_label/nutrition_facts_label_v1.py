from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_document import (
    NutritionFactsLabelV1Document,
)


class NutritionFactsLabelV1(Inference):
    """Nutrition Facts Label API version 1 inference prediction."""

    prediction: NutritionFactsLabelV1Document
    """Document-level prediction."""
    pages: List[Page[NutritionFactsLabelV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "nutrition_facts"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Nutrition Facts Label v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = NutritionFactsLabelV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(NutritionFactsLabelV1Document, page))

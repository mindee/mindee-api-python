from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.fr.carte_grise.carte_grise_v1_document import (
    CarteGriseV1Document,
)


class CarteGriseV1(Inference):
    """Carte Grise API version 1 inference prediction."""

    prediction: CarteGriseV1Document
    """Document-level prediction."""
    pages: List[Page[CarteGriseV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "carte_grise"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Carte Grise v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = CarteGriseV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(CarteGriseV1Document, page))

from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.fr.carte_vitale.carte_vitale_v1_document import (
    CarteVitaleV1Document,
)


class CarteVitaleV1(Inference):
    """Carte Vitale API version 1 inference prediction."""

    prediction: CarteVitaleV1Document
    """Document-level prediction."""
    pages: List[Page[CarteVitaleV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "carte_vitale"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Carte Vitale v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = CarteVitaleV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(CarteVitaleV1Document, page))

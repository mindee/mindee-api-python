from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.fr.id_card.id_card_v1_document import (
    IdCardV1Document,
)
from mindee.product.fr.id_card.id_card_v1_page import (
    IdCardV1Page,
)


class IdCardV1(Inference):
    """Carte Nationale d'Identité API version 1 inference prediction."""

    prediction: IdCardV1Document
    """Document-level prediction."""
    pages: List[Page[IdCardV1Page]]
    """Page-level prediction(s)."""
    endpoint_name = "idcard_fr"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Carte Nationale d'Identité v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = IdCardV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(IdCardV1Page, page))

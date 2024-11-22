from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.fr.id_card.id_card_v2_document import (
    IdCardV2Document,
)
from mindee.product.fr.id_card.id_card_v2_page import (
    IdCardV2Page,
)


class IdCardV2(Inference):
    """Carte Nationale d'Identité API version 2 inference prediction."""

    prediction: IdCardV2Document
    """Document-level prediction."""
    pages: List[Page[IdCardV2Page]]
    """Page-level prediction(s)."""
    endpoint_name = "idcard_fr"
    """Name of the endpoint."""
    endpoint_version = "2"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Carte Nationale d'Identité v2 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = IdCardV2Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(IdCardV2Page, page))

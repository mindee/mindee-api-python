from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.proof_of_address.proof_of_address_v1_document import (
    ProofOfAddressV1Document,
)


class ProofOfAddressV1(Inference):
    """Proof of Address API version 1 inference prediction."""

    prediction: ProofOfAddressV1Document
    """Document-level prediction."""
    pages: List[Page[ProofOfAddressV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "proof_of_address"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Proof of Address v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = ProofOfAddressV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(ProofOfAddressV1Document, page))

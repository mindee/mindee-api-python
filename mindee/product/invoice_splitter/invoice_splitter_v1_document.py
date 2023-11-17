from typing import List

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.product.invoice_splitter.invoice_splitter_v1_page_group import (
    InvoiceSplitterV1PageGroup,
)


class InvoiceSplitterV1Document(Prediction):
    """Document data for Invoice Splitter, API version 1."""

    invoice_page_groups: List[InvoiceSplitterV1PageGroup]
    """Page groups linked to an invoice."""

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Invoice Splitter document.

        :param raw_prediction: Raw prediction from HTTP response
        """
        super().__init__(raw_prediction)

        invoice_page_groups = []
        if (
            "invoice_page_groups" in raw_prediction
            and len(raw_prediction["invoice_page_groups"]) > 0
        ):
            for prediction in raw_prediction["invoice_page_groups"]:
                invoice_page_groups.append(InvoiceSplitterV1PageGroup(prediction))
        self.invoice_page_groups = invoice_page_groups

    def __str__(self) -> str:
        page_group_str = ":Invoice Page Groups:"
        for page_group in self.invoice_page_groups:
            page_group_str += f"\n  {str(page_group)}"
        return clean_out_string(page_group_str)

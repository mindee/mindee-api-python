from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.product.invoice_splitter.invoice_splitter_v1_invoice_page_group import (
    InvoiceSplitterV1InvoicePageGroup,
)


class InvoiceSplitterV1Document(Prediction):
    """Invoice Splitter API version 1.4 document data."""

    invoice_page_groups: List[InvoiceSplitterV1InvoicePageGroup]
    """List of page groups. Each group represents a single invoice within a multi-invoice document."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Invoice Splitter document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.invoice_page_groups = [
            InvoiceSplitterV1InvoicePageGroup(prediction, page_id=page_id)
            for prediction in raw_prediction["invoice_page_groups"]
        ]

    @staticmethod
    def _invoice_page_groups_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 74}"
        return out_str + "+"

    def _invoice_page_groups_to_str(self) -> str:
        if not self.invoice_page_groups:
            return ""

        lines = f"\n{self._invoice_page_groups_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.invoice_page_groups]
        )
        out_str = ""
        out_str += f"\n{self._invoice_page_groups_separator('-')}\n "
        out_str += " | Page Indexes                                                            "
        out_str += f" |\n{self._invoice_page_groups_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._invoice_page_groups_separator('-')}"
        return out_str

    def __str__(self) -> str:
        out_str: str = f":Invoice Page Groups: {self._invoice_page_groups_to_str()}\n"
        return clean_out_string(out_str)

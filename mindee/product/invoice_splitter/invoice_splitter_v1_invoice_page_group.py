from typing import Dict, List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class InvoiceSplitterV1InvoicePageGroup(FieldPositionMixin, FieldConfidenceMixin):
    """List of page groups. Each group represents a single invoice within a multi-invoice document."""

    page_indexes: List[int]
    """List of page indexes that belong to the same invoice (group)."""
    page_n: int
    """The document page on which the information was found."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        self._set_confidence(raw_prediction)
        self._set_position(raw_prediction)

        if page_id is None:
            try:
                self.page_n = raw_prediction["page_id"]
            except KeyError:
                pass
        else:
            self.page_n = page_id

        self.page_indexes = raw_prediction["page_indexes"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["page_indexes"] = ", ".join([str(elem) for elem in self.page_indexes])
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["page_indexes"] = ", ".join([str(elem) for elem in self.page_indexes])
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['page_indexes']:<72} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Page Indexes: {printable['page_indexes']}, \n"
        return clean_out_string(out_str)

from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class ReceiptV5LineItem(FieldPositionMixin, FieldConfidenceMixin):
    """List of all line items on the receipt."""

    description: Optional[str]
    """The item description."""
    quantity: Optional[float]
    """The item quantity."""
    total_amount: Optional[float]
    """The item total amount."""
    unit_price: Optional[float]
    """The item unit price."""
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

        self.description = raw_prediction["description"]
        self.quantity = to_opt_float(raw_prediction, "quantity")
        self.total_amount = to_opt_float(raw_prediction, "total_amount")
        self.unit_price = to_opt_float(raw_prediction, "unit_price")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["description"] = format_for_display(self.description)
        out_dict["quantity"] = float_to_string(self.quantity)
        out_dict["total_amount"] = float_to_string(self.total_amount)
        out_dict["unit_price"] = float_to_string(self.unit_price)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["description"] = format_for_display(self.description, 36)
        out_dict["quantity"] = float_to_string(self.quantity)
        out_dict["total_amount"] = float_to_string(self.total_amount)
        out_dict["unit_price"] = float_to_string(self.unit_price)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['description']:<36} | "
        out_str += f"{printable['quantity']:<8} | "
        out_str += f"{printable['total_amount']:<12} | "
        out_str += f"{printable['unit_price']:<10} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Description: {printable['description']}, \n"
        out_str += f"Quantity: {printable['quantity']}, \n"
        out_str += f"Total Amount: {printable['total_amount']}, \n"
        out_str += f"Unit Price: {printable['unit_price']}, \n"
        return clean_out_string(out_str)

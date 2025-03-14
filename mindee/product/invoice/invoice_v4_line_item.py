from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class InvoiceV4LineItem(FieldPositionMixin, FieldConfidenceMixin):
    """List of all the line items present on the invoice."""

    description: Optional[str]
    """The item description."""
    product_code: Optional[str]
    """The product code of the item."""
    quantity: Optional[float]
    """The item quantity"""
    tax_amount: Optional[float]
    """The item tax amount."""
    tax_rate: Optional[float]
    """The item tax rate in percentage."""
    total_amount: Optional[float]
    """The item total amount."""
    unit_measure: Optional[str]
    """The item unit of measure."""
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
        self.product_code = raw_prediction["product_code"]
        self.quantity = to_opt_float(raw_prediction, "quantity")
        self.tax_amount = to_opt_float(raw_prediction, "tax_amount")
        self.tax_rate = to_opt_float(raw_prediction, "tax_rate")
        self.total_amount = to_opt_float(raw_prediction, "total_amount")
        self.unit_measure = raw_prediction["unit_measure"]
        self.unit_price = to_opt_float(raw_prediction, "unit_price")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["description"] = format_for_display(self.description)
        out_dict["product_code"] = format_for_display(self.product_code)
        out_dict["quantity"] = float_to_string(self.quantity)
        out_dict["tax_amount"] = float_to_string(self.tax_amount)
        out_dict["tax_rate"] = float_to_string(self.tax_rate)
        out_dict["total_amount"] = float_to_string(self.total_amount)
        out_dict["unit_measure"] = format_for_display(self.unit_measure)
        out_dict["unit_price"] = float_to_string(self.unit_price)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["description"] = format_for_display(self.description, 36)
        out_dict["product_code"] = format_for_display(self.product_code, None)
        out_dict["quantity"] = float_to_string(self.quantity)
        out_dict["tax_amount"] = float_to_string(self.tax_amount)
        out_dict["tax_rate"] = float_to_string(self.tax_rate)
        out_dict["total_amount"] = float_to_string(self.total_amount)
        out_dict["unit_measure"] = format_for_display(self.unit_measure, None)
        out_dict["unit_price"] = float_to_string(self.unit_price)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['description']:<36} | "
        out_str += f"{printable['product_code']:<12} | "
        out_str += f"{printable['quantity']:<8} | "
        out_str += f"{printable['tax_amount']:<10} | "
        out_str += f"{printable['tax_rate']:<12} | "
        out_str += f"{printable['total_amount']:<12} | "
        out_str += f"{printable['unit_measure']:<15} | "
        out_str += f"{printable['unit_price']:<10} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Description: {printable['description']}, \n"
        out_str += f"Product code: {printable['product_code']}, \n"
        out_str += f"Quantity: {printable['quantity']}, \n"
        out_str += f"Tax Amount: {printable['tax_amount']}, \n"
        out_str += f"Tax Rate (%): {printable['tax_rate']}, \n"
        out_str += f"Total Amount: {printable['total_amount']}, \n"
        out_str += f"Unit of measure: {printable['unit_measure']}, \n"
        out_str += f"Unit Price: {printable['unit_price']}, \n"
        return clean_out_string(out_str)

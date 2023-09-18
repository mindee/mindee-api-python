from typing import Dict, Optional

from mindee.fields.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    TypePrediction,
    float_to_string,
    to_opt_float,
)


class ReceiptV5LineItem(FieldPositionMixin, FieldConfidenceMixin):
    """List of line item details."""

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
        prediction: TypePrediction,
        page_id: Optional[int] = None,
    ):
        self._set_confidence(prediction)
        self._set_position(prediction)

        if page_id is None:
            try:
                self.page_n = prediction["page_id"]
            except KeyError:
                pass
        else:
            self.page_n = page_id

        self.description = prediction["description"]
        self.quantity = to_opt_float(prediction, "quantity")
        self.total_amount = to_opt_float(prediction, "total_amount")
        self.unit_price = to_opt_float(prediction, "unit_price")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        return {
            "description": self.description if self.description is not None else "",
            "quantity": float_to_string(self.quantity),
            "total_amount": float_to_string(self.total_amount),
            "unit_price": float_to_string(self.unit_price),
        }

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._printable_values()
        return (
            "|"
            f" {printable['description']:<36} |"
            f" {printable['quantity']:<8} |"
            f" {printable['total_amount']:<12} |"
            f" {printable['unit_price']:<10} |"
        )

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        return (
            f"Description: {printable['description']}, "
            f"Quantity: {printable['quantity']}, "
            f"Total Amount: {printable['total_amount']}, "
            f"Unit Price: {printable['unit_price']}, "
        ).strip()

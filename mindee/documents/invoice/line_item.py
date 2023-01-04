from typing import Optional

from mindee.fields.base import FieldPositionMixin, TypePrediction, float_to_string


class InvoiceLineItem(FieldPositionMixin):
    product_code: Optional[str]
    """The product code referring to the item."""
    description: Optional[str]
    """The item description."""
    quantity: Optional[float]
    """The item quantity"""
    unit_price: Optional[float]
    """The item unit price."""
    total_amount: Optional[float]
    """The item total amount."""
    tax_rate: Optional[float]
    """The item tax rate in percentage."""
    tax_amount: Optional[float]
    """The item tax amount."""
    confidence: float = 0.0
    """Confidence score"""
    page_n: int
    """The document page on which the information was found."""

    def __init__(
        self,
        prediction: TypePrediction,
        page_n: Optional[int] = None,
    ):
        self._set_position(prediction)

        if page_n is None:
            self.page_n = prediction["page_id"]
        else:
            self.page_n = page_n

        try:
            self.confidence = float(prediction["confidence"])
        except (KeyError, TypeError):
            pass

        def to_opt_float(key: str) -> Optional[float]:
            try:
                return float(prediction[key])
            except TypeError:
                return None

        self.product_code = prediction["product_code"]
        self.description = prediction["description"]
        self.quantity = to_opt_float("quantity")
        self.unit_price = to_opt_float("unit_price")
        self.total_amount = to_opt_float("total_amount")
        self.tax_rate = to_opt_float("tax_rate")
        self.tax_amount = to_opt_float("tax_amount")

    def __str__(self) -> str:
        tax = float_to_string(self.tax_amount)
        if self.tax_rate is not None:
            tax += f" ({float_to_string(self.tax_rate)}%)"

        description = self.description or ""
        if len(description) > 32:
            description = description[:32] + "..."
        row = [
            self.product_code or "",
            float_to_string(self.quantity),
            float_to_string(self.unit_price),
            float_to_string(self.total_amount),
            tax,
            description,
        ]
        return "{:<14} | {:<6} | {:<7} | {:<8} | {:<16} | {} ".format(*row)

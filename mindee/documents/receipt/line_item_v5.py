from typing import Optional

from mindee.fields.base import FieldPositionMixin, TypePrediction, float_to_string


class ReceiptV5LineItem(FieldPositionMixin):
    description: Optional[str]
    """The item description."""
    quantity: Optional[float]
    """The item quantity"""
    unit_price: Optional[float]
    """The item unit price."""
    total_amount: Optional[float]
    """The item total amount."""
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

        self.description = prediction["description"]
        self.quantity = to_opt_float("quantity")
        self.unit_price = to_opt_float("unit_price")
        self.total_amount = to_opt_float("total_amount")

    def __str__(self) -> str:
        description = self.description or ""
        if len(description) > 32:
            description = description[:32] + "..."
        row = [
            float_to_string(self.quantity),
            float_to_string(self.unit_price),
            float_to_string(self.total_amount),
            description,
        ]
        return "| {:<8} | {:<8} | {:<9} | {:<34} |".format(*row)

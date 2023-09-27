from typing import Dict, Optional

from mindee.fields.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    TypePrediction,
    float_to_string,
    to_opt_float,
)


class PetrolReceiptV1Total(FieldPositionMixin, FieldConfidenceMixin):
    """The total amount paid."""

    amount: Optional[float]
    """The amount."""
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

        self.amount = to_opt_float(prediction, "amount")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        return {
            "amount": float_to_string(self.amount),
        }

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        return f"  :Amount Paid: {printable['amount']}"

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        return (f"Amount Paid: {printable['amount']}, ").strip()

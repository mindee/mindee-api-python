from typing import Dict, Optional

from mindee.parsing.common import StringDict, clean_out_string
from mindee.parsing.standard import (
    FieldConfidenceMixin,
    FieldPositionMixin,
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

        self.amount = to_opt_float(raw_prediction, "amount")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["amount"] = float_to_string(self.amount)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Amount Paid: {printable['amount']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Amount Paid: {printable['amount']}, \n"
        return clean_out_string(out_str)

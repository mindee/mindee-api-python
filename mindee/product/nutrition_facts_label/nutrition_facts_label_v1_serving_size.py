from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class NutritionFactsLabelV1ServingSize(FieldPositionMixin, FieldConfidenceMixin):
    """The size of a single serving of the product."""

    amount: Optional[float]
    """The amount of a single serving."""
    unit: Optional[str]
    """The unit for the amount of a single serving."""
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
        self.unit = raw_prediction["unit"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["amount"] = float_to_string(self.amount)
        out_dict["unit"] = format_for_display(self.unit)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Amount: {printable['amount']}\n"
        out_str += f"  :Unit: {printable['unit']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Amount: {printable['amount']}, \n"
        out_str += f"Unit: {printable['unit']}, \n"
        return clean_out_string(out_str)

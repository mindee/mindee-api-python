from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class PayslipV2Pto(FieldPositionMixin, FieldConfidenceMixin):
    """Information about paid time off."""

    accrued_this_period: Optional[float]
    """The amount of paid time off accrued in this period."""
    balance_end_of_period: Optional[float]
    """The balance of paid time off at the end of the period."""
    used_this_period: Optional[float]
    """The amount of paid time off used in this period."""
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

        self.accrued_this_period = to_opt_float(raw_prediction, "accrued_this_period")
        self.balance_end_of_period = to_opt_float(
            raw_prediction, "balance_end_of_period"
        )
        self.used_this_period = to_opt_float(raw_prediction, "used_this_period")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["accrued_this_period"] = float_to_string(self.accrued_this_period)
        out_dict["balance_end_of_period"] = float_to_string(self.balance_end_of_period)
        out_dict["used_this_period"] = float_to_string(self.used_this_period)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Accrued This Period: {printable['accrued_this_period']}\n"
        out_str += f"  :Balance End of Period: {printable['balance_end_of_period']}\n"
        out_str += f"  :Used This Period: {printable['used_this_period']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Accrued This Period: {printable['accrued_this_period']}, \n"
        out_str += f"Balance End of Period: {printable['balance_end_of_period']}, \n"
        out_str += f"Used This Period: {printable['used_this_period']}, \n"
        return clean_out_string(out_str)

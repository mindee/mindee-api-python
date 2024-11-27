from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class PayslipV3PaidTimeOff(FieldPositionMixin, FieldConfidenceMixin):
    """Information about paid time off."""

    accrued: Optional[float]
    """The amount of paid time off accrued in the period."""
    period: Optional[str]
    """The paid time off period."""
    pto_type: Optional[str]
    """The type of paid time off."""
    remaining: Optional[float]
    """The remaining amount of paid time off at the end of the period."""
    used: Optional[float]
    """The amount of paid time off used in the period."""
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

        self.accrued = to_opt_float(raw_prediction, "accrued")
        self.period = raw_prediction["period"]
        self.pto_type = raw_prediction["pto_type"]
        self.remaining = to_opt_float(raw_prediction, "remaining")
        self.used = to_opt_float(raw_prediction, "used")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["accrued"] = float_to_string(self.accrued)
        out_dict["period"] = format_for_display(self.period)
        out_dict["pto_type"] = format_for_display(self.pto_type)
        out_dict["remaining"] = float_to_string(self.remaining)
        out_dict["used"] = float_to_string(self.used)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["accrued"] = float_to_string(self.accrued)
        out_dict["period"] = format_for_display(self.period, 6)
        out_dict["pto_type"] = format_for_display(self.pto_type, 11)
        out_dict["remaining"] = float_to_string(self.remaining)
        out_dict["used"] = float_to_string(self.used)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['accrued']:<9} | "
        out_str += f"{printable['period']:<6} | "
        out_str += f"{printable['pto_type']:<11} | "
        out_str += f"{printable['remaining']:<9} | "
        out_str += f"{printable['used']:<9} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Accrued: {printable['accrued']}, \n"
        out_str += f"Period: {printable['period']}, \n"
        out_str += f"Type: {printable['pto_type']}, \n"
        out_str += f"Remaining: {printable['remaining']}, \n"
        out_str += f"Used: {printable['used']}, \n"
        return clean_out_string(out_str)

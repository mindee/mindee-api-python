from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class PayslipV3SalaryDetail(FieldPositionMixin, FieldConfidenceMixin):
    """Detailed information about the earnings."""

    amount: Optional[float]
    """The amount of the earning."""
    base: Optional[float]
    """The base rate value of the earning."""
    description: Optional[str]
    """The description of the earnings."""
    number: Optional[float]
    """The number of units in the earning."""
    rate: Optional[float]
    """The rate of the earning."""
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
        self.base = to_opt_float(raw_prediction, "base")
        self.description = raw_prediction["description"]
        self.number = to_opt_float(raw_prediction, "number")
        self.rate = to_opt_float(raw_prediction, "rate")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["amount"] = float_to_string(self.amount)
        out_dict["base"] = float_to_string(self.base)
        out_dict["description"] = format_for_display(self.description)
        out_dict["number"] = float_to_string(self.number)
        out_dict["rate"] = float_to_string(self.rate)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["amount"] = float_to_string(self.amount)
        out_dict["base"] = float_to_string(self.base)
        out_dict["description"] = format_for_display(self.description, 36)
        out_dict["number"] = float_to_string(self.number)
        out_dict["rate"] = float_to_string(self.rate)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['amount']:<12} | "
        out_str += f"{printable['base']:<9} | "
        out_str += f"{printable['description']:<36} | "
        out_str += f"{printable['number']:<6} | "
        out_str += f"{printable['rate']:<9} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Amount: {printable['amount']}, \n"
        out_str += f"Base: {printable['base']}, \n"
        out_str += f"Description: {printable['description']}, \n"
        out_str += f"Number: {printable['number']}, \n"
        out_str += f"Rate: {printable['rate']}, \n"
        return clean_out_string(out_str)

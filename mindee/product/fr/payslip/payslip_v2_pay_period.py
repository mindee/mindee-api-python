from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class PayslipV2PayPeriod(FieldPositionMixin, FieldConfidenceMixin):
    """Information about the pay period."""

    end_date: Optional[str]
    """The end date of the pay period."""
    month: Optional[str]
    """The month of the pay period."""
    payment_date: Optional[str]
    """The date of payment for the pay period."""
    start_date: Optional[str]
    """The start date of the pay period."""
    year: Optional[str]
    """The year of the pay period."""
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

        self.end_date = raw_prediction["end_date"]
        self.month = raw_prediction["month"]
        self.payment_date = raw_prediction["payment_date"]
        self.start_date = raw_prediction["start_date"]
        self.year = raw_prediction["year"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["end_date"] = format_for_display(self.end_date)
        out_dict["month"] = format_for_display(self.month)
        out_dict["payment_date"] = format_for_display(self.payment_date)
        out_dict["start_date"] = format_for_display(self.start_date)
        out_dict["year"] = format_for_display(self.year)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :End Date: {printable['end_date']}\n"
        out_str += f"  :Month: {printable['month']}\n"
        out_str += f"  :Payment Date: {printable['payment_date']}\n"
        out_str += f"  :Start Date: {printable['start_date']}\n"
        out_str += f"  :Year: {printable['year']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"End Date: {printable['end_date']}, \n"
        out_str += f"Month: {printable['month']}, \n"
        out_str += f"Payment Date: {printable['payment_date']}, \n"
        out_str += f"Start Date: {printable['start_date']}, \n"
        out_str += f"Year: {printable['year']}, \n"
        return clean_out_string(out_str)

from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class HealthcareCardV1Copay(FieldPositionMixin, FieldConfidenceMixin):
    """Copayments for covered services."""

    service_fees: Optional[float]
    """The price of the service."""
    service_name: Optional[str]
    """The name of the service."""
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

        self.service_fees = to_opt_float(raw_prediction, "service_fees")
        self.service_name = raw_prediction["service_name"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["service_fees"] = float_to_string(self.service_fees)
        out_dict["service_name"] = format_for_display(self.service_name)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["service_fees"] = float_to_string(self.service_fees)
        out_dict["service_name"] = format_for_display(self.service_name, 20)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['service_fees']:<12} | "
        out_str += f"{printable['service_name']:<20} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Service Fees: {printable['service_fees']}, \n"
        out_str += f"Service Name: {printable['service_name']}, \n"
        return clean_out_string(out_str)

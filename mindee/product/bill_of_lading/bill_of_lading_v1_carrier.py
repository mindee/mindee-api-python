from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class BillOfLadingV1Carrier(FieldPositionMixin, FieldConfidenceMixin):
    """The shipping company responsible for transporting the goods."""

    name: Optional[str]
    """The name of the carrier."""
    professional_number: Optional[str]
    """The professional number of the carrier."""
    scac: Optional[str]
    """The Standard Carrier Alpha Code (SCAC) of the carrier."""
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

        self.name = raw_prediction["name"]
        self.professional_number = raw_prediction["professional_number"]
        self.scac = raw_prediction["scac"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["name"] = format_for_display(self.name)
        out_dict["professional_number"] = format_for_display(self.professional_number)
        out_dict["scac"] = format_for_display(self.scac)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Name: {printable['name']}\n"
        out_str += f"  :Professional Number: {printable['professional_number']}\n"
        out_str += f"  :SCAC: {printable['scac']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Name: {printable['name']}, \n"
        out_str += f"Professional Number: {printable['professional_number']}, \n"
        out_str += f"SCAC: {printable['scac']}, \n"
        return clean_out_string(out_str)

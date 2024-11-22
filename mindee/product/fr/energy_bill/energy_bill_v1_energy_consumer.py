from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class EnergyBillV1EnergyConsumer(FieldPositionMixin, FieldConfidenceMixin):
    """The entity that consumes the energy."""

    address: Optional[str]
    """The address of the energy consumer."""
    name: Optional[str]
    """The name of the energy consumer."""
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

        self.address = raw_prediction["address"]
        self.name = raw_prediction["name"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["address"] = format_for_display(self.address)
        out_dict["name"] = format_for_display(self.name)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Address: {printable['address']}\n"
        out_str += f"  :Name: {printable['name']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Address: {printable['address']}, \n"
        out_str += f"Name: {printable['name']}, \n"
        return clean_out_string(out_str)

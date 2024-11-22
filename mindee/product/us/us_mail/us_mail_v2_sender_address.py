from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class UsMailV2SenderAddress(FieldPositionMixin, FieldConfidenceMixin):
    """The address of the sender."""

    city: Optional[str]
    """The city of the sender's address."""
    complete: Optional[str]
    """The complete address of the sender."""
    postal_code: Optional[str]
    """The postal code of the sender's address."""
    state: Optional[str]
    """Second part of the ISO 3166-2 code, consisting of two letters indicating the US State."""
    street: Optional[str]
    """The street of the sender's address."""
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

        self.city = raw_prediction["city"]
        self.complete = raw_prediction["complete"]
        self.postal_code = raw_prediction["postal_code"]
        self.state = raw_prediction["state"]
        self.street = raw_prediction["street"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["city"] = format_for_display(self.city)
        out_dict["complete"] = format_for_display(self.complete)
        out_dict["postal_code"] = format_for_display(self.postal_code)
        out_dict["state"] = format_for_display(self.state)
        out_dict["street"] = format_for_display(self.street)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :City: {printable['city']}\n"
        out_str += f"  :Complete Address: {printable['complete']}\n"
        out_str += f"  :Postal Code: {printable['postal_code']}\n"
        out_str += f"  :State: {printable['state']}\n"
        out_str += f"  :Street: {printable['street']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"City: {printable['city']}, \n"
        out_str += f"Complete Address: {printable['complete']}, \n"
        out_str += f"Postal Code: {printable['postal_code']}, \n"
        out_str += f"State: {printable['state']}, \n"
        out_str += f"Street: {printable['street']}, \n"
        return clean_out_string(out_str)

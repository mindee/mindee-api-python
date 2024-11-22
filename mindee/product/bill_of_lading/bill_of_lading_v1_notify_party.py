from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class BillOfLadingV1NotifyParty(FieldPositionMixin, FieldConfidenceMixin):
    """The party to be notified of the arrival of the goods."""

    address: Optional[str]
    """The address of the notify party."""
    email: Optional[str]
    """The  email of the shipper."""
    name: Optional[str]
    """The name of the notify party."""
    phone: Optional[str]
    """The phone number of the notify party."""
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
        self.email = raw_prediction["email"]
        self.name = raw_prediction["name"]
        self.phone = raw_prediction["phone"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["address"] = format_for_display(self.address)
        out_dict["email"] = format_for_display(self.email)
        out_dict["name"] = format_for_display(self.name)
        out_dict["phone"] = format_for_display(self.phone)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Address: {printable['address']}\n"
        out_str += f"  :Email: {printable['email']}\n"
        out_str += f"  :Name: {printable['name']}\n"
        out_str += f"  :Phone: {printable['phone']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Address: {printable['address']}, \n"
        out_str += f"Email: {printable['email']}, \n"
        out_str += f"Name: {printable['name']}, \n"
        out_str += f"Phone: {printable['phone']}, \n"
        return clean_out_string(out_str)

from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    bool_to_string,
    to_opt_bool,
)


class UsMailV3RecipientAddress(FieldPositionMixin, FieldConfidenceMixin):
    """The addresses of the recipients."""

    city: Optional[str]
    """The city of the recipient's address."""
    complete: Optional[str]
    """The complete address of the recipient."""
    is_address_change: Optional[bool]
    """Indicates if the recipient's address is a change of address."""
    postal_code: Optional[str]
    """The postal code of the recipient's address."""
    private_mailbox_number: Optional[str]
    """The private mailbox number of the recipient's address."""
    state: Optional[str]
    """Second part of the ISO 3166-2 code, consisting of two letters indicating the US State."""
    street: Optional[str]
    """The street of the recipient's address."""
    unit: Optional[str]
    """The unit number of the recipient's address."""
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
        self.is_address_change = to_opt_bool(raw_prediction, "is_address_change")
        self.postal_code = raw_prediction["postal_code"]
        self.private_mailbox_number = raw_prediction["private_mailbox_number"]
        self.state = raw_prediction["state"]
        self.street = raw_prediction["street"]
        self.unit = raw_prediction["unit"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["city"] = format_for_display(self.city)
        out_dict["complete"] = format_for_display(self.complete)
        out_dict["is_address_change"] = bool_to_string(self.is_address_change)
        out_dict["postal_code"] = format_for_display(self.postal_code)
        out_dict["private_mailbox_number"] = format_for_display(
            self.private_mailbox_number
        )
        out_dict["state"] = format_for_display(self.state)
        out_dict["street"] = format_for_display(self.street)
        out_dict["unit"] = format_for_display(self.unit)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["city"] = format_for_display(self.city, 15)
        out_dict["complete"] = format_for_display(self.complete, 35)
        out_dict["is_address_change"] = bool_to_string(self.is_address_change)
        out_dict["postal_code"] = format_for_display(self.postal_code, None)
        out_dict["private_mailbox_number"] = format_for_display(
            self.private_mailbox_number, None
        )
        out_dict["state"] = format_for_display(self.state, None)
        out_dict["street"] = format_for_display(self.street, 25)
        out_dict["unit"] = format_for_display(self.unit, 15)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['city']:<15} | "
        out_str += f"{printable['complete']:<35} | "
        out_str += f"{printable['is_address_change']:<17} | "
        out_str += f"{printable['postal_code']:<11} | "
        out_str += f"{printable['private_mailbox_number']:<22} | "
        out_str += f"{printable['state']:<5} | "
        out_str += f"{printable['street']:<25} | "
        out_str += f"{printable['unit']:<15} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"City: {printable['city']}, \n"
        out_str += f"Complete Address: {printable['complete']}, \n"
        out_str += f"Is Address Change: {printable['is_address_change']}, \n"
        out_str += f"Postal Code: {printable['postal_code']}, \n"
        out_str += f"Private Mailbox Number: {printable['private_mailbox_number']}, \n"
        out_str += f"State: {printable['state']}, \n"
        out_str += f"Street: {printable['street']}, \n"
        out_str += f"Unit: {printable['unit']}, \n"
        return clean_out_string(out_str)

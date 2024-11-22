from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class PayslipV2Employee(FieldPositionMixin, FieldConfidenceMixin):
    """Information about the employee."""

    address: Optional[str]
    """The address of the employee."""
    date_of_birth: Optional[str]
    """The date of birth of the employee."""
    first_name: Optional[str]
    """The first name of the employee."""
    last_name: Optional[str]
    """The last name of the employee."""
    phone_number: Optional[str]
    """The phone number of the employee."""
    registration_number: Optional[str]
    """The registration number of the employee."""
    social_security_number: Optional[str]
    """The social security number of the employee."""
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
        self.date_of_birth = raw_prediction["date_of_birth"]
        self.first_name = raw_prediction["first_name"]
        self.last_name = raw_prediction["last_name"]
        self.phone_number = raw_prediction["phone_number"]
        self.registration_number = raw_prediction["registration_number"]
        self.social_security_number = raw_prediction["social_security_number"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["address"] = format_for_display(self.address)
        out_dict["date_of_birth"] = format_for_display(self.date_of_birth)
        out_dict["first_name"] = format_for_display(self.first_name)
        out_dict["last_name"] = format_for_display(self.last_name)
        out_dict["phone_number"] = format_for_display(self.phone_number)
        out_dict["registration_number"] = format_for_display(self.registration_number)
        out_dict["social_security_number"] = format_for_display(
            self.social_security_number
        )
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Address: {printable['address']}\n"
        out_str += f"  :Date of Birth: {printable['date_of_birth']}\n"
        out_str += f"  :First Name: {printable['first_name']}\n"
        out_str += f"  :Last Name: {printable['last_name']}\n"
        out_str += f"  :Phone Number: {printable['phone_number']}\n"
        out_str += f"  :Registration Number: {printable['registration_number']}\n"
        out_str += f"  :Social Security Number: {printable['social_security_number']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Address: {printable['address']}, \n"
        out_str += f"Date of Birth: {printable['date_of_birth']}, \n"
        out_str += f"First Name: {printable['first_name']}, \n"
        out_str += f"Last Name: {printable['last_name']}, \n"
        out_str += f"Phone Number: {printable['phone_number']}, \n"
        out_str += f"Registration Number: {printable['registration_number']}, \n"
        out_str += f"Social Security Number: {printable['social_security_number']}, \n"
        return clean_out_string(out_str)

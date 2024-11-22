from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class PayslipV2Employer(FieldPositionMixin, FieldConfidenceMixin):
    """Information about the employer."""

    address: Optional[str]
    """The address of the employer."""
    company_id: Optional[str]
    """The company ID of the employer."""
    company_site: Optional[str]
    """The site of the company."""
    naf_code: Optional[str]
    """The NAF code of the employer."""
    name: Optional[str]
    """The name of the employer."""
    phone_number: Optional[str]
    """The phone number of the employer."""
    urssaf_number: Optional[str]
    """The URSSAF number of the employer."""
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
        self.company_id = raw_prediction["company_id"]
        self.company_site = raw_prediction["company_site"]
        self.naf_code = raw_prediction["naf_code"]
        self.name = raw_prediction["name"]
        self.phone_number = raw_prediction["phone_number"]
        self.urssaf_number = raw_prediction["urssaf_number"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["address"] = format_for_display(self.address)
        out_dict["company_id"] = format_for_display(self.company_id)
        out_dict["company_site"] = format_for_display(self.company_site)
        out_dict["naf_code"] = format_for_display(self.naf_code)
        out_dict["name"] = format_for_display(self.name)
        out_dict["phone_number"] = format_for_display(self.phone_number)
        out_dict["urssaf_number"] = format_for_display(self.urssaf_number)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Address: {printable['address']}\n"
        out_str += f"  :Company ID: {printable['company_id']}\n"
        out_str += f"  :Company Site: {printable['company_site']}\n"
        out_str += f"  :NAF Code: {printable['naf_code']}\n"
        out_str += f"  :Name: {printable['name']}\n"
        out_str += f"  :Phone Number: {printable['phone_number']}\n"
        out_str += f"  :URSSAF Number: {printable['urssaf_number']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Address: {printable['address']}, \n"
        out_str += f"Company ID: {printable['company_id']}, \n"
        out_str += f"Company Site: {printable['company_site']}, \n"
        out_str += f"NAF Code: {printable['naf_code']}, \n"
        out_str += f"Name: {printable['name']}, \n"
        out_str += f"Phone Number: {printable['phone_number']}, \n"
        out_str += f"URSSAF Number: {printable['urssaf_number']}, \n"
        return clean_out_string(out_str)

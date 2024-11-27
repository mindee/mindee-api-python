from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class PayslipV3BankAccountDetail(FieldPositionMixin, FieldConfidenceMixin):
    """Information about the employee's bank account."""

    bank_name: Optional[str]
    """The name of the bank."""
    iban: Optional[str]
    """The IBAN of the bank account."""
    swift: Optional[str]
    """The SWIFT code of the bank."""
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

        self.bank_name = raw_prediction["bank_name"]
        self.iban = raw_prediction["iban"]
        self.swift = raw_prediction["swift"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["bank_name"] = format_for_display(self.bank_name)
        out_dict["iban"] = format_for_display(self.iban)
        out_dict["swift"] = format_for_display(self.swift)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Bank Name: {printable['bank_name']}\n"
        out_str += f"  :IBAN: {printable['iban']}\n"
        out_str += f"  :SWIFT: {printable['swift']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Bank Name: {printable['bank_name']}, \n"
        out_str += f"IBAN: {printable['iban']}, \n"
        out_str += f"SWIFT: {printable['swift']}, \n"
        return clean_out_string(out_str)

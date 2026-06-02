from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.v1.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class BankAccountDetailsV2Bban(FieldPositionMixin, FieldConfidenceMixin):
    """Full extraction of BBAN, including: branch code, bank code, account and key."""

    bban_bank_code: str | None
    """The BBAN bank code outputted as a string."""
    bban_branch_code: str | None
    """The BBAN branch code outputted as a string."""
    bban_key: str | None
    """The BBAN key outputted as a string."""
    bban_number: str | None
    """The BBAN Account number outputted as a string."""
    page_n: int
    """The document page on which the information was found."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: int | None = None,
    ):
        self._set_confidence(raw_prediction)
        self._set_position(raw_prediction)

        if page_id is None:
            self.page_n = raw_prediction.get("page_id", 0)
        else:
            self.page_n = page_id

        self.bban_bank_code = raw_prediction["bban_bank_code"]
        self.bban_branch_code = raw_prediction["bban_branch_code"]
        self.bban_key = raw_prediction["bban_key"]
        self.bban_number = raw_prediction["bban_number"]

    def _printable_values(self) -> dict[str, str]:
        """Return values for printing."""
        out_dict: dict[str, str] = {}
        out_dict["bban_bank_code"] = format_for_display(self.bban_bank_code)
        out_dict["bban_branch_code"] = format_for_display(self.bban_branch_code)
        out_dict["bban_key"] = format_for_display(self.bban_key)
        out_dict["bban_number"] = format_for_display(self.bban_number)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Bank Code: {printable['bban_bank_code']}\n"
        out_str += f"  :Branch Code: {printable['bban_branch_code']}\n"
        out_str += f"  :Key: {printable['bban_key']}\n"
        out_str += f"  :Account Number: {printable['bban_number']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Bank Code: {printable['bban_bank_code']}, \n"
        out_str += f"Branch Code: {printable['bban_branch_code']}, \n"
        out_str += f"Key: {printable['bban_key']}, \n"
        out_str += f"Account Number: {printable['bban_number']}, \n"
        return clean_out_string(out_str)

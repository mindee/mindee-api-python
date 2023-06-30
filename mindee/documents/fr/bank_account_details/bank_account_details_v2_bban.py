from typing import Dict, Optional

from mindee.fields.base import FieldConfidenceMixin, FieldPositionMixin, TypePrediction


class BankAccountDetailsV2Bban(FieldPositionMixin, FieldConfidenceMixin):
    """Full extraction of BBAN, including: branch code, bank code, account and key."""

    bban_bank_code: Optional[str]
    """The BBAN bank code outputted as a string."""
    bban_branch_code: Optional[str]
    """The BBAN branch code outputted as a string."""
    bban_key: Optional[str]
    """The BBAN key outputted as a string."""
    bban_number: Optional[str]
    """The BBAN Account number outputted as a string."""
    page_n: int
    """The document page on which the information was found."""

    def __init__(
        self,
        prediction: TypePrediction,
        page_id: Optional[int] = None,
    ):
        self._set_confidence(prediction)
        self._set_position(prediction)

        if page_id is None:
            try:
                self.page_n = prediction["page_id"]
            except KeyError:
                pass
        else:
            self.page_n = page_id

        self.bban_bank_code = prediction["bban_bank_code"]
        self.bban_branch_code = prediction["bban_branch_code"]
        self.bban_key = prediction["bban_key"]
        self.bban_number = prediction["bban_number"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        return {
            "bban_bank_code": self.bban_bank_code
            if self.bban_bank_code is not None
            else "",
            "bban_branch_code": self.bban_branch_code
            if self.bban_branch_code is not None
            else "",
            "bban_key": self.bban_key if self.bban_key is not None else "",
            "bban_number": self.bban_number if self.bban_number is not None else "",
        }

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        return (
            f"  :Bank Code: {printable['bban_bank_code']}\n"
            f"  :Branch Code: {printable['bban_branch_code']}\n"
            f"  :Key: {printable['bban_key']}\n"
            f"  :Account Number: {printable['bban_number']}"
        )

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        return (
            f"Bank Code: {printable['bban_bank_code']}, "
            f"Branch Code: {printable['bban_branch_code']}, "
            f"Key: {printable['bban_key']}, "
            f"Account Number: {printable['bban_number']}, "
        ).strip()

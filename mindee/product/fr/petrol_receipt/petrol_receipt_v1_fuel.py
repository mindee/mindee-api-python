from typing import Dict, Optional

from mindee.parsing.common import StringDict, clean_out_string, format_for_display
from mindee.parsing.standard import FieldConfidenceMixin, FieldPositionMixin


class PetrolReceiptV1Fuel(FieldPositionMixin, FieldConfidenceMixin):
    """The fuel type."""

    category: Optional[str]
    """The fuel category among a list of 4 possible choices."""
    raw_text: Optional[str]
    """As seen on the receipt."""
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

        self.category = raw_prediction["category"]
        self.raw_text = raw_prediction["raw_text"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["category"] = format_for_display(self.category, None)
        out_dict["raw_text"] = format_for_display(self.raw_text, None)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Category: {printable['category']}\n"
        out_str += f"  :Raw Name: {printable['raw_text']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Category: {printable['category']}, \n"
        out_str += f"Raw Name: {printable['raw_text']}, \n"
        return clean_out_string(out_str)

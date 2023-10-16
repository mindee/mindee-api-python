from typing import Dict, Optional

from mindee.parsing.common import StringDict, format_for_display
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
        return {
            "category": format_for_display(self.category, None),
            "raw_text": format_for_display(self.raw_text, None),
        }

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        return (
            f"  :Category: {printable['category']}\n"
            f"  :Raw Name: {printable['raw_text']}"
        )

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        return (
            f"Category: {printable['category']}, "
            f"Raw Name: {printable['raw_text']}, "
        ).strip()

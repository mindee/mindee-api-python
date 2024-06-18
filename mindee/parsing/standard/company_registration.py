from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import format_for_display
from mindee.parsing.standard.base import BaseField, FieldPositionMixin


class CompanyRegistrationField(FieldPositionMixin, BaseField):
    """A company registration item."""

    type: str
    """The type of registration."""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        super().__init__(raw_prediction, value_key, reconstructed, page_id)
        self.type = raw_prediction["type"]
        self._set_position(raw_prediction)

    def to_table_line(self):
        """Return a table line for RST display."""
        printable = self.printable_values()
        return f"| {printable['type']:<15} | {printable['value']:<20} "

    def __str__(self):
        """String representation of CompanyRegistrationField."""
        printable = self.printable_values()
        return f"Type: {printable['type']}, Value: {printable['value']}"

    def printable_values(self):
        """Printable representation of the field's value & type."""
        printable = {
            "type": format_for_display(self.type, None),
            "value": format_for_display(self.value, None),
        }
        return printable

    def print(self) -> str:
        """Additional print function that doesn't overwrite __str__()."""
        if self.value:
            return f"{self.type}: {self.value}"
        return ""

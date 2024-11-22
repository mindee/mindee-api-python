from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class BillOfLadingV1CarrierItem(FieldPositionMixin, FieldConfidenceMixin):
    """The goods being shipped."""

    description: Optional[str]
    """A description of the item."""
    gross_weight: Optional[float]
    """The gross weight of the item."""
    measurement: Optional[float]
    """The measurement of the item."""
    measurement_unit: Optional[str]
    """The unit of measurement for the measurement."""
    quantity: Optional[float]
    """The quantity of the item being shipped."""
    weight_unit: Optional[str]
    """The unit of measurement for weights."""
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

        self.description = raw_prediction["description"]
        self.gross_weight = to_opt_float(raw_prediction, "gross_weight")
        self.measurement = to_opt_float(raw_prediction, "measurement")
        self.measurement_unit = raw_prediction["measurement_unit"]
        self.quantity = to_opt_float(raw_prediction, "quantity")
        self.weight_unit = raw_prediction["weight_unit"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["description"] = format_for_display(self.description)
        out_dict["gross_weight"] = float_to_string(self.gross_weight)
        out_dict["measurement"] = float_to_string(self.measurement)
        out_dict["measurement_unit"] = format_for_display(self.measurement_unit)
        out_dict["quantity"] = float_to_string(self.quantity)
        out_dict["weight_unit"] = format_for_display(self.weight_unit)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["description"] = format_for_display(self.description, 36)
        out_dict["gross_weight"] = float_to_string(self.gross_weight)
        out_dict["measurement"] = float_to_string(self.measurement)
        out_dict["measurement_unit"] = format_for_display(self.measurement_unit, None)
        out_dict["quantity"] = float_to_string(self.quantity)
        out_dict["weight_unit"] = format_for_display(self.weight_unit, None)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['description']:<36} | "
        out_str += f"{printable['gross_weight']:<12} | "
        out_str += f"{printable['measurement']:<11} | "
        out_str += f"{printable['measurement_unit']:<16} | "
        out_str += f"{printable['quantity']:<8} | "
        out_str += f"{printable['weight_unit']:<11} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Description: {printable['description']}, \n"
        out_str += f"Gross Weight: {printable['gross_weight']}, \n"
        out_str += f"Measurement: {printable['measurement']}, \n"
        out_str += f"Measurement Unit: {printable['measurement_unit']}, \n"
        out_str += f"Quantity: {printable['quantity']}, \n"
        out_str += f"Weight Unit: {printable['weight_unit']}, \n"
        return clean_out_string(out_str)

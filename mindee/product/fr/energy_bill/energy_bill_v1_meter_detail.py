from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class EnergyBillV1MeterDetail(FieldPositionMixin, FieldConfidenceMixin):
    """Information about the energy meter."""

    meter_number: Optional[str]
    """The unique identifier of the energy meter."""
    meter_type: Optional[str]
    """The type of energy meter."""
    unit: Optional[str]
    """The unit of power for energy consumption."""
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

        self.meter_number = raw_prediction["meter_number"]
        self.meter_type = raw_prediction["meter_type"]
        self.unit = raw_prediction["unit"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["meter_number"] = format_for_display(self.meter_number)
        out_dict["meter_type"] = format_for_display(self.meter_type)
        out_dict["unit"] = format_for_display(self.unit)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Meter Number: {printable['meter_number']}\n"
        out_str += f"  :Meter Type: {printable['meter_type']}\n"
        out_str += f"  :Unit of Power: {printable['unit']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Meter Number: {printable['meter_number']}, \n"
        out_str += f"Meter Type: {printable['meter_type']}, \n"
        out_str += f"Unit of Power: {printable['unit']}, \n"
        return clean_out_string(out_str)

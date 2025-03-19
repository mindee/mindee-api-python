from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class EnergyBillV1EnergyUsage(FieldPositionMixin, FieldConfidenceMixin):
    """Details of energy consumption."""

    consumption: Optional[float]
    """The price per unit of energy consumed."""
    description: Optional[str]
    """Description or details of the energy usage."""
    end_date: Optional[str]
    """The end date of the energy usage."""
    start_date: Optional[str]
    """The start date of the energy usage."""
    tax_rate: Optional[float]
    """The rate of tax applied to the total cost."""
    total: Optional[float]
    """The total cost of energy consumed."""
    unit: Optional[str]
    """The unit of measurement for energy consumption."""
    unit_price: Optional[float]
    """The price per unit of energy consumed."""
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

        self.consumption = to_opt_float(raw_prediction, "consumption")
        self.description = raw_prediction["description"]
        self.end_date = raw_prediction["end_date"]
        self.start_date = raw_prediction["start_date"]
        self.tax_rate = to_opt_float(raw_prediction, "tax_rate")
        self.total = to_opt_float(raw_prediction, "total")
        self.unit = raw_prediction["unit"]
        self.unit_price = to_opt_float(raw_prediction, "unit_price")

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["consumption"] = float_to_string(self.consumption)
        out_dict["description"] = format_for_display(self.description)
        out_dict["end_date"] = format_for_display(self.end_date)
        out_dict["start_date"] = format_for_display(self.start_date)
        out_dict["tax_rate"] = float_to_string(self.tax_rate)
        out_dict["total"] = float_to_string(self.total)
        out_dict["unit"] = format_for_display(self.unit)
        out_dict["unit_price"] = float_to_string(self.unit_price)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["consumption"] = float_to_string(self.consumption)
        out_dict["description"] = format_for_display(self.description, 36)
        out_dict["end_date"] = format_for_display(self.end_date, 10)
        out_dict["start_date"] = format_for_display(self.start_date, None)
        out_dict["tax_rate"] = float_to_string(self.tax_rate)
        out_dict["total"] = float_to_string(self.total)
        out_dict["unit"] = format_for_display(self.unit, None)
        out_dict["unit_price"] = float_to_string(self.unit_price)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['consumption']:<11} | "
        out_str += f"{printable['description']:<36} | "
        out_str += f"{printable['end_date']:<10} | "
        out_str += f"{printable['start_date']:<10} | "
        out_str += f"{printable['tax_rate']:<8} | "
        out_str += f"{printable['total']:<9} | "
        out_str += f"{printable['unit']:<15} | "
        out_str += f"{printable['unit_price']:<10} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Consumption: {printable['consumption']}, \n"
        out_str += f"Description: {printable['description']}, \n"
        out_str += f"End Date: {printable['end_date']}, \n"
        out_str += f"Start Date: {printable['start_date']}, \n"
        out_str += f"Tax Rate: {printable['tax_rate']}, \n"
        out_str += f"Total: {printable['total']}, \n"
        out_str += f"Unit of Measure: {printable['unit']}, \n"
        out_str += f"Unit Price: {printable['unit_price']}, \n"
        return clean_out_string(out_str)

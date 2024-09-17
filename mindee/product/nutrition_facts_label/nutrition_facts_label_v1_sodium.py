from typing import Dict, Optional

from mindee.parsing.common import StringDict, clean_out_string, format_for_display
from mindee.parsing.standard import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class NutritionFactsLabelV1Sodium(FieldPositionMixin, FieldConfidenceMixin):
    """The amount of sodium in the product."""

    daily_value: Optional[float]
    """DVs are the recommended amounts of sodium to consume or not to exceed each day."""
    per_100g: Optional[float]
    """The amount of sodium per 100g of the product."""
    per_serving: Optional[float]
    """The amount of sodium per serving of the product."""
    unit: Optional[str]
    """The unit of measurement for the amount of sodium."""
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

        self.daily_value = to_opt_float(raw_prediction, "daily_value")
        self.per_100g = to_opt_float(raw_prediction, "per_100g")
        self.per_serving = to_opt_float(raw_prediction, "per_serving")
        self.unit = raw_prediction["unit"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["daily_value"] = float_to_string(self.daily_value)
        out_dict["per_100g"] = float_to_string(self.per_100g)
        out_dict["per_serving"] = float_to_string(self.per_serving)
        out_dict["unit"] = format_for_display(self.unit)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Daily Value: {printable['daily_value']}\n"
        out_str += f"  :Per 100g: {printable['per_100g']}\n"
        out_str += f"  :Per Serving: {printable['per_serving']}\n"
        out_str += f"  :Unit: {printable['unit']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Daily Value: {printable['daily_value']}, \n"
        out_str += f"Per 100g: {printable['per_100g']}, \n"
        out_str += f"Per Serving: {printable['per_serving']}, \n"
        out_str += f"Unit: {printable['unit']}, \n"
        return clean_out_string(out_str)

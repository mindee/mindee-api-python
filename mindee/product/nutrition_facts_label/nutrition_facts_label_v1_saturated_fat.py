from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class NutritionFactsLabelV1SaturatedFat(FieldPositionMixin, FieldConfidenceMixin):
    """The amount of saturated fat in the product."""

    daily_value: Optional[float]
    """DVs are the recommended amounts of saturated fat to consume or not to exceed each day."""
    per_100g: Optional[float]
    """The amount of saturated fat per 100g of the product."""
    per_serving: Optional[float]
    """The amount of saturated fat per serving of the product."""
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

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["daily_value"] = float_to_string(self.daily_value)
        out_dict["per_100g"] = float_to_string(self.per_100g)
        out_dict["per_serving"] = float_to_string(self.per_serving)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Daily Value: {printable['daily_value']}\n"
        out_str += f"  :Per 100g: {printable['per_100g']}\n"
        out_str += f"  :Per Serving: {printable['per_serving']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Daily Value: {printable['daily_value']}, \n"
        out_str += f"Per 100g: {printable['per_100g']}, \n"
        out_str += f"Per Serving: {printable['per_serving']}, \n"
        return clean_out_string(out_str)

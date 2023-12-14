from typing import List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.position import PositionField


class CropperExtra:
    """Contains information on the cropping of a prediction."""

    croppings: List[PositionField]
    """List of all cropping coordinates."""

    def __init__(
        self, raw_prediction: StringDict, page_id: Optional[int] = None
    ) -> None:
        croppings: List[PositionField] = []
        if "cropping" in raw_prediction and raw_prediction["cropping"]:
            for cropping in raw_prediction["cropping"]:
                croppings.append(PositionField(cropping, page_id=page_id))
        self.cropping = croppings

    def __str__(self) -> str:
        return "\n           ".join(map(str, self.cropping))

from typing import Any, Dict, Optional
from mindee.parsing.common.extras import ExtraField
from mindee.parsing.standard.position import PositionField


class CropperExtra(ExtraField):
    """Contains information on the cropping of a prediction."""

    def __init__(
        self, raw_prediction: Dict[str, Any], page_id: Optional[int] = None
    ) -> None:
        super().__init__()
        croppings = []
        if "cropping" in raw_prediction and raw_prediction["cropping"]:
            for cropping in raw_prediction["cropping"]:
                croppings.append(PositionField(cropping, page_id=page_id))
        self.cropping = croppings

    def __str__(self) -> str:
        return "\n           ".join(map(str, self.cropping))

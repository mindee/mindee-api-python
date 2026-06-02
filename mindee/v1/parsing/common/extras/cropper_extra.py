from mindee.parsing.common.string_dict import StringDict
from mindee.v1.parsing.standard.position import PositionField


class CropperExtra:
    """Contains information on the cropping of a prediction."""

    croppings: list[PositionField]
    """List of all cropping coordinates."""

    def __init__(self, raw_prediction: StringDict, page_id: int | None = None) -> None:
        croppings: list[PositionField] = []
        if raw_prediction.get("cropping"):
            for cropping in raw_prediction["cropping"]:
                croppings.append(PositionField(cropping, page_id=page_id))
        self.cropping = croppings

    def __str__(self) -> str:
        return "\n           ".join(map(str, self.cropping))

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.product.crop.crop_item import CropItem


class CropResult:
    """Crop result info."""

    crops: list[CropItem]

    def __init__(self, raw_response: StringDict) -> None:
        self.crops = [CropItem(crop) for crop in raw_response["crops"]]

    def __str__(self) -> str:
        crops = "\n"
        if len(self.crops) > 0:
            crops += "\n".join([str(crop) for crop in self.crops])
        out_str = f"Crops\n====={crops}"
        return out_str

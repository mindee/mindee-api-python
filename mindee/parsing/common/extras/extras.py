from typing import Optional

from mindee.parsing.common.extras.cropper_extra import CropperExtra
from mindee.parsing.common.string_dict import StringDict


class Extras:
    """
    Extras collection wrapper class.

    Is roughly equivalent to a dict of Extras, with a bit more utility.
    """

    cropper: Optional[CropperExtra]

    def __init__(self, raw_prediction: StringDict) -> None:
        if "cropper" in raw_prediction and raw_prediction["cropper"]:
            self.cropper = CropperExtra(raw_prediction["cropper"])
        for key, extra in raw_prediction.items():
            if key != "cropper":
                setattr(self, key, extra)

    def __str__(self) -> str:
        out_str = ""
        for attr in dir(self):
            if not attr.startswith("__"):
                out_str += f":{attr}: {getattr(self, attr)}\n"
        return out_str

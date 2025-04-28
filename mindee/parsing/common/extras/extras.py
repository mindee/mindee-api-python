from typing import Optional

from mindee.parsing.common.extras.cropper_extra import CropperExtra
from mindee.parsing.common.extras.full_text_ocr_extra import FullTextOcrExtra
from mindee.parsing.common.extras.rag_extra import RagExtra
from mindee.parsing.common.string_dict import StringDict


class Extras:
    """
    Extras collection wrapper class.

    Is roughly equivalent to a dict of Extras, with a bit more utility.
    """

    cropper: Optional[CropperExtra] = None
    full_text_ocr: Optional[FullTextOcrExtra] = None
    rag: Optional[RagExtra] = None

    def __init__(self, raw_prediction: StringDict) -> None:
        if "cropper" in raw_prediction and raw_prediction["cropper"]:
            self.cropper = CropperExtra(raw_prediction["cropper"])
        if "full_text_ocr" in raw_prediction and raw_prediction["full_text_ocr"]:
            self.full_text_ocr = FullTextOcrExtra(raw_prediction["full_text_ocr"])
        if "rag" in raw_prediction and raw_prediction["rag"]:
            self.rag = RagExtra(raw_prediction["rag"])
        for key, extra in raw_prediction.items():
            if key not in ["cropper", "full_text_ocr", "rag"]:
                setattr(self, key, extra)

    def __str__(self) -> str:
        out_str = ""
        for attr in dir(self):
            if not attr.startswith("__"):
                out_str += f":{attr}: {getattr(self, attr)}\n"
        return out_str

    def add_artificial_extra(self, raw_prediction: StringDict):
        """
        Adds artificial extra data for reconstructed extras. Currently only used for full_text_ocr.

        :param raw_prediction: Raw prediction used by the document.
        """
        if "full_text_ocr" in raw_prediction and raw_prediction["full_text_ocr"]:
            self.full_text_ocr = FullTextOcrExtra(raw_prediction["full_text_ocr"])

from mindee.parsing.common.string_dict import StringDict
from mindee.v1.parsing.common.extras.cropper_extra import CropperExtra
from mindee.v1.parsing.common.extras.full_text_ocr_extra import FullTextOCRExtra
from mindee.v1.parsing.common.extras.rag_extra import RAGExtra


class Extras:
    """
    Extras collection wrapper class.

    Is roughly equivalent to a dict of Extras, with a bit more utility.
    """

    cropper: CropperExtra | None = None
    full_text_ocr: FullTextOCRExtra | None = None
    rag: RAGExtra | None = None

    def __init__(self, raw_prediction: StringDict) -> None:
        if raw_prediction.get("cropper"):
            self.cropper = CropperExtra(raw_prediction["cropper"])
        if raw_prediction.get("full_text_ocr"):
            self.full_text_ocr = FullTextOCRExtra(raw_prediction["full_text_ocr"])
        if raw_prediction.get("rag"):
            self.rag = RAGExtra(raw_prediction["rag"])
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
        if raw_prediction.get("full_text_ocr"):
            self.full_text_ocr = FullTextOCRExtra(raw_prediction["full_text_ocr"])

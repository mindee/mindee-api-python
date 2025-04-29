import datetime
from typing import Any, Generic, Optional, Type

from mindee.parsing.common.extras.extras import Extras
from mindee.parsing.common.inference import Inference
from mindee.parsing.common.ocr.ocr import Ocr
from mindee.parsing.common.page import TypePage
from mindee.parsing.common.prediction import TypePrediction
from mindee.parsing.common.string_dict import StringDict


def serialize_for_json(obj: Any) -> Any:
    """
    Custom serializer for Document objects.

    Use as the `default` argument of the `json.dump` functions.
    """
    if isinstance(obj, datetime.date):
        return str(obj)
    return vars(obj)


class Document(Generic[TypePrediction, TypePage]):
    """Base class for all predictions."""

    filename: str
    """Name of the input document"""
    inference: Inference[TypePrediction, TypePage]
    """Result of the base inference"""
    id: str
    """Id of the document as sent back by the server"""
    extras: Optional[Extras] = None
    """Potential Extras fields sent back along the prediction"""
    ocr: Optional[Ocr] = None
    """Potential raw text results read by the OCR (limited feature)"""
    n_pages: int
    """Amount of pages in the document"""

    def __init__(
        self,
        inference_type: Type[Inference],
        raw_response: StringDict,
    ):
        self.id = raw_response.get("id", "")
        self.filename = raw_response.get("name", "")
        if "ocr" in raw_response and raw_response["ocr"]:
            self.ocr = Ocr(raw_response["ocr"])
        if "extras" in raw_response and raw_response["inference"]["extras"]:
            self.extras = Extras(raw_response["extras"])
        self._inject_full_text_ocr(raw_response)
        self.inference = inference_type(raw_response["inference"])
        self.n_pages = raw_response["n_pages"]

    def __str__(self) -> str:
        return (
            f"########\nDocument\n########\n"
            f":Mindee ID: {self.id}\n"
            f":Filename: {self.filename}\n\n"
            f"{self.inference}"
        )

    def _inject_full_text_ocr(self, raw_prediction: StringDict) -> None:
        pages = raw_prediction.get("inference", {}).get("pages", [])

        # check for: empty, missing, or null
        if (
            not pages
            or not pages[0].get("extras", None)
            or not pages[0]["extras"].get("full_text_ocr", None)
        ):
            return

        full_text_content = "\n".join(
            page["extras"]["full_text_ocr"]["content"]
            for page in pages
            if page.get("extras", None) and page["extras"].get("full_text_ocr", None)
        )

        artificial_text_obj = {"content": full_text_content}

        if not hasattr(self, "extras") or not self.extras:
            self.extras = Extras({"full_text_ocr": artificial_text_obj})
        else:
            self.extras.add_artificial_extra({"full_text_ocr": artificial_text_obj})

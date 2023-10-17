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
    extras: Optional[Extras]
    """Potential Extras fields sent back along the prediction"""
    ocr: Optional[Ocr]

    def __init__(
        self,
        prediction_type: Type[Inference],
        raw_response: StringDict,
    ):
        self.id = raw_response.get("id", "")
        self.filename = raw_response.get("name", "")
        if "ocr" in raw_response and raw_response["ocr"]:
            self.ocr = Ocr(raw_response["ocr"])
        if "extras" in raw_response and raw_response["extras"]:
            self.extras = Extras(raw_response["extras"])
        self.inference = prediction_type(raw_response["inference"])

    def __str__(self) -> str:
        return (
            f"########\nDocument\n########\n"
            f":Mindee ID: {self.id}\n"
            f":Filename: {self.filename}\n\n"
            f"{self.inference}"
        )

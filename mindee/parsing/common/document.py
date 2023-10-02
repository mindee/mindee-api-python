import datetime
from typing import Any, Dict, List, Generic, Optional, TypeVar, Union

from mindee.http.endpoints import Endpoint
from mindee.input.sources import LocalInputSource, UrlInputSource
from mindee.parsing.common.extras.cropper_extra import CropperExtra
from mindee.parsing.common.extras.extras import ExtraField, Extras
from mindee.parsing.common.ocr import Ocr
from mindee.parsing.common.prediction import Prediction, TypePrediction


def serialize_for_json(obj: Any) -> Any:
    """
    Custom serializer for Document objects.

    Use as the `default` argument of the `json.dump` functions.
    """
    if isinstance(obj, datetime.date):
        return str(obj)
    return vars(obj)


class Document(Generic[TypePrediction]):
    """Base class for all predictions."""

    filename: str
    """Name of the input document"""
    inference: Prediction
    """Result of the base inference"""
    id: str
    """Id of the document as sent back by the server"""
    extras: Optional[Extras]
    """Potential Extras fields sent back along the prediction"""
    ocr: Optional[Ocr]

    def __init__(
        self,
        prediction_type,
        raw_response: Dict[str, Any],
    ):
        self.id = raw_response.get("id", "")
        self.filename = raw_response.get("name", "")
        if "ocr" in raw_response and raw_response["ocr"]:
            self.ocr = Ocr(raw_response["ocr"])
        extras: Dict[str, ExtraField] = dict()
        if "extras" in raw_response and raw_response["extras"]:
            for key, extra in raw_response["extras"].items():
                if key == "cropper":
                    extras["cropper"] = CropperExtra(extra)
        self.extras = Extras(extras)
        self.inference = prediction_type(raw_response)



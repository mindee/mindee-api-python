from typing import Any, Dict, Generic, Optional

from mindee.parsing.common.extras.cropper_extra import CropperExtra
from mindee.parsing.common.extras.extras import ExtraField, Extras
from mindee.parsing.common.orientation import OrientationField
from mindee.parsing.common.prediction import Prediction, TypePrediction


class Page(Generic[TypePrediction]):
    """Base Page object for predictions."""

    page_id: int
    """Id of the current page."""
    orientation: Optional[OrientationField]
    """Orientation of the page"""
    prediction: Prediction
    """Type of Page prediction."""
    extras: Optional[Extras]

    def __init__(
        self,
        prediction_type,
        raw_prediction: Dict[str, Any],
        page_id: int,
        orientation: Optional[Dict[str, Any]],
    ) -> None:
        if orientation is not None:
            self.orientation = OrientationField(orientation, page_id=page_id)
        self.page_id = page_id
        klass = prediction_type.__class__
        self.prediction = klass(raw_prediction["prediction"], page_id)
        extras: Dict[str, ExtraField] = dict()
        if "extras" in raw_prediction and raw_prediction["extras"]:
            for key, extra in raw_prediction["extras"].items():
                if key == "cropper":
                    extras["cropper"] = CropperExtra(extra)
        self.extras = Extras(extras)

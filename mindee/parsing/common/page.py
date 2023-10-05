from typing import Generic, Optional, TypeVar

from mindee.parsing.common.extras.extras import Extras
from mindee.parsing.common.orientation import OrientationField
from mindee.parsing.common.prediction import Prediction, TypePrediction
from mindee.parsing.common.string_dict import StringDict


class Page(Generic[TypePrediction]):
    """Base Page object for predictions."""

    id: int
    """Id of the current page."""
    orientation: Optional[OrientationField]
    """Orientation of the page"""
    prediction: Prediction
    """Type of Page prediction."""
    extras: Optional[Extras]

    def __init__(
        self,
        prediction_type,
        raw_prediction: StringDict,
        page_id: int,
        orientation: Optional[StringDict],
    ) -> None:
        if orientation is not None:
            self.orientation = OrientationField(orientation, page_id=page_id)
        self.id = page_id
        self.prediction = prediction_type(raw_prediction["prediction"], page_id)
        if "extras" in raw_prediction and raw_prediction["extras"]:
            self.extras = Extras(raw_prediction["extras"])

    def __str__(self) -> str:
        title = f"Page {self.id}"
        dashes = "-" * len(title)
        return f"{title}\n" f"{dashes}\n" f"{self.prediction}"


TypePage = TypeVar("TypePage", bound=Page)

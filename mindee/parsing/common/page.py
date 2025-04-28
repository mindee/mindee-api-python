from typing import Generic, Optional, Type, TypeVar

from mindee.parsing.common.extras.extras import Extras
from mindee.parsing.common.orientation import OrientationField
from mindee.parsing.common.prediction import TypePrediction
from mindee.parsing.common.string_dict import StringDict


class Page(Generic[TypePrediction]):
    """Base Page object for predictions."""

    id: int
    """Id of the current page."""
    orientation: Optional[OrientationField] = None
    """Orientation of the page"""
    prediction: TypePrediction
    """Type of Page prediction."""
    extras: Optional[Extras] = None

    def __init__(
        self,
        prediction_type: Type[TypePrediction],
        raw_prediction: StringDict,
    ) -> None:
        self.id = raw_prediction["id"]
        if (
            "orientation" in raw_prediction
            and raw_prediction["orientation"] is not None
        ):
            self.orientation = OrientationField(
                raw_prediction["orientation"], page_id=self.id
            )
        try:
            self.prediction = prediction_type(raw_prediction["prediction"], self.id)
        except TypeError:
            self.prediction = prediction_type(raw_prediction["prediction"])

        if "extras" in raw_prediction and raw_prediction["extras"]:
            self.extras = Extras(raw_prediction["extras"])

    def __str__(self) -> str:
        title = f"Page {self.id}"
        dashes = "-" * len(title)
        return f"{title}\n" f"{dashes}\n" f"{self.prediction}\n"


TypePage = TypeVar("TypePage", bound=Page)

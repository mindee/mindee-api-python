from typing import Optional

from mindee.fields.base import Field, TypePrediction
from mindee.geometry import Polygon, Quadrilateral


class Position(Field):
    value: Polygon = []
    quadrangle: Optional[Quadrilateral]
    rectangle: Optional[Quadrilateral]
    bounding_box: Optional[Quadrilateral]

    def __init__(
        self,
        position_prediction: TypePrediction,
        value_key: str = "polygon",
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Amount field object.

        :param position_prediction: Position prediction object from HTTP response
        :param value_key: Key to use in the position_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page PDF
        """
        super().__init__(
            position_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )
        try:
            self.value = position_prediction[value_key]
            self.bounding_box = (
                position_prediction["bounding_box"]
                if "bounding_box" in position_prediction.keys()
                else None
            )
            self.quadrangle = (
                position_prediction["quadrangle"]
                if "quadrangle" in position_prediction.keys()
                else None
            )
            self.polygon = (
                position_prediction["polygon"]
                if "polygon" in position_prediction.keys()
                else None
            )
            self.rectangle = (
                position_prediction["rectangle"]
                if "rectangle" in position_prediction.keys()
                else None
            )
        except (ValueError, TypeError, KeyError):
            self.value = []
            self.confidence = 0.0

from typing import Optional

from mindee.fields.base import BaseField, TypePrediction
from mindee.geometry import (
    GeometryError,
    Polygon,
    Quadrilateral,
    polygon_from_prediction,
    quadrilateral_from_prediction,
)


class Position(BaseField):
    value: Optional[Polygon] = None
    polygon: Optional[Polygon] = None
    quadrangle: Optional[Quadrilateral] = None
    rectangle: Optional[Quadrilateral] = None
    bounding_box: Optional[Quadrilateral] = None

    def __init__(
        self,
        prediction: TypePrediction,
        value_key: str = "polygon",
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Position field object.

        :param prediction: Position prediction object from HTTP response
        :param value_key: Key to use in the position_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page document
        """
        super().__init__(
            prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )

        def get_quadrilateral(key: str) -> Optional[Quadrilateral]:
            try:
                return quadrilateral_from_prediction(prediction[key])
            except (KeyError, GeometryError):
                return None

        def get_polygon(key: str) -> Optional[Polygon]:
            try:
                return polygon_from_prediction(prediction[key])
            except (KeyError, GeometryError):
                return None

        self.bounding_box = get_quadrilateral("bounding_box")
        self.quadrangle = get_quadrilateral("quadrangle")
        self.rectangle = get_quadrilateral("rectangle")
        self.polygon = get_polygon("polygon")

        self.value = self.polygon

from typing import Optional

from mindee.fields.base import BaseField, TypePrediction
from mindee.geometry import (
    GeometryError,
    Polygon,
    Quadrilateral,
    polygon_from_prediction,
    quadrilateral_from_prediction,
)


class PositionField(BaseField):
    value: Optional[Polygon] = None
    """Polygon of cropped area, identical to the ``polygon`` property."""
    polygon: Optional[Polygon] = None
    """Polygon of cropped area"""
    quadrangle: Optional[Quadrilateral] = None
    """Quadrangle of cropped area (does not exceed the canvas)"""
    rectangle: Optional[Quadrilateral] = None
    """Oriented rectangle of cropped area (may exceed the canvas)"""
    bounding_box: Optional[Quadrilateral] = None
    """Straight rectangle of cropped area (does not exceed the canvas)"""

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

    def __str__(self) -> str:
        if self.polygon is None:
            return ""
        return f"Polygon with {len(self.polygon)} points."

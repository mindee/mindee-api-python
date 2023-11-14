from typing import Optional

from mindee.error.geometry_error import GeometryError
from mindee.geometry.polygon import Polygon, polygon_from_prediction
from mindee.geometry.quadrilateral import Quadrilateral, quadrilateral_from_prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import BaseField


class PositionField(BaseField):
    """A field indicating a position or area on the document."""

    value: Optional[Polygon]
    """Polygon of cropped area, identical to the ``polygon`` property."""
    polygon: Optional[Polygon]
    """Polygon of cropped area"""
    quadrangle: Optional[Quadrilateral]
    """Quadrangle of cropped area (does not exceed the canvas)"""
    rectangle: Optional[Quadrilateral]
    """Oriented rectangle of cropped area (may exceed the canvas)"""
    bounding_box: Optional[Quadrilateral]
    """Straight rectangle of cropped area (does not exceed the canvas)"""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "polygon",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Position field object.

        :param raw_prediction: Position prediction object from HTTP response
        :param value_key: Key to use in the position_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        super().__init__(
            raw_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_id=page_id,
        )

        def get_quadrilateral(key: str) -> Optional[Quadrilateral]:
            try:
                return quadrilateral_from_prediction(raw_prediction[key])
            except (KeyError, GeometryError):
                return None

        def get_polygon(key: str) -> Optional[Polygon]:
            try:
                polygon = raw_prediction[key]
            except KeyError:
                return None
            if not polygon:
                return None
            try:
                return polygon_from_prediction(polygon)
            except GeometryError:
                return None

        self.bounding_box = get_quadrilateral("bounding_box")
        self.quadrangle = get_quadrilateral("quadrangle")
        self.rectangle = get_quadrilateral("rectangle")
        self.polygon = get_polygon("polygon")

        self.value = self.polygon

    def __str__(self) -> str:
        if self.polygon:
            return f"Polygon with {len(self.polygon)} points."
        if self.bounding_box:
            return f"Polygon with {len(self.bounding_box)} points."
        if self.rectangle:
            return f"Polygon with {len(self.rectangle)} points."
        if self.quadrangle:
            return f"Polygon with {len(self.quadrangle)} points."
        return ""

from mindee.error.geometry_error import MindeeGeometryError
from mindee.geometry.polygon import Polygon
from mindee.geometry.quadrilateral import Quadrilateral, quadrilateral_from_prediction
from mindee.parsing.common import StringDict
from mindee.v1.parsing.standard.base import BaseField


class PositionField(BaseField):
    """A field indicating a position or area on the document."""

    value: Polygon | None
    """Polygon of cropped area, identical to the ``polygon`` property."""
    polygon: Polygon | None
    """Polygon of cropped area"""
    quadrangle: Quadrilateral | None
    """Quadrangle of cropped area (does not exceed the canvas)"""
    rectangle: Quadrilateral | None
    """Oriented rectangle of cropped area (may exceed the canvas)"""
    bounding_box: Quadrilateral | None
    """Straight rectangle of cropped area (does not exceed the canvas)"""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "polygon",
        reconstructed: bool = False,
        page_id: int | None = None,
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

        def get_quadrilateral(key: str) -> Quadrilateral | None:
            try:
                return quadrilateral_from_prediction(raw_prediction[key])
            except (KeyError, MindeeGeometryError):
                return None

        def get_polygon(key: str) -> Polygon | None:
            try:
                polygon = raw_prediction[key]
            except KeyError:
                return None
            if not polygon:
                return None
            try:
                return Polygon(polygon)
            except MindeeGeometryError:
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

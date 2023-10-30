from typing import NamedTuple, Sequence

from mindee.error.geometry_error import GeometryError
from mindee.geometry.bbox import get_bbox
from mindee.geometry.point import Point, Points
from mindee.geometry.polygon_utils import get_centroid


class Quadrilateral(NamedTuple):
    """Contains exactly 4 relative vertices coordinates (Points)."""

    top_left: Point
    """Top left Point"""
    top_right: Point
    """Top right Point"""
    bottom_right: Point
    """Bottom right Point"""
    bottom_left: Point
    """Bottom left Point"""

    @property
    def centroid(self) -> Point:
        """The central point (centroid) of the quadrilateral."""
        return get_centroid(self)


def quadrilateral_from_prediction(prediction: Sequence[list]) -> Quadrilateral:
    """
    Transform a prediction into a Quadrilateral.

    :param prediction: API prediction.
    """
    if len(prediction) != 4:
        raise GeometryError("Prediction must have exactly 4 points")
    return Quadrilateral(
        Point(prediction[0][0], prediction[0][1]),
        Point(prediction[1][0], prediction[1][1]),
        Point(prediction[2][0], prediction[2][1]),
        Point(prediction[3][0], prediction[3][1]),
    )


def get_bounding_box(points: Points) -> Quadrilateral:
    """
    Given a sequence of points, calculate a bounding box that encompasses all points.

    :param points: Polygon to process.
    :return: A bounding box that encompasses all points.
    """
    x_min, y_min, x_max, y_max = get_bbox(points)
    return Quadrilateral(
        Point(x_min, y_min),
        Point(x_max, y_min),
        Point(x_max, y_max),
        Point(x_min, y_max),
    )

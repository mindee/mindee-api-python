from typing import Sequence

from mindee.geometry.minmax import get_min_max_x, get_min_max_y
from mindee.geometry.point import Point
from mindee.geometry.polygon_utils import get_centroid, is_point_in_x, is_point_in_y


class Polygon(list):
    """
    Contains any number of vertex coordinates (Points).

    Inherits from base class ``list`` so is compatible with type ``Points``.
    """

    @property
    def centroid(self) -> Point:
        """The central point (centroid) of the polygon."""
        return get_centroid(self)


def is_point_in_polygon_x(point: Point, polygon: Polygon) -> bool:
    """
    Determine if the Point is in the Polygon's X-axis.

    :param point: Point to compare
    :param polygon: Polygon to look into
    """
    min_x, max_x = get_min_max_x(polygon)
    return is_point_in_x(point, min_x, max_x)


def is_point_in_polygon_y(point: Point, polygon: Polygon) -> bool:
    """
    Determine if the Point is in the Polygon's Y-axis.

    :param point: Point to compare
    :param polygon: Polygon to look into
    """
    min_y, max_y = get_min_max_y(polygon)
    return is_point_in_y(point, min_y, max_y)


def polygon_from_prediction(prediction: Sequence[list]) -> Polygon:
    """
    Transform a prediction into a Polygon.

    :param prediction: API prediction.
    """
    return Polygon(Point(point[0], point[1]) for point in prediction)


def merge_polygons(vertices: Sequence[Polygon]) -> Polygon:
    """
    Given a sequence of polygons, calculate a polygon box that encompasses all polygons.

    :param vertices: List of polygons
    :return: A bounding box that encompasses all polygons
    """
    y_min = min(y for v in vertices for _, y in v)
    y_max = max(y for v in vertices for _, y in v)
    x_min = min(x for v in vertices for x, _ in v)
    x_max = max(x for v in vertices for x, _ in v)
    return Polygon(
        [
            Point(x_min, y_min),
            Point(x_max, y_min),
            Point(x_max, y_max),
            Point(x_min, y_max),
        ]
    )

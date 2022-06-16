"""Pure Python geometry functions for working with polygons."""

from typing import Sequence, Tuple

Point = Tuple[float, float]
Polygon = Sequence[Point]
BoundingBox = Tuple[float, float, float, float]
Quadrilateral = Tuple[Point, Point, Point, Point]


def get_bbox_as_polygon(polygon: Polygon) -> Quadrilateral:
    """
    Given a sequence of points, calculate a polygon that encompasses all points.

    :param polygon: Sequence of ``Point``
    :return: Quadrilateral
    """
    x_min, y_min, x_max, y_max = get_bbox(polygon)
    return (x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)


def get_bbox(polygon: Polygon) -> BoundingBox:
    """
    Given a list of points, calculate a bounding box that encompasses all points.

    :param polygon: Sequence of ``Point``
    :return: BoundingBox
    """
    y_min = min(v[1] for v in polygon)
    y_max = max(v[1] for v in polygon)
    x_min = min(v[0] for v in polygon)
    x_max = max(v[0] for v in polygon)
    return x_min, y_min, x_max, y_max

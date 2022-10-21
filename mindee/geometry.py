"""Pure Python geometry functions for working with polygons."""

from typing import NamedTuple, Sequence, Tuple


class GeomeTryError(RuntimeError):
    pass


class Point(NamedTuple):
    """A relative set of coordinates (X, Y) on the document."""

    x: float
    """X coordinate"""
    y: float
    """Y coordinate"""


class BBox(NamedTuple):
    """Contains exactly 4 coordinates."""

    x_min: float
    """Minimum X coordinate."""
    y_min: float
    """Minimum Y coordinate."""
    x_max: float
    """Maximum X coordinate."""
    y_max: float
    """Maximum Y coordinate."""


Polygon = Sequence[Point]
"""Contains any number of vertices coordinates (Points)"""

Quadrilateral = Tuple[Point, Point, Point, Point]
"""Contains exactly 4 relative vertices coordinates (Points)"""


def polygon_from_prediction(prediction: Sequence[list]) -> Polygon:
    """Transform a prediction into a Polygon."""
    return [Point(point[0], point[1]) for point in prediction]


def quadrilateral_from_prediction(prediction: Sequence[list]) -> Quadrilateral:
    """Transform a prediction into a Quadrilateral."""
    if len(prediction) != 4:
        raise GeomeTryError("Prediction must have exactly 4 points")
    return (
        Point(prediction[0][0], prediction[0][1]),
        Point(prediction[1][0], prediction[1][1]),
        Point(prediction[2][0], prediction[2][1]),
        Point(prediction[3][0], prediction[3][1]),
    )


def get_bounding_box(polygon: Polygon) -> Quadrilateral:
    """
    Given a sequence of points, calculate a polygon that encompasses all points.

    :param polygon: Sequence of ``Point``
    :return: Quadrilateral
    """
    x_min, y_min, x_max, y_max = get_bbox(polygon)
    return (
        Point(x_min, y_min),
        Point(x_max, y_min),
        Point(x_max, y_max),
        Point(x_min, y_max),
    )


def get_bbox(polygon: Polygon) -> BBox:
    """
    Given a list of points, calculate a bounding box that encompasses all points.

    :param polygon: Sequence of ``Point``
    :return: BoundingBox
    """
    y_min = min(v[1] for v in polygon)
    y_max = max(v[1] for v in polygon)
    x_min = min(v[0] for v in polygon)
    x_max = max(v[0] for v in polygon)
    return BBox(x_min, y_min, x_max, y_max)


def get_bounding_box_for_polygons(vertices: Sequence[Polygon]) -> Quadrilateral:
    """
    Given a list of polygons, calculate a polygon that encompasses all polygons.

    :param vertices: List of polygons
    :return: Quadrilateral
    """
    y_min = min(y for v in vertices for _, y in v)
    y_max = max(y for v in vertices for _, y in v)
    x_min = min(x for v in vertices for x, _ in v)
    x_max = max(x for v in vertices for x, _ in v)
    return (
        Point(x_min, y_min),
        Point(x_max, y_min),
        Point(x_max, y_max),
        Point(x_min, y_max),
    )


def get_centroid(polygon: Polygon) -> Point:
    """
    Get the central point (centroid) given a list of points.

    :param polygon: List of Points
    :return: Point
    """
    numb_vertices = len(polygon)
    x_sum = sum(x for x, _ in polygon)
    y_sum = sum(y for _, y in polygon)
    return Point(x_sum / numb_vertices, y_sum / numb_vertices)


def get_min_max_y(vertices: Polygon) -> Tuple[float, float]:
    """
    Get the maximum and minimum Y value given a list of points.

    :param vertices: List of points
    """
    points = [y for _, y in vertices]
    return min(points), max(points)


def is_point_in_polygon_y(point: Point, polygon: Polygon) -> bool:
    """
    Determine if the Point is in the Polygon's Y-axis.

    :param point: Point to compare
    :param polygon: Polygon to look into
    """
    min_y, max_y = get_min_max_y(polygon)
    return is_point_in_y(point, min_y, max_y)


def is_point_in_y(point: Point, min_y: float, max_y: float) -> bool:
    """
    Determine if the Point is in the Polygon's Y-axis.

    :param point: Point to compare
    :param min_y: Minimum Y-axis value
    :param max_y: Maximum Y-axis value
    """
    return min_y <= point.y <= max_y


def get_min_max_x(vertices: Polygon) -> Tuple[float, float]:
    """
    Get the maximum and minimum Y value given a list of points.

    :param vertices: List of points
    """
    points = [x for x, _ in vertices]
    return min(points), max(points)


def is_point_in_polygon_x(point: Point, polygon: Polygon) -> bool:
    """
    Determine if the Point is in the Polygon's Y-axis.

    :param point: Point to compare
    :param polygon: Polygon to look into
    """
    min_x, max_x = get_min_max_x(polygon)
    return is_point_in_x(point, min_x, max_x)


def is_point_in_x(point: Point, min_x: float, max_x: float) -> bool:
    """
    Determine if the Point is in the Polygon's Y-axis.

    :param point: Point to compare
    :param min_x: Minimum X-axis value
    :param max_x: Maximum X-axis value
    """
    return min_x <= point.x <= max_x

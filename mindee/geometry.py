"""Pure Python geometry functions for working with polygons."""

from typing import Sequence, Tuple

Point = Tuple[float, float]
Polygon = Sequence[Point]
BBox = Tuple[float, float, float, float]
Quadrilateral = Tuple[Point, Point, Point, Point]


def get_bounding_box(polygon: Polygon) -> Quadrilateral:
    """
    Given a sequence of points, calculate a polygon that encompasses all points.

    :param polygon: Sequence of ``Point``
    :return: Quadrilateral
    """
    x_min, y_min, x_max, y_max = get_bbox(polygon)
    return (x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)


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
    return x_min, y_min, x_max, y_max


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
    return (x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)


def get_centroid(polygon: Polygon) -> Point:
    """
    Get the central point (centroid) given a list of points.

    :param polygon: List of Points
    :return: Point
    """
    numb_vertices = len(polygon)
    x_sum = sum([x for x, _ in polygon])
    y_sum = sum([y for _, y in polygon])
    return x_sum / numb_vertices, y_sum / numb_vertices


def get_min_max_y(vertices: Polygon) -> Point:
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
    return min_y <= point[1] <= max_y


def get_min_max_x(vertices: Polygon) -> Point:
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
    return min_x <= point[0] <= max_x

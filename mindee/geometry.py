"""Pure Python geometry functions for working with polygons."""

from typing import NamedTuple, Sequence


class GeometryError(RuntimeError):
    pass


class Point(NamedTuple):
    """A relative set of coordinates (X, Y) on the document."""

    x: float
    """X coordinate"""
    y: float
    """Y coordinate"""


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

    @property
    def width(self) -> float:
        """The width of the BBox."""
        return self.x_max - self.x_min

    @property
    def height(self) -> float:
        """The height of the BBox."""
        return self.y_max - self.y_min

    @property
    def area(self) -> float:
        """The area of the BBox."""
        return self.width * self.height


class MinMax(NamedTuple):
    """A set of minimum and maximum values."""

    min: float
    """Minimum"""
    max: float
    """Maximum"""


class Polygon(list):
    """
    Contains any number of vertices coordinates (Points).

    Inherits from base class ``list`` so is compatible with type ``Points``.
    """


Points = Sequence[Point]


def polygon_from_prediction(prediction: Sequence[list]) -> Polygon:
    """
    Transform a prediction into a Polygon.

    :param prediction: API prediction.
    """
    return Polygon(Point(point[0], point[1]) for point in prediction)


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


def get_bbox(points: Points) -> BBox:
    """
    Given a sequence of points, calculate a bbox that encompasses all points.

    :param points: Polygon to process.
    :return: A bbox that encompasses all points
    """
    y_min = min(v[1] for v in points)
    y_max = max(v[1] for v in points)
    x_min = min(v[0] for v in points)
    x_max = max(v[0] for v in points)
    return BBox(x_min, y_min, x_max, y_max)


def get_bounding_box_for_polygons(vertices: Sequence[Polygon]) -> Quadrilateral:
    """
    Given a sequence of polygons, calculate a bounding box that encompasses all polygons.

    :param vertices: List of polygons
    :return: A bounding box that encompasses all polygons
    """
    y_min = min(y for v in vertices for _, y in v)
    y_max = max(y for v in vertices for _, y in v)
    x_min = min(x for v in vertices for x, _ in v)
    x_max = max(x for v in vertices for x, _ in v)
    return Quadrilateral(
        Point(x_min, y_min),
        Point(x_max, y_min),
        Point(x_max, y_max),
        Point(x_min, y_max),
    )


def get_centroid(points: Points) -> Point:
    """
    Get the central point (centroid) given a sequence of points.

    :param points: Polygon to process.
    :return: The centroid
    """
    numb_vertices = len(points)
    x_sum = sum(x for x, _ in points)
    y_sum = sum(y for _, y in points)
    return Point(x_sum / numb_vertices, y_sum / numb_vertices)


def get_min_max_y(points: Points) -> MinMax:
    """
    Get the maximum and minimum Y value given a sequence of points.

    :param points: List of points
    """
    y_coords = [y for _, y in points]
    return MinMax(min=min(y_coords), max=max(y_coords))


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


def get_min_max_x(points: Points) -> MinMax:
    """
    Get the maximum and minimum Y value given a sequence of points.

    :param points: List of points
    """
    x_coords = [x for x, _ in points]
    return MinMax(min=min(x_coords), max=max(x_coords))


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

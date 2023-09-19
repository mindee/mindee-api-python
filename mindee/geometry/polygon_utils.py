from mindee.geometry.point import Point, Points


def get_centroid(points: Points) -> Point:
    """
    Get the central point (centroid) given a sequence of points.

    :param points: Polygon to process.
    :return: The centroid
    """
    vertices_count = len(points)
    x_sum = sum(x for x, _ in points)
    y_sum = sum(y for _, y in points)
    return Point(x_sum / vertices_count, y_sum / vertices_count)


def is_point_in_y(point: Point, min_y: float, max_y: float) -> bool:
    """
    Determine if the Point is in the Polygon's Y-axis.

    :param point: Point to compare
    :param min_y: Minimum Y-axis value
    :param max_y: Maximum Y-axis value
    """
    return min_y <= point.y <= max_y


def is_point_in_x(point: Point, min_x: float, max_x: float) -> bool:
    """
    Determine if the Point is within the X-axis interval.

    :param point: Point to compare
    :param min_x: Minimum X-axis value
    :param max_x: Maximum X-axis value
    """
    return min_x <= point.x <= max_x

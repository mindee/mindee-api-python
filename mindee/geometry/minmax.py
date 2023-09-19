from typing import NamedTuple

from mindee.geometry.point import Points


class MinMax(NamedTuple):
    """A set of minimum and maximum values."""

    min: float
    """Minimum"""
    max: float
    """Maximum"""


def get_min_max_y(points: Points) -> MinMax:
    """
    Get the maximum and minimum Y value given a sequence of points.

    :param points: List of points
    """
    y_coords = [y for _, y in points]
    return MinMax(min=min(y_coords), max=max(y_coords))


def get_min_max_x(points: Points) -> MinMax:
    """
    Get the maximum and minimum Y value given a sequence of points.

    :param points: List of points
    """
    x_coords = [x for x, _ in points]
    return MinMax(min=min(x_coords), max=max(x_coords))

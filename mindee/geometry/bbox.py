from typing import NamedTuple

from mindee.geometry.point import Points


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

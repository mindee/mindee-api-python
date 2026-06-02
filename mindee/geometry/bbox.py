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


def merge_bbox(bbox_1: BBox, bbox_2: BBox) -> BBox:
    """Merges two BBox."""
    return BBox(
        min(bbox_1.x_min, bbox_2.x_min),
        min(bbox_1.y_min, bbox_2.y_min),
        max(bbox_1.x_max, bbox_2.x_max),
        max(bbox_1.y_max, bbox_2.y_max),
    )


def extend_bbox(bbox: BBox, points: Points) -> BBox:
    """
    Given a BBox and a sequence of points, calculate the surrounding bbox that encompasses all.

    :param bbox: initial BBox to extend.
    :param points: Sequence of points to process. Accepts polygons and similar
    """
    all_points = []
    for point in points:
        all_points.append(point)

    y_min = min(v[1] for v in all_points)
    y_max = max(v[1] for v in all_points)
    x_min = min(v[0] for v in all_points)
    x_max = max(v[0] for v in all_points)
    return merge_bbox(bbox, BBox(x_min, y_min, x_max, y_max))

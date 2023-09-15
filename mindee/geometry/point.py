from typing import NamedTuple, Sequence


class Point(NamedTuple):
    """A relative set of coordinates (X, Y) on the document."""

    x: float
    """X coordinate"""
    y: float
    """Y coordinate"""


Points = Sequence[Point]

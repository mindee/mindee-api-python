from collections.abc import Sequence
from typing import NamedTuple


class Point(NamedTuple):
    """A relative set of coordinates (X, Y) on the document."""

    x: float
    """X coordinate"""
    y: float
    """Y coordinate"""

    def __str__(self) -> str:
        return f"({self.x},{self.y})"


Points = Sequence[Point]

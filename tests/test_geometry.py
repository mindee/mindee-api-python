import pytest

from mindee import geometry


@pytest.fixture
def polygon_a():
    """90° rectangle, overlaps polygon_b"""
    return [(0.123, 0.53), (0.175, 0.53), (0.175, 0.546), (0.123, 0.546)]


@pytest.fixture
def polygon_b():
    """90° rectangle, overlaps polygon_a"""
    return [(0.124, 0.535), (0.190, 0.535), (0.190, 0.546), (0.124, 0.546)]


@pytest.fixture
def polygon_c():
    """not 90° rectangle, doesn't overlap any polygons"""
    return [(0.205, 0.407), (0.379, 0.407), (0.381, 0.43), (0.207, 0.43)]


def test_bbox(polygon_a, polygon_b, polygon_c):
    assert geometry.get_bbox(polygon_a) == (0.123, 0.53, 0.175, 0.546)
    assert geometry.get_bbox(polygon_b) == (0.124, 0.535, 0.19, 0.546)
    assert geometry.get_bbox(polygon_c) == (0.205, 0.407, 0.381, 0.43)


def test_bbox_polygon(polygon_a, polygon_b, polygon_c):
    assert geometry.get_bbox_as_polygon(polygon_a) == (
        (0.123, 0.53),
        (0.175, 0.53),
        (0.175, 0.546),
        (0.123, 0.546),
    )
    assert geometry.get_bbox_as_polygon(polygon_b) == (
        (0.124, 0.535),
        (0.19, 0.535),
        (0.19, 0.546),
        (0.124, 0.546),
    )
    assert geometry.get_bbox_as_polygon(polygon_c) == (
        (0.205, 0.407),
        (0.381, 0.407),
        (0.381, 0.43),
        (0.205, 0.43),
    )

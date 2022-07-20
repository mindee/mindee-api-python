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


def test_is_point_in_polygon_y(polygon_a, polygon_b, polygon_c):
    # Should be in polygon A & B, since polygons overlap
    point_a = (0.125, 0.535)
    # Should only be in polygon C
    point_b = (0.300, 0.420)

    assert geometry.is_point_in_polygon_y(point_a, polygon_a)
    assert geometry.is_point_in_polygon_y(point_a, polygon_b)
    assert geometry.is_point_in_polygon_y(point_a, polygon_c) is False

    assert geometry.is_point_in_polygon_y(point_b, polygon_a) is False
    assert geometry.is_point_in_polygon_y(point_b, polygon_b) is False
    assert geometry.is_point_in_polygon_y(point_b, polygon_c)


def test_get_centroid(polygon_a):
    assert geometry.get_centroid(polygon_a) == (0.149, 0.538)

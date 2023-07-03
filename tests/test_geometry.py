import pytest

from mindee import geometry


@pytest.fixture
def rectangle_a():
    """90° rectangle, overlaps polygon_b"""
    return [(0.123, 0.53), (0.175, 0.53), (0.175, 0.546), (0.123, 0.546)]


@pytest.fixture
def rectangle_b():
    """90° rectangle, overlaps polygon_a"""
    return [(0.124, 0.535), (0.190, 0.535), (0.190, 0.546), (0.124, 0.546)]


@pytest.fixture
def quadrangle_a():
    """not 90° rectangle, doesn't overlap any polygons"""
    return [(0.205, 0.407), (0.379, 0.407), (0.381, 0.43), (0.207, 0.43)]


def test_bbox(rectangle_a, rectangle_b, quadrangle_a):
    bbox_a = geometry.get_bbox(rectangle_a)
    assert bbox_a == (0.123, 0.53, 0.175, 0.546)
    assert round(bbox_a.width, 3) == 0.052
    assert round(bbox_a.height, 3) == 0.016
    assert round(bbox_a.area, 6) == 0.000832
    assert geometry.get_bbox(rectangle_b) == (0.124, 0.535, 0.19, 0.546)
    assert geometry.get_bbox(quadrangle_a) == (0.205, 0.407, 0.381, 0.43)


def test_bounding_box_single_polygon(rectangle_a, rectangle_b, quadrangle_a):
    assert geometry.get_bounding_box(rectangle_a) == (
        (0.123, 0.53),
        (0.175, 0.53),
        (0.175, 0.546),
        (0.123, 0.546),
    )
    assert geometry.get_bounding_box(rectangle_b) == (
        geometry.Point(0.124, 0.535),
        geometry.Point(0.19, 0.535),
        geometry.Point(0.19, 0.546),
        geometry.Point(0.124, 0.546),
    )
    assert geometry.get_bounding_box(quadrangle_a) == (
        (0.205, 0.407),
        (0.381, 0.407),
        (0.381, 0.43),
        (0.205, 0.43),
    )


def test_is_point_in_polygon_y(rectangle_a, rectangle_b, quadrangle_a):
    # Should be in polygon A & B, since polygons overlap
    point_a = geometry.Point(0.125, 0.535)
    # Should only be in polygon C
    point_b = geometry.Point(0.300, 0.420)

    assert geometry.is_point_in_polygon_y(point_a, rectangle_a)
    assert geometry.is_point_in_polygon_y(point_a, rectangle_b)
    assert geometry.is_point_in_polygon_y(point_a, quadrangle_a) is False

    assert geometry.is_point_in_polygon_y(point_b, rectangle_a) is False
    assert geometry.is_point_in_polygon_y(point_b, rectangle_b) is False
    assert geometry.is_point_in_polygon_y(point_b, quadrangle_a)


def test_is_point_in_polygon_x(rectangle_a, rectangle_b, quadrangle_a):
    # Should be in polygon A & B, since polygons overlap
    point_a = geometry.Point(0.125, 0.535)
    # Should only be in polygon C
    point_b = geometry.Point(0.300, 0.420)

    assert geometry.is_point_in_polygon_x(point_a, rectangle_a)
    assert geometry.is_point_in_polygon_x(point_a, rectangle_b)
    assert geometry.is_point_in_polygon_x(point_a, quadrangle_a) is False

    assert geometry.is_point_in_polygon_x(point_b, rectangle_a) is False
    assert geometry.is_point_in_polygon_x(point_b, rectangle_b) is False
    assert geometry.is_point_in_polygon_x(point_b, quadrangle_a)


def test_get_centroid(rectangle_a):
    assert geometry.get_centroid(rectangle_a) == (0.149, 0.538)


def test_bounding_box_several_polygons(rectangle_b, quadrangle_a):
    merged = geometry.merge_polygons((rectangle_b, quadrangle_a))
    assert geometry.get_bounding_box(merged) == (
        (0.124, 0.407),
        (0.381, 0.407),
        (0.381, 0.546),
        (0.124, 0.546),
    )


def test_polygon_merge(rectangle_b, quadrangle_a):
    assert geometry.merge_polygons((rectangle_b, quadrangle_a)) == [
        (0.124, 0.407),
        (0.381, 0.407),
        (0.381, 0.546),
        (0.124, 0.546),
    ]

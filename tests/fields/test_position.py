import pytest

from mindee.fields.position import Position


def test_constructor():
    field_dict = {
        "bounding_box": [
            [0.016, 0.707],
            [0.414, 0.707],
            [0.414, 0.831],
            [0.016, 0.831],
        ],
        "confidence": 0.1,
        "quadrangle": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
        "polygon": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
        "rectangle": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
    }
    field = Position(field_dict)
    assert len(field.value) == 4


def test_fail_constructor():
    field_dict = {
        "bounding_box": [
            [0.016, 0.707],
            [0.414, 0.707],
            [0.414, 0.831],
            [0.016, 0.831],
        ],
        "confidence": 0.1,
        "quadrangle": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
        "rectangle": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
    }
    field = Position(field_dict)
    assert len(field.value) == 0

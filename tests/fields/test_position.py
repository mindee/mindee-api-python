from mindee.fields.position import PositionField


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
    field = PositionField(field_dict)
    assert len(field.value) == 4
    assert field.confidence == 0.1
    assert field.polygon[0].x == 0.016


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
    field = PositionField(field_dict)
    assert field.value is None

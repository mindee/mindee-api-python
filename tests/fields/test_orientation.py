from mindee.fields.orientation import OrientationField


def test_constructor():
    field_dict = {
        "value": 90,
    }
    orientation = OrientationField(field_dict)
    assert orientation.value == 90


def test_not_number():
    field_dict = {
        "value": "aze",
    }
    orientation = OrientationField(field_dict)
    assert orientation.value == 0


def test_not_90():
    field_dict = {
        "value": 255,
    }
    orientation = OrientationField(field_dict)
    assert orientation.value == 0

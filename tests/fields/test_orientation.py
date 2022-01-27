from mindee.fields.orientation import Orientation


def test_constructor():
    field_dict = {
        "degrees": 90,
        "confidence": 0.1,
    }
    orientation = Orientation(field_dict)
    assert orientation.value == 90


def test_not_number():
    field_dict = {
        "degrees": "aze",
        "confidence": 0.1,
    }
    orientation = Orientation(field_dict)
    assert orientation.value == 0


def test_not_90():
    field_dict = {
        "degrees": 255,
        "confidence": 0.1,
    }
    orientation = Orientation(field_dict)
    assert orientation.value == 0

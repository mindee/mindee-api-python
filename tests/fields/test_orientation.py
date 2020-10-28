from mindee.fields.orientation import Orientation


def test_constructor():
    field_dict = {
        'degrees': 90,
        'probability': 0.1,
    }
    orientation = Orientation(field_dict)
    assert orientation.value == 90


def test_not_number():
    field_dict = {
        'degrees': "aze",
        'probability': 0.1,
    }
    orientation = Orientation(field_dict)
    assert orientation.value == 0


def test_not_90():
    field_dict = {
        'degrees': 255,
        'probability': 0.1,
    }
    orientation = Orientation(field_dict)
    assert orientation.value == 0

from mindee.parsing.standard.text import StringField


def test_constructor_no_raw_value():
    field_dict = {
        "value": "hello world",
        "confidence": 0.1,
        "polygon": [
            [0.016, 0.707],
            [0.414, 0.707],
            [0.414, 0.831],
            [0.016, 0.831],
        ],
    }
    field = StringField(field_dict)
    assert field.value == "hello world"
    assert field.raw_value is None


def test_constructor_raw_value():
    field_dict = {
        "value": "hello world",
        "raw_value": "HelLO wOrld",
        "confidence": 0.1,
        "polygon": [
            [0.016, 0.707],
            [0.414, 0.707],
            [0.414, 0.831],
            [0.016, 0.831],
        ],
    }
    field = StringField(field_dict)
    assert field.value == "hello world"
    assert field.raw_value == "HelLO wOrld"

import datetime
from mindee.fields.date import Date


def test_constructor():
    field_dict = {
        'iso': "2018-04-01",
        'probability': 0.1,
        'segmentation': {
            "bounding_box": [
                [0.016, 0.707],
                [0.414, 0.707],
                [0.414, 0.831],
                [0.016, 0.831]
            ]
        }
    }
    date = Date(field_dict)
    assert date.value == "2018-04-01"


def test_constructor_no_date():
    field_dict = {
        'iso': "N/A",
        'probability': 0.1
    }
    date = Date(field_dict)
    assert date.value is None


import datetime

from mindee.parsing.standard.date import DateField


def test_constructor():
    field_dict = {
        "value": "2018-04-01",
        "confidence": 0.1,
        "polygon": [
            [0.016, 0.707],
            [0.414, 0.707],
            [0.414, 0.831],
            [0.016, 0.831],
        ],
        "is_computed": True,
    }
    date = DateField(field_dict)
    assert date.value == "2018-04-01"
    assert isinstance(date.date_object, datetime.date)
    assert date.is_computed


def test_constructor_no_date():
    field_dict = {"iso": "N/A", "confidence": 0.1}
    date = DateField(field_dict)
    assert date.value is None

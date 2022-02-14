from mindee.fields.tax import Tax


def test_constructor():
    field_dict = {
        "value": "2",
        "rate": 0.2,
        "code": "QST",
        "confidence": 0.1,
        "polygon": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
    }
    tax = Tax(field_dict, value_key="value")
    assert tax.value == 2
    assert tax.confidence == 0.1
    assert tax.rate == 0.2
    assert len(tax.bbox) > 0
    assert type(str(tax)) == str


def test_constructor_no_rate():
    field_dict = {"value": "2", "rate": "AA", "confidence": 0.1}
    tax = Tax(field_dict)
    assert tax.rate is None
    assert len(tax.bbox) == 0


def test_constructor_no_amount():
    field_dict = {"value": "NA", "rate": "AA", "code": "N/A", "confidence": 0.1}
    tax = Tax(field_dict)
    assert tax.value is None
    assert type(str(tax)) == str

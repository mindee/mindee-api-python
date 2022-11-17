from mindee.fields.amount import AmountField


def test_constructor():
    field_dict = {
        "value": "2",
        "confidence": 0.1,
        "polygon": [
            [0.016, 0.707],
            [0.414, 0.707],
            [0.414, 0.831],
            [0.016, 0.831],
        ],
    }
    amount = AmountField(field_dict)
    assert amount.value == 2
    assert amount.value - amount.value == 0


def test_constructor_no_amount():
    field_dict = {"value": "N/A", "confidence": 0.1}
    amount = AmountField(field_dict)
    assert amount.value is None

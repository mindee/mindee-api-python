from mindee.fields.amount import Amount


def test_constructor():
    field_dict = {
        "amount": "2",
        "confidence": 0.1,
        "segmentation": {
            "bounding_box": [
                [0.016, 0.707],
                [0.414, 0.707],
                [0.414, 0.831],
                [0.016, 0.831],
            ]
        },
    }
    amount = Amount(field_dict)
    assert amount.value == 2
    assert amount.value - amount.value == 0


def test_constructor_no_amount():
    field_dict = {"amount": "N/A", "confidence": 0.1}
    amount = Amount(field_dict)
    assert amount.value is None

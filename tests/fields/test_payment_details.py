from mindee.fields.payment_details import PaymentDetails


def test_constructor():
    field_dict = {
        "account_number": "account_number",
        "iban": "iban",
        "routing_number": "routing_number",
        "swift": "swift",
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
    payment_detail = PaymentDetails(field_dict)
    assert payment_detail.account_number == "account_number"
    assert payment_detail.iban == "iban"
    assert payment_detail.routing_number == "routing_number"
    assert payment_detail.swift == "swift"
    assert str(payment_detail) == "account_number; iban; routing_number; swift;"


def test_constructor_all_na():
    field_dict = {
        "account_number": "N/A",
        "iban": "N/A",
        "routing_number": "N/A",
        "swift": "N/A",
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
    payment_detail = PaymentDetails(field_dict)
    assert payment_detail.account_number is None
    assert payment_detail.iban is None
    assert payment_detail.routing_number is None
    assert payment_detail.swift is None


def test_constructor_all_none():
    field_dict = {
        "account_number": {},
        "iban": {},
        "routing_number": {},
        "swift": {},
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
    payment_detail = PaymentDetails(field_dict)
    assert payment_detail.account_number is None
    assert payment_detail.iban is None
    assert payment_detail.routing_number is None
    assert payment_detail.swift is None

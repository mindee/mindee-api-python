from mindee.fields.tax import TaxField


def test_constructor():
    field_dict = {
        "value": 2,
        "rate": 0.2,
        "code": "QST",
        "confidence": 0.1,
        "polygon": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
    }
    tax = TaxField(field_dict)
    assert tax.value == 2
    assert tax.confidence == 0.1
    assert tax.rate == 0.2
    assert len(tax.bounding_box) > 0
    assert str(tax) == "2.0 0.2% QST"


def test_constructor_no_rate():
    field_dict = {"value": 2.0, "confidence": 0.1}
    tax = TaxField(field_dict)
    assert tax.rate is None
    assert tax.bounding_box is None
    assert str(tax) == "2.0"


def test_constructor_no_amount():
    field_dict = {"value": "NA", "rate": "AA", "code": "N/A", "confidence": 0.1}
    tax = TaxField(field_dict)
    assert tax.value is None
    assert str(tax) == ""


def test_constructor_only_code():
    field_dict = {
        "value": "NA",
        "rate": "None",
        "code": "TAXES AND FEES",
        "confidence": 0.1,
    }
    tax = TaxField(field_dict)
    assert tax.value is None
    assert str(tax) == "TAXES AND FEES"

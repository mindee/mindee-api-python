import pytest

from mindee.parsing.standard.base import (
    BaseField,
    field_array_confidence,
    field_array_sum,
    float_to_string,
)
from mindee.parsing.standard.company_registration import CompanyRegistrationField
from mindee.parsing.standard.text import StringField


def test_constructor():
    field_dict = {
        "value": "test",
        "confidence": 0.1,
        "polygon": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
    }
    field = StringField(field_dict)
    assert field.value == "test"
    assert field.confidence == 0.1
    assert len(field.bounding_box) > 0


def test_type_constructor():
    field_dict = {
        "value": "test",
        "type": "IBAN",
        "confidence": 0.1,
        "polygon": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
    }
    field = CompanyRegistrationField(field_dict)
    assert field.value == "test"
    assert field.type == "IBAN"
    assert field.confidence == 0.1
    assert len(field.bounding_box) == 4


def test_constructor_no_position():
    field_dict = {"value": "test", "confidence": 0.1}
    field = StringField(field_dict)
    assert field.bounding_box is None


def test_equality():
    field_dict_1 = {"value": "test", "confidence": 0.1}
    field_dict_2 = {"value": "other", "confidence": 0.1}
    field_1 = BaseField(field_dict_1)
    field_2 = BaseField(field_dict_2)
    assert field_1 == field_1
    assert field_1 != field_2


def test_constructor_na():
    field_dict = {"value": "N/A", "confidence": 0.1}
    field = BaseField(field_dict)
    assert field.value is None


def test_no_probability():
    field_dict = {
        "value": "N/A",
    }
    field = BaseField(field_dict)
    assert field.confidence == 0.0


def test_array_probability():
    fields = [
        BaseField({"value": None, "confidence": 0.1}),
        BaseField({"value": None, "confidence": 0.8}),
    ]
    assert field_array_confidence(fields) == 0.8 * 0.1
    fields = [
        BaseField({"value": None, "confidence": 0.1}),
        BaseField({"value": None, "confidence": None}),
    ]
    assert field_array_confidence(fields) == 0.0


def test_array_sum():
    fields = [
        BaseField({"value": 1, "confidence": 0.1}),
        BaseField({"value": 2, "confidence": 0.8}),
    ]
    assert field_array_sum(fields) == 3
    fields = [
        BaseField({"value": None, "confidence": 0.1}),
        BaseField({"value": 4, "confidence": 0.8}),
    ]
    assert field_array_sum(fields) == 0.0


def test_float_to_string():
    assert float_to_string(1.0) == "1.00"
    assert float_to_string(1.001, min_precision=1) == "1.001"
    assert float_to_string(1.0, min_precision=4) == "1.0000"

    # should not work on integer values
    with pytest.raises(IndexError):
        float_to_string(1)

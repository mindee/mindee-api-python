from mindee.fields.base import (
    Field,
    TypedField,
    field_array_confidence,
    field_array_sum,
)


def test_constructor():
    field_dict = {
        "value": "test",
        "confidence": 0.1,
        "polygon": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
    }
    field = Field(field_dict)
    assert field.value == "test"
    assert field.confidence == 0.1
    assert len(field.bbox) > 0


def test_type_constructor():
    field_dict = {
        "value": "test",
        "type": "IBAN",
        "confidence": 0.1,
        "polygon": [[0.016, 0.707], [0.414, 0.707], [0.414, 0.831], [0.016, 0.831]],
    }
    field = TypedField(field_dict)
    assert field.value == "test"
    assert field.type == "IBAN"
    assert field.confidence == 0.1
    assert len(field.bbox) > 0


def test_constructor_no_segmentation():
    field_dict = {"value": "test", "confidence": 0.1}
    field = Field(field_dict)
    assert len(field.bbox) == 0


def test_equality():
    field_dict_1 = {"value": "test", "confidence": 0.1}
    field_dict_2 = {"value": "other", "confidence": 0.1}
    field_1 = Field(field_dict_1)
    field_2 = Field(field_dict_2)
    assert field_1 == field_1
    assert field_1 != field_2


def test_constructor_na():
    field_dict = {"value": "N/A", "confidence": 0.1}
    field = Field(field_dict)
    assert field.value is None


def test_no_probability():
    field_dict = {
        "value": "N/A",
    }
    field = Field(field_dict)
    assert field.confidence == 0.0


def test_array_probability():
    fields = [
        Field({"value": None, "confidence": 0.1}),
        Field({"value": None, "confidence": 0.8}),
    ]
    assert field_array_confidence(fields) == 0.8 * 0.1
    fields = [
        Field({"value": None, "confidence": 0.1}),
        Field({"value": None, "confidence": None}),
    ]
    assert field_array_confidence(fields) == 0.0


def test_array_sum():
    fields = [
        Field({"value": 1, "confidence": 0.1}),
        Field({"value": 2, "confidence": 0.8}),
    ]
    assert field_array_sum(fields) == 3
    fields = [
        Field({"value": None, "confidence": 0.1}),
        Field({"value": 4, "confidence": 0.8}),
    ]
    assert field_array_sum(fields) == 0.0

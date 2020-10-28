from mindee.fields import Field


def test_constructor():
    field_dict = {
        'value': "test",
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
    field = Field(field_dict)
    assert field.value == "test"
    assert field.probability == 0.1
    assert len(field.bbox) > 0


def test_constructor_no_segmentation():
    field_dict = {
        'value': "test",
        'probability': 0.1
    }
    field = Field(field_dict)
    assert len(field.bbox) == 0


def test_equality():
    field_dict_1 = {
        'value': "test",
        'probability': 0.1
    }
    field_dict_2 = {
        'value': "other",
        'probability': 0.1
    }
    field_1 = Field(field_dict_1)
    field_2 = Field(field_dict_2)
    assert field_1 == field_1
    assert field_1 != field_2


def test_constructor_na():
    field_dict = {
        'value': "N/A",
        'probability': 0.1
    }
    field = Field(field_dict)
    assert field.value is None


def test_no_probability():
    field_dict = {
        'value': "N/A",
    }
    field = Field(field_dict)
    assert field.probability == 0.


def test_array_probability():
    fields = [Field({"value": None, "probability": 0.1}), Field({"value": None, "probability": 0.8})]
    assert Field.array_probability(fields) == 0.8*0.1
    fields = [Field({"value": None, "probability": 0.1}), Field({"value": None, "probability": None})]
    assert Field.array_probability(fields) == 0.


def test_array_sum():
    fields = [Field({"value": 1, "probability": 0.1}), Field({"value": 2, "probability": 0.8})]
    assert Field.array_sum(fields) == 3
    fields = [Field({"value": None, "probability": 0.1}), Field({"value": 4, "probability": 0.8})]
    assert Field.array_sum(fields) == 0.

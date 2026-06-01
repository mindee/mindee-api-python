import pytest

from mindee.error import MindeeApiV2Error
from mindee.parsing.v2.field.dynamic_field import (
    DynamicField,
    FieldType,
    get_field_type,
)
from mindee.parsing.v2.field.field_confidence import FieldConfidence
from mindee.parsing.v2.field.inference_fields import InferenceFields
from mindee.parsing.v2.field.list_field import ListField
from mindee.parsing.v2.field.object_field import ObjectField
from mindee.parsing.v2.field.simple_field import SimpleField


def test_dynamic_field_multi_str():
    field = DynamicField(FieldType.SIMPLE)

    assert field.multi_str() == str(field)


def test_invalid_field_confidence_is_ignored():
    field = SimpleField({"value": "invoice", "confidence": "Unknown"})

    assert field.confidence is None


def test_field_confidence_comparisons_and_type_errors():
    assert int(FieldConfidence.CERTAIN) == 4
    assert str(FieldConfidence.HIGH) == "High"
    assert FieldConfidence.LOW < FieldConfidence.MEDIUM
    assert FieldConfidence.MEDIUM <= FieldConfidence.HIGH
    assert FieldConfidence.CERTAIN > FieldConfidence.HIGH
    assert FieldConfidence.HIGH >= FieldConfidence.MEDIUM

    with pytest.raises(TypeError, match="Cannot compare FieldConfidence"):
        FieldConfidence.HIGH < "High"
    with pytest.raises(TypeError, match="Cannot compare FieldConfidence"):
        FieldConfidence.HIGH <= "High"
    with pytest.raises(TypeError, match="Cannot compare FieldConfidence"):
        FieldConfidence.HIGH > "High"
    with pytest.raises(TypeError, match="Cannot compare FieldConfidence"):
        FieldConfidence.HIGH >= "High"


def test_get_field_type_rejects_unknown_payloads():
    with pytest.raises(MindeeApiV2Error, match="Unrecognized field type"):
        get_field_type({"confidence": "High"})

    with pytest.raises(MindeeApiV2Error, match="Unrecognized field format"):
        get_field_type("invoice")


def test_inference_fields_attribute_access_and_string():
    fields = InferenceFields(
        {
            "name": {"value": "Jane Doe"},
            "line_items": {"items": [{"value": "Item 1"}]},
            "address": {"fields": {"city": {"value": "Paris"}}},
        }
    )

    assert isinstance(fields.name, SimpleField)
    assert fields.name.value == "Jane Doe"
    assert isinstance(fields.line_items, ListField)
    assert isinstance(fields.address, ObjectField)
    assert ":name: Jane Doe" in str(fields)
    assert ":line_items:" in str(fields)
    assert ":address:" in str(fields)

    with pytest.raises(AttributeError, match="missing"):
        fields.missing

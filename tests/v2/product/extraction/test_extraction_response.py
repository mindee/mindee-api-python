import json
from pathlib import Path
from typing import Tuple

import pytest

from mindee import InferenceResponse
from mindee.parsing.v2 import InferenceActiveOptions
from mindee.parsing.v2.field.field_confidence import FieldConfidence
from mindee.parsing.v2.field.list_field import ListField
from mindee.parsing.v2.field.object_field import ObjectField
from mindee.parsing.v2.field.simple_field import SimpleField
from mindee.parsing.v2.field.inference_fields import InferenceFields
from mindee.parsing.v2.inference import Inference
from mindee.parsing.v2.inference_file import InferenceFile
from mindee.parsing.v2.inference_model import InferenceModel
from mindee.parsing.v2.rag_metadata import RagMetadata
from tests.utils import V2_PRODUCT_DATA_DIR


def _get_samples(json_path: Path, rst_path: Path) -> Tuple[dict, str]:
    with json_path.open("r", encoding="utf-8") as fh:
        json_sample = json.load(fh)
    try:
        with rst_path.open("r", encoding="utf-8") as fh:
            rst_sample = fh.read()
    except FileNotFoundError:
        rst_sample = ""
    return json_sample, rst_sample


def _get_inference_samples(name: str) -> Tuple[dict, str]:
    json_path = V2_PRODUCT_DATA_DIR / "extraction" / f"{name}.json"
    rst_path = V2_PRODUCT_DATA_DIR / "extraction" / f"{name}.rst"
    return _get_samples(json_path, rst_path)


def _get_product_samples(product, name: str) -> Tuple[dict, str]:
    json_path = V2_PRODUCT_DATA_DIR / "extraction" / product / f"{name}.json"
    rst_path = V2_PRODUCT_DATA_DIR / "extraction" / product / f"{name}.rst"
    return _get_samples(json_path, rst_path)


@pytest.mark.v2
def test_deep_nested_fields():
    json_sample, rst_sample = _get_inference_samples("deep_nested_fields")
    response = InferenceResponse(json_sample)
    assert isinstance(response.inference, Inference)
    assert isinstance(response.inference.result.fields["field_simple"], SimpleField)
    assert isinstance(response.inference.result.fields["field_object"], ObjectField)
    assert isinstance(
        response.inference.result.fields["field_object"].fields["sub_object_list"],
        ListField,
    )
    assert isinstance(
        response.inference.result.fields["field_object"].fields["sub_object_object"],
        ObjectField,
    )
    fields = response.inference.result.fields
    assert isinstance(fields.get("field_object"), ObjectField)
    assert isinstance(
        fields.get("field_object").get_simple_field("sub_object_simple"), SimpleField
    )
    assert isinstance(
        fields.get("field_object").get_list_field("sub_object_list"), ListField
    )
    assert isinstance(
        fields.get("field_object").get_object_field("sub_object_object"), ObjectField
    )
    assert len(fields.get("field_object").simple_fields) == 1
    assert len(fields.get("field_object").list_fields) == 1
    assert len(fields.get("field_object").object_fields) == 1
    assert isinstance(
        fields["field_object"].fields["sub_object_object"].fields,
        dict,
    )
    assert isinstance(
        fields["field_object"]
        .fields["sub_object_object"]
        .fields["sub_object_object_sub_object_list"],
        ListField,
    )
    assert isinstance(
        fields["field_object"]
        .fields["sub_object_object"]
        .fields["sub_object_object_sub_object_list"]
        .items,
        list,
    )
    assert isinstance(
        fields["field_object"]
        .fields["sub_object_object"]
        .fields["sub_object_object_sub_object_list"]
        .items[0],
        ObjectField,
    )
    assert isinstance(
        fields["field_object"]
        .fields["sub_object_object"]
        .fields["sub_object_object_sub_object_list"]
        .items[0]
        .fields["sub_object_object_sub_object_list_simple"],
        SimpleField,
    )
    assert (
        fields["field_object"]
        .fields["sub_object_object"]
        .fields["sub_object_object_sub_object_list"]
        .items[0]
        .fields["sub_object_object_sub_object_list_simple"]
        .value
        == "value_9"
    )


@pytest.mark.v2
def test_standard_field_types():
    json_sample, rst_sample = _get_inference_samples("standard_field_types")
    response = InferenceResponse(json_sample)
    assert isinstance(response.inference, Inference)

    field_simple_string = response.inference.result.fields["field_simple_string"]
    assert isinstance(field_simple_string, SimpleField)
    assert field_simple_string.value == "field_simple_string-value"
    assert field_simple_string.confidence == FieldConfidence.CERTAIN
    assert str(field_simple_string) == "field_simple_string-value"

    field_simple_int = response.inference.result.fields["field_simple_int"]
    assert isinstance(field_simple_int, SimpleField)
    assert isinstance(field_simple_int.value, float)

    field_simple_float = response.inference.result.fields["field_simple_float"]
    assert isinstance(field_simple_float, SimpleField)
    assert isinstance(field_simple_float.value, float)

    field_simple_bool = response.inference.result.fields["field_simple_bool"]
    assert isinstance(field_simple_bool, SimpleField)
    assert field_simple_bool.value is True
    assert str(field_simple_bool) == "True"

    field_simple_null = response.inference.result.fields["field_simple_null"]
    assert isinstance(field_simple_null, SimpleField)
    assert field_simple_null.value is None
    assert str(field_simple_null) == ""

    assert rst_sample == str(response)


@pytest.mark.v2
def test_standard_field_object():
    json_sample, _ = _get_inference_samples("standard_field_types")
    response = InferenceResponse(json_sample)

    object_field = response.inference.result.fields["field_object"]
    assert isinstance(object_field, ObjectField)

    sub_fields = object_field.fields
    assert isinstance(sub_fields, InferenceFields)
    assert len(sub_fields) == 2

    subfield_1 = sub_fields["subfield_1"]
    assert isinstance(subfield_1, SimpleField)

    for field_name, sub_field in sub_fields.items():
        assert field_name.startswith("subfield_")
        assert isinstance(sub_field, SimpleField)


@pytest.mark.v2
def test_standard_field_object_list():
    json_sample, _ = _get_inference_samples("standard_field_types")
    response = InferenceResponse(json_sample)
    assert isinstance(response.inference, Inference)

    field_object_list = response.inference.result.fields["field_object_list"]
    assert isinstance(field_object_list, ListField)
    assert len(field_object_list.items) == 2
    for object_field in field_object_list.object_items:
        assert isinstance(object_field, ObjectField)


@pytest.mark.v2
def test_standard_field_simple_list():
    json_sample, _ = _get_inference_samples("standard_field_types")
    response = InferenceResponse(json_sample)
    assert isinstance(response.inference, Inference)

    field_simple_list = response.inference.result.fields["field_simple_list"]
    assert isinstance(field_simple_list, ListField)
    assert len(field_simple_list.simple_items) == 2
    for object_field in field_simple_list.simple_items:
        assert isinstance(object_field, SimpleField)


@pytest.mark.v2
def test_raw_texts():
    json_sample, _ = _get_inference_samples("raw_texts")
    response = InferenceResponse(json_sample)
    assert isinstance(response.inference, Inference)

    assert response.inference.result.raw_text
    assert len(response.inference.result.raw_text.pages) == 2
    assert (
        response.inference.result.raw_text.pages[0].content
        == "This is the raw text of the first page..."
    )
    assert response.inference.active_options.raw_text is True


@pytest.mark.v2
def test_rag_metadata_when_matched():
    """RAG metadata when matched."""
    json_sample, _ = _get_inference_samples("rag_matched")
    response = InferenceResponse(json_sample)
    rag = response.inference.result.rag
    assert isinstance(rag, RagMetadata)
    assert rag.retrieved_document_id == "12345abc-1234-1234-1234-123456789abc"
    assert response.inference.active_options.rag is True


@pytest.mark.v2
def test_rag_metadata_when_not_matched():
    """RAG metadata when not matched."""
    json_sample, _ = _get_inference_samples("rag_not_matched")
    response = InferenceResponse(json_sample)
    rag = response.inference.result.rag
    assert isinstance(rag, RagMetadata)
    assert rag.retrieved_document_id is None
    assert response.inference.active_options.rag is True


@pytest.mark.v2
def test_full_inference_response():
    json_sample, rst_sample = _get_product_samples("financial_document", "complete")
    response = InferenceResponse(json_sample)

    assert isinstance(response.inference, Inference)
    assert response.inference.id == "12345678-1234-1234-1234-123456789abc"
    assert isinstance(response.inference.result.fields["date"], SimpleField)
    assert response.inference.result.fields["date"].value == "2019-11-02"
    assert isinstance(response.inference.result.fields["taxes"], ListField)
    assert isinstance(response.inference.result.fields["taxes"].items[0], ObjectField)
    assert (
        response.inference.result.fields["customer_address"].fields["city"].value
        == "New York"
    )
    assert (
        response.inference.result.fields["taxes"].items[0].fields["base"].value == 31.5
    )

    assert isinstance(response.inference.model, InferenceModel)
    assert response.inference.model.id == "12345678-1234-1234-1234-123456789abc"

    assert isinstance(response.inference.file, InferenceFile)
    assert response.inference.file.name == "complete.jpg"
    assert response.inference.file.page_count == 1
    assert response.inference.file.mime_type == "image/jpeg"
    assert not response.inference.file.alias
    assert not response.inference.result.raw_text


@pytest.mark.v2
def test_field_locations_and_confidence() -> None:
    """
    Validate that the first location polygon for the ``date`` field is correctly
    deserialized together with the associated confidence level.
    """
    json_sample, _ = _get_product_samples(
        "financial_document", "complete_with_coordinates"
    )

    response = InferenceResponse(json_sample)

    date_field: SimpleField = response.inference.result.fields["date"]

    assert date_field.locations, "date field should expose locations"
    location = date_field.locations[0]
    assert location is not None
    assert location.page == 0

    polygon = location.polygon
    assert polygon is not None
    assert len(polygon[0]) == 2

    assert polygon[0].x == 0.948979073166918
    assert polygon[0].y == 0.23097924535067715

    assert polygon[1][0] == 0.85422
    assert polygon[1][1] == 0.230072

    assert polygon[2][0] == 0.8540899268330819
    assert polygon[2][1] == 0.24365775464932288

    assert polygon[3][0] == 0.948849
    assert polygon[3][1] == 0.244565

    assert str(date_field.confidence) == "Medium"
    assert int(date_field.confidence) == 2
    assert date_field.confidence == FieldConfidence.MEDIUM
    assert date_field.confidence >= FieldConfidence.MEDIUM
    assert date_field.confidence <= FieldConfidence.MEDIUM
    assert date_field.confidence >= FieldConfidence.LOW
    assert date_field.confidence > FieldConfidence.LOW
    assert date_field.confidence <= FieldConfidence.HIGH
    assert date_field.confidence < FieldConfidence.HIGH


@pytest.mark.v2
def test_text_context_field_is_false() -> None:
    json_sample, _ = _get_product_samples("financial_document", "complete")
    response = InferenceResponse(json_sample)
    assert isinstance(response.inference.active_options, InferenceActiveOptions)
    assert response.inference.active_options.text_context is False


@pytest.mark.v2
def test_text_context_field_is_true() -> None:
    with open(
        V2_PRODUCT_DATA_DIR / "extraction" / "text_context_enabled.json", "r"
    ) as file:
        json_sample = json.load(file)
    response = InferenceResponse(json_sample)
    assert isinstance(response.inference.active_options, InferenceActiveOptions)
    assert response.inference.active_options.text_context is True

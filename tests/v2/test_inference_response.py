import json
from pathlib import Path
from typing import Tuple

import pytest

from mindee.parsing.v2.field.list_field import ListField
from mindee.parsing.v2.field.object_field import ObjectField
from mindee.parsing.v2.field.simple_field import SimpleField
from mindee.parsing.v2.inference import Inference
from mindee.parsing.v2.inference_file import InferenceFile
from mindee.parsing.v2.inference_model import InferenceModel
from mindee.parsing.v2.inference_response import InferenceResponse
from tests.test_inputs import V2_DATA_DIR


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
    json_path = V2_DATA_DIR / "inference" / f"{name}.json"
    rst_path = V2_DATA_DIR / "inference" / f"{name}.rst"
    return _get_samples(json_path, rst_path)


def _get_product_samples(product, name: str) -> Tuple[dict, str]:
    json_path = V2_DATA_DIR / "products" / product / f"{name}.json"
    rst_path = V2_DATA_DIR / "products" / product / f"{name}.rst"
    return _get_samples(json_path, rst_path)


@pytest.mark.v2
def test_deep_nested_fields():
    json_sample, rst_sample = _get_inference_samples("deep_nested_fields")
    inference_result = InferenceResponse(json_sample)
    assert isinstance(inference_result.inference, Inference)
    assert isinstance(
        inference_result.inference.result.fields.field_simple, SimpleField
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object, ObjectField
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object.fields["sub_object_list"],
        ListField,
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object.fields[
            "sub_object_object"
        ],
        ObjectField,
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object.fields[
            "sub_object_object"
        ].fields,
        dict,
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object.fields[
            "sub_object_object"
        ].fields["sub_object_object_sub_object_list"],
        ListField,
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object.fields[
            "sub_object_object"
        ]
        .fields["sub_object_object_sub_object_list"]
        .items,
        list,
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object.fields[
            "sub_object_object"
        ]
        .fields["sub_object_object_sub_object_list"]
        .items[0],
        ObjectField,
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object.fields[
            "sub_object_object"
        ]
        .fields["sub_object_object_sub_object_list"]
        .items[0]
        .fields["sub_object_object_sub_object_list_simple"],
        SimpleField,
    )
    assert (
        inference_result.inference.result.fields.field_object.fields[
            "sub_object_object"
        ]
        .fields["sub_object_object_sub_object_list"]
        .items[0]
        .fields["sub_object_object_sub_object_list_simple"]
        .value
        == "value_9"
    )


@pytest.mark.v2
def test_standard_field_types():
    json_sample, rst_sample = _get_inference_samples("standard_field_types")
    inference_result = InferenceResponse(json_sample)
    assert isinstance(inference_result.inference, Inference)
    field_simple_string = inference_result.inference.result.fields.field_simple_string
    assert isinstance(field_simple_string, SimpleField)
    assert field_simple_string.value == "field_simple_string-value"
    assert str(field_simple_string) == "field_simple_string-value"

    field_simple_bool = inference_result.inference.result.fields.field_simple_bool
    assert isinstance(field_simple_bool, SimpleField)
    assert field_simple_bool.value is True
    assert str(field_simple_bool) == "True"

    field_simple_null = inference_result.inference.result.fields.field_simple_null
    assert isinstance(field_simple_null, SimpleField)
    assert field_simple_null.value is None
    assert str(field_simple_null) == ""

    assert isinstance(
        inference_result.inference.result.fields.field_object, ObjectField
    )
    assert isinstance(
        inference_result.inference.result.fields.field_simple_list, ListField
    )
    assert isinstance(
        inference_result.inference.result.fields.field_object_list, ListField
    )
    assert rst_sample == str(inference_result)


@pytest.mark.v2
def test_raw_texts():
    json_sample, rst_sample = _get_inference_samples("raw_texts")
    inference_result = InferenceResponse(json_sample)
    assert isinstance(inference_result.inference, Inference)

    assert inference_result.inference.result.options
    assert len(inference_result.inference.result.options.raw_texts) == 2
    assert inference_result.inference.result.options.raw_texts[0].page == 0
    assert (
        inference_result.inference.result.options.raw_texts[0].content
        == "This is the raw text of the first page..."
    )


@pytest.mark.v2
def test_full_inference_response():
    json_sample, rst_sample = _get_product_samples("financial_document", "complete")
    inference_result = InferenceResponse(json_sample)

    assert isinstance(inference_result.inference, Inference)
    assert inference_result.inference.id == "12345678-1234-1234-1234-123456789abc"
    assert isinstance(inference_result.inference.result.fields.date, SimpleField)
    assert inference_result.inference.result.fields.date.value == "2019-11-02"
    assert isinstance(inference_result.inference.result.fields.taxes, ListField)
    assert isinstance(
        inference_result.inference.result.fields.taxes.items[0], ObjectField
    )
    assert (
        inference_result.inference.result.fields.customer_address.fields.city.value
        == "New York"
    )
    assert (
        inference_result.inference.result.fields.taxes.items[0].fields["base"].value
        == 31.5
    )

    assert isinstance(inference_result.inference.model, InferenceModel)
    assert inference_result.inference.model.id == "12345678-1234-1234-1234-123456789abc"

    assert isinstance(inference_result.inference.file, InferenceFile)
    assert inference_result.inference.file.name == "complete.jpg"
    assert inference_result.inference.file.page_count == 1
    assert inference_result.inference.file.mime_type == "image/jpeg"
    assert not inference_result.inference.file.alias
    assert not inference_result.inference.result.options

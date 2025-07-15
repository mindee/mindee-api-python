import json
from typing import Tuple

import pytest

from mindee import ClientV2, LocalResponse
from mindee.parsing.v2.inference import Inference
from mindee.parsing.v2.inference_file import InferenceFile
from mindee.parsing.v2.inference_model import InferenceModel
from mindee.parsing.v2.inference_response import InferenceResponse
from mindee.parsing.v2.list_field import ListField
from mindee.parsing.v2.object_field import ObjectField
from mindee.parsing.v2.simple_field import SimpleField
from tests.test_inputs import V2_DATA_DIR


def _get_samples(name: str) -> Tuple[dict, str]:
    with (V2_DATA_DIR / "inference" / f"{name}.json").open("r", encoding="utf-8") as fh:
        json_sample = json.load(fh)
    try:
        with (V2_DATA_DIR / "inference" / f"{name}.rst").open(
            "r", encoding="utf-8"
        ) as fh:
            rst_sample = fh.read()
    except FileNotFoundError:
        rst_sample = ""
    return json_sample, rst_sample


@pytest.mark.v2
def test_deep_nested_fields():
    json_sample, rst_sample = _get_samples("deep_nested_fields")
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
    json_sample, rst_sample = _get_samples("standard_field_types")
    inference_result = InferenceResponse(json_sample)
    assert isinstance(inference_result.inference, Inference)
    assert isinstance(
        inference_result.inference.result.fields.field_simple, SimpleField
    )
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
    json_sample, rst_sample = _get_samples("raw_texts")
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
    client_v2 = ClientV2("dummy")
    load_response = client_v2.load_inference(
        LocalResponse(V2_DATA_DIR / "products" / "financial_document" / "complete.json")
    )

    assert isinstance(load_response.inference, Inference)
    assert load_response.inference.id == "12345678-1234-1234-1234-123456789abc"
    assert isinstance(load_response.inference.result.fields.date, SimpleField)
    assert load_response.inference.result.fields.date.value == "2019-11-02"
    assert isinstance(load_response.inference.result.fields.taxes, ListField)
    assert isinstance(load_response.inference.result.fields.taxes.items[0], ObjectField)
    assert (
        load_response.inference.result.fields.customer_address.fields.city.value
        == "New York"
    )
    assert (
        load_response.inference.result.fields.taxes.items[0].fields["base"].value
        == 31.5
    )

    assert isinstance(load_response.inference.model, InferenceModel)
    assert load_response.inference.model.id == "12345678-1234-1234-1234-123456789abc"

    assert isinstance(load_response.inference.file, InferenceFile)
    assert load_response.inference.file.name == "complete.jpg"
    assert not load_response.inference.file.alias
    assert not load_response.inference.result.options

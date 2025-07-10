import json

import pytest

from mindee import ClientV2, LocalResponse
from mindee.parsing.v2 import (
    Inference,
    InferenceFile,
    InferenceModel,
    InferenceResponse,
    ListField,
    ObjectField,
    SimpleField,
)
from tests.test_inputs import V2_DATA_DIR


@pytest.fixture
def deep_nested_fields() -> dict:
    with (V2_DATA_DIR / "inference/deep_nested_fields.json").open(
        "r", encoding="utf-8"
    ) as fh:
        return json.load(fh)


@pytest.fixture
def standard_field_types() -> dict:
    with (V2_DATA_DIR / "inference/standard_field_types.json").open(
        "r", encoding="utf-8"
    ) as fh:
        return json.load(fh)


@pytest.fixture
def raw_texts() -> dict:
    with (V2_DATA_DIR / "inference/raw_texts.json").open("r", encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.v2
def test_deep_nested_fields(deep_nested_fields):
    inference_result = InferenceResponse(deep_nested_fields)
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
def test_raw_texts(raw_texts):
    inference_result = InferenceResponse(raw_texts)
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

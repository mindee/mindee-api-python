import json

import pytest

from mindee import ClientV2, LocalResponse
from mindee.parsing.common.string_dict import StringDict
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
def inference_result_json() -> StringDict:
    return {
        "inference": {
            "model": {"id": "test-model-id"},
            "file": {"name": "test-file-name.jpg", "alias": None},
            "result": {
                "fields": {
                    "field_simple": {"value": "value_1"},
                    "field_object": {
                        "fields": {
                            "sub_object_simple": {"value": "value_2"},
                            "sub_object_list": {
                                "items": [
                                    {
                                        "fields": {
                                            "sub_object_list_sub_list_simple": {
                                                "value": "value_3"
                                            }
                                        }
                                    },
                                    {
                                        "fields": {
                                            "sub_object_list_sub_list_object_subobject_1": {
                                                "value": "value_4"
                                            },
                                            "sub_object_list_sub_list_object_subobject_2": {
                                                "value": "value_5"
                                            },
                                        }
                                    },
                                ]
                            },
                            "sub_object_object": {
                                "fields": {
                                    "sub_object_object_sub_object_simple": {
                                        "value": "value_6"
                                    },
                                    "sub_object_object_sub_object_object": {
                                        "fields": {
                                            "sub_object_object_sub_object_object_simple_1": {
                                                "value": "value_7"
                                            },
                                            "sub_object_object_sub_object_object_simple_2": {
                                                "value": "value_8"
                                            },
                                        }
                                    },
                                    "sub_object_object_sub_object_list": {
                                        "items": [
                                            {
                                                "fields": {
                                                    "sub_object_object_sub_object_list_simple": {
                                                        "value": "value_9"
                                                    },
                                                    "sub_object_object_sub_object_list_object": {
                                                        "fields": {
                                                            "sub_object_object_sub_object_list_object_subobject_1": {
                                                                "value": "value_10"
                                                            },
                                                            "sub_object_object_sub_object_list_object_subobject_2": {
                                                                "value": "value_11"
                                                            },
                                                        }
                                                    },
                                                }
                                            }
                                        ]
                                    },
                                }
                            },
                        }
                    },
                },
                "options": {
                    "raw_text": ["toto", "tata", "titi"],
                },
            },
        }
    }


@pytest.mark.v2
def test_inference_response(inference_result_json):
    inference_result = InferenceResponse(inference_result_json)
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

    assert inference_result.inference.result.options
    assert len(inference_result.inference.result.options.raw_text) == 3
    assert inference_result.inference.result.options.raw_text[0] == "toto"


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

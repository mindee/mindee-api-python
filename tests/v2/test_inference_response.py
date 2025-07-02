import pytest

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2 import (
    Inference,
    InferenceResponse,
    InferenceResult,
    ListField,
    ObjectField,
    SimpleField,
)


@pytest.fixture
def inference_json() -> StringDict:
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
                "options": None,
            },
        }
    }


@pytest.mark.v2
def test_inference(inference_json):
    inference_result = InferenceResponse(inference_json)
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

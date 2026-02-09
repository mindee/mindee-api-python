import json

import pytest

from mindee import InferenceParameters
from mindee.input.inference_parameters import (
    DataSchema,
    DataSchemaReplace,
    DataSchemaField,
)
from tests.utils import V2_PRODUCT_DATA_DIR

expected_data_schema_dict = json.loads(
    (V2_PRODUCT_DATA_DIR / "extraction" / "data_schema_replace_param.json").read_text()
)
expected_data_schema_str = json.dumps(
    expected_data_schema_dict, indent=None, sort_keys=True
)


def test_data_schema_replace_none():
    params = InferenceParameters(model_id="test-id")
    assert params.data_schema is None


def test_data_schema_replace_str():
    params = InferenceParameters(
        model_id="test-id", data_schema=expected_data_schema_str
    )
    assert str(params.data_schema) == expected_data_schema_str


def test_data_schema_replace_dict():
    params = InferenceParameters(
        model_id="test-id", data_schema=expected_data_schema_dict
    )
    assert str(params.data_schema) == expected_data_schema_str


def test_data_schema_replace_obj_top():
    params = InferenceParameters(
        model_id="test-id",
        data_schema=DataSchema(replace=expected_data_schema_dict["replace"]),
    )
    assert str(params.data_schema) == expected_data_schema_str


def test_data_schema_replace_obj_fields():
    params = InferenceParameters(
        model_id="test-id",
        data_schema=DataSchema(
            replace=DataSchemaReplace(
                fields=expected_data_schema_dict["replace"]["fields"]
            )
        ),
    )
    assert str(params.data_schema) == expected_data_schema_str


def test_data_schema_replace_empty_fields():
    with pytest.raises(
        ValueError, match="Data schema replacement fields cannot be empty"
    ):
        InferenceParameters(model_id="test-id", data_schema={"replace": {"fields": []}})


def test_data_schema_replace_obj_full():
    params = InferenceParameters(
        model_id="test-id",
        data_schema=DataSchema(
            replace=DataSchemaReplace(
                fields=[
                    DataSchemaField(
                        name="test_replace",
                        title="Test Replace",
                        type="string",
                        is_array=False,
                        description="A static value for testing.",
                        guidelines="IMPORTANT: always return this exact string: 'a test value'",
                    )
                ]
            )
        ),
    )
    assert str(params.data_schema) == expected_data_schema_str

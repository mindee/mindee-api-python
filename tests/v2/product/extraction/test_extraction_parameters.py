import json

import pytest

from mindee import ExtractionParameters
from tests.utils import V2_PRODUCT_PATH

MODEL_ID = "test-model-id"
DATA_SCHEMA_DICT = json.loads(
    (V2_PRODUCT_PATH / "extraction" / "data_schema_replace_param.json").read_text()
)
DATA_SCHEMA = json.dumps(
    DATA_SCHEMA_DICT, indent=None, sort_keys=True, separators=(",", ":")
)


@pytest.mark.v2
def test_parameters_must_init_with_required():
    product_params = ExtractionParameters(MODEL_ID)

    request_params = product_params.get_request_parameters()
    assert request_params["model_id"] == MODEL_ID
    assert "alias" not in request_params
    assert "webhook_ids" not in request_params
    assert "rag" not in request_params
    assert "raw_text" not in request_params
    assert "polygon" not in request_params
    assert "confidence" not in request_params
    assert "text_context" not in request_params
    assert "data_schema" not in request_params


@pytest.mark.v2
def test_parameters_must_init_with_all():
    product_params = ExtractionParameters(
        MODEL_ID,
        alias="test-alias",
        webhook_ids=["webhook-1", "webhook-2"],
        rag=True,
        raw_text=False,
        polygon=True,
        confidence=False,
        text_context="test context",
        data_schema=DATA_SCHEMA,
    )

    request_params = product_params.get_request_parameters()
    assert request_params["model_id"] == MODEL_ID
    assert request_params["alias"] == "test-alias"
    assert request_params["webhook_ids"] == ["webhook-1", "webhook-2"]
    assert request_params["rag"] == "true"
    assert request_params["raw_text"] == "false"
    assert request_params["polygon"] == "true"
    assert request_params["confidence"] == "false"
    assert request_params["text_context"] == "test context"
    assert request_params["data_schema"] == DATA_SCHEMA


@pytest.mark.v2
def test_data_schema_should_leave_unset_when_not_provided():
    product_params = ExtractionParameters(MODEL_ID)

    request_params = product_params.get_request_parameters()
    assert "data_schema" not in request_params


@pytest.mark.v2
def test_data_schema_string_should_initialize():
    product_params = ExtractionParameters(MODEL_ID, data_schema=DATA_SCHEMA)

    request_params = product_params.get_request_parameters()
    assert request_params["data_schema"] == DATA_SCHEMA

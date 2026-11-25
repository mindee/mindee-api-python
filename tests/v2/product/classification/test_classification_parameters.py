import pytest

from mindee import ClassificationParameters

MODEL_ID = "test-model-id"


@pytest.mark.v2
def test_parameters_must_init_with_required():
    product_params = ClassificationParameters(MODEL_ID)

    request_params = product_params.get_request_parameters()
    assert request_params["model_id"] == MODEL_ID
    assert "alias" not in request_params
    assert "webhook_ids" not in request_params
    assert "extraction_text_context" not in request_params


@pytest.mark.v2
def test_parameters_must_init_with_all():
    product_params = ClassificationParameters(
        MODEL_ID,
        alias="test-alias",
        webhook_ids=["webhook-1", "webhook-2"],
        extraction_text_context="context",
    )

    request_params = product_params.get_request_parameters()
    assert request_params["model_id"] == MODEL_ID
    assert request_params["alias"] == "test-alias"
    assert request_params["webhook_ids"] == ["webhook-1", "webhook-2"]
    assert request_params["extraction_text_context"] == "context"

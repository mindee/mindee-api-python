import json
from datetime import datetime

import pytest

from mindee.v2.parsing import FailedInferenceResponse
from tests.utils import V2_DATA_DIR


@pytest.mark.v2
def test_should_load_when_failed():
    """Should load when the webhook didn't return a correct reply."""

    json_path = V2_DATA_DIR / "errors" / "webhook_error_500_failed.json"
    with json_path.open("r", encoding="utf-8") as fh:
        json_sample = json.load(fh)
    response = FailedInferenceResponse(json_sample)

    assert response is not None
    assert response.inference_id == "12345678-1234-1234-1234-123456789ABC"
    assert response.file_name == "default_sample.jpg"
    assert response.file_alias == "dummy-alias.jpg"
    assert isinstance(response.created_at, datetime)
    assert response.error is not None
    assert response.error.status == 500
    assert response.error.code == "500-012"

import json

import pytest

from mindee import JobResponse
from mindee.parsing.v2 import ErrorItem, ErrorResponse
from tests.utils import V2_DATA_DIR


def _get_job_samples(json_file: str) -> dict:
    json_path = V2_DATA_DIR / "job" / json_file
    with json_path.open("r", encoding="utf-8") as fh:
        json_sample = json.load(fh)
    return json_sample


@pytest.mark.v2
def test_should_load_when_status_is_processing():
    """Should load when status is Processing."""
    json_sample = _get_job_samples("ok_processing.json")
    response = JobResponse(json_sample)

    assert response.job is not None
    assert response.job.error is None


@pytest.mark.v2
def test_should_load_with_422_error():
    """Should load with 422 error."""
    json_sample = _get_job_samples("fail_422.json")
    response = JobResponse(json_sample)

    assert response.job is not None
    assert isinstance(response.job.error, ErrorResponse)
    assert response.job.error.status == 422
    assert response.job.error.code.startswith("422-")
    assert isinstance(response.job.error.errors, list)
    assert len(response.job.error.errors) == 1
    assert isinstance(response.job.error.errors[0], ErrorItem)

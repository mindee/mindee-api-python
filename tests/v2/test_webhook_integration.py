from datetime import datetime

import pytest

from mindee import (
    ExtractionParameters,
    ExtractionResponse,
    PathInput,
    PollingOptions,
    SplitParameters,
    SplitResponse,
)
from mindee.v2 import Client
from mindee.v2.error import MindeeHTTPErrorV2
from mindee.v2.parsing import Job
from tests.utils import FILE_TYPES_PATH, V2_PRODUCT_PATH


@pytest.mark.integration
@pytest.mark.v2
def test_unknown_webhook_ids_must_throw_error(
    v2_client: Client, findoc_model_id: str
) -> None:
    """
    Using an unknown webhook identifier must trigger an error.
    """
    input_path = FILE_TYPES_PATH / "pdf" / "blank_1.pdf"

    input_source = PathInput(input_path)
    params = ExtractionParameters(
        model_id=findoc_model_id,
        webhook_ids=[
            "fc405e37-4ba4-4d03-aeba-533a8d1f0f21",
            "fc405e37-4ba4-4d03-aeba-533a8d1f0f21",
        ],
        rag=None,
        raw_text=None,
        polygon=None,
        confidence=None,
    )

    with pytest.raises(MindeeHTTPErrorV2) as e:
        v2_client.enqueue(input_source, params)

    exc: MindeeHTTPErrorV2 = e.value
    assert exc.status == 422
    assert exc.title is not None
    assert exc.code.startswith("422-")
    assert isinstance(exc.errors, list)
    assert "no matching webhooks" in exc.detail.lower()


def _enqueue_and_poll_job(v2_client: Client, input_source, params) -> Job:
    """Enqueue a document and poll until the job and its webhooks reach a final status."""
    initial_response = v2_client.enqueue(input_source, params)
    job_response = v2_client._poll_on_job(
        initial_response=initial_response,
        polling_options=PollingOptions(),
        wait_for_webhooks=True,
    )
    return job_response.job


def _assert_webhook_job_success(job: Job, webhook_ids: list) -> None:
    assert job.status == "Processed"
    assert isinstance(job.completed_at, datetime)
    assert job.error is None
    assert len(job.webhooks) == len(webhook_ids)
    assert all(webhook.status in {"Processed", "Failed"} for webhook in job.webhooks)
    assert {webhook.id for webhook in job.webhooks} == set(webhook_ids)


@pytest.mark.integration
@pytest.mark.v2
def test_extraction_with_two_webhooks_must_complete_and_succeed(
    v2_client: Client, findoc_model_id: str
) -> None:
    webhook_ids = [
        "9a0d88be-6913-484d-a019-9d2e16e2d3b9",
        "32286ed9-fe40-4f42-bdc5-2f8496c5641a",
    ]

    input_source = PathInput(
        V2_PRODUCT_PATH / "extraction" / "financial_document" / "default_sample.jpg"
    )
    params = ExtractionParameters(model_id=findoc_model_id, webhook_ids=webhook_ids)

    job = _enqueue_and_poll_job(v2_client, input_source, params)
    _assert_webhook_job_success(job, webhook_ids)

    response = v2_client.get_result_from_url(ExtractionResponse, job.result_url)
    assert response.inference is not None
    assert response.inference.result is not None
    assert response.inference.result.fields["supplier_name"].value == "John Smith"


@pytest.mark.integration
@pytest.mark.v2
def test_split_with_two_webhooks_must_complete_and_succeed(
    v2_client: Client, split_model_id: str
) -> None:
    webhook_ids = [
        "b8fdfea3-24b6-438a-a6ca-7cd8c87a8875",
        "d5bf36a9-1301-42c7-95be-03dc20d8f10e",
    ]

    input_source = PathInput(V2_PRODUCT_PATH / "split" / "default_sample.pdf")
    params = SplitParameters(model_id=split_model_id, webhook_ids=webhook_ids)

    job = _enqueue_and_poll_job(v2_client, input_source, params)
    _assert_webhook_job_success(job, webhook_ids)

    response = v2_client.get_result_from_url(SplitResponse, job.result_url)
    assert response.inference is not None
    assert response.inference.result is not None
    assert len(response.inference.result.splits) == 2

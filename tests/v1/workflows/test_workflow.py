import json
from datetime import timezone

import pytest

from mindee.parsing.common.workflow_response import WorkflowResponse
from mindee.product.generated.generated_v1 import GeneratedV1
from tests.utils import V1_DATA_DIR

WORKFLOW_DIR = V1_DATA_DIR / "workflows"


@pytest.fixture
def success_workflow() -> WorkflowResponse:
    file_path = WORKFLOW_DIR / "success.json"
    with open(file_path, encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return WorkflowResponse(GeneratedV1, json_data)


@pytest.fixture
def success_low_priority_workflow() -> WorkflowResponse:
    file_path = WORKFLOW_DIR / "success_low_priority.json"
    with open(file_path, encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return WorkflowResponse(GeneratedV1, json_data)


def test_deserialize_workflow(success_workflow: WorkflowResponse):
    assert success_workflow is not None
    assert success_workflow.api_request is not None
    assert success_workflow.execution.batch_name is None
    assert success_workflow.execution.created_at is None
    assert success_workflow.execution.file.alias is None
    assert success_workflow.execution.file.name == "default_sample.jpg"
    assert success_workflow.execution.id == "8c75c035-e083-4e77-ba3b-7c3598bd1d8a"
    assert success_workflow.execution.inference is None
    assert success_workflow.execution.priority == "medium"
    assert success_workflow.execution.reviewed_at is None
    assert success_workflow.execution.reviewed_prediction is None
    assert success_workflow.execution.status == "processing"
    assert success_workflow.execution.type == "manual"
    assert (
        success_workflow.execution.uploaded_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        == "2024-11-13T13:02:31.699190"
    )
    assert (
        success_workflow.execution.workflow_id == "07ebf237-ff27-4eee-b6a2-425df4a5cca6"
    )


def test_deserialize_workflow_with_priority_and_alias(
    success_low_priority_workflow: WorkflowResponse,
):
    assert success_low_priority_workflow is not None
    assert success_low_priority_workflow.api_request is not None
    assert success_low_priority_workflow.execution.batch_name is None
    assert success_low_priority_workflow.execution.created_at is None
    assert (
        success_low_priority_workflow.execution.file.alias == "low-priority-sample-test"
    )
    assert success_low_priority_workflow.execution.file.name == "default_sample.jpg"
    assert (
        success_low_priority_workflow.execution.id
        == "b743e123-e18c-4b62-8a07-811a4f72afd3"
    )
    assert success_low_priority_workflow.execution.inference is None
    assert success_low_priority_workflow.execution.priority == "low"
    assert success_low_priority_workflow.execution.reviewed_at is None
    assert success_low_priority_workflow.execution.reviewed_prediction is None
    assert success_low_priority_workflow.execution.status == "processing"
    assert success_low_priority_workflow.execution.type == "manual"
    assert (
        success_low_priority_workflow.execution.uploaded_at.strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        == "2024-11-13T13:17:01.315179"
    )
    assert (
        success_low_priority_workflow.execution.workflow_id
        == "07ebf237-ff27-4eee-b6a2-425df4a5cca6"
    )


def test_deserialize_workflow_with_inference_and_reviewed_prediction():
    raw_response = {
        "api_request": {
            "error": {},
            "resources": ["execution"],
            "status": "success",
            "status_code": 200,
            "url": "https://api.mindee.net/v1/workflows/workflow-id/executions",
        },
        "execution": {
            "available_at": "2024-11-13T13:04:31.699190Z",
            "batch_name": "batch-name",
            "created_at": "2024-11-13T13:02:31.699190Z",
            "file": {
                "alias": "sample-alias",
                "name": "default_sample.jpg",
            },
            "id": "execution-id",
            "inference": {
                "product": {
                    "name": "custom",
                    "version": "1",
                },
                "prediction": {
                    "customer_name": {
                        "confidence": 0.98,
                        "value": "Jane Doe",
                    },
                },
                "pages": [
                    {
                        "id": 0,
                        "prediction": {
                            "customer_name": {
                                "confidence": 0.98,
                                "value": "Jane Doe",
                            },
                        },
                    },
                ],
            },
            "priority": "high",
            "reviewed_at": "2024-11-13T13:05:31.699190Z",
            "reviewed_prediction": {
                "customer_name": {
                    "confidence": 1,
                    "value": "Jane Doe",
                },
            },
            "status": "completed",
            "type": "manual",
            "uploaded_at": "2024-11-13T13:03:31.699190Z",
            "workflow_id": "workflow-id",
        },
    }

    response = WorkflowResponse(GeneratedV1, raw_response)

    assert response.execution.available_at.tzinfo == timezone.utc
    assert response.execution.created_at.isoformat() == (
        "2024-11-13T13:02:31.699190+00:00"
    )
    assert response.execution.reviewed_at.isoformat() == (
        "2024-11-13T13:05:31.699190+00:00"
    )
    assert response.execution.uploaded_at.isoformat() == (
        "2024-11-13T13:03:31.699190+00:00"
    )
    assert response.execution.inference is not None
    assert response.execution.inference.prediction.fields["customer_name"].value == (
        "Jane Doe"
    )
    assert (
        response.execution.inference.pages[0].prediction.fields["customer_name"].value
        == "Jane Doe"
    )
    assert response.execution.reviewed_prediction is not None
    assert response.execution.reviewed_prediction.fields["customer_name"].value == (
        "Jane Doe"
    )

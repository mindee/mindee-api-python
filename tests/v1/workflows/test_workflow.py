import json
from pathlib import Path

import pytest

from mindee.parsing.common.workflow_response import WorkflowResponse
from mindee.product.generated.generated_v1 import GeneratedV1

WORKFLOW_DIR = Path("./tests/data") / "workflows"


@pytest.fixture
def success_workflow() -> WorkflowResponse:
    file_path = WORKFLOW_DIR / "success.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return WorkflowResponse(GeneratedV1, json_data)


@pytest.fixture
def success_low_priority_workflow() -> WorkflowResponse:
    file_path = WORKFLOW_DIR / "success_low_priority.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
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

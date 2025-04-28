import os
from datetime import datetime

import pytest

from mindee import Client
from mindee.input import WorkflowOptions
from mindee.parsing.common.execution_priority import ExecutionPriority
from mindee.product import FinancialDocumentV1, GeneratedV1
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def mindee_client():
    return Client()


@pytest.fixture
def workflow_id():
    return os.getenv("WORKFLOW_ID", "")


@pytest.fixture
def input_path():
    return PRODUCT_DATA_DIR / "financial_document" / "default_sample.jpg"


@pytest.mark.integration
def test_workflow_execution(mindee_client: Client, workflow_id: str, input_path: str):
    input_source = mindee_client.source_from_path(str(input_path))
    current_date_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    alias = f"python-{current_date_time}"
    priority = ExecutionPriority.LOW
    options = WorkflowOptions(alias=alias, priority=priority, rag=True)

    response = mindee_client.execute_workflow(input_source, workflow_id, options)

    assert response.api_request.status_code == 202
    assert response.execution.file.alias == f"python-{current_date_time}"
    assert response.execution.priority == "low"


@pytest.mark.integration
def test_workflow_predict_ots_rag(
    mindee_client: Client, workflow_id: str, input_path: str
):
    input_source = mindee_client.source_from_path(str(input_path))

    response = mindee_client.enqueue_and_parse(
        FinancialDocumentV1,
        input_source,
        workflow_id=workflow_id,
        rag=True,
    )
    assert len(response.document.inference.extras.rag.matching_document_id) > 5


@pytest.mark.integration
def test_workflow_predict_ots_no_rag(
    mindee_client: Client, workflow_id: str, input_path: str
):
    input_source = mindee_client.source_from_path(str(input_path))

    response = mindee_client.enqueue_and_parse(
        FinancialDocumentV1,
        input_source,
        workflow_id=workflow_id,
    )
    assert response.document.inference.extras is None


@pytest.mark.integration
def test_workflow_predict_custom_rag(
    mindee_client: Client, workflow_id: str, input_path: str
):
    my_endpoint = mindee_client.create_endpoint(
        account_name="mindee",
        endpoint_name="financial_document",
    )

    input_source = mindee_client.source_from_path(str(input_path))

    response = mindee_client.enqueue_and_parse(
        GeneratedV1,
        input_source,
        endpoint=my_endpoint,
        workflow_id=workflow_id,
        rag=True,
    )
    assert len(response.document.inference.extras.rag.matching_document_id) > 5


@pytest.mark.integration
def test_workflow_predict_custom_no_rag(
    mindee_client: Client, workflow_id: str, input_path: str
):
    my_endpoint = mindee_client.create_endpoint(
        account_name="mindee",
        endpoint_name="financial_document",
    )

    input_source = mindee_client.source_from_path(str(input_path))

    response = mindee_client.enqueue_and_parse(
        GeneratedV1,
        input_source,
        endpoint=my_endpoint,
        workflow_id=workflow_id,
    )
    assert response.document.inference.extras is None

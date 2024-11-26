import os
from datetime import datetime

import pytest

from mindee import Client
from mindee.input import WorkflowOptions
from mindee.parsing.common.execution_priority import ExecutionPriority
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
def test_workflow(mindee_client: Client, workflow_id: str, input_path: str):
    input_source = mindee_client.source_from_path(str(input_path))
    current_date_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    alias = f"python-{current_date_time}"
    priority = ExecutionPriority.LOW
    options = WorkflowOptions(alias=alias, priority=priority)

    response = mindee_client.execute_workflow(input_source, workflow_id, options)

    assert response.api_request.status_code == 202
    assert response.execution.file.alias == f"python-{current_date_time}"
    assert response.execution.priority == "low"

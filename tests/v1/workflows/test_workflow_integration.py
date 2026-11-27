import os

import pytest

from mindee import PathInput
from mindee.v1.client import Client
from mindee.v1.product import FinancialDocumentV1, GeneratedV1
from tests.utils import V1_PRODUCT_PATH


@pytest.fixture
def mindee_client():
    return Client()


@pytest.fixture
def workflow_id():
    return os.getenv("WORKFLOW_ID", "")


@pytest.fixture
def input_path():
    return V1_PRODUCT_PATH / "financial_document" / "default_sample.jpg"


@pytest.mark.integration
def test_workflow_predict_ots_rag(
    mindee_client: Client, workflow_id: str, input_path: str
):
    input_source = PathInput(str(input_path))

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
    input_source = PathInput(str(input_path))

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

    input_source = PathInput(str(input_path))

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

    input_source = PathInput(str(input_path))

    response = mindee_client.enqueue_and_parse(
        GeneratedV1,
        input_source,
        endpoint=my_endpoint,
        workflow_id=workflow_id,
    )
    assert response.document.inference.extras is None

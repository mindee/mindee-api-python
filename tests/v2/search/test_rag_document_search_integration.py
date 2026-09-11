import os

import pytest

from mindee.v2.client import Client
from mindee.v2.search.rag_documents import RagDocumentSearchParameters


@pytest.fixture(scope="session")
def v2_client() -> Client:
    return Client()


@pytest.fixture(scope="session")
def findoc_model_id() -> str:
    findoc_model_id = os.getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID")
    assert findoc_model_id, "MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID must be set"
    return findoc_model_id


@pytest.mark.integration
@pytest.mark.v2
def test_search_must_have_results(v2_client: Client, findoc_model_id: str):
    response = v2_client.search(RagDocumentSearchParameters(model_id=findoc_model_id))

    assert response is not None
    assert len(response.rag_documents) > 0
    for rag_doc in response.rag_documents:
        assert rag_doc.id
        assert rag_doc.created_at
        assert rag_doc.filename
        assert rag_doc.total_matches >= 0
    assert response.pagination is not None
    assert response.pagination.total_items >= 1
    assert response.pagination.page == 1


@pytest.mark.integration
@pytest.mark.v2
def test_search_must_return_empty(v2_client: Client, findoc_model_id: str):
    response = v2_client.search(
        RagDocumentSearchParameters(
            model_id=findoc_model_id, filename="invoice_32GB-RAM_450k-USD.pdf"
        )
    )

    assert response is not None
    assert len(response.rag_documents) == 0
    assert response.pagination is not None
    assert response.pagination.total_items == 0
    assert response.pagination.page == 1

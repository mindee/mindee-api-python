import os

import pytest

from mindee.v2.client import Client
from mindee.v2.search.rag_documents.rag_document_search_parameters import (
    RagDocumentSearchParameters,
)


@pytest.fixture(scope="session")
def v2_client() -> Client:
    return Client()


@pytest.mark.integration
@pytest.mark.v2
def test_must_have_results(v2_client: Client):
    findoc_model_id = os.getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID", "")
    response = v2_client.search(RagDocumentSearchParameters(model_id=findoc_model_id))

    assert response is not None
    assert len(response.rag_documents) > 0
    assert response.pagination is not None
    assert response.pagination.total_items >= 1
    assert response.pagination.page == 1

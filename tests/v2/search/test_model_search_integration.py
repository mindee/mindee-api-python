import pytest

from mindee.v2.client import Client
from mindee.v2.search.models.model_search_parameters import ModelSearchParameters


@pytest.fixture(scope="session")
def v2_client() -> Client:
    return Client()


@pytest.mark.integration
@pytest.mark.v2
def test_must_have_results(v2_client: Client):
    response = v2_client.search(ModelSearchParameters())

    assert response is not None
    assert len(response.models) > 0
    assert response.pagination is not None
    assert response.pagination.total_items >= 1
    assert response.pagination.page == 1


@pytest.mark.integration
@pytest.mark.v2
def test_must_return_empty(v2_client: Client):
    response = v2_client.search(ModelSearchParameters(name="je n'existe pas tralala"))

    assert response is not None
    assert len(response.models) == 0
    assert response.pagination is not None
    assert response.pagination.total_items == 0
    assert response.pagination.page == 1
